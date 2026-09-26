"""power_budget: wire-level voltage/provider checks plus a system-level provides-vs-consumes budget."""

from __future__ import annotations

from ..context import CompositionContext
from .base import CheckResult, aggregate

_BUDGET_HEADROOM = 0.8  # warn above 80% utilization


def check_power_budget(ctx: CompositionContext, check_id: str, name: str) -> CheckResult:
    problems: list[tuple[str, str]] = []
    notes: list[str] = []

    for wire in ctx.doc.get("wiring", []):
        if wire["kind"] != "power":
            continue
        wid = wire["id"]
        src = ctx.power_port(wire["from"]["instance"], wire["from"]["port"])
        dst = ctx.power_port(wire["to"]["instance"], wire["to"]["port"])
        if src is None:
            problems.append(("fail", f"{wid}: power port {wire['from']['instance']}.{wire['from']['port']} not found"))
            continue
        if dst is None:
            problems.append(("fail", f"{wid}: power port {wire['to']['instance']}.{wire['to']['port']} not found"))
            continue
        if not src.get("provides", False):
            problems.append(("fail", f"{wid}: {wire['from']['instance']}.{wire['from']['port']} is a consumer port "
                                     f"(provides=false) wired as a source"))
        lo = max(src["voltage_range"][0], dst["voltage_range"][0])
        hi = min(src["voltage_range"][1], dst["voltage_range"][1])
        if lo > hi:
            problems.append(("fail", f"{wid}: no voltage overlap — "
                                     f"{wire['from']['instance']} {src['voltage_range']} V vs "
                                     f"{wire['to']['instance']} {dst['voltage_range']} V"))
        else:
            notes.append(f"{wid}: voltage overlap {lo:g}-{hi:g} V")
        ca, cb = src.get("connector"), dst.get("connector")
        if ca and cb and ca != cb:
            problems.append(("warn", f"{wid}: connector mismatch {ca} -> {cb} (adapter required)"))

    provides = 0.0
    consumes = 0.0
    for iid, module in ctx.modules.items():
        budget = module.get("compat", {}).get("power_budget", {})
        provides += budget.get("provides_w", 0.0)
        consumes += budget.get("consumes_w", 0.0)
    if provides > 0:
        notes.append(f"system budget: {provides:g} W provided vs {consumes:g} W consumed")
        if consumes > provides:
            problems.append(("fail", f"power deficit: {consumes:g} W consumed exceeds {provides:g} W provided"))
        elif consumes > _BUDGET_HEADROOM * provides:
            problems.append(("warn", f"power headroom below 20%: {consumes:g} W of {provides:g} W"))
    elif consumes > 0:
        problems.append(("fail", f"no power provider in composition but {consumes:g} W is consumed"))

    result = aggregate(problems, "Voltage ranges overlap on all power wires; budget within limits.", check_id, name)
    result.details.extend(notes)
    return result
