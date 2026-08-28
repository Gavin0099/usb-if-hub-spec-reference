#!/usr/bin/env python3
"""Smoke-test the public specification-copy policy validator fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_public_spec_copy_policy.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "public_spec_copy_policy"
RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "public_spec_copy_policy_fixtures"

CASES = [
    {
        "name": "valid_policy",
        "expected_exit": 0,
        "expected_error_codes": [],
        "note": "complete policy boundary and attribution anchors",
    },
    {
        "name": "invalid_missing_must_not_rule",
        "expected_exit": 1,
        "expected_error_codes": ["MISSING_MUST_NOT_RULE"],
        "note": "omitting a reproduction prohibition must fail",
    },
    {
        "name": "invalid_missing_authority_anchor",
        "expected_exit": 1,
        "expected_error_codes": ["MISSING_AUTHORITY_ANCHOR"],
        "note": "omitting the non-affiliation boundary must fail",
    },
    {
        "name": "invalid_missing_licensing_boundary",
        "expected_exit": 1,
        "expected_error_codes": ["MISSING_LICENSING_BOUNDARY"],
        "note": "omitting the third-party licensing boundary must fail",
    },
]


def run_case(case: dict[str, object]) -> dict[str, object]:
    fixture = FIXTURE_DIR / str(case["name"]) / "policy.md"
    receipt_path = RECEIPT_DIR / f"{case['name']}_receipt.json"
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--policy",
            str(fixture),
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
            actual_error_codes = [entry["code"] for entry in receipt.get("errors", [])]
        except Exception as exc:  # pragma: no cover - diagnostic path
            receipt_parse_error = str(exc)

    expected_codes = [str(code) for code in case["expected_error_codes"]]
    passed = result.returncode == int(case["expected_exit"]) and set(expected_codes).issubset(
        set(actual_error_codes)
    )
    return {
        "name": case["name"],
        "expected_exit": case["expected_exit"],
        "actual_exit": result.returncode,
        "expected_error_codes": expected_codes,
        "actual_error_codes": actual_error_codes,
        "result": "PASS" if passed else "FAIL",
        "receipt_path": str(receipt_path),
        "receipt_parse_error": receipt_parse_error,
        "note": case["note"],
    }


def main() -> int:
    results = [run_case(case) for case in CASES]
    failed = [result for result in results if result["result"] == "FAIL"]
    summary = {
        "validator": "validate_public_spec_copy_policy.py",
        "smoke_runner": "smoke_validate_public_spec_copy_policy_fixtures.py",
        "authority_ceiling": "policy_structure_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }
    receipt_out = ROOT / "evidence" / "validation_receipt_public_spec_copy_policy_fixtures.json"
    receipt_out.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    for result in results:
        print(f"[{result['result']}] {result['name']} - {result['note']}")
        if result["result"] == "FAIL":
            print(
                "  error_codes: "
                f"expected={result['expected_error_codes']} actual={result['actual_error_codes']}"
            )
            if result["receipt_parse_error"]:
                print(f"  receipt_parse_error: {result['receipt_parse_error']}")

    if failed:
        print(f"\nSmoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1
    print(f"\nSmoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
