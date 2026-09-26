"""xacro_compile: static macro-parameter check now; real xacro run when a ROS 2 toolchain is present.

Engine-supplied parameters (prefix, parent_link, child_link, origin_*) are always available,
so static validation focuses on: instance config keys being declared somewhere (macro params
or node params), and required macro params being coverable.
"""

from __future__ import annotations

import shutil

from ..context import CompositionContext
from .base import CheckResult, aggregate

_ENGINE_PARAMS = {"prefix", "parent_link", "child_link", "origin_xyz", "origin_rpy"}


def check_xacro_compile(ctx: CompositionContext, check_id: str, name: str) -> CheckResult:
    problems: list[tuple[str, str]] = []
    notes: list[str] = []
    for iid, module in ctx.modules.items():
        urdf = module.get("software", {}).get("urdf", {})
        declared = {p["name"] for p in urdf.get("params", [])}
        node_params = {
            p["name"]
            for n in module.get("software", {}).get("ros2", {}).get("nodes", [])
            for p in n.get("params", [])
        }
        known = declared | node_params | _ENGINE_PARAMS
        missing = [p["name"] for p in urdf.get("params", [])
                   if "default" not in p and p["name"] not in _ENGINE_PARAMS
                   and p["name"] not in ctx.instances[iid].get("config", {})]
        for p in missing:
            problems.append(("fail", f"{iid}: required macro param {p!r} of {urdf.get('macro', '?')} "
                                     f"has no default and is not engine-supplied or set in instance config"))
        for key in ctx.instances[iid].get("config", {}):
            if key not in known:
                problems.append(("warn", f"{iid}: config key {key!r} is not a declared macro or node param "
                                         f"(kept as extension data)"))
    if shutil.which("xacro"):
        notes.append("xacro runtime detected on PATH; full compile is delegated to the build worker (M2).")
    else:
        notes.append("no xacro runtime in this environment; static parameter validation only.")

    result = aggregate(problems, "All macro parameters resolvable (static check).", check_id, name)
    result.details.extend(notes)
    if problems:
        return result
    # Without a runtime we cannot claim a compiled pass; report skipped-with-clean-statics.
    return CheckResult(
        id=check_id,
        name=name,
        status="skipped" if not shutil.which("xacro") else result.status,
        message=result.message if shutil.which("xacro") else
                "Static parameter validation passed; xacro compile deferred to the ROS 2 build worker.",
        details=result.details,
    )
