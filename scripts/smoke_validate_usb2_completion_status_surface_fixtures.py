#!/usr/bin/env python3
"""Smoke test validate_usb2_completion_status_surface.py text checks."""

from __future__ import annotations

import json
import sys

from validate_usb2_completion_status_surface import (
    REQUIRED_EN_LITERALS,
    REQUIRED_SHARED_LITERALS,
    validate_text,
)


VALID_TEXT = "\n".join(REQUIRED_SHARED_LITERALS + REQUIRED_EN_LITERALS)

CASES = [
    {
        "name": "valid_status_text",
        "text": VALID_TEXT,
        "expected_error_codes": [],
    },
    {
        "name": "invalid_missing_guard",
        "text": VALID_TEXT.replace("Completion surface aggregate", ""),
        "expected_error_codes": ["STATUS_REQUIRED_LITERAL_MISSING"],
    },
    {
        "name": "invalid_missing_formula",
        "text": VALID_TEXT.replace("151 = 105 verified + 46 reviewed + 0 inferred + 0 missing", ""),
        "expected_error_codes": ["STATUS_REQUIRED_LITERAL_MISSING"],
    },
    {
        "name": "invalid_missing_nonclaim",
        "text": VALID_TEXT.replace("firmware correctness", ""),
        "expected_error_codes": ["STATUS_REQUIRED_LITERAL_MISSING"],
    },
]


def run_case(case: dict) -> dict:
    errors = validate_text(case["text"], REQUIRED_SHARED_LITERALS + REQUIRED_EN_LITERALS, "fixture")
    actual_error_codes = [error["code"] for error in errors]
    expected = case["expected_error_codes"]
    passed = bool(actual_error_codes) == bool(expected) and set(expected).issubset(set(actual_error_codes))
    return {
        "name": case["name"],
        "expected_error_codes": expected,
        "actual_error_codes": actual_error_codes,
        "result": "PASS" if passed else "FAIL",
        "errors": errors,
    }


def main() -> int:
    results = [run_case(case) for case in CASES]
    failed = [result for result in results if result["result"] == "FAIL"]
    summary = {
        "validator": "validate_usb2_completion_status_surface.py",
        "smoke_runner": "smoke_validate_usb2_completion_status_surface_fixtures.py",
        "authority_ceiling": "usb2_completion_status_visibility_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }

    for result in results:
        print(f"[{result['result']}] {result['name']}")
        if result["result"] != "PASS":
            print(
                "  error_codes: "
                f"expected={result['expected_error_codes']} actual={result['actual_error_codes']}"
            )

    print(json.dumps(summary, indent=2, ensure_ascii=True))
    if failed:
        print(f"\nSmoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1
    print(f"\nSmoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
