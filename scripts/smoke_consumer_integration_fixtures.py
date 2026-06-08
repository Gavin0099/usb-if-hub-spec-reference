#!/usr/bin/env python3
"""Smoke test the consumer integration contract against the real governed surface.

Authority ceiling: consumer_integration_contract_smoke_only.
Does not validate table semantics or claim levels.

Cases:
  manifest_integrity_pass
    Run validate_hub_governed_surface_manifest.py against the real manifest.
    Expect exit 0 and PASS in stdout.

  fingerprint_no_drift
    Run probe_table_fingerprint.py --mode check against the real manifest
    and real baseline. Expect exit 0, 12 tables checked, 0 drift.

  fingerprint_drift_detected
    Build a temp baseline copy with one hash corrupted
    (usb20_hub_descriptor_field_matrix). Run check. Expect exit 1,
    drift_count=1, and the drifted table id named in stdout.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VALIDATOR = ROOT / "scripts" / "validate_hub_governed_surface_manifest.py"
FINGERPRINT_PROBE = ROOT / "scripts" / "probe_table_fingerprint.py"
REAL_MANIFEST = ROOT / "exports" / "hub_governed_surface_manifest.yaml"
REAL_BASELINE = ROOT / "evidence" / "table_fingerprint_baseline.jsonl"

RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "consumer_integration_smoke"
RECEIPT_SUMMARY = ROOT / "evidence" / "validation_receipt_consumer_integration_smoke.json"

# Table id whose hash we corrupt in the drift case.
DRIFT_TARGET_ID = "usb20_hub_descriptor_field_matrix"
CORRUPT_HASH = "sha256:0000000000000000000000000000000000000000000000000000000000000000"


def _run(cmd: list[str]) -> tuple[int, str, str]:
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def _make_drifted_baseline(src: Path, target_id: str, corrupt_hash: str) -> Path:
    """Return a tmp-dir path containing a baseline JSONL with one corrupted hash."""
    tmpdir = Path(tempfile.mkdtemp())
    dest = tmpdir / "baseline.jsonl"
    lines = []
    for raw in src.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        entry = json.loads(raw)
        if entry.get("table_id") == target_id:
            entry["content_hash"] = corrupt_hash
        lines.append(json.dumps(entry, ensure_ascii=True))
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return dest


def case_manifest_integrity_pass() -> dict:
    name = "manifest_integrity_pass"
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPT_DIR / f"{name}.json"

    exit_code, stdout, stderr = _run([sys.executable, str(MANIFEST_VALIDATOR)])

    passed = exit_code == 0 and "PASS" in stdout
    result = {
        "name": name,
        "note": "validate_hub_governed_surface_manifest.py against real manifest",
        "expected_exit": 0,
        "actual_exit": exit_code,
        "expected_stdout_contains": "PASS",
        "stdout_contains_pass": "PASS" in stdout,
        "result": "PASS" if passed else "FAIL",
    }
    receipt_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    if not passed:
        result["stdout"] = stdout[:400]
        result["stderr"] = stderr[:200]
    return result


def case_fingerprint_no_drift() -> dict:
    name = "fingerprint_no_drift"
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPT_DIR / f"{name}.json"

    with tempfile.TemporaryDirectory() as tmpdir:
        receipt_out = Path(tmpdir) / "receipt.json"
        exit_code, stdout, stderr = _run([
            sys.executable, str(FINGERPRINT_PROBE),
            "--mode", "check",
            "--manifest", str(REAL_MANIFEST),
            "--baseline-in", str(REAL_BASELINE),
            "--receipt-out", str(receipt_out),
        ])

        probe_receipt: dict = {}
        if receipt_out.exists():
            probe_receipt = json.loads(receipt_out.read_text(encoding="utf-8"))

    tables_checked = probe_receipt.get("tables_checked", -1)
    drift_count = probe_receipt.get("drift_count", -1)
    error_count = probe_receipt.get("error_count", -1)

    passed = (
        exit_code == 0
        and tables_checked == 13
        and drift_count == 0
        and error_count == 0
    )
    result = {
        "name": name,
        "note": "fingerprint check on real manifest + real baseline; expect 13 tables, 0 drift",
        "expected_exit": 0,
        "actual_exit": exit_code,
        "expected_tables_checked": 13,
        "actual_tables_checked": tables_checked,
        "expected_drift_count": 0,
        "actual_drift_count": drift_count,
        "expected_error_count": 0,
        "actual_error_count": error_count,
        "result": "PASS" if passed else "FAIL",
    }
    receipt_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    if not passed:
        result["stdout"] = stdout[:400]
        result["stderr"] = stderr[:200]
    return result


def case_fingerprint_drift_detected() -> dict:
    name = "fingerprint_drift_detected"
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPT_DIR / f"{name}.json"

    drifted_baseline = _make_drifted_baseline(
        REAL_BASELINE, DRIFT_TARGET_ID, CORRUPT_HASH
    )

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            receipt_out = Path(tmpdir) / "receipt.json"
            exit_code, stdout, stderr = _run([
                sys.executable, str(FINGERPRINT_PROBE),
                "--mode", "check",
                "--manifest", str(REAL_MANIFEST),
                "--baseline-in", str(drifted_baseline),
                "--receipt-out", str(receipt_out),
            ])

            probe_receipt: dict = {}
            if receipt_out.exists():
                probe_receipt = json.loads(receipt_out.read_text(encoding="utf-8"))
    finally:
        # clean up temp baseline parent dir
        try:
            drifted_baseline.parent.rmdir()
        except Exception:
            pass

    drift_count = probe_receipt.get("drift_count", -1)
    findings = probe_receipt.get("findings", [])
    drifted_ids = [f.get("table_id") for f in findings]
    target_named = DRIFT_TARGET_ID in drifted_ids
    target_in_stdout = DRIFT_TARGET_ID in stdout

    passed = (
        exit_code == 1
        and drift_count == 1
        and target_named
        and target_in_stdout
    )
    result = {
        "name": name,
        "note": (
            f"fingerprint check with corrupted hash for {DRIFT_TARGET_ID}; "
            "expect exit 1, drift_count=1, table id named in stdout"
        ),
        "expected_exit": 1,
        "actual_exit": exit_code,
        "expected_drift_count": 1,
        "actual_drift_count": drift_count,
        "expected_drifted_table": DRIFT_TARGET_ID,
        "drifted_table_in_findings": target_named,
        "drifted_table_in_stdout": target_in_stdout,
        "result": "PASS" if passed else "FAIL",
    }
    receipt_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    if not passed:
        result["stdout"] = stdout[:400]
        result["stderr"] = stderr[:200]
        result["drifted_ids_found"] = drifted_ids
    return result


def main() -> int:
    cases = [
        case_manifest_integrity_pass,
        case_fingerprint_no_drift,
        case_fingerprint_drift_detected,
    ]
    results = [fn() for fn in cases]
    failed = [r for r in results if r["result"] == "FAIL"]

    summary = {
        "smoke_runner": "smoke_consumer_integration_fixtures.py",
        "authority_ceiling": "consumer_integration_contract_smoke_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }
    RECEIPT_SUMMARY.write_text(
        json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
    )

    for r in results:
        status = r["result"]
        print(f"[{status}] {r['name']} — {r['note']}")
        if status == "FAIL":
            for key in ("expected_exit", "actual_exit", "actual_drift_count",
                        "drifted_table_in_findings", "drifted_table_in_stdout",
                        "stdout", "stderr"):
                if key in r:
                    print(f"  {key}: {r[key]}")

    print()
    if failed:
        print(f"Consumer integration smoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1
    print(f"Consumer integration smoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
