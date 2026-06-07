#!/usr/bin/env python3
"""Validate USB 3.x SS hub class request matrix schema.

Authority ceiling: scaffold_reviewed — request linkage identity only.
No verified promotion is open for this scaffold phase.

Checks:
  R1  matrix_id present
  R2  entries list not empty
  R3  request_ids unique
  R4  required fields per entry (request_id, request_name, bRequest_hex,
      claim_level, evidence_status, source_refs)
  R5  claim_level must not be 'verified' (scaffold gate)
  R6  expected request ids present
  R7  spec_family must be usb3
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "tables" / "ss_hub_class_request_matrix.yaml"

VALID_CLAIM_LEVELS = {"reviewed", "inferred"}
VALID_EVIDENCE_STATUS = {"reviewed", "review_required", "inferred"}

EXPECTED_REQUEST_IDS = {
    "usb3_get_status_hub",
    "usb3_get_status_port",
    "usb3_set_feature_hub",
    "usb3_set_feature_port",
    "usb3_clear_feature_hub",
    "usb3_clear_feature_port",
    "usb3_get_descriptor_hub",
    "usb3_set_descriptor_hub",
    "usb3_set_hub_depth",
    "usb3_get_port_err_count",
}


def main() -> int:
    if not MATRIX_PATH.exists():
        print(f"FAIL: matrix file not found: {MATRIX_PATH}")
        return 1

    with MATRIX_PATH.open("r", encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}

    errors: list[str] = []

    # R1
    if not doc.get("matrix_id"):
        errors.append("R1: matrix_id missing or empty")

    # R7
    if doc.get("spec_family") != "usb3":
        errors.append("R7: spec_family must be 'usb3'")

    entries = doc.get("entries") or []
    # R2
    if not entries:
        errors.append("R2: entries list missing or empty")

    seen_ids: set[str] = set()

    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"R3: entry[{i}] is not a dict")
            continue

        rid = entry.get("request_id", f"<entry[{i}]>")

        # R3
        if rid in seen_ids:
            errors.append(f"R3: duplicate request_id {rid!r}")
        seen_ids.add(rid)

        # R4
        for fld in ("request_id", "request_name", "bRequest_hex", "claim_level",
                    "evidence_status", "source_refs"):
            if fld not in entry:
                errors.append(f"R4: entry {rid!r} missing required field '{fld}'")

        # R5
        if entry.get("claim_level") == "verified":
            errors.append(f"R5: entry {rid!r} has claim_level=verified; scaffold gate is closed")

    # R6
    missing = EXPECTED_REQUEST_IDS - seen_ids
    if missing:
        errors.append(f"R6: missing expected request ids: {sorted(missing)}")

    if errors:
        print("FAIL: ss_hub_class_request_matrix validation")
        for e in errors:
            print(f"  {e}")
        return 1

    print("PASS: SS hub class request matrix validation")
    print(f"  matrix_id: {doc.get('matrix_id')}")
    print(f"  entries: {len(entries)}")
    ss_only = [e for e in entries if e.get("applicability", "").startswith("ss_only")]
    print(f"  ss_only entries: {len(ss_only)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
