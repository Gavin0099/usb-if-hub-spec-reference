#!/usr/bin/env python3
"""Validate permanent reviewed USB2 boundary entries.

Authority ceiling: reviewed_boundary_lock_only

This validator does not verify USB semantics. It only enforces that entries
which are intentionally modeled as reviewed boundary surfaces remain
non-verified and do not gain entry-level verification packets.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PORT_MATRIX = ROOT / "tables" / "port_status_bit_matrix.yaml"
DEFAULT_WHC_MATRIX = ROOT / "tables" / "wHubCharacteristics_bit_matrix.yaml"
DEFAULT_PACKET_DIR = ROOT / "evidence" / "entry_verification_packets"

EXPECTED_PORT_REVIEWED_BOUNDARIES = 45
EXPECTED_PORT_HIGH_BIT_BOUNDARIES = 4
EXPECTED_PORT_RESERVED_BIT_BOUNDARIES = 41
EXPECTED_WHC_REVIEWED_BOUNDARIES = 1
EXPECTED_WHC_RESERVED_ID = "usb20_whc_reserved_high"
ALLOWED_PORT_REVIEWED_SCOPES = {
    "high_bit_boundary_placeholder_only",
    "reserved_bit_namespace_only",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _entry_id(entry: dict[str, Any]) -> str:
    if "id" in entry:
        return str(entry.get("id"))
    return f"{entry.get('field')}.bit{entry.get('bit')}.{entry.get('name')}"


def _load_packet_targets(packet_dir: Path) -> dict[str, Path]:
    targets: dict[str, Path] = {}
    if not packet_dir.exists():
        return targets
    for path in sorted(packet_dir.rglob("*.yaml")):
        doc = _load_yaml(path)
        target = doc.get("target") or {}
        entry_id = target.get("entry_id")
        if isinstance(entry_id, str) and entry_id:
            targets[entry_id] = path
    return targets


def _port_reviewed_boundaries(port_matrix: Path) -> list[dict[str, Any]]:
    doc = _load_yaml(port_matrix)
    entries = doc.get("entries") or []
    return [
        entry
        for entry in entries
        if isinstance(entry, dict)
        and (
            _reviewed_scope(entry) in ALLOWED_PORT_REVIEWED_SCOPES
            or (
                entry.get("claim_level") != "verified"
                and entry.get("evidence_status") == "reviewed"
            )
        )
    ]


def _reviewed_scope(entry: dict[str, Any]) -> str:
    evidence = entry.get("evidence") or {}
    scope = evidence.get("reviewed_scope")
    return str(scope) if scope is not None else ""


def _validate_port_boundaries(
    port_matrix: Path,
    packet_targets: dict[str, Path],
    expected_port_count: int,
    expected_high_bit_count: int,
    expected_reserved_bit_count: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    boundaries = _port_reviewed_boundaries(port_matrix)
    high_bit = [entry for entry in boundaries if _reviewed_scope(entry) == "high_bit_boundary_placeholder_only"]
    reserved_bit = [entry for entry in boundaries if _reviewed_scope(entry) == "reserved_bit_namespace_only"]

    if len(boundaries) != expected_port_count:
        errors.append({
            "code": "PORT_REVIEWED_BOUNDARY_COUNT_MISMATCH",
            "message": (
                "port_status_bit_matrix reviewed boundary count mismatch: "
                f"expected {expected_port_count}, actual {len(boundaries)}"
            ),
            "expected": expected_port_count,
            "actual": len(boundaries),
        })

    if len(high_bit) != expected_high_bit_count:
        errors.append({
            "code": "PORT_HIGH_BIT_BOUNDARY_COUNT_MISMATCH",
            "message": (
                "port_status_bit_matrix high-bit boundary count mismatch: "
                f"expected {expected_high_bit_count}, actual {len(high_bit)}"
            ),
            "expected": expected_high_bit_count,
            "actual": len(high_bit),
        })

    if len(reserved_bit) != expected_reserved_bit_count:
        errors.append({
            "code": "PORT_RESERVED_BIT_BOUNDARY_COUNT_MISMATCH",
            "message": (
                "port_status_bit_matrix reserved-bit boundary count mismatch: "
                f"expected {expected_reserved_bit_count}, actual {len(reserved_bit)}"
            ),
            "expected": expected_reserved_bit_count,
            "actual": len(reserved_bit),
        })

    for entry in boundaries:
        entry_id = _entry_id(entry)
        if entry.get("claim_level") == "verified":
            errors.append({
                "code": "REVIEWED_BOUNDARY_PROMOTED",
                "entry_id": entry_id,
                "message": f"{entry_id}: reviewed boundary must not be claim_level verified",
            })
        if entry.get("evidence_status") != "reviewed":
            errors.append({
                "code": "REVIEWED_BOUNDARY_STATUS_INVALID",
                "entry_id": entry_id,
                "message": f"{entry_id}: reviewed boundary evidence_status must remain reviewed",
            })
        if entry.get("status") != "reserved":
            errors.append({
                "code": "REVIEWED_BOUNDARY_NOT_RESERVED",
                "entry_id": entry_id,
                "message": f"{entry_id}: reviewed port boundary must remain status reserved",
            })
        scope = _reviewed_scope(entry)
        if scope not in ALLOWED_PORT_REVIEWED_SCOPES:
            errors.append({
                "code": "REVIEWED_BOUNDARY_SCOPE_INVALID",
                "entry_id": entry_id,
                "message": f"{entry_id}: reviewed_scope must be one of {sorted(ALLOWED_PORT_REVIEWED_SCOPES)}",
                "actual": scope,
            })
        if entry_id in packet_targets:
            errors.append({
                "code": "REVIEWED_BOUNDARY_HAS_PACKET",
                "entry_id": entry_id,
                "packet": str(packet_targets[entry_id]),
                "message": f"{entry_id}: reviewed boundary must not have an entry verification packet",
            })

    return errors, {
        "port_reviewed_boundaries": len(boundaries),
        "port_high_bit_boundaries": len(high_bit),
        "port_reserved_bit_boundaries": len(reserved_bit),
    }


def _validate_whc_boundary(
    whc_matrix: Path,
    packet_targets: dict[str, Path],
    expected_whc_count: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    doc = _load_yaml(whc_matrix)
    entries = doc.get("entries") or []
    boundaries = [
        entry
        for entry in entries
        if isinstance(entry, dict)
        and entry.get("id") == EXPECTED_WHC_RESERVED_ID
    ]

    if len(boundaries) != expected_whc_count:
        errors.append({
            "code": "WHC_REVIEWED_BOUNDARY_COUNT_MISMATCH",
            "message": (
                "wHubCharacteristics reviewed boundary count mismatch: "
                f"expected {expected_whc_count}, actual {len(boundaries)}"
            ),
            "expected": expected_whc_count,
            "actual": len(boundaries),
        })

    for entry in boundaries:
        entry_id = _entry_id(entry)
        if entry.get("claim_level") == "verified":
            errors.append({
                "code": "REVIEWED_BOUNDARY_PROMOTED",
                "entry_id": entry_id,
                "message": f"{entry_id}: reviewed boundary must not be claim_level verified",
            })
        if entry.get("evidence_status") != "reviewed":
            errors.append({
                "code": "WHC_REVIEWED_BOUNDARY_STATUS_INVALID",
                "entry_id": entry_id,
                "message": f"{entry_id}: evidence_status must remain reviewed",
            })
        if entry.get("semantic_group") != "reserved_boundary":
            errors.append({
                "code": "WHC_REVIEWED_BOUNDARY_GROUP_INVALID",
                "entry_id": entry_id,
                "message": f"{entry_id}: semantic_group must remain reserved_boundary",
            })
        if str(entry.get("bit_range")) != "15:8":
            errors.append({
                "code": "WHC_REVIEWED_BOUNDARY_RANGE_INVALID",
                "entry_id": entry_id,
                "message": f"{entry_id}: bit_range must remain 15:8",
            })
        if entry_id in packet_targets:
            errors.append({
                "code": "REVIEWED_BOUNDARY_HAS_PACKET",
                "entry_id": entry_id,
                "packet": str(packet_targets[entry_id]),
                "message": f"{entry_id}: reviewed boundary must not have an entry verification packet",
            })

    return errors, {"whc_reviewed_boundaries": len(boundaries)}


def validate(
    port_matrix: Path = DEFAULT_PORT_MATRIX,
    whc_matrix: Path = DEFAULT_WHC_MATRIX,
    packet_dir: Path = DEFAULT_PACKET_DIR,
    expected_port_count: int = EXPECTED_PORT_REVIEWED_BOUNDARIES,
    expected_high_bit_count: int = EXPECTED_PORT_HIGH_BIT_BOUNDARIES,
    expected_reserved_bit_count: int = EXPECTED_PORT_RESERVED_BIT_BOUNDARIES,
    expected_whc_count: int = EXPECTED_WHC_REVIEWED_BOUNDARIES,
) -> tuple[str, list[dict[str, Any]], dict[str, Any]]:
    packet_targets = _load_packet_targets(packet_dir)
    port_errors, port_counts = _validate_port_boundaries(
        port_matrix,
        packet_targets,
        expected_port_count,
        expected_high_bit_count,
        expected_reserved_bit_count,
    )
    whc_errors, whc_counts = _validate_whc_boundary(whc_matrix, packet_targets, expected_whc_count)
    errors = port_errors + whc_errors
    counts = {**port_counts, **whc_counts}
    counts["total_reviewed_boundaries"] = (
        counts["port_reviewed_boundaries"] + counts["whc_reviewed_boundaries"]
    )
    counts["packet_dir"] = str(packet_dir)
    return ("FAIL" if errors else "PASS"), errors, counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port-matrix", type=Path, default=DEFAULT_PORT_MATRIX)
    parser.add_argument("--whc-matrix", type=Path, default=DEFAULT_WHC_MATRIX)
    parser.add_argument("--packet-dir", type=Path, default=DEFAULT_PACKET_DIR)
    parser.add_argument("--expected-port-count", type=int, default=EXPECTED_PORT_REVIEWED_BOUNDARIES)
    parser.add_argument("--expected-high-bit-count", type=int, default=EXPECTED_PORT_HIGH_BIT_BOUNDARIES)
    parser.add_argument("--expected-reserved-bit-count", type=int, default=EXPECTED_PORT_RESERVED_BIT_BOUNDARIES)
    parser.add_argument("--expected-whc-count", type=int, default=EXPECTED_WHC_REVIEWED_BOUNDARIES)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    result, errors, counts = validate(
        port_matrix=args.port_matrix,
        whc_matrix=args.whc_matrix,
        packet_dir=args.packet_dir,
        expected_port_count=args.expected_port_count,
        expected_high_bit_count=args.expected_high_bit_count,
        expected_reserved_bit_count=args.expected_reserved_bit_count,
        expected_whc_count=args.expected_whc_count,
    )

    for error in errors:
        print(f"[FAIL] {error['code']}: {error['message']}")

    print(f"\nReviewed boundary lock validation {result}")
    print(f"- port status reviewed boundaries: {counts['port_reviewed_boundaries']}")
    print(f"- wHubCharacteristics reviewed boundaries: {counts['whc_reviewed_boundaries']}")
    print(f"- total locked boundaries: {counts['total_reviewed_boundaries']}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "validator": "validate_reviewed_boundary_lock",
            "result": result,
            "authority_ceiling": "reviewed_boundary_lock_only",
            "counts": counts,
            "errors": errors,
        }
        args.receipt_out.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
