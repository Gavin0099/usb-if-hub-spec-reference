#!/usr/bin/env python3
"""Smoke test validate_port_status_bit_matrix.py against deterministic fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_port_status_bit_matrix.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "port_status_bit_matrix"
RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "port_status_bit_matrix_fixtures"

CASES = [
    {
        "name": "valid_structural_pass",
        "expected_exit": 0,
        "expected_error_codes": [],
        "note": "valid scaffold entries with allowed fields and bit range",
    },
    {
        "name": "valid_verified_pilot",
        "expected_exit": 0,
        "expected_error_codes": [],
        "note": "single reviewed pilot verified entry is structurally allowed",
    },
    {
        "name": "invalid_duplicate_field_bit",
        "expected_exit": 1,
        "expected_error_codes": ["DUPLICATE_FIELD_BIT"],
        "note": "duplicate field+bit pair must fail",
    },
    {
        "name": "invalid_field",
        "expected_exit": 1,
        "expected_error_codes": ["INVALID_FIELD"],
        "note": "unknown field value must fail",
    },
    {
        "name": "invalid_bit_range",
        "expected_exit": 1,
        "expected_error_codes": ["BIT_OUT_OF_RANGE"],
        "note": "bit outside 0-15 must fail",
    },
    {
        "name": "invalid_verified_nonpilot",
        "expected_exit": 1,
        "expected_error_codes": ["VERIFIED_NOT_ALLOWED"],
        "note": "entry outside the Phase 8J pilot set must still fail",
    },
]


def run_case(case: dict) -> dict:
    fdir = FIXTURE_DIR / case["name"]
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPT_DIR / f"{case['name']}_receipt.json"

    result = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--matrix",
            str(fdir / "matrix.yaml"),
            "--receipt-out",
            str(receipt_path),
        ],
        capture_output=True,
        text=True,
    )

    actual_error_codes: list[str] = []
    receipt_parse_error = ""
    if receipt_path.exists():
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            actual_error_codes = [e["code"] for e in receipt.get("errors", [])]
        except Exception as ex:
            receipt_parse_error = str(ex)

    passed = (
        result.returncode == case["expected_exit"]
        and set(case["expected_error_codes"]).issubset(set(actual_error_codes))
    )

    return {
        "name": case["name"],
        "expected_exit": case["expected_exit"],
        "actual_exit": result.returncode,
        "expected_error_codes": case["expected_error_codes"],
        "actual_error_codes": actual_error_codes,
        "result": "PASS" if passed else "FAIL",
        "receipt_path": str(receipt_path),
        "receipt_parse_error": receipt_parse_error,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "note": case.get("note", ""),
    }


def main() -> int:
    results = [run_case(c) for c in CASES]
    failed = [r for r in results if r["result"] == "FAIL"]

    summary = {
        "validator": "validate_port_status_bit_matrix.py",
        "smoke_runner": "smoke_validate_port_status_bit_matrix_fixtures.py",
        "authority_ceiling": "status_bit_namespace_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }

    receipt_out = ROOT / "evidence" / "validation_receipt_port_status_bit_matrix_fixtures.json"
    receipt_out.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    for r in results:
        print(f"[{r['result']}] {r['name']} - {r['note']}")
        if r["result"] == "FAIL":
            print(f"  exit: expected={r['expected_exit']} actual={r['actual_exit']}")
            print(f"  error_codes: expected={r['expected_error_codes']} actual={r['actual_error_codes']}")
            if r["receipt_parse_error"]:
                print(f"  receipt_parse_error: {r['receipt_parse_error']}")

    if failed:
        print(f"\nSmoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1
    print(f"\nSmoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
