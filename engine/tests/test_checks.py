"""Per-check unit tests over synthetic compositions."""

from __future__ import annotations

import pytest

from conftest import (
    bracket_iface,
    bus_module,
    checks_by_name,
    inst,
    make_composition,
    make_module,
    power_module,
    run,
    sw_module,
    write_registry,
)


# -- mate_matching ------------------------------------------------------------

def _mate_lab(tmp_path, child_iface, root_iface, *, mate_type=None, child_mass=1.0):
    child = make_module("child-mod", mass_kg=child_mass, interfaces=[child_iface])
    root = make_module("root-mod", interfaces=[root_iface])
    registry = write_registry(tmp_path, [child, root])
    mate = {
        "id": "m1",
        "a": {"instance": "child", "interface": child_iface["id"]},
        "b": {"instance": "root", "interface": root_iface["id"]},
    }
    if mate_type:
        mate["type"] = mate_type
    doc = make_composition(
        [
            inst("root", "root-mod"),
            inst("child", "child-mod", parent={"instance": "root", "frame": "body"}),
        ],
        mates=[mate],
    )
    return run(doc, registry)


def test_mate_compatible_pair_passes(tmp_path):
    result = _mate_lab(
        tmp_path,
        bracket_iface("iface-a", "male"),
        bracket_iface("iface-b", "female"),
    )
    assert checks_by_name(result)["mate_matching"]["status"] == "pass"


def test_mate_kind_mismatch_fails(tmp_path):
    result = _mate_lab(
        tmp_path,
        bracket_iface("iface-a", "male", kind="flange"),
        bracket_iface("iface-b", "female", kind="bracket"),
    )
    check = checks_by_name(result)["mate_matching"]
    assert check["status"] == "fail"
    assert "kind mismatch" in check["message"]


def test_mate_non_complementary_sides_fail(tmp_path):
    result = _mate_lab(
        tmp_path,
        bracket_iface("iface-a", "male"),
        bracket_iface("iface-b", "male"),
    )
    check = checks_by_name(result)["mate_matching"]
    assert check["status"] == "fail"
    assert "non-complementary sides" in check["message"]


def test_mate_bolt_size_mismatch_fails(tmp_path):
    result = _mate_lab(
        tmp_path,
        bracket_iface("iface-a", "male", size="M3"),
        bracket_iface("iface-b", "female", size="M4"),
    )
    check = checks_by_name(result)["mate_matching"]
    assert check["status"] == "fail"
    assert "bolt pattern mismatch" in check["message"]


def test_mate_pitch_mismatch_fails(tmp_path):
    result = _mate_lab(
        tmp_path,
        bracket_iface("iface-a", "male", pitch=30),
        bracket_iface("iface-b", "female", pitch=40),
    )
    check = checks_by_name(result)["mate_matching"]
    assert check["status"] == "fail"
    assert "pitch mismatch" in check["message"]


def test_mate_disjoint_tags_warn(tmp_path):
    result = _mate_lab(
        tmp_path,
        bracket_iface("iface-a", "male", tags=("pattern:a",)),
        bracket_iface("iface-b", "female", tags=("pattern:b",)),
    )
    check = checks_by_name(result)["mate_matching"]
    assert check["status"] == "warn"
    assert "compatible_with" in check["message"]


def test_mate_authored_type_mismatch_warns(tmp_path):
    result = _mate_lab(
        tmp_path,
        bracket_iface("iface-a", "male"),
        bracket_iface("iface-b", "female"),
        mate_type="magnetic",  # bracket/bracket computes to "bolted"
    )
    check = checks_by_name(result)["mate_matching"]
    assert check["status"] == "warn"
    assert "differs from computed" in check["message"]


