#!/usr/bin/env python3
"""Smoke test probe_table_fingerprint.py against deterministic fixtures.

Cases:
  no_drift       baseline then check same tables, exit 0, drift_count=0
  hash_changed   pre-written stale baseline, table was modified, exit 1, drift_count=1
  baseline_fresh run baseline mode with no prior baseline, exit 0, 1 table fingerprinted
  compact_latest compact duplicate baseline entries, exit 0, 1 entry retained
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "scripts" / "probe_table_fingerprint.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "table_fingerprint"
RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "table_fingerprint_fixtures"

CASES = [
    {
        "name": "no_drift",
        "fixture_dir": "no_drift",
        "mode": "check",
        "setup": "baseline_then_check",
        "expected_exit": 0,
        "expected_drift_count": 0,
        "note": "same content as baseline, no drift",
    },
    {
        "name": "hash_changed",
        "fixture_dir": "hash_changed",
        "mode": "check",
        "setup": "use_fixture_baseline",
        "expected_exit": 1,
        "expected_drift_count": 1,
        "note": "table modified since baseline was recorded, drift detected",
    },
    {
        "name": "baseline_fresh",
        "fixture_dir": "baseline_fresh",
        "mode": "baseline",
        "setup": "fresh",
        "expected_exit": 0,
        "expected_tables_fingerprinted": 1,
        "note": "fresh baseline mode, 1 table fingerprinted",
    },
    {
        "name": "compact_latest",
        "fixture_dir": "no_drift",
        "mode": "compact",
        "setup": "baseline_twice_then_compact",
        "expected_exit": 0,
        "expected_input_entries": 2,
        "expected_entries_retained": 1,
        "expected_entries_removed": 1,
        "note": "duplicate baseline entries compacted to latest table_id entry",
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
    manifest_path = fdir / "manifest.yaml"

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        baseline_path = tmpdir_path / "baseline.jsonl"
        result_exit = -1
        stderr_text = ""

        if case["setup"] == "baseline_then_check":
            # Step 1: run baseline to record hashes.
            r1 = subprocess.run(
                [
                    sys.executable, str(PROBE),
                    "--mode", "baseline",
                    "--manifest", str(manifest_path),
                    "--baseline-out", str(baseline_path),
                ],
                capture_output=True, text=True,
            )
            if r1.returncode != 0:
                return {
                    "name": case["name"],
                    "result": "FAIL",
                    "note": case["note"],
                    "detail": f"baseline step failed: {r1.stderr[:200]}",
                    "expected_exit": case["expected_exit"],
                    "actual_exit": r1.returncode,
                }
            # Step 2: run check against same tables.
            r2 = subprocess.run(
                [
                    sys.executable, str(PROBE),
                    "--mode", "check",
                    "--manifest", str(manifest_path),
                    "--baseline-in", str(baseline_path),
                    "--receipt-out", str(receipt_path),
                ],
                capture_output=True, text=True,
            )
            result_exit = r2.returncode
            stderr_text = r2.stderr

        elif case["setup"] == "use_fixture_baseline":
            src = fdir / "baseline.jsonl"
            if src.exists():
                baseline_path.write_bytes(src.read_bytes())
            r = subprocess.run(
                [
                    sys.executable, str(PROBE),
                    "--mode", "check",
                    "--manifest", str(manifest_path),
                    "--baseline-in", str(baseline_path),
                    "--receipt-out", str(receipt_path),
                ],
                capture_output=True, text=True,
            )
            result_exit = r.returncode
            stderr_text = r.stderr

        elif case["setup"] == "fresh":
            r = subprocess.run(
                [
                    sys.executable, str(PROBE),
                    "--mode", "baseline",
                    "--manifest", str(manifest_path),
                    "--baseline-out", str(baseline_path),
                    "--receipt-out", str(receipt_path),
                ],
                capture_output=True, text=True,
            )
            result_exit = r.returncode
            stderr_text = r.stderr

        elif case["setup"] == "baseline_twice_then_compact":
            for _ in range(2):
                r_baseline = subprocess.run(
                    [
                        sys.executable, str(PROBE),
                        "--mode", "baseline",
                        "--manifest", str(manifest_path),
                        "--baseline-out", str(baseline_path),
                    ],
                    capture_output=True, text=True,
                )
                if r_baseline.returncode != 0:
                    return {
                        "name": case["name"],
                        "result": "FAIL",
                        "note": case["note"],
                        "detail": f"baseline step failed: {r_baseline.stderr[:200]}",
                        "expected_exit": case["expected_exit"],
                        "actual_exit": r_baseline.returncode,
                    }
            compacted_path = tmpdir_path / "baseline_compacted.jsonl"
            r = subprocess.run(
                [
                    sys.executable, str(PROBE),
                    "--mode", "compact",
                    "--baseline-in", str(baseline_path),
                    "--baseline-out", str(compacted_path),
                    "--receipt-out", str(receipt_path),
                ],
                capture_output=True, text=True,
            )
            result_exit = r.returncode
            stderr_text = r.stderr

    receipt = _parse_receipt(receipt_path)
    expected_exit = case["expected_exit"]
    exit_ok = result_exit == expected_exit

    mode = case["mode"]
    if mode == "check":
        expected_drift = case.get("expected_drift_count", 0)
        actual_drift = receipt.get("drift_count", -1)
        metric_ok = actual_drift == expected_drift
        detail = f"drift_count: expected={expected_drift} actual={actual_drift}"
    elif mode == "compact":
        expected_input = case.get("expected_input_entries", 0)
        expected_retained = case.get("expected_entries_retained", 0)
        expected_removed = case.get("expected_entries_removed", 0)
        actual_input = receipt.get("input_entries", -1)
        actual_retained = receipt.get("entries_retained", -1)
        actual_removed = receipt.get("entries_removed", -1)
        metric_ok = (
            actual_input == expected_input
            and actual_retained == expected_retained
            and actual_removed == expected_removed
        )
        detail = (
            "compact_entries: "
            f"input expected={expected_input} actual={actual_input}; "
            f"retained expected={expected_retained} actual={actual_retained}; "
            f"removed expected={expected_removed} actual={actual_removed}"
        )
    else:
        expected_fp = case.get("expected_tables_fingerprinted", 0)
        actual_fp = receipt.get("tables_fingerprinted", -1)
        metric_ok = actual_fp == expected_fp
        detail = f"tables_fingerprinted: expected={expected_fp} actual={actual_fp}"

    passed = exit_ok and metric_ok
    return {
        "name": case["name"],
        "mode": mode,
        "expected_exit": expected_exit,
        "actual_exit": result_exit,
        "metric_detail": detail,
        "result": "PASS" if passed else "FAIL",
        "receipt_path": str(receipt_path),
        "stderr": stderr_text,
        "note": case["note"],
    }


def main() -> int:
    results = [run_case(c) for c in CASES]
    failed = [r for r in results if r["result"] == "FAIL"]

    summary = {
        "probe": "probe_table_fingerprint.py",
        "smoke_runner": "smoke_probe_table_fingerprint_fixtures.py",
        "authority_ceiling": "table_content_fingerprint_drift_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }

    receipt_out = ROOT / "evidence" / "validation_receipt_probe_table_fingerprint_fixtures.json"
    receipt_out.write_text(
        json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
    )

    for r in results:
        status = r["result"]
        print(f"[{status}] {r['name']} ({r['mode']}) - {r['note']}")
        if status == "FAIL":
            print(f"  exit: expected={r['expected_exit']} actual={r['actual_exit']}")
            print(f"  {r['metric_detail']}")
            if r.get("stderr"):
                print(f"  stderr: {r['stderr'][:300]}")

    if failed:
        print(f"\nSmoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1
    print(f"\nSmoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
