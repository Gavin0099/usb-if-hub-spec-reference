#!/usr/bin/env python3
"""Smoke test manifest access-contract validator against deterministic fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_usb20_hub_class_request_manifest.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "manifest_access_contract"
RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "manifest_access_contract_fixtures"

CASES = [
    {"name": "valid_manifest", "expected_exit": 0, "expected_error_codes": []},
    {"name": "missing_table_path", "expected_exit": 1, "expected_error_codes": ["PATH_NOT_FOUND"]},
    {"name": "id_mismatch", "expected_exit": 1, "expected_error_codes": ["ID_MISMATCH"]},
    {"name": "unparsable_target", "expected_exit": 1, "expected_error_codes": ["TARGET_UNPARSABLE"]},
]


def run_case(case: dict) -> dict:
    fdir = FIXTURE_DIR / case["name"]
    receipt_path = RECEIPT_DIR / f"{case['name']}_receipt.json"
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--manifest",
            str(fdir / "manifest.yaml"),
            "--receipt-out",
            str(receipt_path),
        ],
        capture_output=True,
        text=True,
    )

    parsed_codes: list[str] = []
    if receipt_path.exists():
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        parsed_codes = [e["code"] for e in receipt.get("errors", [])]

    ok = result.returncode == case["expected_exit"] and set(case["expected_error_codes"]).issubset(set(parsed_codes))
    return {
        "name": case["name"],
        "result": "PASS" if ok else "FAIL",
        "expected_exit": case["expected_exit"],
        "actual_exit": result.returncode,
        "expected_error_codes": case["expected_error_codes"],
        "actual_error_codes": parsed_codes,
    }


def main() -> int:
    results = [run_case(c) for c in CASES]
    failed = [r for r in results if r["result"] == "FAIL"]
    summary = {
        "validator": "validate_usb20_hub_class_request_manifest.py",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }
    out = ROOT / "evidence" / "validation_receipt_usb20_hub_class_request_manifest_fixtures.json"
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"Smoke {'PASSED' if not failed else 'FAILED'}: {len(results)-len(failed)}/{len(results)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
