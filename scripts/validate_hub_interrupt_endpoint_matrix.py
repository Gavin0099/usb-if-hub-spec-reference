#!/usr/bin/env python3
"""Validate USB 2.0 hub interrupt endpoint descriptor matrix structure.

Authority ceiling: hub_interrupt_endpoint_field_role_only

Structural checks only:
  R1 field_id must be unique
  R2 field_name must be one of the tracked USB 2.0 hub interrupt endpoint descriptor fields
  R3 source_refs must exist
  R4 claim_level must be valid
  R5 evidence_status must be valid
  R6 all expected fields must be present

Non-goals:
  - Does not fetch USB-IF sources.
  - Does not validate descriptor dump values.
  - Does not verify firmware behavior.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "tables" / "hub_interrupt_endpoint_matrix.yaml"

EXPECTED_FIELDS = {
    "bEndpointAddress",
    "bmAttributes",
    "wMaxPacketSize",
    "bInterval",
}
VALID_CLAIM_LEVELS = {"verified", "inferred", "provisional", "draft", "reviewed"}
VALID_EVIDENCE_STATUS = {"reviewed", "review_required", "unreviewed", "unknown"}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def validate(matrix_path: Path) -> tuple[str, list[dict[str, str]]]:
    errors: list[dict[str, str]] = []

    def fail(code: str, message: str) -> None:
        errors.append({"code": code, "message": message})

    doc = _load_yaml(matrix_path)
    entries = doc.get("entries") or []

    seen_field_ids: set[str] = set()
    seen_field_names: set[str] = set()

    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            fail("INVALID_ENTRY_TYPE", f"entry[{i}] must be a mapping")
            continue

        loc = f"entry[{i}]"
        field_id = entry.get("field_id")
        field_name = entry.get("field_name")
        claim = entry.get("claim_level")
        evidence = entry.get("evidence_status")

        # R1
        if field_id in seen_field_ids:
            fail("DUPLICATE_FIELD_ID", f"{loc}: duplicate field_id '{field_id}'")
        elif field_id:
            seen_field_ids.add(field_id)

        # R2
        if field_name not in EXPECTED_FIELDS:
            fail(
                "UNEXPECTED_FIELD_NAME",
                f"{loc}: field_name '{field_name}' is not in expected set {sorted(EXPECTED_FIELDS)}",
            )
        elif field_name in seen_field_names:
            fail("DUPLICATE_FIELD_NAME", f"{loc}: duplicate field_name '{field_name}'")
        else:
            seen_field_names.add(field_name)

        # R3
        if not entry.get("source_refs"):
            fail("MISSING_SOURCE_REFS", f"{loc}: source_refs must be present and non-empty")

        # R4
        if claim not in VALID_CLAIM_LEVELS:
            fail("INVALID_CLAIM_LEVEL", f"{loc}: claim_level '{claim}' is not in {sorted(VALID_CLAIM_LEVELS)}")

        # R5
        if evidence not in VALID_EVIDENCE_STATUS:
            fail(
                "INVALID_EVIDENCE_STATUS",
                f"{loc}: evidence_status '{evidence}' is not in {sorted(VALID_EVIDENCE_STATUS)}",
            )

    # R6
    missing_fields = sorted(EXPECTED_FIELDS - seen_field_names)
    if missing_fields:
        fail(
            "MISSING_EXPECTED_FIELDS",
            f"missing expected field entries: {missing_fields}",
        )

    return ("FAIL" if errors else "PASS"), errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    result, errors = validate(args.matrix)

    for e in errors:
        print(f"[FAIL] {e['code']}: {e['message']}")
    print(f"\nHub interrupt endpoint matrix validation {result}")
    if result == "PASS":
        print(f"- field coverage: {len(EXPECTED_FIELDS)}/{len(EXPECTED_FIELDS)}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        receipt = {
            "validator": "validate_hub_interrupt_endpoint_matrix",
            "matrix": str(args.matrix),
            "result": result,
            "authority_ceiling": "hub_interrupt_endpoint_field_role_only",
            "coverage": {
                "fields_covered": len(EXPECTED_FIELDS) if result == "PASS" else None,
                "expected_fields": len(EXPECTED_FIELDS),
                "coverage_status": "complete" if result == "PASS" else "review_required",
            },
            "errors": errors,
        }
        args.receipt_out.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    sys.exit(0 if result == "PASS" else 1)


if __name__ == "__main__":
    main()
