#!/usr/bin/env python3
"""Validate USB2 governed entry claim partition.

Authority ceiling: usb2_claim_partition_consistency_only

This validator does not verify USB semantics. It only checks that the governed
USB2 entry surface is partitioned into the current admissible buckets:

- entry-level verified entries guarded by the verification gate and packets
- permanent reviewed boundary entries guarded by the boundary lock
- no inferred or missing entries
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from validate_entry_verification_gate import (
    DEFAULT_MATRICES,
    DEFAULT_PACKET_DIR,
    TABLE_RULES,
    _entry_id,
    _load_packets,
    _load_yaml,
    _matrix_table_key,
)
from validate_reviewed_boundary_lock import (
    ALLOWED_PORT_REVIEWED_SCOPES,
    DEFAULT_PORT_MATRIX,
    DEFAULT_WHC_MATRIX,
    EXPECTED_WHC_RESERVED_ID,
)


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TRACKED = 151
EXPECTED_VERIFIED = 105
EXPECTED_REVIEWED = 46
EXPECTED_INFERRED = 0
EXPECTED_MISSING = 0


def _reviewed_scope(entry: dict[str, Any]) -> str:
    evidence = entry.get("evidence") or {}
    scope = evidence.get("reviewed_scope")
    return str(scope) if scope is not None else ""


def _locked_reviewed_boundary_ids(
    port_matrix: Path = DEFAULT_PORT_MATRIX,
    whc_matrix: Path = DEFAULT_WHC_MATRIX,
) -> set[str]:
    locked: set[str] = set()
    port_doc = _load_yaml(port_matrix)
    for entry in port_doc.get("entries") or []:
        if isinstance(entry, dict) and _reviewed_scope(entry) in ALLOWED_PORT_REVIEWED_SCOPES:
            locked.add(_entry_id(entry))

    whc_doc = _load_yaml(whc_matrix)
    for entry in whc_doc.get("entries") or []:
        if isinstance(entry, dict) and entry.get("id") == EXPECTED_WHC_RESERVED_ID:
            locked.add(_entry_id(entry))

    return locked


def _collect_entries(matrices: list[Path]) -> dict[str, dict[str, Any]]:
    entries: dict[str, dict[str, Any]] = {}
    for matrix_path in matrices:
        matrix = _load_yaml(matrix_path)
        table_key = _matrix_table_key(matrix_path, matrix)
        for entry in matrix.get("entries") or []:
            if not isinstance(entry, dict):
                entry_id = f"{table_key}:<non-dict-entry>"
            else:
                entry_id = _entry_id(entry)
            entries[entry_id] = {
                "entry": entry,
                "table": table_key,
                "matrix": str(matrix_path),
            }
    return entries


def _partition(entries: dict[str, dict[str, Any]]) -> dict[str, set[str]]:
    buckets = {
        "verified": set(),
        "reviewed": set(),
        "inferred": set(),
        "missing": set(),
    }
    for entry_id, record in entries.items():
        entry = record["entry"]
        if not isinstance(entry, dict):
            buckets["missing"].add(entry_id)
            continue

        claim_level = entry.get("claim_level")
        evidence_status = entry.get("evidence_status")
        if claim_level == "verified":
            buckets["verified"].add(entry_id)
        elif evidence_status == "reviewed":
            buckets["reviewed"].add(entry_id)
        elif claim_level == "inferred":
            buckets["inferred"].add(entry_id)
        else:
            buckets["missing"].add(entry_id)
    return buckets


def _allowed_verified_ids(table_rules: dict[str, dict[str, Any]]) -> set[str]:
    allowed: set[str] = set()
    for rule in table_rules.values():
        allowed.update(rule.get("allowed_entries") or set())
    return allowed


def _packet_target_ids(packet_dir: Path) -> set[str]:
    return set(_load_packets(packet_dir))


def _add_count_error(
    errors: list[dict[str, Any]],
    code: str,
    label: str,
    expected: int,
    actual: int,
) -> None:
    if actual != expected:
        errors.append({
            "code": code,
            "message": f"{label} count mismatch: expected {expected}, actual {actual}",
            "expected": expected,
            "actual": actual,
        })


def validate(
    matrices: list[Path] | None = None,
    table_rules: dict[str, dict[str, Any]] | None = None,
    packet_dir: Path = DEFAULT_PACKET_DIR,
    locked_reviewed_ids: set[str] | None = None,
    expected_tracked: int = EXPECTED_TRACKED,
    expected_verified: int = EXPECTED_VERIFIED,
    expected_reviewed: int = EXPECTED_REVIEWED,
    expected_inferred: int = EXPECTED_INFERRED,
    expected_missing: int = EXPECTED_MISSING,
) -> tuple[str, list[dict[str, Any]], dict[str, Any]]:
    matrices = DEFAULT_MATRICES if matrices is None else matrices
    table_rules = TABLE_RULES if table_rules is None else table_rules
    locked_reviewed_ids = _locked_reviewed_boundary_ids() if locked_reviewed_ids is None else locked_reviewed_ids

    entries = _collect_entries(matrices)
    buckets = _partition(entries)
    verified_ids = buckets["verified"]
    reviewed_ids = buckets["reviewed"]
    inferred_ids = buckets["inferred"]
    missing_ids = buckets["missing"]
    allowed_verified = _allowed_verified_ids(table_rules)
    packet_targets = _packet_target_ids(packet_dir)

    errors: list[dict[str, Any]] = []
    _add_count_error(errors, "TRACKED_COUNT_MISMATCH", "tracked", expected_tracked, len(entries))
    _add_count_error(errors, "VERIFIED_COUNT_MISMATCH", "verified", expected_verified, len(verified_ids))
    _add_count_error(errors, "REVIEWED_COUNT_MISMATCH", "reviewed", expected_reviewed, len(reviewed_ids))
    _add_count_error(errors, "INFERRED_COUNT_MISMATCH", "inferred", expected_inferred, len(inferred_ids))
    _add_count_error(errors, "MISSING_COUNT_MISMATCH", "missing", expected_missing, len(missing_ids))

    verified_not_gated = sorted(verified_ids - allowed_verified)
    gated_not_verified = sorted(allowed_verified - verified_ids)
    if verified_not_gated:
        errors.append({
            "code": "VERIFIED_ENTRIES_NOT_GATED",
            "entries": verified_not_gated,
            "message": "verified entries exist outside the entry verification gate allowlist",
        })
    if gated_not_verified:
        errors.append({
            "code": "GATED_ENTRIES_NOT_VERIFIED",
            "entries": gated_not_verified,
            "message": "entry verification gate allowlist contains entries not currently verified",
        })

    reviewed_not_locked = sorted(reviewed_ids - locked_reviewed_ids)
    locked_not_reviewed = sorted(locked_reviewed_ids - reviewed_ids)
    if reviewed_not_locked:
        errors.append({
            "code": "REVIEWED_ENTRIES_NOT_BOUNDARY_LOCKED",
            "entries": reviewed_not_locked,
            "message": "reviewed entries exist outside the reviewed boundary lock set",
        })
    if locked_not_reviewed:
        errors.append({
            "code": "BOUNDARY_LOCK_ENTRIES_NOT_REVIEWED",
            "entries": locked_not_reviewed,
            "message": "reviewed boundary lock set contains entries not currently reviewed",
        })

    packet_not_verified = sorted(packet_targets - verified_ids)
    verified_without_packet = sorted(verified_ids - packet_targets)
    if packet_not_verified:
        errors.append({
            "code": "PACKETS_TARGET_NON_VERIFIED_ENTRIES",
            "entries": packet_not_verified,
            "message": "entry verification packets target entries outside the verified partition",
        })
    if verified_without_packet:
        errors.append({
            "code": "VERIFIED_ENTRIES_WITHOUT_PACKETS",
            "entries": verified_without_packet,
            "message": "verified entries are missing entry verification packets",
        })

    counts = {
        "tracked": len(entries),
        "verified": len(verified_ids),
        "reviewed": len(reviewed_ids),
        "inferred": len(inferred_ids),
        "missing": len(missing_ids),
        "locked_reviewed_boundaries": len(locked_reviewed_ids),
        "entry_verification_packets": len(packet_targets),
    }
    return ("FAIL" if errors else "PASS"), errors, counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet-dir", type=Path, default=DEFAULT_PACKET_DIR)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    result, errors, counts = validate(packet_dir=args.packet_dir)

    for error in errors:
        print(f"[FAIL] {error['code']}: {error['message']}")

    print(f"\nUSB2 claim partition validation {result}")
    print(
        "- totals: "
        f"tracked={counts['tracked']}, verified={counts['verified']}, "
        f"reviewed={counts['reviewed']}, inferred={counts['inferred']}, "
        f"missing={counts['missing']}"
    )
    print(f"- locked reviewed boundaries: {counts['locked_reviewed_boundaries']}")
    print(f"- entry verification packets: {counts['entry_verification_packets']}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "validator": "validate_usb2_claim_partition",
            "result": result,
            "authority_ceiling": "usb2_claim_partition_consistency_only",
            "counts": counts,
            "errors": errors,
        }
        args.receipt_out.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
