#!/usr/bin/env python3
"""Validate USB 3.x SS hub class request matrix schema.

Authority ceiling: request_linkage_identity_only for shared requests;
request_identity_requiredness_only for SET_HUB_DEPTH;
request_identity_optionality_only for GET_PORT_ERR_COUNT.

Verified gate: PARTIAL / allowlist-only (USB3-3B pilot).
Only the 10 SS hub class request IDs are eligible for verified promotion.
SS port status bit matrix still has verified gate CLOSED.

Checks:
  R1  matrix_id present
  R2  entries list not empty
  R3  request_ids unique
  R4  required fields per entry (request_id, request_name, claim_level,
      evidence_status, source_refs)
  R5  claim_level=verified only allowed for ALLOWLIST_VERIFIED_IDS
  R6  verified entries must have evidence.verification_packet present
  R7  expected request ids present
  R8  spec_family must be usb3
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "tables" / "ss_hub_class_request_matrix.yaml"

VALID_CLAIM_LEVELS = {"verified", "reviewed", "inferred"}

ALLOWLIST_VERIFIED_IDS = {
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

EXPECTED_REQUEST_IDS = ALLOWLIST_VERIFIED_IDS


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

        rid = entry.get("request_id", f"<entry[{i}]>")

        # R3
        if rid in seen_ids:
            errors.append(f"R3: duplicate request_id {rid!r}")
        seen_ids.add(rid)

        # R4
        for fld in ("request_id", "request_name", "claim_level", "evidence_status", "source_refs"):
            if fld not in entry:
                errors.append(f"R4: entry {rid!r} missing required field '{fld}'")

        cl = entry.get("claim_level")

        # R5
        if cl == "verified" and rid not in ALLOWLIST_VERIFIED_IDS:
            errors.append(
                f"R5: entry {rid!r} has claim_level=verified but is not in the "
                f"allowlist; USB3-3B pilot covers SS hub class requests only"
            )

        # R6
        if cl == "verified":
            evidence = entry.get("evidence") or {}
            if not evidence.get("verification_packet"):
                errors.append(
                    f"R6: entry {rid!r} is verified but missing "
                    f"evidence.verification_packet"
                )

    # R7
    missing = EXPECTED_REQUEST_IDS - seen_ids
    if missing:
        errors.append(f"R7: missing expected request ids: {sorted(missing)}")

    if errors:
        print("FAIL: ss_hub_class_request_matrix validation")
        for e in errors:
            print(f"  {e}")
        return 1

    verified_count = sum(1 for e in entries if e.get("claim_level") == "verified")
    reviewed_count = sum(1 for e in entries if e.get("claim_level") == "reviewed")
    ss_only = sum(
        1 for e in entries
        if e.get("applicability") in ("ss_only_mandatory", "ss_only_optional")
    )
    print("PASS: SS hub class request matrix validation")
    print(f"  matrix_id: {doc.get('matrix_id')}")
    print(f"  entries: {len(entries)} (verified={verified_count}, reviewed={reviewed_count})")
    print(f"  ss_only entries: {ss_only}")
    print(f"  verified gate: PARTIAL / allowlist-only ({len(ALLOWLIST_VERIFIED_IDS)} eligible ids)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
