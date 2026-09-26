"""MERLIN API: HTTP front-end over merlin-engine.

Run from this directory:  uvicorn app.main:app --reload --port 8000
Registry source:          MERLIN_REGISTRY_DIR (default: <workspace>/examples)
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from merlin_engine import (
    ModuleRegistry,
    RegistryError,
    SchemaValidationError,
    __version__,
    validate_composition,
)

WORKSPACE = Path(__file__).resolve().parents[3]

app = FastAPI(title="MERLIN API", version=__version__)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache(maxsize=4)
def _load_registry(path: str) -> ModuleRegistry:
    return ModuleRegistry.from_directory(path)


def get_registry() -> ModuleRegistry:
    path = os.environ.get("MERLIN_REGISTRY_DIR", str(WORKSPACE / "examples"))
    try:
        return _load_registry(path)
    except RegistryError as exc:
        raise HTTPException(status_code=500, detail=f"registry unavailable: {exc}")


@app.exception_handler(SchemaValidationError)
async def schema_error(_: Request, exc: SchemaValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": f"{exc.kind} failed schema validation", "errors": exc.messages},
    )


@app.exception_handler(RegistryError)
async def registry_error(_: Request, exc: RegistryError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})


def _summary(doc: dict) -> dict:
    m = doc["module"]
    interfaces = doc.get("mechanical", {}).get("interfaces", [])
    compat = list(dict.fromkeys(c for i in interfaces for c in i.get("compatible_with", [])))
    return {
        "id": m["id"],
        "version": m["version"],
        "name": m.get("name", m["id"]),
        "category": m.get("category"),
        "vendor": m.get("vendor"),
        "description": m.get("description", ""),
        "tags": m.get("tags", []),
        "licenses": {k: v.get("id") for k, v in doc.get("licenses", {}).items()},
        "mass_kg": doc.get("mechanical", {}).get("mass_kg"),
        "power_budget": doc.get("compat", {}).get("power_budget"),
        "interfaces": [i["id"] for i in interfaces],
        "compat": compat,
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "engine": __version__}


@app.get("/modules")
def list_modules(registry: ModuleRegistry = Depends(get_registry)) -> list[dict]:
    return [_summary(doc) for doc in registry.all()]


@app.get("/modules/{module_id}")
def module_versions(module_id: str, registry: ModuleRegistry = Depends(get_registry)) -> dict:
    docs = [d for d in registry.all() if d["module"]["id"] == module_id]
    if not docs:
        raise HTTPException(status_code=404, detail=f"unknown module id: {module_id}")
    return {"id": module_id, "versions": [_summary(d) for d in docs]}


@app.get("/modules/{module_id}/{version}")
def module_manifest(
    module_id: str, version: str, registry: ModuleRegistry = Depends(get_registry)
) -> dict:
    try:
        return registry.resolve(module_id, version)
    except RegistryError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@app.post("/compositions/validate")
def validate(doc: dict, registry: ModuleRegistry = Depends(get_registry)) -> dict:
    return validate_composition(doc, registry)
