#!/usr/bin/env python3
"""Validate USB2 entry verification gate coverage.

Authority ceiling: gate_coverage_consistency_only

This validator does not verify USB semantics. It checks that the entry-level
verification gate covers the intended USB2 matrices and that each matrix rule
matches the actual verified entry set.
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


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_USB2_TABLES = {
    "port_status_bit_matrix": ROOT / "tables" / "port_status_bit_matrix.yaml",
    "hub_descriptor_matrix": ROOT / "tables" / "hub_descriptor_matrix.yaml",
    "class_request_matrix": ROOT / "tables" / "class_request_matrix.yaml",
    "feature_selector_matrix": ROOT / "tables" / "feature_selector_matrix.yaml",
    "transaction_translator_matrix": ROOT / "tables" / "transaction_translator_matrix.yaml",
    "standard_device_request_matrix": ROOT / "tables" / "standard_device_request_matrix.yaml",
    "hub_interrupt_endpoint_matrix": ROOT / "tables" / "hub_interrupt_endpoint_matrix.yaml",
    "wHubCharacteristics_bit_matrix": ROOT / "tables" / "wHubCharacteristics_bit_matrix.yaml",
    "escalation_trigger_matrix": ROOT / "tables" / "escalation_trigger_matrix.yaml",
}


def _verified_entry_ids(matrix_path: Path) -> set[str]:
    doc = _load_yaml(matrix_path)
    entries = doc.get("entries") or []
    return {
        _entry_id(entry)
        for entry in entries
        if isinstance(entry, dict) and entry.get("claim_level") == "verified"
    }


def validate(packet_dir: Path = DEFAULT_PACKET_DIR) -> tuple[str, list[dict[str, Any]], dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    packets = _load_packets(packet_dir)

    default_keys: dict[str, str] = {}
    for matrix_path in DEFAULT_MATRICES:
        matrix = _load_yaml(matrix_path)
        key = _matrix_table_key(matrix_path, matrix)
        default_keys[key] = str(matrix_path.relative_to(ROOT))

    for table_key, matrix_path in EXPECTED_USB2_TABLES.items():
        if table_key not in default_keys:
            errors.append({
                "code": "DEFAULT_MATRIX_MISSING",
                "table": table_key,
                "message": f"{table_key}: not present in DEFAULT_MATRICES",
            })

        if table_key not in TABLE_RULES:
            errors.append({
                "code": "TABLE_RULE_MISSING",
                "table": table_key,
                "message": f"{table_key}: no TABLE_RULES entry",
            })
            continue

        verified = _verified_entry_ids(matrix_path)
        allowed = set(TABLE_RULES[table_key].get("allowed_entries") or [])

        extra_allowed = sorted(allowed - verified)
        missing_allowed = sorted(verified - allowed)

        if extra_allowed:
            errors.append({
                "code": "ALLOWLIST_HAS_NON_VERIFIED_ENTRIES",
                "table": table_key,
                "entries": extra_allowed,
                "message": f"{table_key}: allowlist includes entries not verified in matrix",
            })

        if missing_allowed:
            errors.append({
                "code": "VERIFIED_ENTRIES_NOT_GATED",
                "table": table_key,
                "entries": missing_allowed,
                "message": f"{table_key}: verified entries missing from gate allowlist",
            })

        missing_packets = sorted(entry_id for entry_id in verified if entry_id not in packets)
        if missing_packets:
            errors.append({
                "code": "VERIFIED_ENTRIES_MISSING_PACKETS",
                "table": table_key,
                "entries": missing_packets,
                "message": f"{table_key}: verified entries missing evidence packets",
            })

    unexpected_default = sorted(set(default_keys) - set(EXPECTED_USB2_TABLES))
    if unexpected_default:
        errors.append({
            "code": "DEFAULT_MATRIX_OUTSIDE_USB2_COVERAGE",
            "entries": unexpected_default,
            "message": "DEFAULT_MATRICES includes tables outside this USB2 gate coverage contract",
        })

    coverage = {
        "expected_table_count": len(EXPECTED_USB2_TABLES),
        "default_matrix_count": len(DEFAULT_MATRICES),
        "covered_tables": sorted(EXPECTED_USB2_TABLES),
        "verified_entry_count": sum(len(_verified_entry_ids(path)) for path in EXPECTED_USB2_TABLES.values()),
        "packet_dir": str(packet_dir),
    }
    return ("FAIL" if errors else "PASS"), errors, coverage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet-dir", type=Path, default=DEFAULT_PACKET_DIR)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    result, errors, coverage = validate(args.packet_dir)

    for error in errors:
        print(f"[FAIL] {error['code']}: {error['message']}")

    print(f"\nEntry gate coverage validation {result}")
    print(f"- covered tables: {coverage['expected_table_count']}")
    print(f"- verified entries covered: {coverage['verified_entry_count']}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "validator": "validate_entry_gate_coverage",
            "result": result,
            "authority_ceiling": "gate_coverage_consistency_only",
            "coverage": coverage,
            "errors": errors,
        }
        args.receipt_out.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())

