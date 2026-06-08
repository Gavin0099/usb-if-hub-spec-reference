#!/usr/bin/env python3
"""Validate USB 3.x SS hub feature selector matrix schema.

Authority ceiling: selector name/value/applicability/recipient identity only.

Verified gate: PARTIAL / allowlist-only (USB3-FS-2 pilot).
All 6 SS-only port feature selector IDs are eligible for verified promotion.

Checks:
  R1  matrix_id present
  R2  entries list not empty
  R3  selector_ids unique
  R4  required fields per entry (selector_id, selector_name, selector_value,
      recipient, claim_level, evidence_status, source_refs)
  R5  claim_level=verified only allowed for ALLOWLIST_VERIFIED_IDS
  R6  verified entries must have evidence.verification_packet present
  R7  expected selector ids present
  R8  spec_family must be usb3
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "tables" / "ss_feature_selector_matrix.yaml"

VALID_CLAIM_LEVELS = {"verified", "reviewed", "inferred"}

ALLOWLIST_VERIFIED_IDS = {
    "usb3_port_u1_enable",
    "usb3_port_u2_enable",
    "usb3_port_u1_timeout",
    "usb3_port_u2_timeout",
    "usb3_port_remote_wake_mask",
    "usb3_port_bh_port_reset",
}

EXPECTED_SELECTOR_IDS = ALLOWLIST_VERIFIED_IDS


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

        # R5 — verified only allowed for entries in the allowlist
        if cl == "verified" and sid not in ALLOWLIST_VERIFIED_IDS:
            errors.append(
                f"R5: entry {sid!r} has claim_level=verified but is not in the "
                f"allowlist; USB3-FS-2 pilot covers SS feature selector entries only"
            )

        # R6 — verified entries must have evidence.verification_packet
        if cl == "verified":
            evidence = entry.get("evidence") or {}
            if not evidence.get("verification_packet"):
                errors.append(
                    f"R6: entry {sid!r} is verified but missing "
                    f"evidence.verification_packet"
                )

        # claim_level must be in valid set
        if cl not in VALID_CLAIM_LEVELS:
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

    verified_count = sum(1 for e in entries if e.get("claim_level") == "verified")
    reviewed_count = sum(1 for e in entries if e.get("claim_level") == "reviewed")
    print("PASS: SS feature selector matrix validation")
    print(f"  matrix_id: {doc.get('matrix_id')}")
    print(f"  entries: {len(entries)} (verified={verified_count}, reviewed={reviewed_count})")
    print(f"  verified gate: PARTIAL / allowlist-only ({len(ALLOWLIST_VERIFIED_IDS)} eligible ids)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
