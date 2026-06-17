#!/usr/bin/env python3
"""Smoke test validate_usb2_completion_surface.py aggregation behavior."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

from validate_usb2_completion_surface import CommandSpec, run_command_specs


PASS_SCRIPT = "pass_validator.py"
FAIL_SCRIPT = "fail_validator.py"

CASES = [
    {
        "name": "valid_all_pass",
        "commands": [
            CommandSpec("pass_one", [PASS_SCRIPT], "fixture_only"),
            CommandSpec("pass_two", [PASS_SCRIPT], "fixture_only"),
        ],
        "expected_result": "PASS",
        "expected_failed": 0,
    },
    {
        "name": "invalid_one_fails",
        "commands": [
            CommandSpec("pass_one", [PASS_SCRIPT], "fixture_only"),
            CommandSpec("fail_one", [FAIL_SCRIPT], "fixture_only"),
        ],
        "expected_result": "FAIL",
        "expected_failed": 1,
    },
]


def _write_fixture_scripts(root: Path) -> None:
    (root / PASS_SCRIPT).write_text("print('fixture pass')\n", encoding="utf-8")
    (root / FAIL_SCRIPT).write_text(
        "import sys\nprint('fixture fail')\nsys.exit(9)\n",
        encoding="utf-8",
    )


def run_case(case: dict, root: Path) -> dict:
    result, command_results = run_command_specs(case["commands"], cwd=root)
    failed = [item for item in command_results if item["result"] != "PASS"]
    passed = result == case["expected_result"] and len(failed) == case["expected_failed"]
    return {
        "name": case["name"],
        "expected_result": case["expected_result"],
        "actual_result": result,
        "expected_failed": case["expected_failed"],
        "actual_failed": len(failed),
        "result": "PASS" if passed else "FAIL",
        "commands": command_results,
    }


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="usb2-completion-surface-") as tmp:
        root = Path(tmp)
        _write_fixture_scripts(root)
        results = [run_case(case, root) for case in CASES]

    failed = [result for result in results if result["result"] == "FAIL"]
    summary = {
        "validator": "validate_usb2_completion_surface.py",
        "smoke_runner": "smoke_validate_usb2_completion_surface_fixtures.py",
        "authority_ceiling": "usb2_completion_surface_consistency_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }

    for result in results:
        print(f"[{result['result']}] {result['name']}")
        if result["result"] != "PASS":
            print(
                "  result: "
                f"expected={result['expected_result']} actual={result['actual_result']}"
            )
            print(
                "  failed: "
                f"expected={result['expected_failed']} actual={result['actual_failed']}"
            )

    print(json.dumps(summary, indent=2, ensure_ascii=True))
    if failed:
        print(f"\nSmoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1
    print(f"\nSmoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
