#!/usr/bin/env python3
"""Smoke test validate_entry_gate_coverage.py against deterministic fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from validate_entry_gate_coverage import validate


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "entry_gate_coverage"
RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "entry_gate_coverage_fixtures"
TABLE_KEY = "class_request_matrix"


CASES = [
    {
        "name": "valid_single_table",
        "default_matrices": ["matrix.yaml"],
        "table_rules": {"class_request_matrix": {"allowed_entries": {"usb20_get_status_hub"}}},
        "packet_dir": "packets",
        "expected_exit": 0,
        "expected_error_codes": [],
    },
    {
        "name": "invalid_missing_default_matrix",
        "default_matrices": [],
        "table_rules": {"class_request_matrix": {"allowed_entries": {"usb20_get_status_hub"}}},
        "packet_dir": "packets",
        "expected_exit": 1,
        "expected_error_codes": ["DEFAULT_MATRIX_MISSING"],
    },
    {
        "name": "invalid_missing_table_rule",
        "default_matrices": ["matrix.yaml"],
        "table_rules": {},
        "packet_dir": "packets",
        "expected_exit": 1,
        "expected_error_codes": ["TABLE_RULE_MISSING"],
    },
    {
        "name": "invalid_verified_not_gated",
        "default_matrices": ["matrix.yaml"],
        "table_rules": {"class_request_matrix": {"allowed_entries": set()}},
        "packet_dir": "packets",
        "expected_exit": 1,
        "expected_error_codes": ["VERIFIED_ENTRIES_NOT_GATED"],
    },
    {
        "name": "invalid_allowlist_extra",
        "default_matrices": ["matrix.yaml"],
        "table_rules": {
            "class_request_matrix": {
                "allowed_entries": {"usb20_get_status_hub", "usb20_extra_unverified"}
            }
        },
        "packet_dir": "packets",
        "expected_exit": 1,
        "expected_error_codes": ["ALLOWLIST_HAS_NON_VERIFIED_ENTRIES"],
    },
    {
        "name": "invalid_missing_packet",
        "default_matrices": ["matrix.yaml"],
        "table_rules": {"class_request_matrix": {"allowed_entries": {"usb20_get_status_hub"}}},
        "packet_dir": "missing_packets",
        "expected_exit": 1,
        "expected_error_codes": ["VERIFIED_ENTRIES_MISSING_PACKETS"],
    },
]


def _case_paths(case: dict) -> tuple[dict[str, Path], list[Path], Path]:
    case_dir = FIXTURE_DIR / case["name"]
    expected_tables = {TABLE_KEY: case_dir / "matrix.yaml"}
    default_matrices = [case_dir / name for name in case["default_matrices"]]
    packet_dir = case_dir / case["packet_dir"]
    return expected_tables, default_matrices, packet_dir


def run_case(case: dict) -> dict:
    expected_tables, default_matrices, packet_dir = _case_paths(case)
    result, errors, coverage = validate(
        packet_dir=packet_dir,
        expected_tables=expected_tables,
        default_matrices=default_matrices,
        table_rules=case["table_rules"],
    )
    actual_exit = 0 if result == "PASS" else 1
    actual_error_codes = [error["code"] for error in errors]
    passed = (
        actual_exit == case["expected_exit"]
        and set(case["expected_error_codes"]).issubset(set(actual_error_codes))
    )
    return {
        "name": case["name"],
        "expected_exit": case["expected_exit"],
        "actual_exit": actual_exit,
        "expected_error_codes": case["expected_error_codes"],
        "actual_error_codes": actual_error_codes,
        "result": "PASS" if passed else "FAIL",
        "coverage": coverage,
        "errors": errors,
    }


def main() -> int:
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    results = [run_case(case) for case in CASES]
    failed = [result for result in results if result["result"] == "FAIL"]
    summary = {
        "validator": "validate_entry_gate_coverage.py",
        "smoke_runner": "smoke_validate_entry_gate_coverage_fixtures.py",
        "authority_ceiling": "gate_coverage_consistency_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }
    receipt_out = ROOT / "evidence" / "validation_receipt_entry_gate_coverage_fixtures.json"
    receipt_out.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    for result in results:
        print(f"[{result['result']}] {result['name']}")
        if result["result"] == "FAIL":
            print(f"  exit: expected={result['expected_exit']} actual={result['actual_exit']}")
            print(
                "  error_codes: "
                f"expected={result['expected_error_codes']} actual={result['actual_error_codes']}"
            )

    if failed:
        print(f"\nSmoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1
    print(f"\nSmoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