def test_mate_unknown_interface_fails(tmp_path):
    root = make_module("root-mod")
    registry = write_registry(tmp_path, [root])
    doc = make_composition(
        [inst("root", "root-mod")],
        mates=[{
            "id": "m1",
            "a": {"instance": "root", "interface": "iface-ghost"},
            "b": {"instance": "root", "interface": "iface-main"},
        }],
    )
    check = checks_by_name(run(doc, registry))["mate_matching"]
    assert check["status"] == "fail"
    assert "not found" in check["message"]


# -- load_rating --------------------------------------------------------------

def test_load_within_rating_passes(tmp_path):
    result = _mate_lab(
        tmp_path,
        bracket_iface("iface-a", "male"),
        bracket_iface("iface-b", "female", load={"axial_n": 100}),
        child_mass=1.0,  # 9.81 N << 100 N
    )
    assert checks_by_name(result)["load_rating"]["status"] == "pass"


def test_load_above_80_percent_warns(tmp_path):
    result = _mate_lab(
        tmp_path,
        bracket_iface("iface-a", "male"),
        bracket_iface("iface-b", "female", load={"axial_n": 100}),
        child_mass=9.0,  # 88.3 N > 80 N
    )
    check = checks_by_name(result)["load_rating"]
    assert check["status"] == "warn"
    assert "80%" in check["message"]


def test_load_exceeding_rating_fails(tmp_path):
    result = _mate_lab(
        tmp_path,
        bracket_iface("iface-a", "male"),
        bracket_iface("iface-b", "female", load={"axial_n": 100}),
        child_mass=50.0,  # 490.5 N > 100 N
    )
    check = checks_by_name(result)["load_rating"]
    assert check["status"] == "fail"
    assert "exceeds rating" in check["message"]


def test_load_counts_whole_downstream_branch(tmp_path):
    # root <- mid (40 kg) <- leaf (15 kg): the mid/root mate carries 55 kg = 539.6 N
    leaf = make_module("leaf-mod", mass_kg=15.0)
    mid = make_module("mid-mod", mass_kg=40.0)
    root = make_module(
        "root-mod",
        interfaces=[bracket_iface("iface-b", "female", load={"axial_n": 500})],
    )
    registry = write_registry(tmp_path, [leaf, mid, root])
    doc = make_composition(
        [
            inst("root", "root-mod"),
            inst("mid", "mid-mod", parent={"instance": "root", "frame": "body"}),
            inst("leaf", "leaf-mod", parent={"instance": "mid", "frame": "body"}),
        ],
        mates=[{
            "id": "m1",
            "a": {"instance": "mid", "interface": "iface-main"},
            "b": {"instance": "root", "interface": "iface-b"},
        }],
    )
    check = checks_by_name(run(doc, registry))["load_rating"]
    assert check["status"] == "fail"
    assert "55.00 kg" in check["message"]


# -- power_budget -------------------------------------------------------------

def _power_lab(tmp_path, src, dst, *, wire=True, extra_modules=()):
    modules = [m for m in (src, dst) if m is not None] + list(extra_modules)
    registry = write_registry(tmp_path, modules)
    instances = [inst(m["module"]["id"].replace("-", "_"), m["module"]["id"]) for m in modules]
    wiring = []
    if wire and src is not None and dst is not None:
        wiring = [{
            "id": "w1",
            "kind": "power",
            "from": {"instance": src["module"]["id"].replace("-", "_"), "port": "power-main"},
            "to": {"instance": dst["module"]["id"].replace("-", "_"), "port": "power-main"},
        }]
    return run(make_composition(instances, wiring=wiring), registry)


def test_power_clean_wire_passes(tmp_path):
    src = power_module("batt-mod", provides=True, voltage=[42, 50.4], provides_w=480)
    dst = power_module("load-mod", provides=False, voltage=[10, 48], consumes_w=96)
    assert checks_by_name(_power_lab(tmp_path, src, dst))["power_budget"]["status"] == "pass"


def test_power_consumer_wired_as_source_fails(tmp_path):
    src = power_module("load-mod", provides=False, voltage=[10, 48], consumes_w=10)
    dst = power_module("batt-mod", provides=True, voltage=[42, 50.4], provides_w=480)
    check = checks_by_name(_power_lab(tmp_path, src, dst))["power_budget"]
    assert check["status"] == "fail"
    assert "provides=false" in check["message"]


