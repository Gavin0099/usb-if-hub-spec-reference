#!/usr/bin/env python3
"""Validate consumer access contract of usb20_hub_class_request_manifest.yaml."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "exports" / "usb20_hub_class_request_manifest.yaml"


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _safe_repo_path(rel_path: str) -> Path | None:
    p = (ROOT / rel_path).resolve()
    try:
        p.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return p


def validate(manifest_path: Path) -> tuple[str, list[dict[str, str]]]:
    errors: list[dict[str, str]] = []

    def fail(code: str, message: str) -> None:
        errors.append({"code": code, "message": message})

    # M1
    try:
        manifest = _load_yaml(manifest_path)
    except Exception as ex:
        fail("MANIFEST_UNPARSABLE", f"manifest parse failed: {ex}")
        return "FAIL", errors

    # M2
    tables = manifest.get("governed_tables")
    if not isinstance(tables, list) or not tables:
        fail("MISSING_GOVERNED_TABLES", "governed_tables must exist and be non-empty")
        return "FAIL", errors

    seen_ids: set[str] = set()
    for i, row in enumerate(tables):
        loc = f"governed_tables[{i}]"
        if not isinstance(row, dict):
            fail("INVALID_TABLE_ROW", f"{loc} must be a mapping")
            continue

        table_id = row.get("id")
        table_path = row.get("path")

        # M3
        if not isinstance(table_id, str) or not table_id.strip():
            fail("MISSING_TABLE_ID", f"{loc}: id is required")
        if not isinstance(table_path, str) or not table_path.strip():
            fail("MISSING_TABLE_PATH", f"{loc}: path is required")
            continue

        # M8
        if isinstance(table_id, str) and table_id:
            if table_id in seen_ids:
                fail("DUPLICATE_TABLE_ID", f"{loc}: duplicate id '{table_id}'")
            else:
                seen_ids.add(table_id)

        # M4
        resolved = _safe_repo_path(table_path)
        if resolved is None:
            fail("PATH_ESCAPE", f"{loc}: path escapes repo root: {table_path}")
            continue

        # M5
        if not resolved.exists():
            fail("PATH_NOT_FOUND", f"{loc}: target path does not exist: {table_path}")
            continue

        # M6
        try:
            table_doc = _load_yaml(resolved)
        except Exception as ex:
            fail("TARGET_UNPARSABLE", f"{loc}: target YAML parse failed: {table_path} ({ex})")
            continue

        # M7
        actual_id = table_doc.get("matrix_id") or table_doc.get("table_id")
        if not isinstance(actual_id, str) or not actual_id.strip():
            fail("TARGET_MISSING_ID", f"{loc}: target missing matrix_id/table_id: {table_path}")
            continue
        if isinstance(table_id, str) and table_id != actual_id:
            fail(
                "ID_MISMATCH",
                f"{loc}: manifest id '{table_id}' != target id '{actual_id}' ({table_path})",
            )

    return ("FAIL" if errors else "PASS"), errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    result, errors = validate(args.manifest)
    for e in errors:
        print(f"[FAIL] {e['code']}: {e['message']}")
    print(f"\nManifest access contract validation {result}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        receipt = {
            "validator": "validate_usb20_hub_class_request_manifest",
            "manifest": str(args.manifest),
            "result": result,
            "errors": errors,
        }
        args.receipt_out.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    sys.exit(0 if result == "PASS" else 1)


if __name__ == "__main__":
    main()
