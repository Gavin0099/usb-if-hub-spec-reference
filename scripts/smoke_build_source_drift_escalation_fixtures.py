#!/usr/bin/env python3
"""Smoke-test source drift escalation classifications."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "build_source_drift_escalation.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "source_drift_escalation"
REGISTRY = FIXTURE_DIR / "source_registry.yaml"
RULES = ROOT / "contract" / "staleness_rules.yaml"
RECEIPT_PATH = ROOT / "evidence" / "validation_receipt_source_drift_escalation_fixtures.json"
CASE_RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "source_drift_escalation_fixtures"

CASES = [
    ("no_drift", 0, "CLEAR", []),
    ("unresolved_normative", 1, "ESCALATION_REQUIRED", ["NORMATIVE_DRIFT_ESCALATION"]),
    ("unresolved_official_index", 0, "ADVISORY", ["OFFICIAL_INDEX_DRIFT_ADVISORY"]),
    ("resolved_normative", 0, "CLEAR", []),
    ("unknown_source", 1, "ERROR", ["DRIFT_SOURCE_UNREGISTERED"]),
]


def run_case(name: str, expected_exit: int, expected_status: str, expected_codes: list[str]) -> dict:
    receipt_path = CASE_RECEIPT_DIR / f"{name}.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    process = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--drift-events",
            str(FIXTURE_DIR / f"{name}.jsonl"),
            "--source-registry",
            str(REGISTRY),
            "--staleness-rules",
            str(RULES),
            "--receipt-out",
            str(receipt_path),
        ],
        capture_output=True,
        text=True,
    )
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    actual_codes = sorted({item.get("code", "") for item in receipt.get("findings", [])})
    passed = (
        process.returncode == expected_exit
        and receipt.get("status") == expected_status
        and actual_codes == sorted(expected_codes)
    )
    return {
        "fixture": name,
        "expected_exit": expected_exit,
        "actual_exit": process.returncode,
        "expected_status": expected_status,
        "actual_status": receipt.get("status"),
        "expected_reason_codes": sorted(expected_codes),
        "actual_reason_codes": actual_codes,
        "result": "PASS" if passed else "FAIL",
        "stdout": process.stdout,
        "stderr": process.stderr,
    }


def main() -> int:
    results = [run_case(*case) for case in CASES]
    failed = [result for result in results if result["result"] == "FAIL"]
    receipt = {
        "validator": "build_source_drift_escalation.py",
        "smoke_runner": "smoke_build_source_drift_escalation_fixtures.py",
        "authority_ceiling": "source_drift_escalation_observation_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }
    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    if failed:
        print(f"Smoke FAILED ({len(failed)}/{len(results)} cases failed)")
        return 1
    print(f"Smoke PASSED ({len(results)}/{len(results)} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())