def test_power_no_voltage_overlap_fails(tmp_path):
    src = power_module("batt-mod", provides=True, voltage=[42, 50.4], provides_w=480)
    dst = power_module("load-mod", provides=False, voltage=[10, 30], consumes_w=10)
    check = checks_by_name(_power_lab(tmp_path, src, dst))["power_budget"]
    assert check["status"] == "fail"
    assert "no voltage overlap" in check["message"]


def test_power_connector_mismatch_warns(tmp_path):
    src = power_module("batt-mod", provides=True, voltage=[42, 50.4], connector="XT60", provides_w=480)
    dst = power_module("load-mod", provides=False, voltage=[10, 48], connector="XT30", consumes_w=96)
    check = checks_by_name(_power_lab(tmp_path, src, dst))["power_budget"]
    assert check["status"] == "warn"
    assert "connector mismatch" in check["message"]
    assert "XT60" in check["message"] and "XT30" in check["message"]


def test_power_consumers_without_provider_fail(tmp_path):
    consumer = power_module("load-mod", provides=False, voltage=[10, 48], consumes_w=50)
    check = checks_by_name(_power_lab(tmp_path, consumer, None, wire=False))["power_budget"]
    assert check["status"] == "fail"
    assert "no power provider" in check["message"]


def test_power_deficit_fails(tmp_path):
    src = power_module("batt-mod", provides=True, voltage=[42, 50.4], provides_w=10)
    dst = power_module("load-mod", provides=False, voltage=[10, 48], consumes_w=96)
    check = checks_by_name(_power_lab(tmp_path, src, dst))["power_budget"]
    assert check["status"] == "fail"
    assert "deficit" in check["message"]


def test_power_headroom_warns(tmp_path):
    src = power_module("batt-mod", provides=True, voltage=[42, 50.4], provides_w=100)
    dst = power_module("load-mod", provides=False, voltage=[10, 48], consumes_w=96)
    check = checks_by_name(_power_lab(tmp_path, src, dst))["power_budget"]
    assert check["status"] == "warn"
    assert "headroom" in check["message"]


# -- bus_config ---------------------------------------------------------------

def _bus_lab(tmp_path, mod_a, mod_b, *, inst_a=None, inst_b=None):
    registry = write_registry(tmp_path, [mod_a, mod_b])
    id_a = inst_a or inst("mod_a", mod_a["module"]["id"])
    id_b = inst_b or inst("mod_b", mod_b["module"]["id"])
    doc = make_composition(
        [id_a, id_b],
        wiring=[{
            "id": "w1",
            "kind": "bus",
            "from": {"instance": id_a["id"], "port": "bus-main"},
            "to": {"instance": id_b["id"], "port": "bus-main"},
        }],
    )
    return run(doc, registry)


def test_bus_same_protocol_and_baud_passes(tmp_path):
    result = _bus_lab(
        tmp_path,
        bus_module("node-a", "CAN", 1_000_000, node_default=1),
        bus_module("node-b", "CAN", 1_000_000, node_default=2),
    )
    assert checks_by_name(result)["bus_config"]["status"] == "pass"


def test_bus_can_vs_canfd_warns(tmp_path):
    result = _bus_lab(
        tmp_path,
        bus_module("node-a", "CAN", 1_000_000, node_default=1),
        bus_module("node-b", "CAN-FD", 5_000_000, node_default=2),
    )
    check = checks_by_name(result)["bus_config"]
    assert check["status"] == "warn"
    assert "CAN" in check["message"] and "CAN-FD" in check["message"]


def test_bus_can_vs_uart_fails(tmp_path):
    result = _bus_lab(
        tmp_path,
        bus_module("node-a", "CAN", 1_000_000, node_default=1),
        bus_module("node-b", "UART", 115_200, node_default=2),
    )
    check = checks_by_name(result)["bus_config"]
    assert check["status"] == "fail"
    assert "incompatible protocols" in check["message"]


