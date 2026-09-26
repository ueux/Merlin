"""MERLIN manifest validation engine.

Public API:
    validate_document(doc, kind)          -> None (raises SchemaValidationError)
    ModuleRegistry.from_directory(path)   -> registry
    validate_composition(doc, registry)   -> {"validation": ..., "licenses": ...}
"""

from .errors import RegistryError, SchemaValidationError
from .registry import ModuleRegistry
from .schemas import detect_kind, validate_document
from .engine import validate_composition

__version__ = "0.1.0"

__all__ = [
    "ModuleRegistry",
    "RegistryError",
    "SchemaValidationError",
    "detect_kind",
    "validate_document",
    "validate_composition",
    "__version__",
]
