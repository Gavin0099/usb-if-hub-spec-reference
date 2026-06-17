#!/usr/bin/env python3
"""Smoke test validate_usb2_claim_partition.py against deterministic fixtures."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

from validate_usb2_claim_partition import validate


VERIFIED_ENTRY = {
    "request_id": "usb20_get_status_hub",
    "claim_level": "verified",
    "evidence_status": "reviewed",
}
REVIEWED_BOUNDARY_ENTRY = {
    "field": "wPortStatus",
    "bit": 15,
    "name": "PORT_STATUS_HIGH_BIT_BOUNDARY",
    "status": "reserved",
    "claim_level": "inferred",
    "evidence_status": "reviewed",
    "evidence": {"reviewed_scope": "high_bit_boundary_placeholder_only"},
}
STRAY_REVIEWED_ENTRY = {
    "request_id": "usb20_stray_reviewed",
    "claim_level": "inferred",
    "evidence_status": "reviewed",
}
MISSING_ENTRY = {
    "request_id": "usb20_missing_claim",
}

CASES = [
    {
        "name": "valid_partition",
        "entries": [VERIFIED_ENTRY, REVIEWED_BOUNDARY_ENTRY],
        "table_rules": {"class_request_matrix": {"allowed_entries": {"usb20_get_status_hub"}}},
        "packets": ["usb20_get_status_hub"],
        "locked_reviewed_ids": {"wPortStatus.bit15.PORT_STATUS_HIGH_BIT_BOUNDARY"},
        "expected": {"tracked": 2, "verified": 1, "reviewed": 1, "inferred": 0, "missing": 0},
        "expected_exit": 0,
        "expected_error_codes": [],
    },
    {
        "name": "invalid_verified_not_gated",
        "entries": [VERIFIED_ENTRY, REVIEWED_BOUNDARY_ENTRY],
        "table_rules": {"class_request_matrix": {"allowed_entries": set()}},
        "packets": ["usb20_get_status_hub"],
        "locked_reviewed_ids": {"wPortStatus.bit15.PORT_STATUS_HIGH_BIT_BOUNDARY"},
        "expected": {"tracked": 2, "verified": 1, "reviewed": 1, "inferred": 0, "missing": 0},
        "expected_exit": 1,
        "expected_error_codes": ["VERIFIED_ENTRIES_NOT_GATED"],
    },
    {
        "name": "invalid_reviewed_not_locked",
        "entries": [VERIFIED_ENTRY, REVIEWED_BOUNDARY_ENTRY, STRAY_REVIEWED_ENTRY],
        "table_rules": {"class_request_matrix": {"allowed_entries": {"usb20_get_status_hub"}}},
        "packets": ["usb20_get_status_hub"],
        "locked_reviewed_ids": {"wPortStatus.bit15.PORT_STATUS_HIGH_BIT_BOUNDARY"},
        "expected": {"tracked": 3, "verified": 1, "reviewed": 2, "inferred": 0, "missing": 0},
        "expected_exit": 1,
        "expected_error_codes": ["REVIEWED_ENTRIES_NOT_BOUNDARY_LOCKED"],
    },
    {
        "name": "invalid_packet_non_verified",
        "entries": [VERIFIED_ENTRY, REVIEWED_BOUNDARY_ENTRY],
        "table_rules": {"class_request_matrix": {"allowed_entries": {"usb20_get_status_hub"}}},
        "packets": ["usb20_get_status_hub", "wPortStatus.bit15.PORT_STATUS_HIGH_BIT_BOUNDARY"],
        "locked_reviewed_ids": {"wPortStatus.bit15.PORT_STATUS_HIGH_BIT_BOUNDARY"},
        "expected": {"tracked": 2, "verified": 1, "reviewed": 1, "inferred": 0, "missing": 0},
        "expected_exit": 1,
        "expected_error_codes": ["PACKETS_TARGET_NON_VERIFIED_ENTRIES"],
    },
    {
        "name": "invalid_missing_bucket",
        "entries": [VERIFIED_ENTRY, REVIEWED_BOUNDARY_ENTRY, MISSING_ENTRY],
        "table_rules": {"class_request_matrix": {"allowed_entries": {"usb20_get_status_hub"}}},
        "packets": ["usb20_get_status_hub"],
        "locked_reviewed_ids": {"wPortStatus.bit15.PORT_STATUS_HIGH_BIT_BOUNDARY"},
        "expected": {"tracked": 3, "verified": 1, "reviewed": 1, "inferred": 0, "missing": 0},
        "expected_exit": 1,
        "expected_error_codes": ["MISSING_COUNT_MISMATCH"],
    },
]


def _write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def _run_case(case: dict[str, Any], root: Path) -> dict[str, Any]:
    case_dir = root / case["name"]
    matrix_path = case_dir / "matrix.yaml"
    packet_dir = case_dir / "packets"
    packet_dir.mkdir(parents=True, exist_ok=True)
    _write_yaml(matrix_path, {"matrix_id": "class_request_matrix", "entries": case["entries"]})

    for entry_id in case["packets"]:
        packet_name = f"{entry_id.replace('.', '_')}.yaml"
        _write_yaml(packet_dir / packet_name, {"target": {"entry_id": entry_id}})

    expected = case["expected"]
    result, errors, counts = validate(
        matrices=[matrix_path],
        table_rules=case["table_rules"],
        packet_dir=packet_dir,
        locked_reviewed_ids=case["locked_reviewed_ids"],
        expected_tracked=expected["tracked"],
        expected_verified=expected["verified"],
        expected_reviewed=expected["reviewed"],
        expected_inferred=expected["inferred"],
        expected_missing=expected["missing"],
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
    with tempfile.TemporaryDirectory(prefix="usb2-claim-partition-") as tmp:
        results = [_run_case(case, Path(tmp)) for case in CASES]

    failed = [result for result in results if result["result"] == "FAIL"]
    summary = {
        "validator": "validate_usb2_claim_partition.py",
        "smoke_runner": "smoke_validate_usb2_claim_partition_fixtures.py",
        "authority_ceiling": "usb2_claim_partition_consistency_only",
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
