"""ModuleRegistry: directory loading, resolution, and error paths."""

from __future__ import annotations

import json

import pytest

from merlin_engine import ModuleRegistry, RegistryError, SchemaValidationError

from conftest import make_module


def test_examples_registry_loads_all_modules(examples_registry):
    assert len(examples_registry) == 4
    assert ("odri-actuator-60", "1.2.0") in examples_registry
    assert ("chassis-plate", "0.7.0") in examples_registry
    assert ("tube-link-300", "0.9.0") in examples_registry
    assert ("battery-pack-48v", "0.4.1") in examples_registry


def test_resolve_returns_manifest(examples_registry):
    mod = examples_registry.resolve("odri-actuator-60", "1.2.0")
    assert mod["module"]["category"] == "actuator"


def test_resolve_unknown_module_id(examples_registry):
    with pytest.raises(RegistryError, match="module id unknown"):
        examples_registry.resolve("no-such-module", "1.0.0")


def test_resolve_unknown_version_lists_known(examples_registry):
    with pytest.raises(RegistryError, match=r"known versions: odri-actuator-60@1\.2\.0"):
        examples_registry.resolve("odri-actuator-60", "9.9.9")


def test_duplicate_module_version_rejected(tmp_path):
    mod = make_module("dup-mod")
    for name in ("a.module.manifest.json", "b.module.manifest.json"):
        (tmp_path / name).write_text(json.dumps(mod), encoding="utf-8")
    with pytest.raises(RegistryError, match="duplicate module version"):
        ModuleRegistry.from_directory(tmp_path)


def test_same_module_two_versions_is_fine(tmp_path):
    for version in ("1.0.0", "2.0.0"):
        mod = make_module("multi-mod", version=version)
        (tmp_path / f"multi-mod-{version}.module.manifest.json").write_text(json.dumps(mod), encoding="utf-8")
    registry = ModuleRegistry.from_directory(tmp_path)
    assert len(registry) == 2
    assert registry.resolve("multi-mod", "2.0.0")["module"]["version"] == "2.0.0"


def test_empty_directory_rejected(tmp_path):
    with pytest.raises(RegistryError, match="no module manifests"):
        ModuleRegistry.from_directory(tmp_path)


def test_missing_directory_rejected(tmp_path):
    with pytest.raises(RegistryError, match="registry directory not found"):
        ModuleRegistry.from_directory(tmp_path / "nope")


def test_invalid_manifest_rejected_at_load(tmp_path):
    mod = make_module("broken-mod")
    del mod["mechanical"]["mass_kg"]
    (tmp_path / "broken-mod.module.manifest.json").write_text(json.dumps(mod), encoding="utf-8")
    with pytest.raises(SchemaValidationError):
        ModuleRegistry.from_directory(tmp_path)
