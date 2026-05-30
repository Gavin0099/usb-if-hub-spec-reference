#!/usr/bin/env python3
"""Smoke test validate_source_reachability.py against deterministic fixtures.

All fixtures run with --skip-network; no external HTTP calls.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_source_reachability.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "source_reachability"
RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "source_reachability_fixtures"

CASES = [
    {
        "fixture": "valid_reachable.yaml",
        "expected_exit": 0,
        "expected_reason_codes": [],
    },
    {
        "fixture": "invalid_unreachable.yaml",
        "expected_exit": 0,
        "expected_reason_codes": [],
        "note": "unreachable URL only affects advisory reachability, not metadata PASS/FAIL",
    },
    {
        "fixture": "invalid_url_type_mismatch.yaml",
        "expected_exit": 1,
        "expected_reason_codes": ["URL_TYPE_NOT_ALLOWED_FOR_AUTHORITY"],
    },
]


def run_case(case: dict) -> dict:
    fixture_path = FIXTURE_DIR / case["fixture"]
    receipt_stem = case["fixture"].replace(".yaml", ".json")
    receipt_path = RECEIPT_DIR / receipt_stem

    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--registry-file", str(fixture_path),
            "--skip-network",
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
        **({"note": case["note"]} if "note" in case else {}),
    }


def main() -> int:
    results = [run_case(c) for c in CASES]
    failed = [r for r in results if r["result"] == "FAIL"]

    summary = {
        "validator": "validate_source_reachability.py",
        "smoke_runner": "smoke_validate_source_reachability_fixtures.py",
        "authority_ceiling": "source_reachability_and_metadata_consistency_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }

    receipt_out = ROOT / "evidence" / "validation_receipt_source_reachability_fixtures.json"
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
