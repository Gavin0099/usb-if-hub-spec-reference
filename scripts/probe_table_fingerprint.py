#!/usr/bin/env python3
"""Fingerprint baseline and drift check probe for governed tables.

Authority ceiling: table_content_fingerprint_drift_only

Two modes:
  --mode baseline  Compute content hashes for all governed tables and append
                   each entry to --baseline-out (JSONL). Emits a receipt.
  --mode check     Re-hash governed tables, compare to stored baseline entries,
                   and emit a drift receipt. Exit 1 if any table has drifted.

Non-goals:
  - Does not validate table semantics.
  - Does not modify table content.
  - Does not update claim levels.
  - Does not fetch remote sources.
  - Does not resolve drift events.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "exports" / "usb20_hub_class_request_manifest.yaml"
DEFAULT_BASELINE = ROOT / "evidence" / "table_fingerprint_baseline.jsonl"

GOVERNANCE_METADATA = {
    "time_bound": True,
    "observation_only": True,
    "does_not_change_claim_level": True,
}


def _utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _load_manifest(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    return doc.get("governed_tables", [])


def _load_baseline(path: Path) -> dict[str, dict]:
    """Return dict table_id → most-recent entry (last write wins)."""
    if not path.exists():
        return {}
    latest: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        entry = json.loads(line)
        tid = entry.get("table_id", "")
        if tid:
            latest[tid] = entry
    return latest


def _append_jsonl(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=True) + "\n")


def _resolve_table_path(table_entry: dict, manifest_path: Path) -> Path:
    """Resolve table path relative to ROOT, falling back to manifest directory."""
    raw = table_entry.get("path", "")
    p = Path(raw)
    if p.is_absolute():
        return p
    candidate = ROOT / p
    if candidate.exists():
        return candidate
    return manifest_path.parent / p


def run_baseline(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest)
    baseline_path = Path(args.baseline_out)
    receipt_path = Path(args.receipt_out) if args.receipt_out else None

    tables = _load_manifest(manifest_path)
    recorded_at = _utc_now_iso()
    entries: list[dict] = []
    errors: list[dict] = []

    for t in tables:
        tid = t.get("id") or t.get("table_id", "")
        tpath = _resolve_table_path(t, manifest_path)
        if not tpath.exists():
            errors.append({"table_id": tid, "path": str(tpath), "error": "FILE_NOT_FOUND"})
            continue
        content_hash = _sha256_file(tpath)
        rel = str(tpath.relative_to(ROOT)) if tpath.is_relative_to(ROOT) else str(tpath)
        entry = {
            "table_id": tid,
            "path": rel,
            "content_hash": content_hash,
            "recorded_at": recorded_at,
            **GOVERNANCE_METADATA,
        }
        _append_jsonl(baseline_path, entry)
        entries.append(entry)

    result = "PASS" if not errors else "PARTIAL"
    receipt: dict = {
        "probe": "probe_table_fingerprint.py",
        "authority_ceiling": "table_content_fingerprint_drift_only",
        "mode": "baseline",
        "result": result,
        "recorded_at": recorded_at,
        "tables_fingerprinted": len(entries),
        "entries": entries,
        "errors": errors,
        **GOVERNANCE_METADATA,
    }

    if receipt_path:
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(
            json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
        )

    print(f"Baseline recorded: {len(entries)} table(s) → {baseline_path}")
    for e in errors:
        print(f"  ERROR: {e['table_id']} → {e['error']}: {e['path']}")
    return 0 if not errors else 1


def run_check(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest)
    baseline_path = Path(args.baseline_in)
    receipt_path = Path(args.receipt_out) if args.receipt_out else None

    tables = _load_manifest(manifest_path)
    baseline = _load_baseline(baseline_path)
    checked_at = _utc_now_iso()
    findings: list[dict] = []
    errors: list[dict] = []

    for t in tables:
        tid = t.get("id") or t.get("table_id", "")
        tpath = _resolve_table_path(t, manifest_path)

        if not tpath.exists():
            errors.append({"table_id": tid, "path": str(tpath), "error": "FILE_NOT_FOUND"})
            continue

        if tid not in baseline:
            errors.append({"table_id": tid, "error": "NOT_IN_BASELINE"})
            continue

        current_hash = _sha256_file(tpath)
        prev = baseline[tid]
        baseline_hash = prev.get("content_hash")

        if current_hash != baseline_hash:
            rel = str(tpath.relative_to(ROOT)) if tpath.is_relative_to(ROOT) else str(tpath)
            findings.append({
                "table_id": tid,
                "path": rel,
                "impact": "drift_detected",
                "baseline_hash": baseline_hash,
                "current_hash": current_hash,
                "baseline_recorded_at": prev.get("recorded_at"),
                "checked_at": checked_at,
                "required_action": "review_required",
            })

    drift_count = len(findings)
    has_error = len(errors) > 0
    passed = drift_count == 0 and not has_error

    if drift_count > 0:
        result = "DRIFT_DETECTED"
    elif has_error:
        result = "ERROR"
    else:
        result = "PASS"

    receipt: dict = {
        "probe": "probe_table_fingerprint.py",
        "authority_ceiling": "table_content_fingerprint_drift_only",
        "mode": "check",
        "result": result,
        "checked_at": checked_at,
        "tables_checked": len(tables) - len(errors),
        "drift_count": drift_count,
        "error_count": len(errors),
        "findings": findings,
        "errors": errors,
        **GOVERNANCE_METADATA,
    }

    if receipt_path:
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(
            json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
        )

    if passed:
        print(f"Table fingerprint check PASSED: {receipt['tables_checked']} table(s), 0 drift")
    else:
        print(f"Table fingerprint check {result}: {drift_count} drift, {len(errors)} error(s)")
        for f in findings:
            print(f"  [drift] {f['table_id']}: {f['baseline_hash']} -> {f['current_hash']}")
        for e in errors:
            print(f"  [error] {e['table_id']}: {e['error']}")

    return 0 if passed else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fingerprint governed tables for drift detection."
    )
    parser.add_argument(
        "--mode", choices=["baseline", "check"], required=True,
        help="baseline: record hashes; check: compare to stored baseline",
    )
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST),
                        help="governed_tables manifest YAML")
    parser.add_argument("--baseline-out", default=str(DEFAULT_BASELINE),
                        help="(baseline mode) append fingerprint entries here (JSONL)")
    parser.add_argument("--baseline-in", default=str(DEFAULT_BASELINE),
                        help="(check mode) read fingerprint baseline from here (JSONL)")
    parser.add_argument("--receipt-out",
                        help="write run receipt JSON to this path")
    args = parser.parse_args()

    if args.mode == "baseline":
        return run_baseline(args)
    return run_check(args)


if __name__ == "__main__":
    sys.exit(main())
