"""bus_config: protocol/baud compatibility, node-id allocation and collisions per bus network."""

from __future__ import annotations

from ..context import CompositionContext
from .base import CheckResult, aggregate

# Protocol pairs that can interoperate (with a warning); anything else wired together fails.
_RELAXED_PAIRS = {frozenset(("CAN", "CAN-FD"))}


def check_bus_config(ctx: CompositionContext, check_id: str, name: str) -> CheckResult:
    problems: list[tuple[str, str]] = []
    notes: list[str] = []
    # network key: instances connected by bus wires share one segment (union-find over wires)
    parent: dict[str, str] = {}

    def find(x: str) -> str:
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        parent[find(a)] = find(b)

    for wire in ctx.doc.get("wiring", []):
        if wire["kind"] != "bus":
            continue
        wid = wire["id"]
        fa, ta = wire["from"], wire["to"]
        ba = ctx.bus(fa["instance"], fa["port"])
        bb = ctx.bus(ta["instance"], ta["port"])
        if ba is None:
            problems.append(("fail", f"{wid}: bus port {fa['instance']}.{fa['port']} not found"))
            continue
        if bb is None:
            problems.append(("fail", f"{wid}: bus port {ta['instance']}.{ta['port']} not found"))
            continue
        union(fa["instance"], ta["instance"])
        pa, pb = ba["protocol"], bb["protocol"]
        if pa != pb:
            if frozenset((pa, pb)) in _RELAXED_PAIRS:
                problems.append(("warn", f"{wid}: protocol mismatch {pa} ({ba.get('baud', '?')} bit/s, "
                                         f"{fa['instance']}) vs {pb} ({bb.get('baud', '?')} bit/s, {ta['instance']}) "
                                         f"- verify FD/classic arbitration interop"))
            else:
                problems.append(("fail", f"{wid}: incompatible protocols {pa} ({fa['instance']}) vs {pb} ({ta['instance']})"))
        elif ba.get("baud") and bb.get("baud") and ba["baud"] != bb["baud"]:
            problems.append(("fail", f"{wid}: baud mismatch on {pa}: {ba['baud']} vs {bb['baud']} bit/s"))

    # node-id allocation per network segment
    segments: dict[str, list[str]] = {}
    wired = {w["from"]["instance"] for w in ctx.doc.get("wiring", []) if w["kind"] == "bus"} | \
            {w["to"]["instance"] for w in ctx.doc.get("wiring", []) if w["kind"] == "bus"}
    for iid in wired:
        segments.setdefault(find(iid), []).append(iid)
    for members in segments.values():
        seen: dict[int, str] = {}
        for iid in members:
            inst = ctx.instances[iid]
            module = ctx.modules.get(iid)
            if module is None:
                continue
            spec = module.get("electrical", {}).get("node_ids")
            if spec is None:
                continue  # module has a bus but no addressable node id
            nid = inst.get("node_id", spec.get("default"))
            if nid is None:
                continue
            allowed = spec.get("range")
            if allowed and not (allowed[0] <= nid <= allowed[1]):
                problems.append(("fail", f"{iid}: node_id {nid} outside module range [{allowed[0]}, {allowed[1]}]"))
            if "node_id" in inst and not spec.get("configurable", True):
                problems.append(("fail", f"{iid}: node_id overridden but module declares configurable=false"))
            if nid in seen:
                problems.append(("fail", f"node_id collision on shared bus segment: {iid} and {seen[nid]} both use {nid}"))
            else:
                seen[nid] = iid
        if seen:
            notes.append(f"bus segment ({', '.join(members)}): node ids {sorted(seen)} unique")

    result = aggregate(problems, "All bus wires share protocol and baud; node ids unique per segment.", check_id, name)
    result.details.extend(notes)
    return result
