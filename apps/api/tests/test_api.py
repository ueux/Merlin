"""API tests: FastAPI surface over the examples registry."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

EXAMPLES = Path(__file__).resolve().parents[3] / "examples"


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("MERLIN_REGISTRY_DIR", str(EXAMPLES))
    from app.main import app

    return TestClient(app)


def test_health(client: TestClient):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["engine"]


def test_modules_lists_example_registry(client: TestClient):
    r = client.get("/modules")
    assert r.status_code == 200
    ids = {m["id"] for m in r.json()}
    assert ids == {"odri-actuator-60", "chassis-plate", "tube-link-300", "battery-pack-48v"}
    odri = next(m for m in r.json() if m["id"] == "odri-actuator-60")
    assert odri["version"] == "1.2.0"
    assert odri["category"] == "actuator"
    assert odri["licenses"]["hardware"] == "BSD-3-Clause"
    assert odri["mass_kg"] == 0.48
    assert "pattern:6xM3_on_25mm_PCD" in odri["compat"]


def test_module_versions(client: TestClient):
    r = client.get("/modules/odri-actuator-60")
    assert r.status_code == 200
    assert [v["version"] for v in r.json()["versions"]] == ["1.2.0"]


def test_unknown_module_404(client: TestClient):
    assert client.get("/modules/no-such-module").status_code == 404


def test_full_manifest_roundtrip(client: TestClient):
    r = client.get("/modules/odri-actuator-60/1.2.0")
    assert r.status_code == 200
    doc = r.json()
    assert doc["mechanical"]["interfaces"][0]["bolt_pattern"]["pcd_mm"] == 25.0
    assert doc["electrical"]["buses"][0]["protocol"] == "CAN-FD"


def test_unknown_version_404(client: TestClient):
    assert client.get("/modules/odri-actuator-60/9.9.9").status_code == 404


def test_validate_mini_leg(client: TestClient):
    doc = json.loads((EXAMPLES / "mini-leg.composition.json").read_text(encoding="utf-8"))
    r = client.post("/compositions/validate", json=doc)
    assert r.status_code == 200
    body = r.json()
    assert body["validation"]["status"] == "warnings"
    assert len(body["validation"]["checks"]) == 7
    assert len(body["validation"]["warnings"]) == 2
    assert "hardware" in body["licenses"]


def test_validate_schema_garbage_422(client: TestClient):
    r = client.post("/compositions/validate", json={"schema_version": "1.0.0"})
    assert r.status_code == 422
    assert r.json()["errors"]