def test_bus_baud_mismatch_fails(tmp_path):
    result = _bus_lab(
        tmp_path,
        bus_module("node-a", "CAN", 500_000, node_default=1),
        bus_module("node-b", "CAN", 1_000_000, node_default=2),
    )
    check = checks_by_name(result)["bus_config"]
    assert check["status"] == "fail"
    assert "baud mismatch" in check["message"]


def test_bus_node_id_collision_fails(tmp_path):
    mod_a = bus_module("node-a", "CAN", 1_000_000, node_default=1)
    mod_b = bus_module("node-b", "CAN", 1_000_000, node_default=1)
    result = _bus_lab(tmp_path, mod_a, mod_b)
    check = checks_by_name(result)["bus_config"]
    assert check["status"] == "fail"
    assert "collision" in check["message"]


def test_bus_node_id_out_of_range_fails(tmp_path):
    mod_a = bus_module("node-a", "CAN", 1_000_000, node_default=1, node_max=32)
    mod_b = bus_module("node-b", "CAN", 1_000_000, node_default=2)
    result = _bus_lab(tmp_path, mod_a, mod_b, inst_a=inst("mod_a", "node-a", node_id=99))
    check = checks_by_name(result)["bus_config"]
    assert check["status"] == "fail"
    assert "outside module range" in check["message"]


def test_bus_separate_segments_do_not_collide(tmp_path):
    # Two unwired pairs may reuse the same node id.
    mod_a = bus_module("node-a", "CAN", 1_000_000, node_default=1)
    mod_b = bus_module("node-b", "CAN", 1_000_000, node_default=1)
    registry = write_registry(tmp_path, [mod_a, mod_b])
    doc = make_composition([inst("mod_a", "node-a"), inst("mod_b", "node-b")])  # no bus wire
    check = checks_by_name(run(doc, registry))["bus_config"]
    assert check["status"] == "pass"


# -- software_interfaces ------------------------------------------------------

def _sw_lab(tmp_path, mod_a, mod_b, *, link_kind="topic"):
    registry = write_registry(tmp_path, [mod_a, mod_b])
    doc = make_composition(
        [inst("mod_a", mod_a["module"]["id"]), inst("mod_b", mod_b["module"]["id"])],
        software_links=[{
            "id": "l1",
            "kind": link_kind,
            "from": {"instance": "mod_a", "interface": "iface-out"},
            "to": {"instance": "mod_b", "interface": "iface-in"},
        }],
    )
    return run(doc, registry)


def test_sw_pub_sub_passes(tmp_path):
    result = _sw_lab(
        tmp_path,
        sw_module("pub-mod", "iface-out", "pub"),
        sw_module("sub-mod", "iface-in", "sub"),
    )
    assert checks_by_name(result)["software_interfaces"]["status"] == "pass"


def test_sw_type_mismatch_fails(tmp_path):
    result = _sw_lab(
        tmp_path,
        sw_module("pub-mod", "iface-out", "pub", type_="sensor_msgs/JointState"),
        sw_module("sub-mod", "iface-in", "sub", type_="geometry_msgs/Twist"),
    )
    check = checks_by_name(result)["software_interfaces"]
    assert check["status"] == "fail"
    assert "type mismatch" in check["message"]


def test_sw_pub_to_pub_fails(tmp_path):
    result = _sw_lab(
        tmp_path,
        sw_module("pub-mod", "iface-out", "pub"),
        sw_module("sub-mod", "iface-in", "pub"),
    )
    check = checks_by_name(result)["software_interfaces"]
    assert check["status"] == "fail"
    assert "direction pairing" in check["message"]


