#!/usr/bin/env python3
"""Smoke-test the public specification boundary inventory validator."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_public_spec_boundary_inventory.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "public_spec_boundary_inventory"
RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "public_spec_boundary_inventory_fixtures"

CASES = [
    {
        "name": "valid",
        "expected_exit": 0,
        "expected_error_codes": [],
        "note": "all public pages accounted with matching source metadata",
    },
    {
        "name": "invalid_untracked_page",
        "expected_exit": 1,
        "expected_error_codes": ["UNTRACKED_PUBLIC_PAGE"],
        "note": "a public page omitted from inventory must fail",
    },
    {
        "name": "invalid_source_refs_mismatch",
        "expected_exit": 1,
        "expected_error_codes": ["SOURCE_REFS_MISMATCH"],
        "note": "inventory and page frontmatter source refs must agree",
    },
    {
        "name": "invalid_missing_source_metadata",
        "expected_exit": 1,
        "expected_error_codes": ["MISSING_SOURCE_METADATA"],
        "note": "a source-backed page must have a source scope",
    },
    {
        "name": "invalid_review_state",
        "expected_exit": 1,
        "expected_error_codes": ["CLEARED_REQUIRES_EVIDENCE"],
        "note": "cleared pages require review evidence",
    },
    {
        "name": "invalid_risk_class",
        "expected_exit": 1,
        "expected_error_codes": ["INVALID_RISK_CLASS"],
        "note": "risk classes are a closed inventory vocabulary",
    },
    {
        "name": "invalid_review_state_enum",
        "expected_exit": 1,
        "expected_error_codes": ["INVALID_REVIEW_STATE"],
        "note": "review states are a closed inventory vocabulary",
    },
]


def run_case(case: dict[str, object]) -> dict[str, object]:
    fixture = FIXTURE_DIR / str(case["name"])
    receipt_path = RECEIPT_DIR / f"{case['name']}_receipt.json"
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--repo-root",
            str(fixture),
            "--inventory",
            str(fixture / "governance" / "inventory.yaml"),
            "--source-registry",
            str(fixture / "evidence" / "source_registry.yaml"),
            "--receipt-out",
            str(receipt_path),
        ],
        capture_output=True,
        text=True,
    )

    actual_error_codes: list[str] = []
    receipt_parse_error = ""
    if receipt_path.exists():
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            actual_error_codes = [entry["code"] for entry in receipt.get("errors", [])]
        except Exception as exc:  # pragma: no cover - diagnostic path
            receipt_parse_error = str(exc)

    expected_codes = [str(code) for code in case["expected_error_codes"]]
    passed = result.returncode == int(case["expected_exit"]) and set(expected_codes).issubset(
        set(actual_error_codes)
    )
    return {
        "name": case["name"],
        "expected_exit": case["expected_exit"],
        "actual_exit": result.returncode,
        "expected_error_codes": expected_codes,
        "actual_error_codes": actual_error_codes,
        "result": "PASS" if passed else "FAIL",
        "receipt_path": str(receipt_path),
        "receipt_parse_error": receipt_parse_error,
        "note": case["note"],
    }


def main() -> int:
    results = [run_case(case) for case in CASES]
    failed = [result for result in results if result["result"] == "FAIL"]
    summary = {
        "validator": "validate_public_spec_boundary_inventory.py",
        "smoke_runner": "smoke_validate_public_spec_boundary_inventory_fixtures.py",
        "authority_ceiling": "public_page_boundary_inventory_structural_only",
        "legal_clearance": "NOT CLAIMED",
        "semantic_copy_detection": "NOT CLAIMED",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }
    receipt_out = ROOT / "evidence" / "validation_receipt_public_spec_boundary_inventory_fixtures.json"
    receipt_out.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    for result in results:
        print(f"[{result['result']}] {result['name']} - {result['note']}")
        if result["result"] == "FAIL":
            print(
                "  error_codes: "
                f"expected={result['expected_error_codes']} actual={result['actual_error_codes']}"
            )
            if result["receipt_parse_error"]:
                print(f"  receipt_parse_error: {result['receipt_parse_error']}")

    if failed:
        print(f"\nSmoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1
    print(f"\nSmoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
