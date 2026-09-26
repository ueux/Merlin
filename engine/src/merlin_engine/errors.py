class SchemaValidationError(Exception):
    """Raised when a document fails its JSON Schema. Carries all violations."""

    def __init__(self, kind: str, messages: list[str]):
        self.kind = kind
        self.messages = messages
        super().__init__(f"{kind} failed schema validation:\n" + "\n".join(f"  - {m}" for m in messages))


class RegistryError(Exception):
    """Raised when a (module_id, version) cannot be resolved in the registry."""
