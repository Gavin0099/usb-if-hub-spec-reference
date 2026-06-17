#!/usr/bin/env python3
"""Smoke test validate_reviewed_boundary_lock.py against deterministic fixtures."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

from validate_reviewed_boundary_lock import validate


PORT_VALID_ENTRIES = [
    {
        "field": "wPortStatus",
        "bit": 15,
        "name": "PORT_STATUS_HIGH_BIT_BOUNDARY",
        "status": "reserved",
        "claim_level": "inferred",
        "evidence_status": "reviewed",
        "evidence": {"reviewed_scope": "high_bit_boundary_placeholder_only"},
    },
    {
        "field": "wPortStatus",
        "bit": 5,
        "name": "PORT_STATUS_RESERVED_BIT5",
        "status": "reserved",
        "claim_level": "inferred",
        "evidence_status": "reviewed",
        "evidence": {"reviewed_scope": "reserved_bit_namespace_only"},
    },
]

WHC_VALID_ENTRIES = [
    {
        "id": "usb20_whc_reserved_high",
        "field": "wHubCharacteristics",
        "bit_range": "15:8",
        "semantic_group": "reserved_boundary",
        "claim_level": "inferred",
        "evidence_status": "reviewed",
    },
]

CASES = [
    {
        "name": "valid_minimal_boundaries",
        "port_entries": PORT_VALID_ENTRIES,
        "whc_entries": WHC_VALID_ENTRIES,
        "packets": [],
        "expected_exit": 0,
        "expected_error_codes": [],
    },
    {
        "name": "invalid_promoted_boundary",
        "port_entries": [
            {**PORT_VALID_ENTRIES[0], "claim_level": "verified"},
            PORT_VALID_ENTRIES[1],
        ],
        "whc_entries": WHC_VALID_ENTRIES,
        "packets": [],
        "expected_exit": 1,
        "expected_error_codes": ["REVIEWED_BOUNDARY_PROMOTED"],
    },
    {
        "name": "invalid_scope",
        "port_entries": [
            {**PORT_VALID_ENTRIES[0], "evidence": {"reviewed_scope": "semantic_verification"}},
            PORT_VALID_ENTRIES[1],
        ],
        "whc_entries": WHC_VALID_ENTRIES,
        "packets": [],
        "expected_exit": 1,
        "expected_error_codes": [
            "PORT_HIGH_BIT_BOUNDARY_COUNT_MISMATCH",
            "REVIEWED_BOUNDARY_SCOPE_INVALID",
        ],
    },
    {
        "name": "invalid_missing_whc_boundary",
        "port_entries": PORT_VALID_ENTRIES,
        "whc_entries": [],
        "packets": [],
        "expected_exit": 1,
        "expected_error_codes": ["WHC_REVIEWED_BOUNDARY_COUNT_MISMATCH"],
    },
    {
        "name": "invalid_boundary_packet",
        "port_entries": PORT_VALID_ENTRIES,
        "whc_entries": WHC_VALID_ENTRIES,
        "packets": ["wPortStatus.bit5.PORT_STATUS_RESERVED_BIT5"],
        "expected_exit": 1,
        "expected_error_codes": ["REVIEWED_BOUNDARY_HAS_PACKET"],
    },
]


def _write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def _run_case(case: dict[str, Any], root: Path) -> dict[str, Any]:
    case_dir = root / case["name"]
    port_matrix = case_dir / "port_status_bit_matrix.yaml"
    whc_matrix = case_dir / "wHubCharacteristics_bit_matrix.yaml"
    packet_dir = case_dir / "packets"
    packet_dir.mkdir(parents=True, exist_ok=True)

    _write_yaml(port_matrix, {"entries": case["port_entries"]})
    _write_yaml(whc_matrix, {"entries": case["whc_entries"]})

    for entry_id in case["packets"]:
        packet_name = f"{entry_id.replace('.', '_')}.yaml"
        _write_yaml(packet_dir / packet_name, {"target": {"entry_id": entry_id}})

    result, errors, counts = validate(
        port_matrix=port_matrix,
        whc_matrix=whc_matrix,
        packet_dir=packet_dir,
        expected_port_count=2,
        expected_high_bit_count=1,
        expected_reserved_bit_count=1,
        expected_whc_count=1,
    )
    actual_exit = 0 if result == "PASS" else 1
    actual_error_codes = [error["code"] for error in errors]
    passed = (
        actual_exit == case["expected_exit"]
        and set(case["expected_error_codes"]).issubset(set(actual_error_codes))
    )
    return {
        "name": case["name"],
        "expected_exit": case["expected_exit"],
        "actual_exit": actual_exit,
        "expected_error_codes": case["expected_error_codes"],
        "actual_error_codes": actual_error_codes,
        "result": "PASS" if passed else "FAIL",
        "counts": counts,
        "errors": errors,
    }


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="reviewed-boundary-lock-") as tmp:
        results = [_run_case(case, Path(tmp)) for case in CASES]

    failed = [result for result in results if result["result"] == "FAIL"]
    summary = {
        "validator": "validate_reviewed_boundary_lock.py",
        "smoke_runner": "smoke_validate_reviewed_boundary_lock_fixtures.py",
        "authority_ceiling": "reviewed_boundary_lock_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }

    for result in results:
        print(f"[{result['result']}] {result['name']}")
        if result["result"] == "FAIL":
            print(f"  exit: expected={result['expected_exit']} actual={result['actual_exit']}")
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
