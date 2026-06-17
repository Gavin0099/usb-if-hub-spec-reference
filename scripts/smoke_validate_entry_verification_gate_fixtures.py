#!/usr/bin/env python3
"""Smoke test validate_entry_verification_gate.py against deterministic fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_entry_verification_gate.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "entry_verification_gate"
RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "entry_verification_gate_fixtures"

CASES = [
    {
        "name": "no_verified_entries_pass",
        "expected_exit": 0,
        "expected_error_codes": [],
        "note": "no entry-level verified promotion present; gate should pass",
    },
    {
        "name": "invalid_verified_without_packet",
        "expected_exit": 1,
        "expected_error_codes": ["VERIFIED_ENTRY_MISSING_PACKET"],
        "note": "verified entry without packet must fail",
    },
    {
        "name": "invalid_verified_wrong_scope",
        "expected_exit": 1,
        "expected_error_codes": ["PACKET_SCOPE_TOO_BROAD"],
        "note": "verified entry with a packet but broad scope must fail",
    },
    {
        "name": "valid_verified_pilot",
        "expected_exit": 0,
        "expected_error_codes": [],
        "note": "pilot entry (PORT_CONNECTION) with reviewed, eligible, narrow packet may pass the gate",
    },
    {
        "name": "valid_verified_port_enable",
        "expected_exit": 0,
        "expected_error_codes": [],
        "note": "Phase 8H: PORT_ENABLE with reviewed, eligible, narrow packet may pass the gate",
    },
    {
        "name": "valid_verified_feature_selector",
        "expected_exit": 0,
        "expected_error_codes": [],
        "note": "feature selector entry with reviewed, eligible, selector-name/value packet may pass the gate",
    },
    {
        "name": "invalid_verified_nonpilot",
        "expected_exit": 1,
        "expected_error_codes": ["VERIFIED_ENTRY_NOT_IN_PILOT_SCOPE"],
        "note": "entry not in the allowed Phase 8K pilot set (PORT_STATUS_HIGH_BIT_BOUNDARY) must be rejected",
    },
]


def run_case(case: dict) -> dict:
    fdir = FIXTURE_DIR / case["name"]
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPT_DIR / f"{case['name']}_receipt.json"
    matrix_arg = (fdir / "matrix.yaml").relative_to(ROOT)
    packet_dir_arg = (fdir / "packets").relative_to(ROOT)
    receipt_arg = receipt_path.relative_to(ROOT)

    result = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--matrix",
            str(matrix_arg),
            "--packet-dir",
            str(packet_dir_arg),
            "--receipt-out",
            str(receipt_arg),
        ],
        cwd=ROOT,
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
        "receipt_path": str(receipt_arg),
        "receipt_parse_error": receipt_parse_error,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "note": case.get("note", ""),
    }


def main() -> int:
    results = [run_case(c) for c in CASES]
    failed = [r for r in results if r["result"] == "FAIL"]

    summary = {
        "validator": "validate_entry_verification_gate.py",
        "smoke_runner": "smoke_validate_entry_verification_gate_fixtures.py",
        "authority_ceiling": "entry_level_verified_gate_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }

    receipt_out = ROOT / "evidence" / "validation_receipt_entry_verification_gate_fixtures.json"
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
