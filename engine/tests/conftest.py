"""Shared fixtures and synthetic-document factories for the merlin-engine test suite."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from merlin_engine import ModuleRegistry, validate_composition

WORKSPACE = Path(__file__).resolve().parents[2]
EXAMPLES = WORKSPACE / "examples"
ENGINE_SRC = WORKSPACE / "engine" / "src"


@pytest.fixture(scope="session")
def examples_registry() -> ModuleRegistry:
    return ModuleRegistry.from_directory(EXAMPLES)


@pytest.fixture()
def mini_leg() -> dict:
    return json.loads((EXAMPLES / "mini-leg.composition.json").read_text(encoding="utf-8"))


# -- synthetic document factories --------------------------------------------

def make_module(
    module_id: str,
    *,
    version: str = "1.0.0",
    category: str = "structure",
    mass_kg: float = 1.0,
    frames: tuple[str, ...] = ("body",),
    interfaces: list[dict] | None = None,
    buses: list[dict] | None = None,
    power: list[dict] | None = None,
    node_ids: dict | None = None,
    sw_interfaces: list[dict] | None = None,
    urdf_params: list[dict] | None = None,
    consumes_w: float = 0.0,
    provides_w: float = 0.0,
    hw_license: str = "MIT",
) -> dict:
    """Minimal module manifest that still passes module-manifest.schema.json."""
    if interfaces is None:
        interfaces = [{"id": "iface-main", "kind": "bracket", "side": "neutral", "plane": frames[0]}]
    mod = {
        "schema_version": "1.0.0",
        "module": {"id": module_id, "name": module_id, "version": version, "category": category},
        "licenses": {"hardware": {"id": hw_license}},
        "mechanical": {
            "mass_kg": mass_kg,
            "frames": [{"id": f, "origin": {"xyz": [0, 0, 0]}} for f in frames],
            "interfaces": interfaces,
        },
        "software": {
            "urdf": {
                "fragment": f"urdf/{module_id}.macro.xacro",
                "macro": f"{module_id.replace('-', '_')}_macro",
            }
        },
        "compat": {"power_budget": {"consumes_w": consumes_w, "provides_w": provides_w}},
    }
    if buses or power or node_ids:
        mod["electrical"] = {}
        if buses:
            mod["electrical"]["buses"] = buses
        if power:
            mod["electrical"]["power"] = power
        if node_ids:
            mod["electrical"]["node_ids"] = node_ids
    if sw_interfaces:
        mod["software"]["interfaces"] = sw_interfaces
    if urdf_params:
        mod["software"]["urdf"]["params"] = urdf_params
    return mod


def bracket_iface(
    iface_id: str,
    side: str,
    *,
    plane: str = "body",
    kind: str = "bracket",
    size: str = "M4",
    pitch: float = 30,
    tags: tuple[str, ...] = ("pattern:4xm4",),
    load: dict | None = None,
) -> dict:
    iface = {
        "id": iface_id,
        "kind": kind,
        "side": side,
        "plane": plane,
        "bolt_pattern": {
            "count": 4,
            "size": size,
            "layout": "rectangular",
            "pitch_x_mm": pitch,
            "pitch_y_mm": pitch,
        },
        "compatible_with": list(tags),
    }
    if load:
        iface["load"] = load
    return iface


def bus_module(module_id: str, protocol: str, baud: int, *, node_default: int = 1, node_max: int = 32) -> dict:
    return make_module(
        module_id,
        category="comms",
        buses=[{"id": "bus-main", "protocol": protocol, "baud": baud, "topology": "bus", "connector": "JST-GH-4"}],
        node_ids={"default": node_default, "configurable": True, "range": [1, node_max]},
    )


def power_module(
    module_id: str,
    *,
    provides: bool,
    voltage: list[float],
    connector: str = "XT60",
    provides_w: float = 0.0,
    consumes_w: float = 0.0,
) -> dict:
    return make_module(
        module_id,
        category="power",
        power=[{
            "id": "power-main",
            "voltage_range": voltage,
            "nominal_v": sum(voltage) / 2,
            "connector": connector,
            "provides": provides,
        }],
        provides_w=provides_w,
        consumes_w=consumes_w,
    )


def sw_module(
    module_id: str,
    iface_id: str,
    direction: str,
    *,
    type_: str = "sensor_msgs/JointState",
    kind: str = "topic",
    qos: dict | None = None,
) -> dict:
    iface = {"id": iface_id, "kind": kind, "type": type_, "direction": direction}
    if qos:
        iface["qos"] = qos
    return make_module(module_id, category="sensor", sw_interfaces=[iface])


def inst(
    iid: str,
    module_id: str,
    *,
    version: str = "1.0.0",
    parent: dict | None = None,
    node_id: int | None = None,
    config: dict | None = None,
) -> dict:
    d = {"id": iid, "module_id": module_id, "module_version": version}
    if parent:
        d["parent"] = parent
    if node_id is not None:
        d["node_id"] = node_id
    if config:
        d["config"] = config
    return d


def make_composition(
    instances: list[dict],
    mates: list[dict] | None = None,
    wiring: list[dict] | None = None,
    software_links: list[dict] | None = None,
) -> dict:
    doc = {
        "schema_version": "1.0.0",
        "composition": {"id": "test-comp", "name": "Test Composition"},
        "instances": instances,
        "mates": mates or [],
    }
    if wiring:
        doc["wiring"] = wiring
    if software_links:
        doc["software_links"] = software_links
    return doc


def write_registry(tmp_path: Path, modules: list[dict]) -> ModuleRegistry:
    for mod in modules:
        path = tmp_path / f"{mod['module']['id']}.module.manifest.json"
        path.write_text(json.dumps(mod, indent=2), encoding="utf-8")
    return ModuleRegistry.from_directory(tmp_path)


def run(doc: dict, registry: ModuleRegistry) -> dict:
    return validate_composition(doc, registry)


def checks_by_name(result: dict) -> dict[str, dict]:
    return {c["name"]: c for c in result["validation"]["checks"]}
