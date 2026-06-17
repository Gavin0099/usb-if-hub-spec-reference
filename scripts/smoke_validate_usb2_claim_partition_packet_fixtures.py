#!/usr/bin/env python3
"""Smoke test validate_usb2_claim_partition_packet.py text checks."""

from __future__ import annotations

import json
import sys

from validate_usb2_claim_partition_packet import validate_packet_text


COUNTS = {
    "tracked": 151,
    "verified": 105,
    "reviewed": 46,
    "inferred": 0,
    "missing": 0,
    "entry_verification_packets": 105,
    "locked_reviewed_boundaries": 46,
}

VALID_TEXT = """
# USB2 Claim Partition Evidence Packet

- `scripts/validate_entry_verification_gate.py`
- `scripts/validate_entry_gate_coverage.py`
- `scripts/validate_reviewed_boundary_lock.py`
- `scripts/validate_usb2_claim_partition.py`
- `evidence/entry_verification_packets/`
- `evidence/validation_receipt_entry_verification_gate.json`
- `evidence/validation_receipt_entry_gate_coverage.json`
- `evidence/validation_receipt_reviewed_boundary_lock.json`
- `evidence/validation_receipt_usb2_claim_partition.json`
- `ci-receipts/usb2_claim_partition.json`

| Bucket | Count |
|---|---:|
| tracked | 151 |
| verified | 105 |
| reviewed | 46 |
| inferred | 0 |
| missing | 0 |
| entry verification packets | 105 |
| locked reviewed boundaries | 46 |

The current partition is 151 = 105 verified + 46 reviewed + 0 inferred + 0 missing.

This packet does not claim USB behavior correctness.
This packet does not claim USB 2.0 behavior completeness.
This packet does not claim Firmware implementation correctness.
This packet does not claim Host stack behavior coverage.
This packet does not claim New verified entries.
This packet does not claim New USB spec semantics.
"""

CASES = [
    {
        "name": "valid_packet_text",
        "text": VALID_TEXT,
        "expected_error_codes": [],
    },
    {
        "name": "invalid_missing_validator",
        "text": VALID_TEXT.replace("- `scripts/validate_usb2_claim_partition.py`\n", ""),
        "expected_error_codes": ["PACKET_REQUIRED_LITERAL_MISSING"],
    },
    {
        "name": "invalid_wrong_count",
        "text": VALID_TEXT.replace("| verified | 105 |", "| verified | 104 |"),
        "expected_error_codes": ["PACKET_COUNT_MISMATCH"],
    },
    {
        "name": "invalid_missing_formula",
        "text": VALID_TEXT.replace(
            "151 = 105 verified + 46 reviewed + 0 inferred + 0 missing",
            "partition is current",
        ),
        "expected_error_codes": ["PACKET_PARTITION_FORMULA_MISSING"],
    },
]


def run_case(case: dict) -> dict:
    errors = validate_packet_text(case["text"], COUNTS)
    actual_error_codes = [error["code"] for error in errors]
    expected = case["expected_error_codes"]
    passed = bool(actual_error_codes) == bool(expected) and set(expected).issubset(set(actual_error_codes))
    return {
        "name": case["name"],
        "expected_error_codes": expected,
        "actual_error_codes": actual_error_codes,
        "result": "PASS" if passed else "FAIL",
        "errors": errors,
    }


def main() -> int:
    results = [run_case(case) for case in CASES]
    failed = [result for result in results if result["result"] == "FAIL"]
    summary = {
        "validator": "validate_usb2_claim_partition_packet.py",
        "smoke_runner": "smoke_validate_usb2_claim_partition_packet_fixtures.py",
        "authority_ceiling": "usb2_claim_partition_packet_consistency_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }

    for result in results:
        print(f"[{result['result']}] {result['name']}")
        if result["result"] == "FAIL":
            print(
                "  error_codes: "
                f"expected={result['expected_error_codes']} actual={result['actual_error_codes']}"
            )

    print(json.dumps(summary, indent=2, ensure_ascii=True))
    if failed:
        print(f"\nSmoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1
    print(f"\nSmoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
