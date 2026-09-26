"""mate_matching: kind equality, side complementarity, bolt pattern/pilot agreement, tag overlap."""

from __future__ import annotations

import math

from ..context import CompositionContext
from .base import CheckResult, aggregate

# Expected mate type per interface-kind pair (used to verify the authored mate type).
_MATE_TYPE = {
    "flange": "bolted",
    "bracket": "bolted",
    "tube_clamp": "clamped",
    "shaft": "clamped",
    "dovetail": "sliding",
    "rail": "sliding",
    "slot": "sliding",
    "magnet": "magnetic",
    "tool_mount": "bolted",
}

_MM_TOL = 0.01


def _bolt_problems(a: dict, b: dict) -> list[tuple[str, str]]:
    pa, pb = a.get("bolt_pattern"), b.get("bolt_pattern")
    if pa is None or pb is None:
        return []  # pattern-less kinds (tube_clamp, magnet) match via tags instead
    problems: list[tuple[str, str]] = []
    if pa["count"] != pb["count"] or pa["size"] != pb["size"]:
        problems.append(("fail", f"bolt pattern mismatch: {pa['count']}x{pa['size']} vs {pb['count']}x{pb['size']}"))
    layout_a, layout_b = pa.get("layout", "custom"), pb.get("layout", "custom")
    if layout_a != layout_b and "custom" not in (layout_a, layout_b):
        problems.append(("warn", f"bolt layout differs: {layout_a} vs {layout_b}"))
    if layout_a == "circular" and layout_b == "circular":
        if not math.isclose(pa.get("pcd_mm", 0), pb.get("pcd_mm", 0), abs_tol=_MM_TOL):
            problems.append(("fail", f"PCD mismatch: {pa.get('pcd_mm')} mm vs {pb.get('pcd_mm')} mm"))
    if layout_a in ("rectangular", "grid") and layout_b in ("rectangular", "grid"):
        for axis in ("pitch_x_mm", "pitch_y_mm"):
            va, vb = pa.get(axis), pb.get(axis)
            if va is not None and vb is not None and not math.isclose(va, vb, abs_tol=_MM_TOL):
                problems.append(("fail", f"pitch mismatch on {axis}: {va} mm vs {vb} mm"))
    return problems


def _pilot_problems(a: dict, b: dict) -> list[tuple[str, str]]:
    pa, pb = a.get("pilot"), b.get("pilot")
    if pa and pb and not math.isclose(pa["diameter_mm"], pb["diameter_mm"], abs_tol=_MM_TOL):
        return [("fail", f"pilot diameter mismatch: {pa['diameter_mm']} mm vs {pb['diameter_mm']} mm")]
    return []


def check_mate_matching(ctx: CompositionContext, check_id: str, name: str) -> CheckResult:
    problems: list[tuple[str, str]] = []
    checked = 0
    for mate in ctx.doc.get("mates", []):
        mid = mate["id"]
        ia = ctx.mech_interface(mate["a"]["instance"], mate["a"]["interface"])
        ib = ctx.mech_interface(mate["b"]["instance"], mate["b"]["interface"])
        if ia is None:
            problems.append(("fail", f"{mid}: interface {mate['a']['instance']}.{mate['a']['interface']} not found"))
            continue
        if ib is None:
            problems.append(("fail", f"{mid}: interface {mate['b']['instance']}.{mate['b']['interface']} not found"))
            continue
        checked += 1
        label = f"{mid} ({ia['kind']}->{ib['kind']})"
        if ia["kind"] != ib["kind"]:
            problems.append(("fail", f"{label}: kind mismatch"))
        sa, sb = ia.get("side", "neutral"), ib.get("side", "neutral")
        if sa == sb and sa != "neutral":
            problems.append(("fail", f"{label}: non-complementary sides ({sa} vs {sb})"))
        problems.extend((sev, f"{label}: {d}") for sev, d in _bolt_problems(ia, ib))
        problems.extend((sev, f"{label}: {d}") for sev, d in _pilot_problems(ia, ib))
        ta, tb = set(ia.get("compatible_with", [])), set(ib.get("compatible_with", []))
        if ta and tb and not (ta & tb):
            problems.append(("warn", f"{label}: no shared compatible_with tags ({sorted(ta)} vs {sorted(tb)})"))
        expected = _MATE_TYPE.get(ia["kind"])
        authored = mate.get("type")
        if expected and authored and authored != expected and authored != "custom":
            problems.append(("warn", f"{mid}: authored mate type {authored!r} differs from computed {expected!r}"))
    ok = f"{checked}/{len(ctx.doc.get('mates', []))} mates matched: kinds, sides, patterns and tags align."
    return aggregate(problems, ok, check_id, name)
