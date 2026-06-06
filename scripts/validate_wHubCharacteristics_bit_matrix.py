#!/usr/bin/env python3
"""Validate wHubCharacteristics bit-group matrix schema.

Authority ceiling: schema_and_required_fields_only

Checks that wHubCharacteristics_bit_matrix.yaml is structurally valid.
Does not verify USB semantics or firmware behavior.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "tables" / "wHubCharacteristics_bit_matrix.yaml"

REQUIRED_ENTRY_FIELDS = {"id", "field", "bit_range", "claim_level", "evidence_status", "source_refs"}
VALID_CLAIM_LEVELS = {"verified", "reviewed", "inferred"}
VALID_EVIDENCE_STATUS = {"verified", "reviewed", "inferred"}
BIT_RANGE_RE = re.compile(r"^\d+(:\d+)?$")

EXPECTED_IDS = {
    "usb20_whc_power_switching",
    "usb20_whc_compound_device",
    "usb20_whc_over_current_mode",
    "usb20_whc_tt_think_time",
    "usb20_whc_port_indicators",
    "usb20_whc_reserved_high",
}


def main() -> int:
    if not MATRIX_PATH.exists():
        print(f"FAIL: matrix file not found: {MATRIX_PATH}")
        return 1

    with MATRIX_PATH.open("r", encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}

    errors: list[str] = []

    if not doc.get("matrix_id"):
        errors.append("R1: matrix_id is missing or empty")

    entries = doc.get("entries") or []
    if not entries:
        errors.append("R2: entries list is missing or empty")

    seen_ids: set[str] = set()
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"R3: entry[{i}] is not a dict")
            continue

        entry_id = entry.get("id", f"<entry[{i}]>")

        # R4: required fields
        missing = REQUIRED_ENTRY_FIELDS - set(entry.keys())
        if missing:
            errors.append(f"R4: entry {entry_id!r} missing required fields: {sorted(missing)}")

        # R5: duplicate ids
        if entry_id in seen_ids:
            errors.append(f"R5: duplicate entry id {entry_id!r}")
        seen_ids.add(entry_id)

        # R6: claim_level valid
        cl = entry.get("claim_level")
        if cl not in VALID_CLAIM_LEVELS:
            errors.append(f"R6: entry {entry_id!r} has invalid claim_level {cl!r}")

        # R7: evidence_status valid
        ev = entry.get("evidence_status")
        if ev not in VALID_EVIDENCE_STATUS:
            errors.append(f"R7: entry {entry_id!r} has invalid evidence_status {ev!r}")

        # R8: bit_range format
        br = str(entry.get("bit_range", ""))
        if not BIT_RANGE_RE.match(br):
            errors.append(f"R8: entry {entry_id!r} has invalid bit_range {br!r} (expected e.g. '2' or '4:3')")

        # R9: field must be wHubCharacteristics
        if entry.get("field") != "wHubCharacteristics":
            errors.append(f"R9: entry {entry_id!r} field must be 'wHubCharacteristics'")

    # R10: expected entries present
    found_ids = seen_ids
    missing_expected = EXPECTED_IDS - found_ids
    if missing_expected:
        errors.append(f"R10: missing expected entries: {sorted(missing_expected)}")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        print(f"\nwHubCharacteristics bit matrix validation FAIL ({len(errors)} errors)")
        return 1

    print("wHubCharacteristics bit matrix validation PASS")
    print(f"- matrix_id: {doc.get('matrix_id')}")
    print(f"- entries: {len(entries)}")
    v = sum(1 for e in entries if e.get("claim_level") == "verified")
    r = sum(1 for e in entries if e.get("claim_level") != "verified" and e.get("evidence_status") == "reviewed")
    print(f"- verified: {v}, reviewed: {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
