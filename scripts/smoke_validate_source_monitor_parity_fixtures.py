#!/usr/bin/env python3
"""Smoke-test source/monitor parity validator fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_source_monitor_parity.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "source_monitor_parity"
RECEIPT_PATH = ROOT / "evidence" / "validation_receipt_source_monitor_parity_fixtures.json"
CASE_RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "source_monitor_parity_fixtures"

CASES = [
    ("valid", 0, []),
    ("active_source_unmonitored", 1, ["ACTIVE_SOURCE_UNMONITORED"]),
    ("unknown_mapping", 1, ["ACTIVE_SOURCE_UNMONITORED", "MONITOR_SOURCE_MAPPING_UNKNOWN"]),
    ("metadata_mismatch", 1, ["MONITOR_METADATA_MISMATCH"]),
    ("mapping_missing", 1, ["ACTIVE_SOURCE_UNMONITORED", "MONITOR_SOURCE_MAPPING_MISSING"]),
]


def run_case(name: str, expected_exit: int, expected_codes: list[str]) -> dict:
    source_registry = FIXTURE_DIR / name / "source_registry.yaml"
    monitor_registry = FIXTURE_DIR / name / "monitored_sources.yaml"
    receipt_path = CASE_RECEIPT_DIR / f"{name}.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    process = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--source-registry",
            str(source_registry),
            "--monitor-registry",
            str(monitor_registry),
            "--receipt-out",
            str(receipt_path),
        ],
        capture_output=True,
        text=True,
    )
    actual_codes: list[str] = []
    parse_error = ""
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        actual_codes = sorted({item.get("code", "") for item in receipt.get("findings", [])})
    except Exception as exc:  # noqa: BLE001
        parse_error = str(exc)
    passed = process.returncode == expected_exit and actual_codes == sorted(expected_codes) and not parse_error
    return {
        "fixture": name,
        "expected_exit": expected_exit,
        "actual_exit": process.returncode,
        "expected_reason_codes": sorted(expected_codes),
        "actual_reason_codes": actual_codes,
        "result": "PASS" if passed else "FAIL",
        "receipt_path": str(receipt_path),
        "receipt_parse_error": parse_error,
        "stdout": process.stdout,
        "stderr": process.stderr,
    }


def main() -> int:
    results = [run_case(*case) for case in CASES]
    failed = [result for result in results if result["result"] == "FAIL"]
    receipt = {
        "validator": "validate_source_monitor_parity.py",
        "smoke_runner": "smoke_validate_source_monitor_parity_fixtures.py",
        "authority_ceiling": "source_monitor_registry_parity_only",
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