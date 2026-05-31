#!/usr/bin/env python3
"""Smoke test validate_feature_selector_matrix.py against deterministic fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_feature_selector_matrix.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "feature_selector_matrix"
RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "feature_selector_matrix_fixtures"

CASES = [
    {
        "name": "valid_structural_pass",
        "expected_exit": 0,
        "expected_error_codes": [],
        "note": "hub+port+reserved entries, valid structure → PASS (advisory for partial coverage)",
    },
    {
        "name": "invalid_duplicate_selector_id",
        "expected_exit": 1,
        "expected_error_codes": ["DUPLICATE_SELECTOR_ID"],
        "note": "two entries share selector_id → structural FAIL (R1)",
    },
    {
        "name": "invalid_missing_selector_name",
        "expected_exit": 1,
        "expected_error_codes": ["EMPTY_SELECTOR_NAME"],
        "note": "selector_name is empty string → structural FAIL (R2)",
    },
    {
        "name": "invalid_port_value_out_of_range",
        "expected_exit": 1,
        "expected_error_codes": ["PORT_SELECTOR_OUT_OF_RANGE"],
        "note": "port entry with selector_value=23 → structural FAIL (R4)",
    },
]


def run_case(case: dict) -> dict:
    fdir = FIXTURE_DIR / case["name"]
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPT_DIR / f"{case['name']}_receipt.json"

    result = subprocess.run(
        [
            sys.executable, str(VALIDATOR),
            "--matrix", str(fdir / "matrix.yaml"),
            "--source-registry", str(fdir / "source_registry.yaml"),
            "--receipt-out", str(receipt_path),
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

    expected_exit = case["expected_exit"]
    expected_errs = case["expected_error_codes"]
    passed = (
        result.returncode == expected_exit
        and set(expected_errs).issubset(set(actual_error_codes))
    )

    return {
        "name": case["name"],
        "expected_exit": expected_exit,
        "actual_exit": result.returncode,
        "expected_error_codes": expected_errs,
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
        "validator": "validate_feature_selector_matrix.py",
        "smoke_runner": "smoke_validate_feature_selector_matrix_fixtures.py",
        "authority_ceiling": "feature_selector_namespace_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }

    receipt_out = ROOT / "evidence" / "validation_receipt_feature_selector_matrix_fixtures.json"
    receipt_out.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    for r in results:
        status = r["result"]
        print(f"[{status}] {r['name']} — {r['note']}")
        if status == "FAIL":
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
