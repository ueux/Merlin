"""Module registry: resolves (module_id, version) -> validated module manifest."""

from __future__ import annotations

import json
from pathlib import Path

from .errors import RegistryError
from .schemas import validate_document


class ModuleRegistry:
    """An immutable, version-pinned view over a set of module manifests.

    v1 backend: a directory of *.module.manifest.json files. The DB-backed
    registry (M3) implements the same resolve() contract.
    """

    def __init__(self, modules: dict[tuple[str, str], dict]):
        self._modules = modules

    @classmethod
    def from_directory(cls, path: str | Path, *, validate: bool = True) -> "ModuleRegistry":
        root = Path(path)
        if not root.is_dir():
            raise RegistryError(f"registry directory not found: {root}")
        modules: dict[tuple[str, str], dict] = {}
        for file in sorted(root.glob("*.module.manifest.json")):
            doc = json.loads(file.read_text(encoding="utf-8"))
            if validate:
                validate_document(doc, "module")
            key = (doc["module"]["id"], doc["module"]["version"])
            if key in modules:
                raise RegistryError(f"duplicate module version in registry: {key[0]}@{key[1]} ({file.name})")
            modules[key] = doc
        if not modules:
            raise RegistryError(f"no module manifests (*.module.manifest.json) found in {root}")
        return cls(modules)

    def resolve(self, module_id: str, version: str) -> dict:
        try:
            return self._modules[(module_id, version)]
        except KeyError:
            known = sorted(f"{mid}@{ver}" for mid, ver in self._modules if mid == module_id)
            hint = f" (known versions: {', '.join(known)})" if known else " (module id unknown)"
            raise RegistryError(f"cannot resolve {module_id}@{version}{hint}")

    def all(self) -> list[dict]:
        """All module manifests, sorted by (module_id, version)."""
        return [self._modules[key] for key in sorted(self._modules)]

    def __contains__(self, key: tuple[str, str]) -> bool:
        return key in self._modules

    def __len__(self) -> int:
        return len(self._modules)
