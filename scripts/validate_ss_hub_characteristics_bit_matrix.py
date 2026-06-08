#!/usr/bin/env python3
"""Validate USB 3.x SS hub wHubCharacteristics bit matrix schema.

Authority ceiling: bit group name, bit range, and value encoding identity only.

Verified gate: PARTIAL / allowlist-only (USB3-WHC-1 pilot).
All 4 SS hub wHubCharacteristics defined bit group IDs are eligible for
verified promotion. Reserved boundary entry is reviewed only.

Checks:
  R1  matrix_id present
  R2  entries list not empty
  R3  entry ids unique
  R4  required fields per entry (id, field, bit_range, semantic_group,
      claim_level, evidence_status, source_refs)
  R5  claim_level=verified only allowed for ALLOWLIST_VERIFIED_IDS
  R6  verified entries must have evidence.verification_packet present
  R7  expected entry ids present
  R8  spec_family must be usb3
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "tables" / "ss_hub_characteristics_bit_matrix.yaml"

VALID_CLAIM_LEVELS = {"verified", "reviewed", "inferred"}

ALLOWLIST_VERIFIED_IDS = {
    "usb3_ss_whc_power_switching",
    "usb3_ss_whc_compound_device",
    "usb3_ss_whc_over_current_mode",
    "usb3_ss_whc_port_indicators",
}

EXPECTED_ENTRY_IDS = ALLOWLIST_VERIFIED_IDS | {"usb3_ss_whc_reserved_high"}


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

        eid = entry.get("id", f"<entry[{i}]>")

        # R3
        if eid in seen_ids:
            errors.append(f"R3: duplicate entry id {eid!r}")
        seen_ids.add(eid)

        # R4
        for fld in ("id", "field", "bit_range", "semantic_group",
                    "claim_level", "evidence_status", "source_refs"):
            if fld not in entry:
                errors.append(f"R4: entry {eid!r} missing required field '{fld}'")

        cl = entry.get("claim_level")

        # R5 — verified only allowed for entries in the allowlist
        if cl == "verified" and eid not in ALLOWLIST_VERIFIED_IDS:
            errors.append(
                f"R5: entry {eid!r} has claim_level=verified but is not in the "
                f"allowlist; USB3-WHC-1 pilot covers SS hub wHubCharacteristics "
                f"defined bit groups only"
            )

        # R6 — verified entries must have evidence.verification_packet
        if cl == "verified":
            evidence = entry.get("evidence") or {}
            if not evidence.get("verification_packet"):
                errors.append(
                    f"R6: entry {eid!r} is verified but missing "
                    f"evidence.verification_packet"
                )

        # claim_level must be in valid set
        if cl not in VALID_CLAIM_LEVELS:
            errors.append(
                f"R6: entry {eid!r} has invalid claim_level {cl!r}; "
                f"allowed: {sorted(VALID_CLAIM_LEVELS)}"
            )

    # R7
    missing = EXPECTED_ENTRY_IDS - seen_ids
    if missing:
        errors.append(f"R7: missing expected entry ids: {sorted(missing)}")

    if errors:
        print("FAIL: ss_hub_characteristics_bit_matrix validation")
        for e in errors:
            print(f"  {e}")
        return 1

    verified_count = sum(1 for e in entries if e.get("claim_level") == "verified")
    reviewed_count = sum(1 for e in entries if e.get("claim_level") == "reviewed")
    print("PASS: SS hub characteristics bit matrix validation")
    print(f"  matrix_id: {doc.get('matrix_id')}")
    print(f"  entries: {len(entries)} (verified={verified_count}, reviewed={reviewed_count})")
    print(f"  verified gate: PARTIAL / allowlist-only ({len(ALLOWLIST_VERIFIED_IDS)} eligible ids)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
