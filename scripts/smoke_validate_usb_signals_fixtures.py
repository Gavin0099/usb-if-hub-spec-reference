#!/usr/bin/env python3
"""Smoke test validate_usb_signals.py against deterministic fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_usb_signals.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "usb_signals"
RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "usb_signals_fixtures"

CASES = [
    {
        "fixture": "valid_normative_usb20.json",
        "expected_exit": 0,
        "expected_reason_codes": [],
    },
    {
        "fixture": "invalid_normative_from_community.json",
        "expected_exit": 1,
        "expected_reason_codes": ["NORMATIVE_CLAIM_REQUIRES_NORMATIVE_OFFICIAL"],
    },
    {
        "fixture": "invalid_unresolved_drift_verified.json",
        "expected_exit": 1,
        "expected_reason_codes": ["UNRESOLVED_DRIFT_INCOMPATIBLE_WITH_CLAIM_LEVEL"],
    },
    {
        "fixture": "invalid_usb21_base_scope.json",
        "expected_exit": 1,
        "expected_reason_codes": ["USB21_SCOPE_ROLE_MUST_NOT_BE_BASE"],
    },
    {
        "fixture": "invalid_usb4_hub_equivalence.json",
        "expected_exit": 1,
        "expected_reason_codes": ["USB4_HUB_CLASS_EQUIVALENCE_INVALID"],
    },
]


def run_case(case: dict) -> dict:
    fixture_path = FIXTURE_DIR / case["fixture"]
    receipt_stem = case["fixture"].replace(".json", "_receipt.json")
    receipt_path = RECEIPT_DIR / receipt_stem

    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--file", str(fixture_path),
            "--receipt-out", str(receipt_path),
        ],
        capture_output=True,
        text=True,
    )

    actual_reason_codes: list[str] = []
    receipt_parse_error = ""
    if receipt_path.exists():
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            actual_reason_codes = [f["code"] for f in receipt.get("findings", [])]
        except Exception as e:
            receipt_parse_error = str(e)

    expected_exit = case["expected_exit"]
    expected_codes = case["expected_reason_codes"]
    passed = (
        result.returncode == expected_exit
        and set(expected_codes).issubset(set(actual_reason_codes))
    )

    return {
        "fixture": case["fixture"],
        "expected_exit": expected_exit,
        "actual_exit": result.returncode,
        "expected_reason_codes": expected_codes,
        "actual_reason_codes": actual_reason_codes,
        "result": "PASS" if passed else "FAIL",
        "receipt_path": str(receipt_path),
        "receipt_parse_error": receipt_parse_error,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def main() -> int:
    results = [run_case(c) for c in CASES]
    failed = [r for r in results if r["result"] == "FAIL"]

    summary = {
        "validator": "validate_usb_signals.py",
        "smoke_runner": "smoke_validate_usb_signals_fixtures.py",
        "authority_ceiling": "claim_authority_invariants_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }

    receipt_out = ROOT / "evidence" / "validation_receipt_usb_signals_fixtures.json"
    receipt_out.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    for r in results:
        status = r["result"]
        print(f"[{status}] {r['fixture']}")
        if status == "FAIL":
            print(f"  expected_exit={r['expected_exit']} actual_exit={r['actual_exit']}")
            print(f"  expected_codes={r['expected_reason_codes']}")
            print(f"  actual_codes={r['actual_reason_codes']}")

    if failed:
        print(f"\nSmoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1

    print(f"\nSmoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
