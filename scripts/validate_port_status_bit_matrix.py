#!/usr/bin/env python3
"""Validate USB 2.0 hub/port status-bit matrix structure.

Authority ceiling: status_bit_namespace_only

Structural checks only:
  R1 field+bit must be unique
  R2 bit must be in range 0-15
  R3 field must be one of wHubStatus, wHubChange, wPortStatus, wPortChange
  R4 status must be one of defined, reserved, vendor_or_spec_dependent
  R5 claim/evidence must exist at matrix level or entry level
  R6 claim_level=verified is not allowed in this validator
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "tables" / "port_status_bit_matrix.yaml"

VALID_FIELDS = {"wHubStatus", "wHubChange", "wPortStatus", "wPortChange"}
VALID_STATUS = {"defined", "reserved", "vendor_or_spec_dependent"}
VALID_CLAIM_LEVELS = {"inferred", "provisional", "draft", "verified"}
VALID_EVIDENCE_STATUS = {"review_required", "reviewed", "unreviewed", "unknown"}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def validate(matrix_path: Path) -> tuple[str, list[dict[str, str]]]:
    errors: list[dict[str, str]] = []

    def fail(code: str, message: str) -> None:
        errors.append({"code": code, "message": message})

    doc = _load_yaml(matrix_path)
    entries = doc.get("entries") or []

    matrix_claim = doc.get("claim_level")
    matrix_evidence = doc.get("evidence_status")

    if matrix_claim is not None and matrix_claim not in VALID_CLAIM_LEVELS:
        fail("INVALID_MATRIX_CLAIM_LEVEL", f"matrix claim_level '{matrix_claim}' is invalid")
    if matrix_evidence is not None and matrix_evidence not in VALID_EVIDENCE_STATUS:
        fail("INVALID_MATRIX_EVIDENCE_STATUS", f"matrix evidence_status '{matrix_evidence}' is invalid")

    if matrix_claim == "verified":
        fail(
            "VERIFIED_NOT_ALLOWED",
            "matrix claim_level=verified is not allowed for port status bit scaffold",
        )

    seen_field_bit: set[tuple[str, int]] = set()
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            fail("INVALID_ENTRY_TYPE", f"entry[{i}] must be a mapping")
            continue

        loc = f"entry[{i}]"
        field = entry.get("field")
        bit = entry.get("bit")
        status = entry.get("status")

        # R3
        if field not in VALID_FIELDS:
            fail("INVALID_FIELD", f"{loc}: field '{field}' is not in {sorted(VALID_FIELDS)}")

        # R2
        if not isinstance(bit, int) or bit < 0 or bit > 15:
            fail("BIT_OUT_OF_RANGE", f"{loc}: bit '{bit}' is not in 0-15")

        # R1
        if isinstance(bit, int) and field in VALID_FIELDS:
            key = (field, bit)
            if key in seen_field_bit:
                fail("DUPLICATE_FIELD_BIT", f"{loc}: duplicate field+bit pair ({field}, {bit})")
            else:
                seen_field_bit.add(key)

        # R4
        if status not in VALID_STATUS:
            fail("INVALID_STATUS", f"{loc}: status '{status}' is not in {sorted(VALID_STATUS)}")

        # R5/R6
        claim = entry.get("claim_level", matrix_claim)
        evidence = entry.get("evidence_status", matrix_evidence)

        if claim is None or evidence is None:
            fail(
                "MISSING_CLAIM_OR_EVIDENCE",
                f"{loc}: claim_level/evidence_status missing at entry and matrix level",
            )
        else:
            if claim not in VALID_CLAIM_LEVELS:
                fail("INVALID_CLAIM_LEVEL", f"{loc}: claim_level '{claim}' is invalid")
            if evidence not in VALID_EVIDENCE_STATUS:
                fail("INVALID_EVIDENCE_STATUS", f"{loc}: evidence_status '{evidence}' is invalid")
            if claim == "verified":
                fail(
                    "VERIFIED_NOT_ALLOWED",
                    f"{loc}: claim_level=verified is not allowed for this table",
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
    print(f"\nPort status bit matrix validation {result}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        receipt = {
            "validator": "validate_port_status_bit_matrix",
            "matrix": str(args.matrix),
            "result": result,
            "authority_ceiling": "status_bit_namespace_only",
            "errors": errors,
        }
        args.receipt_out.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    sys.exit(0 if result == "PASS" else 1)


if __name__ == "__main__":
    main()
