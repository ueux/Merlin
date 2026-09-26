"""CLI: merlin-engine validate <file> [--registry DIR] [--write] [--json]"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .engine import validate_composition
from .errors import RegistryError, SchemaValidationError
from .registry import ModuleRegistry
from .schemas import detect_kind, validate_document

_STATUS_ICON = {"pass": "PASS", "warn": "WARN", "fail": "FAIL", "skipped": "SKIP"}


def _cmd_validate(args: argparse.Namespace) -> int:
    doc = json.loads(Path(args.file).read_text(encoding="utf-8"))
    kind = detect_kind(doc)

    if kind != "composition":
        validate_document(doc, kind)
        print(f"{args.file}: VALID {kind} manifest")
        return 0

    if args.registry is None:
        print("error: composition validation requires --registry DIR", file=sys.stderr)
        return 2
    registry = ModuleRegistry.from_directory(args.registry)
    result = validate_composition(doc, registry)
    validation, licenses = result["validation"], result["licenses"]

    if args.write:
        doc["validation"] = validation
        doc["licenses"] = licenses
        Path(args.file).write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
        print(f"wrote computed sections back to {args.file}")

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for check in validation["checks"]:
            print(f"[{_STATUS_ICON[check['status']]}] {check['name']}: {check['message']}")
            for detail in check["details"]:
                print(f"       - {detail}")
        print(f"\nstatus: {validation['status']}")
        for w in validation["warnings"]:
            print(f"  warning: {w}")
        for e in validation["errors"]:
            print(f"  error:   {e}")
        hw = ", ".join(licenses["hardware"]) or "-"
        sw = ", ".join(licenses["software"]) or "-"
        print(f"licenses: hardware [{hw}] software [{sw}] compatible={licenses['compatible']}")

    return 1 if validation["status"] == "invalid" else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="merlin-engine", description="MERLIN manifest validation engine")
    sub = parser.add_subparsers(dest="command", required=True)
    p_val = sub.add_parser("validate", help="validate a manifest or composition document")
    p_val.add_argument("file", help="path to the document (kind auto-detected)")
    p_val.add_argument("--registry", help="directory of *.module.manifest.json (required for compositions)")
    p_val.add_argument("--write", action="store_true", help="write computed validation/licenses sections back into the file")
    p_val.add_argument("--json", action="store_true", help="print the computed sections as JSON")
    args = parser.parse_args(argv)

    try:
        if args.command == "validate":
            return _cmd_validate(args)
    except SchemaValidationError as e:
        print(str(e), file=sys.stderr)
        return 1
    except (RegistryError, ValueError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
