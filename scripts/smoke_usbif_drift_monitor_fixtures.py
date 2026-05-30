#!/usr/bin/env python3
"""Smoke test usbif_source_monitor.py against deterministic fixtures.

All fixtures run with --skip-network; no external HTTP calls.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MONITOR = ROOT / "monitor" / "usbif_source_monitor.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "drift_monitor"
RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "drift_monitor_fixtures"

CASES = [
    {
        "name": "unchanged",
        "fixture_dir": "unchanged",
        "expected_drift_events": 0,
        "expected_snapshots": 1,
        "note": "same hash → no drift event",
    },
    {
        "name": "changed_hash",
        "fixture_dir": "changed_hash",
        "expected_drift_events": 1,
        "expected_snapshots": 1,
        "note": "different hash → drift event produced",
    },
    {
        "name": "missing_previous",
        "fixture_dir": "missing_previous",
        "expected_drift_events": 0,
        "expected_snapshots": 1,
        "note": "no previous snapshot → baseline only, no drift event",
    },
    {
        "name": "unreachable",
        "fixture_dir": "unreachable",
        "expected_drift_events": 0,
        "expected_snapshots": 1,
        "note": "unreachable source → advisory only, snapshot written, no drift event",
    },
]


def count_jsonl_lines(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def run_case(case: dict) -> dict:
    fdir = FIXTURE_DIR / case["fixture_dir"]
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPT_DIR / f"{case['name']}_receipt.json"

    with tempfile.TemporaryDirectory() as tmpdir:
        snap_path = Path(tmpdir) / "snapshots.jsonl"
        drift_path = Path(tmpdir) / "drift_events.jsonl"

        # copy previous_snapshots into temp (simulate prior state)
        prev_src = fdir / "previous_snapshots.jsonl"
        if prev_src.exists() and prev_src.stat().st_size > 0:
            snap_path.write_bytes(prev_src.read_bytes())
        else:
            snap_path.write_text("", encoding="utf-8")

        result = subprocess.run(
            [
                sys.executable,
                str(MONITOR),
                "--sources", str(fdir / "sources.yaml"),
                "--snapshots", str(snap_path),
                "--drift-events", str(drift_path),
                "--skip-network",
                "--mock-responses", str(fdir / "mock_responses.json"),
                "--receipt-out", str(receipt_path),
            ],
            capture_output=True,
            text=True,
        )

        # count only NEW snapshots written this run (not previous)
        prev_count = count_jsonl_lines(prev_src) if prev_src.exists() else 0
        total_snaps = count_jsonl_lines(snap_path)
        new_snaps = total_snaps - prev_count
        actual_drift_events = count_jsonl_lines(drift_path)

    expected_drift = case["expected_drift_events"]
    expected_snaps = case["expected_snapshots"]
    passed = (
        result.returncode == 0
        and actual_drift_events == expected_drift
        and new_snaps == expected_snaps
    )

    return {
        "name": case["name"],
        "expected_drift_events": expected_drift,
        "actual_drift_events": actual_drift_events,
        "expected_new_snapshots": expected_snaps,
        "actual_new_snapshots": new_snaps,
        "monitor_exit": result.returncode,
        "result": "PASS" if passed else "FAIL",
        "receipt_path": str(receipt_path),
        "stdout": result.stdout,
        "stderr": result.stderr,
        "note": case.get("note", ""),
    }


def main() -> int:
    results = [run_case(c) for c in CASES]
    failed = [r for r in results if r["result"] == "FAIL"]

    summary = {
        "monitor": "usbif_source_monitor.py",
        "smoke_runner": "smoke_usbif_drift_monitor_fixtures.py",
        "authority_ceiling": "drift_observation_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }

    receipt_out = ROOT / "evidence" / "validation_receipt_drift_monitor_fixtures.json"
    receipt_out.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    for r in results:
        status = r["result"]
        print(f"[{status}] {r['name']} — {r['note']}")
        if status == "FAIL":
            print(f"  drift events: expected={r['expected_drift_events']} actual={r['actual_drift_events']}")
            print(f"  new snapshots: expected={r['expected_new_snapshots']} actual={r['actual_new_snapshots']}")
            if r["stderr"]:
                print(f"  stderr: {r['stderr'][:200]}")

    if failed:
        print(f"\nSmoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1
    print(f"\nSmoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
