"""Loads the three MERLIN JSON Schemas and validates documents against them."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema

from .errors import SchemaValidationError

SCHEMA_DIR = Path(__file__).resolve().parents[3] / "schemas"

_KIND_FILES = {
    "robot": "robot-manifest.schema.json",
    "module": "module-manifest.schema.json",
    "composition": "composition.schema.json",
}

_cache: dict[str, dict] = {}


def load_schema(kind: str) -> dict:
    if kind not in _KIND_FILES:
        raise ValueError(f"unknown schema kind: {kind!r} (expected one of {sorted(_KIND_FILES)})")
    if kind not in _cache:
        schema = json.loads((SCHEMA_DIR / _KIND_FILES[kind]).read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        _cache[kind] = schema
    return _cache[kind]


def detect_kind(doc: dict) -> str:
    """Infers the document kind from its top-level shape."""
    if "instances" in doc and "mates" in doc:
        return "composition"
    if "module" in doc:
        return "module"
    if "robot" in doc:
        return "robot"
    raise ValueError("cannot detect document kind: expected top-level 'instances'+'mates', 'module', or 'robot'")


def validate_document(doc: dict, kind: str | None = None) -> str:
    """Validates doc against its schema. Returns the kind; raises SchemaValidationError listing every violation."""
    kind = kind or detect_kind(doc)
    validator = jsonschema.Draft202012Validator(load_schema(kind))
    errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path))
    if errors:
        messages = []
        for e in errors[:25]:
            path = "$" + "".join(f"[{p!r}]" if isinstance(p, int) else f".{p}" for p in e.absolute_path)
            messages.append(f"{path}: {e.message}")
        if len(errors) > 25:
            messages.append(f"... and {len(errors) - 25} more")
        raise SchemaValidationError(kind, messages)
    return kind