def test_sw_best_effort_pub_cannot_feed_reliable_sub(tmp_path):
    result = _sw_lab(
        tmp_path,
        sw_module("pub-mod", "iface-out", "pub", qos={"reliability": "best_effort"}),
        sw_module("sub-mod", "iface-in", "sub", qos={"reliability": "reliable"}),
    )
    check = checks_by_name(result)["software_interfaces"]
    assert check["status"] == "fail"
    assert "QoS" in check["message"]


def test_sw_volatile_pub_cannot_feed_transient_local_sub(tmp_path):
    result = _sw_lab(
        tmp_path,
        sw_module("pub-mod", "iface-out", "pub", qos={"durability": "volatile"}),
        sw_module("sub-mod", "iface-in", "sub", qos={"durability": "transient_local"}),
    )
    check = checks_by_name(result)["software_interfaces"]
    assert check["status"] == "fail"
    assert "QoS" in check["message"]


def test_sw_kind_mismatch_fails(tmp_path):
    result = _sw_lab(
        tmp_path,
        sw_module("pub-mod", "iface-out", "pub", kind="topic"),
        sw_module("sub-mod", "iface-in", "server", kind="service"),
        link_kind="topic",
    )
    check = checks_by_name(result)["software_interfaces"]
    assert check["status"] == "fail"
    assert "kind mismatch" in check["message"]


def test_sw_no_links_passes(tmp_path):
    mod = make_module("solo-mod")
    registry = write_registry(tmp_path, [mod])
    check = checks_by_name(run(make_composition([inst("solo", "solo-mod")]), registry))["software_interfaces"]
    assert check["status"] == "pass"


# -- collision / xacro_compile -------------------------------------------------

def test_collision_is_honestly_skipped(tmp_path):
    mod = make_module("solo-mod")
    registry = write_registry(tmp_path, [mod])
    check = checks_by_name(run(make_composition([inst("solo", "solo-mod")]), registry))["collision"]
    assert check["status"] == "skipped"


def test_xacro_missing_required_param_fails(tmp_path):
    mod = make_module("param-mod", urdf_params=[{"name": "length_m"}])
    registry = write_registry(tmp_path, [mod])
    check = checks_by_name(run(make_composition([inst("mod_a", "param-mod")]), registry))["xacro_compile"]
    assert check["status"] == "fail"
    assert "length_m" in check["message"]


def test_xacro_config_covers_required_param(tmp_path):
    mod = make_module("param-mod", urdf_params=[{"name": "length_m"}])
    registry = write_registry(tmp_path, [mod])
    doc = make_composition([inst("mod_a", "param-mod", config={"length_m": "0.3"})])
    check = checks_by_name(run(doc, registry))["xacro_compile"]
    assert check["status"] in ("skipped", "pass")  # skipped without a xacro runtime


def test_xacro_unknown_config_key_warns(tmp_path):
    mod = make_module("param-mod")
    registry = write_registry(tmp_path, [mod])
    doc = make_composition([inst("mod_a", "param-mod", config={"bogus_key": "1"})])
    check = checks_by_name(run(doc, registry))["xacro_compile"]
    assert check["status"] == "warn"
    assert "bogus_key" in check["message"]


def test_xacro_engine_supplied_params_need_no_config(tmp_path):
    params = [{"name": n} for n in ("prefix", "parent_link", "child_link")]
    mod = make_module("param-mod", urdf_params=params)
    registry = write_registry(tmp_path, [mod])
    check = checks_by_name(run(make_composition([inst("mod_a", "param-mod")]), registry))["xacro_compile"]
    assert check["status"] in ("skipped", "pass")


# -- aggregation ---------------------------------------------------------------

def test_engine_always_returns_all_seven_checks(tmp_path):
    mod = make_module("solo-mod")
    registry = write_registry(tmp_path, [mod])
    result = run(make_composition([inst("solo", "solo-mod")]), registry)
    names = {c["name"] for c in result["validation"]["checks"]}
    assert names == {
        "mate_matching", "load_rating", "collision", "power_budget",
        "bus_config", "software_interfaces", "xacro_compile",
    }
