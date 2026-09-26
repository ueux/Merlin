"""Schema self-checks and validation of every shipped example document."""

from __future__ import annotations

import copy
import json

import pytest

from merlin_engine import SchemaValidationError, detect_kind, validate_document
from merlin_engine.schemas import load_schema

from conftest import EXAMPLES


def test_all_three_schemas_are_valid_draft_2020_12():
    for kind in ("robot", "module", "composition"):
        schema = load_schema(kind)  # check_schema() runs inside
        assert schema["$schema"].endswith("2020-12/schema")


def test_every_example_document_validates():
    files = sorted(EXAMPLES.glob("*.json"))
    assert len(files) >= 5, f"expected the shipped examples, found {files}"
    for path in files:
        doc = json.loads(path.read_text(encoding="utf-8"))
        kind = validate_document(doc)  # raises on any violation
        if path.name.endswith(".module.manifest.json"):
            assert kind == "module"
        elif path.name.endswith(".composition.json"):
            assert kind == "composition"


def test_detect_kind():
    module_doc = json.loads((EXAMPLES / "odri-actuator-60.module.manifest.json").read_text(encoding="utf-8"))
    comp_doc = json.loads((EXAMPLES / "mini-leg.composition.json").read_text(encoding="utf-8"))
    assert detect_kind(module_doc) == "module"
    assert detect_kind(comp_doc) == "composition"
    with pytest.raises(ValueError):
        detect_kind({"unrelated": True})


def test_invalid_ros_name_rejected(mini_leg):
    bad = copy.deepcopy(mini_leg)
    bad["instances"][0]["id"] = "Chassis"  # rosName must be lower_snake
    with pytest.raises(SchemaValidationError):
        validate_document(bad, "composition")


def test_missing_required_license_rejected(mini_leg, examples_registry):
    bad = copy.deepcopy(examples_registry.resolve("chassis-plate", "0.7.0"))
    del bad["licenses"]["hardware"]
    with pytest.raises(SchemaValidationError):
        validate_document(bad, "module")


def test_wrong_schema_version_rejected(mini_leg):
    bad = copy.deepcopy(mini_leg)
    bad["schema_version"] = "2.0.0"
    with pytest.raises(SchemaValidationError):
        validate_document(bad, "composition")


def test_error_message_lists_all_violations(mini_leg):
    bad = copy.deepcopy(mini_leg)
    bad["instances"][0]["id"] = "Bad ID"
    bad["instances"][1]["module_version"] = "not-semver"
    with pytest.raises(SchemaValidationError) as exc_info:
        validate_document(bad, "composition")
    assert len(exc_info.value.messages) >= 2
