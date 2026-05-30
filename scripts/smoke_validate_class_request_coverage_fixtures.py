#!/usr/bin/env python3
"""Smoke test validate_class_request_coverage.py against deterministic fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_class_request_coverage.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "class_request_coverage"
RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "class_request_coverage_fixtures"

CASES = [
    {
        "name": "complete_coverage_pass",
        "expected_exit": 0,
        "expected_error_codes": [],
        "expected_advisory_codes": [],
        "note": "all expected families in matrix, missing=[] → complete PASS",
    },
    {
        "name": "partial_coverage_pass",
        "expected_exit": 0,
        "expected_error_codes": [],
        "expected_advisory_codes": [],
        "note": "some missing, correctly declared → partial PASS",
    },
    {
        "name": "missing_calculation_mismatch_fail",
        "expected_exit": 1,
        "expected_error_codes": ["MISSING_FAMILIES_INVARIANT_VIOLATED"],
        "expected_advisory_codes": [],
        "note": "declared missing != computed missing → invariant FAIL (R3)",
    },
    {
        "name": "extra_request_family_advisory",
        "expected_exit": 0,
        "expected_error_codes": [],
        "expected_advisory_codes": ["ADVISORY_EXTRA_FAMILIES_IN_MATRIX"],
        "note": "matrix has family not in expected → advisory A1, PASS",
    },
    {
        "name": "empty_expected_fail",
        "expected_exit": 1,
        "expected_error_codes": ["EXPECTED_FAMILIES_EMPTY"],
        "expected_advisory_codes": [],
        "note": "expected_request_families is empty → structural FAIL (R1)",
    },
]


def run_case(case: dict) -> dict:
    fdir = FIXTURE_DIR / case["name"]
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPT_DIR / f"{case['name']}_receipt.json"

    result = subprocess.run(
        [
            sys.executable, str(VALIDATOR),
            "--coverage", str(fdir / "coverage.json"),
            "--matrix", str(fdir / "matrix.yaml"),
            "--receipt-out", str(receipt_path),
        ],
        capture_output=True,
        text=True,
    )

    actual_error_codes: list[str] = []
    actual_advisory_codes: list[str] = []
    receipt_parse_error = ""
    if receipt_path.exists():
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            actual_error_codes = [f["code"] for f in receipt.get("errors", [])]
            actual_advisory_codes = [f["code"] for f in receipt.get("advisories", [])]
        except Exception as e:
            receipt_parse_error = str(e)

    expected_exit = case["expected_exit"]
    expected_errs = case["expected_error_codes"]
    expected_advs = case["expected_advisory_codes"]
    passed = (
        result.returncode == expected_exit
        and set(expected_errs).issubset(set(actual_error_codes))
        and set(expected_advs).issubset(set(actual_advisory_codes))
    )

    return {
        "name": case["name"],
        "expected_exit": expected_exit,
        "actual_exit": result.returncode,
        "expected_error_codes": expected_errs,
        "actual_error_codes": actual_error_codes,
        "expected_advisory_codes": expected_advs,
        "actual_advisory_codes": actual_advisory_codes,
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
        "validator": "validate_class_request_coverage.py",
        "smoke_runner": "smoke_validate_class_request_coverage_fixtures.py",
        "authority_ceiling": "class_request_family_coverage_structural_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }

    receipt_out = ROOT / "evidence" / "validation_receipt_class_request_coverage_fixtures.json"
    receipt_out.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    for r in results:
        status = r["result"]
        print(f"[{status}] {r['name']} — {r['note']}")
        if status == "FAIL":
            print(f"  exit: expected={r['expected_exit']} actual={r['actual_exit']}")
            print(f"  error_codes: expected={r['expected_error_codes']} actual={r['actual_error_codes']}")

    if failed:
        print(f"\nSmoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1
    print(f"\nSmoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
