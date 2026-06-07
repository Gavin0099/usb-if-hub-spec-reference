#!/usr/bin/env python3
"""Validate USB 3.x SS hub feature selector matrix schema.

Authority ceiling: selector name/value/applicability/recipient identity only.

Verified gate: CLOSED (USB3-FS-1 scaffold phase).
No entry is eligible for verified promotion until USB3-FS-2.

Checks:
  R1  matrix_id present
  R2  entries list not empty
  R3  selector_ids unique
  R4  required fields per entry (selector_id, selector_name, selector_value,
      recipient, claim_level, evidence_status, source_refs)
  R5  claim_level=verified BLOCKED (verified gate is CLOSED)
  R6  claim_level values in allowed set
  R7  expected selector ids present
  R8  spec_family must be usb3
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "tables" / "ss_feature_selector_matrix.yaml"

VALID_CLAIM_LEVELS = {"reviewed", "inferred"}

EXPECTED_SELECTOR_IDS = {
    "usb3_port_u1_enable",
    "usb3_port_u2_enable",
    "usb3_port_u1_timeout",
    "usb3_port_u2_timeout",
    "usb3_port_remote_wake_mask",
    "usb3_port_bh_port_reset",
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

    # R8
    if doc.get("spec_family") != "usb3":
        errors.append("R8: spec_family must be 'usb3'")

    entries = doc.get("entries") or []

    # R2
    if not entries:
        errors.append("R2: entries list missing or empty")

    seen_ids: set[str] = set()

    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"R3: entry[{i}] is not a dict")
            continue

        sid = entry.get("selector_id", f"<entry[{i}]>")

        # R3
        if sid in seen_ids:
            errors.append(f"R3: duplicate selector_id {sid!r}")
        seen_ids.add(sid)

        # R4
        for fld in ("selector_id", "selector_name", "selector_value",
                    "recipient", "claim_level", "evidence_status", "source_refs"):
            if fld not in entry:
                errors.append(f"R4: entry {sid!r} missing required field '{fld}'")

        cl = entry.get("claim_level")

        # R5 — verified gate is CLOSED; no verified entries permitted
        if cl == "verified":
            errors.append(
                f"R5: entry {sid!r} has claim_level=verified but verified gate is "
                f"CLOSED (USB3-FS-1 scaffold phase); verified promotion requires USB3-FS-2"
            )

        # R6
        if cl not in VALID_CLAIM_LEVELS and cl != "verified":
            errors.append(
                f"R6: entry {sid!r} has invalid claim_level {cl!r}; "
                f"allowed: {sorted(VALID_CLAIM_LEVELS)}"
            )

    # R7
    missing = EXPECTED_SELECTOR_IDS - seen_ids
    if missing:
        errors.append(f"R7: missing expected selector ids: {sorted(missing)}")

    if errors:
        print("FAIL: ss_feature_selector_matrix validation")
        for e in errors:
            print(f"  {e}")
        return 1

    reviewed_count = sum(1 for e in entries if e.get("claim_level") == "reviewed")
    print("PASS: SS feature selector matrix validation")
    print(f"  matrix_id: {doc.get('matrix_id')}")
    print(f"  entries: {len(entries)} (verified=0, reviewed={reviewed_count})")
    print(f"  verified gate: CLOSED (scaffold phase USB3-FS-1)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
