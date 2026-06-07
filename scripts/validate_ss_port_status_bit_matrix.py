#!/usr/bin/env python3
"""Validate USB 3.x SS hub port status bit matrix schema.

Authority ceiling: bit_name_and_position_only for single-bit entries;
bit_name_range_and_encoding_identity_only for multi-bit entries.
No LTSSM behavior, xHCI interaction, or electrical compliance claimed.

Checks:
  R1  matrix_id present
  R2  entries list not empty
  R3  entry ids unique
  R4  required fields per entry (id, field, status, claim_level, evidence_status,
      source_refs) plus either 'bit' or 'bit_range'
  R5  field must be wPortStatus or wPortChange
  R6  bit in range 0–15 (single-bit entries)
  R7  bit_range format valid (N or N:M)
  R8  claim_level=verified only for allowlisted defined entry ids; reserved
      entries must remain reviewed
  R9  expected defined entry ids present
  R10 spec_family must be usb3
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "tables" / "ss_port_status_bit_matrix.yaml"

VALID_FIELDS = {"wPortStatus", "wPortChange"}
VALID_STATUS = {"defined", "reserved", "vendor_or_spec_dependent"}
VALID_CLAIM_LEVELS = {"reviewed", "inferred", "verified"}
VALID_EVIDENCE_STATUS = {"reviewed", "review_required", "inferred"}
BIT_RANGE_RE = re.compile(r"^\d+(:\d+)?$")

# Allowlist for verified promotion (USB3-3C pilot — 15 defined entries).
# Reserved entries are permanently excluded from this allowlist.
ALLOWLIST_VERIFIED_IDS = {
    "ss_wPortStatus.bit0.PORT_CONNECTION",
    "ss_wPortStatus.bit1.PORT_ENABLE",
    "ss_wPortStatus.bit2.PORT_OVER_CURRENT",
    "ss_wPortStatus.bit3.PORT_RESET",
    "ss_wPortStatus.bits85.PORT_LINK_STATE",
    "ss_wPortStatus.bit9.PORT_POWER",
    "ss_wPortStatus.bits1210.PORT_SPEED",
    "ss_wPortStatus.bit13.PORT_U1_ENABLE",
    "ss_wPortStatus.bit14.PORT_U2_ENABLE",
    "ss_wPortChange.bit0.C_PORT_CONNECTION",
    "ss_wPortChange.bit2.C_PORT_OVER_CURRENT",
    "ss_wPortChange.bit3.C_PORT_RESET",
    "ss_wPortChange.bit4.C_BH_PORT_RESET",
    "ss_wPortChange.bit5.C_PORT_LINK_STATE",
    "ss_wPortChange.bit6.C_PORT_CONFIG_ERROR",
}

EXPECTED_DEFINED_IDS = ALLOWLIST_VERIFIED_IDS


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

    # R10
    if doc.get("spec_family") != "usb3":
        errors.append("R10: spec_family must be 'usb3'")

    entries = doc.get("entries") or []
    # R2
    if not entries:
        errors.append("R2: entries list missing or empty")

    seen_ids: set[str] = set()
    seen_ids_defined: set[str] = set()

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
        has_bit = "bit" in entry
        has_bit_range = "bit_range" in entry
        if not (has_bit or has_bit_range):
            errors.append(f"R4: entry {eid!r} missing both 'bit' and 'bit_range'")
        for fld in ("field", "status", "claim_level", "evidence_status", "source_refs"):
            if fld not in entry:
                errors.append(f"R4: entry {eid!r} missing required field '{fld}'")

        # R5
        field = entry.get("field", "")
        if field not in VALID_FIELDS:
            errors.append(f"R5: entry {eid!r} field {field!r} not in {VALID_FIELDS}")

        # R6
        if has_bit:
            b = entry["bit"]
            if not isinstance(b, int) or not (0 <= b <= 15):
                errors.append(f"R6: entry {eid!r} bit {b!r} out of range 0–15")

        # R7
        if has_bit_range:
            br = str(entry.get("bit_range", ""))
            if not BIT_RANGE_RE.match(br):
                errors.append(f"R7: entry {eid!r} bit_range {br!r} invalid format")

        # R8 — allowlist gate: verified only for explicitly promoted defined entries
        cl = entry.get("claim_level", "")
        status = entry.get("status", "")
        if cl == "verified":
            if eid not in ALLOWLIST_VERIFIED_IDS:
                errors.append(
                    f"R8: entry {eid!r} has claim_level=verified but is not in "
                    f"ALLOWLIST_VERIFIED_IDS (reserved entries must stay reviewed)"
                )

        if status == "defined":
            seen_ids_defined.add(eid)

    # R9
    missing = EXPECTED_DEFINED_IDS - seen_ids_defined
    if missing:
        errors.append(f"R9: missing expected defined entry ids: {sorted(missing)}")

    if errors:
        print("FAIL: ss_port_status_bit_matrix validation")
        for e in errors:
            print(f"  {e}")
        return 1

    defined = sum(1 for e in entries if e.get("status") == "defined")
    reserved = sum(1 for e in entries if e.get("status") == "reserved")
    verified = sum(1 for e in entries if e.get("claim_level") == "verified")
    reviewed = sum(1 for e in entries if e.get("claim_level") == "reviewed")
    print("PASS: SS port status bit matrix validation")
    print(f"  matrix_id: {doc.get('matrix_id')}")
    print(f"  entries: {len(entries)} (defined={defined}, reserved={reserved})")
    print(f"  claim_level: verified={verified}, reviewed={reviewed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
