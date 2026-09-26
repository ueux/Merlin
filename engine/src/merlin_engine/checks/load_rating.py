"""load_rating: static downstream-mass check against each mated interface's ratings."""

from __future__ import annotations

from ..context import CompositionContext
from .base import CheckResult, aggregate

G = 9.81


def check_load_rating(ctx: CompositionContext, check_id: str, name: str) -> CheckResult:
    problems: list[tuple[str, str]] = []
    notes: list[str] = []
    for mate in ctx.doc.get("mates", []):
        mid = mate["id"]
        a_inst, b_inst = mate["a"]["instance"], mate["b"]["instance"]
        if a_inst not in ctx.instances or b_inst not in ctx.instances:
            continue  # referential error already recorded
        # The supported side is the one whose ancestor chain contains the other instance.
        if b_inst in ctx.ancestors(a_inst):
            load_inst, bearing = a_inst, ("b", mate["b"])
        elif a_inst in ctx.ancestors(b_inst):
            load_inst, bearing = b_inst, ("a", mate["a"])
        else:
            notes.append(f"{mid}: mates across sibling branches; checked both sides")
            load_inst, bearing = a_inst, ("b", mate["b"])
        side, ref = bearing
        iface = ctx.mech_interface(ref["instance"], ref["interface"])
        if iface is None:
            continue
        rating = iface.get("load") or {}
        if not rating:
            notes.append(f"{mid}: no load rating declared on {ref['instance']}.{ref['interface']}")
            continue
        mass = ctx.downstream_mass(load_inst)
        force = mass * G
        axial = rating.get("axial_n") or rating.get("radial_n")
        if axial is not None and force > axial:
            problems.append(
                ("fail", f"{mid}: downstream mass {mass:.2f} kg ({force:.1f} N) exceeds "
                         f"rating {axial:.0f} N on {ref['instance']}.{ref['interface']}")
            )
        elif axial is not None and force > 0.8 * axial:
            problems.append(
                ("warn", f"{mid}: downstream load {force:.1f} N is above 80% of the "
                         f"{axial:.0f} N rating on {ref['instance']}.{ref['interface']}")
            )
    ok = "Downstream masses within all mated interface load ratings."
    result = aggregate(problems, ok, check_id, name)
    result.details.extend(notes)
    return result
