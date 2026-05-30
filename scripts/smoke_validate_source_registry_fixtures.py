#!/usr/bin/env python3
"""Smoke-test source registry validator fixtures and emit a receipt."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_source_registry.py"
AUTHORITY = ROOT / "contract" / "authority_levels.yaml"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "source_registry"
RECEIPT_PATH = ROOT / "evidence" / "validation_receipt_source_registry_fixtures.json"
CASE_RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "source_registry_fixtures"


CASES = [
    ("valid_minimal.yaml", 0, []),
    ("invalid_unknown_authority_level.yaml", 1, ["UNKNOWN_AUTHORITY_LEVEL"]),
    ("invalid_usb_version_scope.yaml", 1, ["USB_VERSION_SCOPE_INVALID"]),
    (
        "invalid_non_normative_uses_normative_claim.yaml",
        1,
        ["NORMATIVE_CLAIM_USAGE_FOR_NON_NORMATIVE_AUTHORITY"],
    ),
    ("invalid_missing_required_field.yaml", 1, ["REQUIRED_FIELD_MISSING"]),
]


def run_case(name: str, expected_exit: int, expected_reason_codes: list[str]) -> dict:
    fixture = FIXTURE_DIR / name
    case_receipt = CASE_RECEIPT_DIR / f"{Path(name).stem}.json"
    CASE_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(VALIDATOR),
        "--authority-file",
        str(AUTHORITY),
        "--registry-file",
        str(fixture),
        "--receipt-out",
        str(case_receipt),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    reason_codes: list[str] = []
    receipt_parse_error = ""
    if case_receipt.exists():
        try:
            rec = json.loads(case_receipt.read_text(encoding="utf-8"))
            reason_codes = [f.get("code", "") for f in rec.get("findings", []) if isinstance(f, dict)]
        except Exception as exc:
            receipt_parse_error = str(exc)
    expected_reason_ok = all(code in reason_codes for code in expected_reason_codes)
    passed = proc.returncode == expected_exit and expected_reason_ok and not receipt_parse_error
    return {
        "fixture": name,
        "expected_exit": expected_exit,
        "actual_exit": proc.returncode,
        "expected_reason_codes": expected_reason_codes,
        "actual_reason_codes": sorted(set(reason_codes)),
        "result": "PASS" if passed else "FAIL",
        "receipt_path": str(case_receipt),
        "receipt_parse_error": receipt_parse_error,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def main() -> int:
    case_results = [run_case(name, expected, reason_codes) for name, expected, reason_codes in CASES]
    failed = [r for r in case_results if r["result"] == "FAIL"]

    receipt = {
        "validator": "validate_source_registry.py",
        "smoke_runner": "smoke_validate_source_registry_fixtures.py",
        "authority_ceiling": "structural_registry_validation_only",
        "total_cases": len(case_results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": case_results,
    }
    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    if failed:
        print(f"Smoke FAILED ({len(failed)}/{len(case_results)} cases failed)")
        return 1

    print(f"Smoke PASSED ({len(case_results)}/{len(case_results)} cases)")
    print(f"Receipt: {RECEIPT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
