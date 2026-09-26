"""software_interfaces: kind/type/direction/QoS matching for declared software_links."""

from __future__ import annotations

from ..context import CompositionContext
from .base import CheckResult, aggregate

_OK_PAIRS = {
    ("pub", "sub"),
    ("server", "client"),
    ("both", "pub"), ("pub", "both"),
    ("both", "sub"), ("sub", "both"),
    ("both", "server"), ("server", "both"),
    ("both", "client"), ("client", "both"),
    ("both", "both"),
}


def check_software_interfaces(ctx: CompositionContext, check_id: str, name: str) -> CheckResult:
    problems: list[tuple[str, str]] = []
    links = ctx.doc.get("software_links", [])
    checked = 0
    for link in links:
        lid = link["id"]
        sa = ctx.sw_interface(link["from"]["instance"], link["from"]["interface"])
        sb = ctx.sw_interface(link["to"]["instance"], link["to"]["interface"])
        if sa is None:
            problems.append(("fail", f"{lid}: interface {link['from']['instance']}.{link['from']['interface']} not found"))
            continue
        if sb is None:
            problems.append(("fail", f"{lid}: interface {link['to']['instance']}.{link['to']['interface']} not found"))
            continue
        checked += 1
        if sa["kind"] != link["kind"] or sb["kind"] != link["kind"]:
            problems.append(("fail", f"{lid}: kind mismatch (link {link['kind']}, "
                                     f"{link['from']['interface']} {sa['kind']}, {link['to']['interface']} {sb['kind']})"))
        if sa["type"] != sb["type"]:
            problems.append(("fail", f"{lid}: type mismatch {sa['type']} vs {sb['type']}"))
        if (sa["direction"], sb["direction"]) not in _OK_PAIRS:
            problems.append(("fail", f"{lid}: direction pairing {sa['direction']} -> {sb['direction']} cannot connect"))
        qa, qb = sa.get("qos", {}), sb.get("qos", {})
        # ROS 2 QoS rules: a reliable subscriber never matches a best-effort publisher;
        # a transient_local subscriber never matches a volatile publisher.
        if qa.get("reliability") == "best_effort" and qb.get("reliability", "reliable") == "reliable":
            problems.append(("fail", f"{lid}: QoS incompatible — best_effort publisher cannot feed reliable subscriber"))
        if qa.get("durability", "volatile") == "volatile" and qb.get("durability") == "transient_local":
            problems.append(("fail", f"{lid}: QoS incompatible — volatile publisher cannot feed transient_local subscriber"))
    ok = f"{checked}/{len(links)} software links matched on kind, type, direction and QoS." if links else \
         "No software links declared; nothing to match."
    return aggregate(problems, ok, check_id, name)
