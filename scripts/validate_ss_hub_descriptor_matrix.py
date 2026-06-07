#!/usr/bin/env python3
"""Validate USB 3.x SS hub descriptor field matrix schema.

Authority ceiling: scaffold_reviewed — descriptor field identity only.
No verified promotion is open for this scaffold phase.

Checks:
  R1  matrix_id present
  R2  entries list not empty
  R3  field_ids unique
  R4  required fields per entry (field_id, field_name, claim_level,
      evidence_status, source_refs)
  R5  claim_level must not be 'verified' (scaffold gate)
  R6  expected field ids present
  R7  spec_family must be usb3
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "tables" / "ss_hub_descriptor_matrix.yaml"

VALID_CLAIM_LEVELS = {"reviewed", "inferred"}

EXPECTED_FIELD_IDS = {
    "usb3_hub_desc_bLength",
    "usb3_hub_desc_bDescriptorType",
    "usb3_hub_desc_bNbrPorts",
    "usb3_hub_desc_wHubCharacteristics",
    "usb3_hub_desc_bPwrOn2PwrGood",
    "usb3_hub_desc_bHubContrCurrent",
    "usb3_hub_desc_bHubDecLat",
    "usb3_hub_desc_wHubDelay",
    "usb3_hub_desc_DeviceRemovable",
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

        fid = entry.get("field_id", f"<entry[{i}]>")

        # R3
        if fid in seen_ids:
            errors.append(f"R3: duplicate field_id {fid!r}")
        seen_ids.add(fid)

        # R4
        for fld in ("field_id", "field_name", "claim_level", "evidence_status", "source_refs"):
            if fld not in entry:
                errors.append(f"R4: entry {fid!r} missing required field '{fld}'")

        # R5
        if entry.get("claim_level") == "verified":
            errors.append(f"R5: entry {fid!r} has claim_level=verified; scaffold gate is closed")

    # R6
    missing = EXPECTED_FIELD_IDS - seen_ids
    if missing:
        errors.append(f"R6: missing expected field ids: {sorted(missing)}")

    if errors:
        print("FAIL: ss_hub_descriptor_matrix validation")
        for e in errors:
            print(f"  {e}")
        return 1

    print("PASS: SS hub descriptor matrix validation")
    print(f"  matrix_id: {doc.get('matrix_id')}")
    print(f"  entries: {len(entries)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
