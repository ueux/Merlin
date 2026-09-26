"""End-to-end runs against the shipped mini-leg composition, plus the CLI."""

from __future__ import annotations

import copy
import json
import os
import subprocess
import sys

from merlin_engine import validate_composition

from conftest import ENGINE_SRC, EXAMPLES, checks_by_name


def test_mini_leg_status_is_warnings(mini_leg, examples_registry):
    result = validate_composition(mini_leg, examples_registry)
    validation = result["validation"]
    assert validation["status"] == "warnings"
    assert validation["errors"] == []
    assert len(validation["warnings"]) == 2


def test_mini_leg_all_seven_checks_present(mini_leg, examples_registry):
    result = validate_composition(mini_leg, examples_registry)
    names = [c["name"] for c in result["validation"]["checks"]]
    assert names == [
        "mate_matching", "load_rating", "collision", "power_budget",
        "bus_config", "software_interfaces", "xacro_compile",
    ]


def test_mini_leg_check_statuses(mini_leg, examples_registry):
    checks = checks_by_name(validate_composition(mini_leg, examples_registry))
    assert checks["mate_matching"]["status"] == "pass"
    assert checks["load_rating"]["status"] == "pass"
    assert checks["collision"]["status"] == "skipped"
    assert checks["power_budget"]["status"] == "warn"
    assert "XT60" in checks["power_budget"]["message"]  # XT60 -> XT30 adapter
    assert checks["bus_config"]["status"] == "warn"
    assert "CAN-FD" in checks["bus_config"]["message"]  # classic CAN vs CAN-FD
    assert checks["software_interfaces"]["status"] == "pass"
    assert checks["xacro_compile"]["status"] in ("skipped", "pass")


def test_mini_leg_licenses(mini_leg, examples_registry):
    licenses = validate_composition(mini_leg, examples_registry)["licenses"]
    assert licenses["compatible"] is True
    assert licenses["conflicts"] == []
    assert set(licenses["hardware"]) == {"BSD-3-Clause", "CERN-OHL-P-2.0"}
    assert set(licenses["software"]) == {"BSD-3-Clause", "MIT"}
    assert licenses["docs"] == ["CC-BY-SA-4.0"]


def test_result_is_json_serializable(mini_leg, examples_registry):
    result = validate_composition(mini_leg, examples_registry)
    assert json.loads(json.dumps(result)) == result


def test_unresolvable_module_marks_invalid(mini_leg, examples_registry):
    bad = copy.deepcopy(mini_leg)
    bad["instances"][0]["module_id"] = "no-such-module"
    result = validate_composition(bad, examples_registry)
    assert result["validation"]["status"] == "invalid"
    assert any("no-such-module" in e for e in result["validation"]["errors"])
    assert len(result["validation"]["checks"]) == 7  # checks still run on what resolved


def test_duplicate_instance_id_marks_invalid(mini_leg, examples_registry):
    bad = copy.deepcopy(mini_leg)
    bad["instances"].append(copy.deepcopy(bad["instances"][1]))
    result = validate_composition(bad, examples_registry)
    assert result["validation"]["status"] == "invalid"
    assert any("duplicate instance id" in e for e in result["validation"]["errors"])


def test_unknown_parent_frame_marks_invalid(mini_leg, examples_registry):
    bad = copy.deepcopy(mini_leg)
    bad["instances"][1]["parent"]["frame"] = "no_such_frame"
    result = validate_composition(bad, examples_registry)
    assert result["validation"]["status"] == "invalid"
    assert any("no_such_frame" in e for e in result["validation"]["errors"])


def test_disconnected_cycle_marks_invalid(mini_leg, examples_registry):
    bad = copy.deepcopy(mini_leg)
    bad["instances"][1]["parent"] = {"instance": "main_batt", "frame": "body"}
    bad["instances"][3]["parent"] = {"instance": "hip", "frame": "base"}
    result = validate_composition(bad, examples_registry)
    assert result["validation"]["status"] == "invalid"
    assert result["validation"]["errors"]


def _cli(*args: str) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ENGINE_SRC) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, "-m", "merlin_engine", *args],
        capture_output=True, text=True, env=env, timeout=60,
    )


def test_cli_validate_composition():
    proc = _cli("validate", str(EXAMPLES / "mini-leg.composition.json"), "--registry", str(EXAMPLES))
    assert proc.returncode == 0, proc.stderr
    assert "[WARN] bus_config" in proc.stdout
    assert "[WARN] power_budget" in proc.stdout
    assert "status: warnings" in proc.stdout
    assert "compatible=True" in proc.stdout


def test_cli_validate_module_manifest_needs_no_registry():
    proc = _cli("validate", str(EXAMPLES / "odri-actuator-60.module.manifest.json"))
    assert proc.returncode == 0, proc.stderr
    assert "VALID module manifest" in proc.stdout


def test_cli_json_output_parses():
    proc = _cli(
        "validate", str(EXAMPLES / "mini-leg.composition.json"),
        "--registry", str(EXAMPLES), "--json",
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["validation"]["status"] == "warnings"
