#!/usr/bin/env python3
"""Smoke test validate_wiki_source_coverage.py against deterministic fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_wiki_source_coverage.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "wiki_source_coverage"
RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "wiki_source_coverage_fixtures"

CASES = [
    {
        "name": "valid_verified_with_normative_source",
        "expected_exit": 0,
        "expected_error_codes": [],
        "expected_advisory_codes": [],
        "note": "verified + normative_official source → PASS",
    },
    {
        "name": "invalid_verified_without_source_refs",
        "expected_exit": 1,
        "expected_error_codes": ["HIGH_CLAIM_LEVEL_MISSING_SOURCE_REFS"],
        "expected_advisory_codes": [],
        "note": "verified + no source_refs → structural FAIL (R1)",
    },
    {
        "name": "invalid_normative_with_unknown_source_ref",
        "expected_exit": 1,
        "expected_error_codes": ["SOURCE_REF_NOT_IN_REGISTRY"],
        "expected_advisory_codes": [],
        "note": "normative + source_ref not in registry → structural FAIL (R2)",
    },
    {
        "name": "invalid_normative_with_community_only",
        "expected_exit": 1,
        "expected_error_codes": ["HIGH_CLAIM_LEVEL_NO_NORMATIVE_OFFICIAL_SOURCE"],
        "expected_advisory_codes": [],
        "note": "normative + community_reference only → structural FAIL (R4)",
    },
    {
        "name": "invalid_verified_with_official_index_only",
        "expected_exit": 1,
        "expected_error_codes": ["HIGH_CLAIM_LEVEL_NO_NORMATIVE_OFFICIAL_SOURCE"],
        "expected_advisory_codes": [],
        "note": "verified + official_index only → structural FAIL (R4)",
    },
    {
        "name": "provisional_without_source_refs_advisory",
        "expected_exit": 0,
        "expected_error_codes": [],
        "expected_advisory_codes": ["ADVISORY_LOW_CLAIM_WITHOUT_SOURCE_REFS"],
        "note": "provisional + no source_refs → PASS with advisory (A1)",
    },
]


def run_case(case: dict) -> dict:
    fdir = FIXTURE_DIR / case["name"]
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPT_DIR / f"{case['name']}_receipt.json"

    result = subprocess.run(
        [
            sys.executable, str(VALIDATOR),
            "--source-registry", str(fdir / "source_registry.yaml"),
            "--wiki-dir", str(fdir / "wiki_pages"),
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
        "validator": "validate_wiki_source_coverage.py",
        "smoke_runner": "smoke_validate_wiki_source_coverage_fixtures.py",
        "authority_ceiling": "wiki_source_reference_coverage_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }

    receipt_out = ROOT / "evidence" / "validation_receipt_wiki_source_coverage_fixtures.json"
    receipt_out.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    for r in results:
        status = r["result"]
        print(f"[{status}] {r['name']} — {r['note']}")
        if status == "FAIL":
            print(f"  exit: expected={r['expected_exit']} actual={r['actual_exit']}")
            print(f"  error_codes: expected={r['expected_error_codes']} actual={r['actual_error_codes']}")
            print(f"  advisory_codes: expected={r['expected_advisory_codes']} actual={r['actual_advisory_codes']}")

    if failed:
        print(f"\nSmoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1
    print(f"\nSmoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
