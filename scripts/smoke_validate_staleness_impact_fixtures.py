#!/usr/bin/env python3
"""Smoke test validate_staleness_impact.py against deterministic fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_staleness_impact.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "staleness_impact"
RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "staleness_impact_fixtures"

CASES = [
    {
        "name": "unresolved_normative_blocks_verified",
        "expected_exit": 1,
        "expected_structural_fails": 1,
        "expected_advisories": 0,
        "note": "unresolved normative_official drift → verified claim = structural_fail",
    },
    {
        "name": "unresolved_normative_blocks_normative",
        "expected_exit": 1,
        "expected_structural_fails": 1,
        "expected_advisories": 0,
        "note": "unresolved normative_official drift → normative claim = structural_fail",
    },
    {
        "name": "official_index_drift_advisory",
        "expected_exit": 0,
        "expected_structural_fails": 0,
        "expected_advisories": 1,
        "note": "unresolved official_index drift → advisory only, PASS",
    },
    {
        "name": "community_drift_no_impact",
        "expected_exit": 0,
        "expected_structural_fails": 0,
        "expected_advisories": 0,
        "note": "community_reference drift → no impact on any claim level",
    },
    {
        "name": "reviewed_drift_no_impact",
        "expected_exit": 0,
        "expected_structural_fails": 0,
        "expected_advisories": 0,
        "note": "reviewed_no_impact drift → no impact regardless of authority level",
    },
    {
        "name": "no_drift_clean_pass",
        "expected_exit": 0,
        "expected_structural_fails": 0,
        "expected_advisories": 0,
        "note": "no drift events → clean PASS",
    },
]


def run_case(case: dict) -> dict:
    fdir = FIXTURE_DIR / case["name"]
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPT_DIR / f"{case['name']}_receipt.json"

    result = subprocess.run(
        [
            sys.executable, str(VALIDATOR),
            "--drift-events", str(fdir / "drift_events.jsonl"),
            "--source-registry", str(fdir / "source_registry.yaml"),
            "--staleness-rules", str(ROOT / "contract" / "staleness_rules.yaml"),
            "--wiki-dir", str(fdir / "wiki_pages"),
            "--receipt-out", str(receipt_path),
        ],
        capture_output=True,
        text=True,
    )

    actual_fails = 0
    actual_advisories = 0
    receipt_parse_error = ""
    if receipt_path.exists():
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            actual_fails = receipt.get("structural_fail_count", 0)
            actual_advisories = receipt.get("advisory_count", 0)
        except Exception as e:
            receipt_parse_error = str(e)

    expected_exit = case["expected_exit"]
    expected_fails = case["expected_structural_fails"]
    expected_adv = case["expected_advisories"]
    passed = (
        result.returncode == expected_exit
        and actual_fails == expected_fails
        and actual_advisories == expected_adv
    )

    return {
        "name": case["name"],
        "expected_exit": expected_exit,
        "actual_exit": result.returncode,
        "expected_structural_fails": expected_fails,
        "actual_structural_fails": actual_fails,
        "expected_advisories": expected_adv,
        "actual_advisories": actual_advisories,
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
        "validator": "validate_staleness_impact.py",
        "smoke_runner": "smoke_validate_staleness_impact_fixtures.py",
        "authority_ceiling": "drift_to_claim_level_impact_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }

    receipt_out = ROOT / "evidence" / "validation_receipt_staleness_impact_fixtures.json"
    receipt_out.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    for r in results:
        status = r["result"]
        print(f"[{status}] {r['name']} — {r['note']}")
        if status == "FAIL":
            print(f"  exit: expected={r['expected_exit']} actual={r['actual_exit']}")
            print(f"  structural_fails: expected={r['expected_structural_fails']} actual={r['actual_structural_fails']}")
            print(f"  advisories: expected={r['expected_advisories']} actual={r['actual_advisories']}")
            if r["stderr"]:
                print(f"  stderr: {r['stderr'][:300]}")

    if failed:
        print(f"\nSmoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1
    print(f"\nSmoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
