#!/usr/bin/env python3
"""Smoke test validate_wiki_frontmatter.py against deterministic fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_wiki_frontmatter.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "wiki_frontmatter"
RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "wiki_frontmatter_fixtures"

CASES = [
    {
        "fixture": "valid_concept.md",
        "expected_exit": 0,
        "expected_error_codes": [],
    },
    {
        "fixture": "invalid_missing_required_fields.md",
        "expected_exit": 1,
        "expected_error_codes": ["REQUIRED_FIELD_MISSING"],
    },
    {
        "fixture": "invalid_bad_authority_level.md",
        "expected_exit": 1,
        "expected_error_codes": ["AUTHORITY_REQUIRED_INVALID"],
    },
    {
        "fixture": "advisory_normative_draft.md",
        "expected_exit": 0,
        "expected_error_codes": [],
        "expected_advisory_codes": ["ADVISORY_NORMATIVE_CLAIM_WITH_DRAFT_STATUS"],
        "note": "advisory finding recorded but does not cause FAIL",
    },
]


def run_case(case: dict) -> dict:
    fixture_path = FIXTURE_DIR / case["fixture"]
    receipt_stem = case["fixture"].replace(".md", "_receipt.json")
    receipt_path = RECEIPT_DIR / receipt_stem
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--file", str(fixture_path), "--receipt-out", str(receipt_path)],
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
    expected_err_codes = case["expected_error_codes"]
    expected_adv_codes = case.get("expected_advisory_codes", [])
    passed = (
        result.returncode == expected_exit
        and set(expected_err_codes).issubset(set(actual_error_codes))
        and set(expected_adv_codes).issubset(set(actual_advisory_codes))
    )

    return {
        "fixture": case["fixture"],
        "expected_exit": expected_exit,
        "actual_exit": result.returncode,
        "expected_error_codes": expected_err_codes,
        "actual_error_codes": actual_error_codes,
        "expected_advisory_codes": expected_adv_codes,
        "actual_advisory_codes": actual_advisory_codes,
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
        "validator": "validate_wiki_frontmatter.py",
        "smoke_runner": "smoke_validate_wiki_frontmatter_fixtures.py",
        "authority_ceiling": "wiki_frontmatter_structural_consistency_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }

    receipt_out = ROOT / "evidence" / "validation_receipt_wiki_frontmatter_fixtures.json"
    receipt_out.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    for r in results:
        status = r["result"]
        print(f"[{status}] {r['fixture']}")
        if status == "FAIL":
            print(f"  expected_exit={r['expected_exit']} actual_exit={r['actual_exit']}")
            print(f"  expected_error_codes={r['expected_error_codes']}")
            print(f"  actual_error_codes={r['actual_error_codes']}")

    if failed:
        print(f"\nSmoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1
    print(f"\nSmoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
