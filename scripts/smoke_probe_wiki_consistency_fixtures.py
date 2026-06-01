#!/usr/bin/env python3
"""Smoke test probe_wiki_consistency.py against deterministic fixtures.

Cases:
  consistent        all table names found in page → exit 0, missing_count=0, advisory_count=0
  partial_coverage  one name missing from page   → exit 0, missing_count=1, advisory_count=1
  empty_table       table has no entries          → exit 0, missing_count=0, coverage_pct=100.0
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "scripts" / "probe_wiki_consistency.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "wiki_consistency"
RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "wiki_consistency_fixtures"

CASES = [
    {
        "name": "consistent",
        "fixture_dir": "consistent",
        "name_field": "request_name",
        "expected_exit": 0,
        "expected_missing_count": 0,
        "expected_advisory_count": 0,
        "note": "all table names present in page → no advisories",
    },
    {
        "name": "partial_coverage",
        "fixture_dir": "partial_coverage",
        "name_field": "request_name",
        "expected_exit": 0,
        "expected_missing_count": 1,
        "expected_advisory_count": 1,
        "note": "one name absent from page → 1 advisory, still exit 0",
    },
    {
        "name": "empty_table",
        "fixture_dir": "empty_table",
        "name_field": "request_name",
        "expected_exit": 0,
        "expected_missing_count": 0,
        "expected_advisory_count": 0,
        "note": "empty table → 100% coverage trivially, 0 advisories",
    },
]


def _parse_receipt(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def run_case(case: dict) -> dict:
    fdir = FIXTURE_DIR / case["fixture_dir"]
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPT_DIR / f"{case['name']}_receipt.json"

    r = subprocess.run(
        [
            sys.executable, str(PROBE),
            "--table", str(fdir / "table.yaml"),
            "--name-field", case["name_field"],
            "--page", str(fdir / "page.md"),
            "--table-id", case["name"],
            "--receipt-out", str(receipt_path),
        ],
        capture_output=True, text=True,
    )

    receipt = _parse_receipt(receipt_path)
    actual_exit = r.returncode
    exit_ok = actual_exit == case["expected_exit"]

    actual_missing = receipt.get("missing_count", -1)
    actual_advisory = receipt.get("advisory_count", -1)
    missing_ok = actual_missing == case["expected_missing_count"]
    advisory_ok = actual_advisory == case["expected_advisory_count"]

    passed = exit_ok and missing_ok and advisory_ok
    return {
        "name": case["name"],
        "expected_exit": case["expected_exit"],
        "actual_exit": actual_exit,
        "expected_missing_count": case["expected_missing_count"],
        "actual_missing_count": actual_missing,
        "expected_advisory_count": case["expected_advisory_count"],
        "actual_advisory_count": actual_advisory,
        "result": "PASS" if passed else "FAIL",
        "receipt_path": str(receipt_path),
        "stderr": r.stderr,
        "note": case["note"],
    }


def main() -> int:
    results = [run_case(c) for c in CASES]
    failed = [r for r in results if r["result"] == "FAIL"]

    summary = {
        "probe": "probe_wiki_consistency.py",
        "smoke_runner": "smoke_probe_wiki_consistency_fixtures.py",
        "authority_ceiling": "wiki_specs_governed_table_cross_reference_observation_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }

    receipt_out = ROOT / "evidence" / "validation_receipt_probe_wiki_consistency_fixtures.json"
    receipt_out.write_text(
        json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
    )

    for r in results:
        status = r["result"]
        print(f"[{status}] {r['name']} — {r['note']}")
        if status == "FAIL":
            print(f"  exit: expected={r['expected_exit']} actual={r['actual_exit']}")
            print(f"  missing_count: expected={r['expected_missing_count']} actual={r['actual_missing_count']}")
            print(f"  advisory_count: expected={r['expected_advisory_count']} actual={r['actual_advisory_count']}")
            if r.get("stderr"):
                print(f"  stderr: {r['stderr'][:300]}")

    if failed:
        print(f"\nSmoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1
    print(f"\nSmoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
