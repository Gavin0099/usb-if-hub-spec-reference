#!/usr/bin/env python3
"""Validate signal JSON files against schemas/usb_signal_schema.json.

Usage:
  py scripts/validate_signals.py
  py scripts/validate_signals.py --file examples/sample_signal.json
  py scripts/validate_signals.py --dir examples
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "usb_signal_schema.json"
DEFAULT_DIR = ROOT / "examples"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_against_minimal_schema(instance: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = schema.get("required", [])
    properties = schema.get("properties", {})
    additional_properties = schema.get("additionalProperties", True)

    # Required fields
    for key in required:
        if key not in instance:
            errors.append(f"missing required field: {key}")

    # Type and enum checks for known properties
    for key, value in instance.items():
        rule = properties.get(key)
        if rule is None:
            if additional_properties is False:
                errors.append(f"unexpected field: {key}")
            continue

        expected_type = rule.get("type")
        if expected_type == "string" and not isinstance(value, str):
            errors.append(f"{key}: expected string")
            continue
        if expected_type == "array":
            if not isinstance(value, list):
                errors.append(f"{key}: expected array")
                continue
            min_items = rule.get("minItems")
            if isinstance(min_items, int) and len(value) < min_items:
                errors.append(f"{key}: expected at least {min_items} item(s)")
            item_rule = rule.get("items", {})
            item_enum = item_rule.get("enum")
            item_type = item_rule.get("type")
            for i, item in enumerate(value):
                if item_type == "string" and not isinstance(item, str):
                    errors.append(f"{key}[{i}]: expected string")
                    continue
                if isinstance(item_enum, list) and item not in item_enum:
                    errors.append(f"{key}[{i}]: invalid value '{item}'")
            continue

        enum_values = rule.get("enum")
        if isinstance(enum_values, list) and value not in enum_values:
            errors.append(f"{key}: invalid value '{value}'")

    return errors


def collect_target_files(file_arg: str | None, dir_arg: str | None) -> list[Path]:
    if file_arg:
        path = (ROOT / file_arg) if not Path(file_arg).is_absolute() else Path(file_arg)
        return [path]
    target_dir = Path(dir_arg) if dir_arg else DEFAULT_DIR
    if not target_dir.is_absolute():
        target_dir = ROOT / target_dir
    return sorted(target_dir.glob("*.json"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="single JSON signal file to validate")
    parser.add_argument("--dir", help="directory containing JSON signal files")
    args = parser.parse_args()

    schema = load_json(SCHEMA_PATH)
    files = collect_target_files(args.file, args.dir)

    if not files:
        print("Validation FAILED")
        print("- no JSON files found to validate")
        return 1

    total = 0
    failed = 0

    for path in files:
        total += 1
        try:
            instance = load_json(path)
        except Exception as exc:
            failed += 1
            print(f"[FAIL] {path}: cannot parse JSON ({exc})")
            continue

        if not isinstance(instance, dict):
            failed += 1
            print(f"[FAIL] {path}: top-level JSON must be an object")
            continue

        errors = validate_against_minimal_schema(instance, schema)
        if errors:
            failed += 1
            print(f"[FAIL] {path}")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"[PASS] {path}")

    if failed:
        print(f"Validation FAILED ({failed}/{total} file(s) failed)")
        return 1

    print(f"Validation PASSED ({total}/{total} file(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
