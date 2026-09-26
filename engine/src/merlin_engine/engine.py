"""Composition orchestrator: schema validation -> referential integrity -> 7 checks -> license report.

Returns exactly the composition schema's COMPUTED sections (validation, licenses) so the
result can be embedded into the document or returned by the API verbatim.
"""

from __future__ import annotations

from .checks import CHECKS
from .context import CompositionContext
from .licenses import compute_license_report
from .registry import ModuleRegistry
from .schemas import validate_document


def validate_composition(
    doc: dict,
    registry: ModuleRegistry,
    *,
    skip_schema: bool = False,
) -> dict:
    """Full composition validation. Returns {"validation": ..., "licenses": ...}."""
    if not skip_schema:
        validate_document(doc, "composition")

    ctx = CompositionContext(doc, registry)

    checks = [fn(ctx, check_id, name) for check_id, name, fn in CHECKS]

    fails = [c for c in checks if c.status == "fail"]
    warns = [c for c in checks if c.status == "warn"]
    structural = list(ctx.errors)

    if structural or fails:
        status = "invalid"
    elif warns:
        status = "warnings"
    else:
        status = "valid"

    validation = {
        "status": status,
        "checks": [c.to_dict() for c in checks],
        "errors": structural + [f"{c.name}: {c.message}" for c in fails],
        "warnings": [f"{c.name}: {c.message}" for c in warns],
    }
    return {"validation": validation, "licenses": compute_license_report(ctx)}
