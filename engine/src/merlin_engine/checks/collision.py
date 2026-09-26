"""collision: requires mesh assets and a transform solver; deferred to the geometry pipeline (M4)."""

from __future__ import annotations

from ..context import CompositionContext
from .base import CheckResult


def check_collision(ctx: CompositionContext, check_id: str, name: str) -> CheckResult:
    have_boxes = sum(
        1 for m in ctx.modules.values() if "bounding_box_m" in m.get("mechanical", {})
    )
    return CheckResult(
        id=check_id,
        name=name,
        status="skipped",
        message="Collision checking needs assembled geometry (mesh assets + transform solver); "
                "deferred to the M4 derivative pipeline.",
        details=[f"{have_boxes}/{len(ctx.modules)} resolved modules declare bounding_box_m (not sufficient alone)."],
    )
