"""License intersection across all instantiated modules, per domain (hardware/software/docs).

v1 rules:
- Every registry module must carry a hardware license (schema-enforced).
- A module licensing a domain as proprietary/closed conflicts with every other module
  in that domain (viral incompatibility with distribution as an open bundle).
- Reciprocal hardware licenses (CERN-OHL-S/W) combined with a DIFFERENT hardware license
  produce a conflict warning pair (combined work cannot satisfy both grant styles).
"""

from __future__ import annotations

import itertools

from .context import CompositionContext

_DOMAINS = ("hardware", "software", "docs")
_CLOSED_MARKERS = ("proprietary", "closed", "all-rights-reserved", "none")
_RECIPROCAL_HW = ("CERN-OHL-S", "CERN-OHL-W", "GPL", "AGPL", "CC-BY-SA")


def _is_closed(license_id: str) -> bool:
    lowered = license_id.lower()
    return any(m in lowered for m in _CLOSED_MARKERS)


def _is_reciprocal(license_id: str) -> bool:
    return any(license_id.startswith(m) for m in _RECIPROCAL_HW)


def compute_license_report(ctx: CompositionContext) -> dict:
    report: dict = {"hardware": [], "software": [], "docs": [], "compatible": True, "conflicts": []}
    # domain -> license id -> [module ids]
    by_domain: dict[str, dict[str, list[str]]] = {d: {} for d in _DOMAINS}
    for module in ctx.modules.values():
        mid = module["module"]["id"]
        for domain in _DOMAINS:
            spec = module.get("licenses", {}).get(domain)
            if spec:
                by_domain[domain].setdefault(spec["id"], []).append(mid)

    for domain in _DOMAINS:
        report[domain] = sorted(by_domain[domain])

    for domain in _DOMAINS:
        licenses = by_domain[domain]
        for lid, owners in licenses.items():
            if _is_closed(lid) and len(licenses) > 1:
                others = sorted(o for l, os_ in licenses.items() for o in os_ if l != lid)
                report["conflicts"].append({
                    "modules": sorted(set(owners) | set(others))[:2] if len(set(owners) | set(others)) > 1 else sorted(set(owners)),
                    "detail": f"{domain}: closed license {lid} cannot be redistributed in a combined open bundle",
                })
        reciprocal = [l for l in licenses if _is_reciprocal(l)]
        for a, b in itertools.combinations(sorted(set(reciprocal) | set(licenses)), 2):
            if a != b and (_is_reciprocal(a) and _is_reciprocal(b)):
                pair_modules = sorted(set(licenses[a]) | set(licenses[b]))
                report["conflicts"].append({
                    "modules": pair_modules,
                    "detail": f"{domain}: reciprocal licenses {a} and {b} impose conflicting share-alike obligations",
                })
    report["compatible"] = not report["conflicts"]
    return report
