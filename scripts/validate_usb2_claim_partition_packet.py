#!/usr/bin/env python3
"""Validate USB2 claim partition evidence packet.

Authority ceiling: usb2_claim_partition_packet_consistency_only

This validator does not verify USB semantics. It checks that the evidence packet
for the USB2 claim partition names the required validators, receipt paths,
current counts, and non-claims.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from validate_usb2_claim_partition import validate as validate_partition


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "docs" / "evidence" / "usb2_claim_partition_packet.md"

REQUIRED_LITERALS = [
    "scripts/validate_entry_verification_gate.py",
    "scripts/validate_entry_gate_coverage.py",
    "scripts/validate_reviewed_boundary_lock.py",
    "scripts/validate_usb2_claim_partition.py",
    "evidence/entry_verification_packets/",
    "evidence/validation_receipt_entry_verification_gate.json",
    "evidence/validation_receipt_entry_gate_coverage.json",
    "evidence/validation_receipt_reviewed_boundary_lock.json",
    "evidence/validation_receipt_usb2_claim_partition.json",
    "ci-receipts/usb2_claim_partition.json",
    "USB behavior correctness",
    "USB 2.0 behavior completeness",
    "Firmware implementation correctness",
    "Host stack behavior coverage",
    "New verified entries",
    "New USB spec semantics",
]

COUNT_LABELS = {
    "tracked": "tracked",
    "verified": "verified",
    "reviewed": "reviewed",
    "inferred": "inferred",
    "missing": "missing",
    "entry_verification_packets": "entry verification packets",
    "locked_reviewed_boundaries": "locked reviewed boundaries",
}


def _count_present(text: str, label: str, value: int) -> bool:
    table_pattern = rf"\|\s*{re.escape(label)}\s*\|\s*{value}\s*\|"
    inline_pattern = rf"\b{re.escape(label)}\s*=\s*{value}\b"
    return bool(re.search(table_pattern, text) or re.search(inline_pattern, text))


def validate_packet_text(text: str, counts: dict[str, int]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []

    for literal in REQUIRED_LITERALS:
        if literal not in text:
            errors.append({
                "code": "PACKET_REQUIRED_LITERAL_MISSING",
                "literal": literal,
                "message": f"packet missing required literal: {literal}",
            })

    for key, label in COUNT_LABELS.items():
        if key not in counts:
            errors.append({
                "code": "PACKET_COUNT_SOURCE_MISSING",
                "count": key,
                "message": f"partition count missing from validator output: {key}",
            })
            continue
        if not _count_present(text, label, counts[key]):
            errors.append({
                "code": "PACKET_COUNT_MISMATCH",
                "count": key,
                "expected": counts[key],
                "message": f"packet missing current {label} count: {counts[key]}",
            })

    if "151 = 105 verified + 46 reviewed + 0 inferred + 0 missing" not in text:
        errors.append({
            "code": "PACKET_PARTITION_FORMULA_MISSING",
            "message": "packet must state the current 151 = 105 verified + 46 reviewed + 0 inferred + 0 missing formula",
        })

    return errors


def validate(packet_path: Path = DEFAULT_PACKET) -> tuple[str, list[dict[str, Any]], dict[str, Any]]:
    partition_result, partition_errors, counts = validate_partition()
    errors: list[dict[str, Any]] = []

    if partition_result != "PASS":
        errors.append({
            "code": "PARTITION_VALIDATOR_FAILED",
            "message": "validate_usb2_claim_partition.py must pass before the packet can be valid",
            "partition_errors": partition_errors,
        })

    if not packet_path.exists():
        errors.append({
            "code": "PACKET_MISSING",
            "message": f"packet not found: {packet_path}",
        })
        return "FAIL", errors, counts

    text = packet_path.read_text(encoding="utf-8")
    errors.extend(validate_packet_text(text, counts))
    return ("FAIL" if errors else "PASS"), errors, counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    result, errors, counts = validate(args.packet)

    for error in errors:
        print(f"[FAIL] {error['code']}: {error['message']}")

    print(f"\nUSB2 claim partition packet validation {result}")
    print(
        "- packet counts: "
        f"tracked={counts.get('tracked')}, verified={counts.get('verified')}, "
        f"reviewed={counts.get('reviewed')}, inferred={counts.get('inferred')}, "
        f"missing={counts.get('missing')}"
    )

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "validator": "validate_usb2_claim_partition_packet",
            "result": result,
            "authority_ceiling": "usb2_claim_partition_packet_consistency_only",
            "packet": str(args.packet),
            "counts": counts,
            "errors": errors,
        }
        args.receipt_out.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
