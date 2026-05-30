#!/usr/bin/env python3
"""Smoke test validate_class_request_matrix.py against deterministic fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_class_request_matrix.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "class_request_matrix"
RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "class_request_matrix_fixtures"

CASES = [
    {
        "name": "valid_verified_usb20_get_status",
        "expected_exit": 0,
        "expected_error_codes": [],
        "note": "verified entry with normative_official source and section_anchor → PASS",
    },
    {
        "name": "invalid_verified_without_section_anchor",
        "expected_exit": 1,
        "expected_error_codes": ["HIGH_CLAIM_LEVEL_MISSING_SECTION_ANCHOR"],
        "note": "verified entry missing section_anchor → structural FAIL (R5)",
    },
    {
        "name": "invalid_unknown_source_ref",
        "expected_exit": 1,
        "expected_error_codes": ["SOURCE_REF_NOT_IN_REGISTRY"],
        "note": "source_ref not in registry → structural FAIL (R6)",
    },
    {
        "name": "invalid_verified_with_official_index_only",
        "expected_exit": 1,
        "expected_error_codes": ["HIGH_CLAIM_LEVEL_NO_NORMATIVE_OFFICIAL_SOURCE"],
        "note": "verified entry with only official_index source → structural FAIL (R7)",
    },
    {
        "name": "invalid_duplicate_request_id",
        "expected_exit": 1,
        "expected_error_codes": ["DUPLICATE_REQUEST_ID"],
        "note": "duplicate request_id → structural FAIL (R8)",
    },
    {
        "name": "draft_without_section_anchor_pass",
        "expected_exit": 0,
        "expected_error_codes": [],
        "note": "draft entry without section_anchor → PASS (R5 only applies to verified/normative)",
    },
    {
        "name": "valid_usb20_get_status_hub_and_port",
        "expected_exit": 0,
        "expected_error_codes": [],
        "note": "Phase 3B: GET_STATUS hub + port inferred entries with real source_id → PASS",
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
            actual_error_codes = [f["code"] for f in receipt.get("errors", [])]
        except Exception as e:
            receipt_parse_error = str(e)

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
        "validator": "validate_class_request_matrix.py",
        "smoke_runner": "smoke_validate_class_request_matrix_fixtures.py",
        "authority_ceiling": "class_request_matrix_structural_validation_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }

    receipt_out = ROOT / "evidence" / "validation_receipt_class_request_matrix_fixtures.json"
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
