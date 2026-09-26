from __future__ import annotations

from dataclasses import dataclass, field

from ..context import CompositionContext


@dataclass
class CheckResult:
    """Mirrors the composition schema's checkResult def."""

    id: str
    name: str
    status: str  # pass | warn | fail | skipped
    message: str = ""
    details: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "message": self.message,
            "details": self.details,
        }


def aggregate(problems: list[tuple[str, str]], ok_message: str, check_id: str, name: str) -> CheckResult:
    """problems: (severity, detail) pairs -> single CheckResult (fail > warn > pass)."""
    fails = [d for sev, d in problems if sev == "fail"]
    warns = [d for sev, d in problems if sev == "warn"]
    if fails:
        status, message = "fail", fails[0]
    elif warns:
        status, message = "warn", warns[0]
    else:
        status, message = "pass", ok_message
    return CheckResult(id=check_id, name=name, status=status, message=message, details=fails + warns)


def fmt_interface(inst: str, iface: dict) -> str:
    side = iface.get("side", "neutral")
    return f"{inst}.{iface['id']} ({iface['kind']}/{side})"
