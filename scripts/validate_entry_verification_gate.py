#!/usr/bin/env python3
"""Validate entry-level verified promotion gate for governed table entries.

Authority ceiling: entry_level_verified_gate_only

This validator does not verify USB semantics. It only enforces that any
entry-level `claim_level: verified` promotion is backed by a narrow, explicit,
reviewable evidence packet.

Current Phase 8J scope:
  - only `tables/port_status_bit_matrix.yaml`
  - allowed entries: `wPortStatus.bit0.PORT_CONNECTION`, `wPortStatus.bit1.PORT_ENABLE`,
    `wPortChange.bit0.C_PORT_CONNECTION`, `wPortChange.bit1.C_PORT_ENABLE`,
    `wHubStatus.bit0.HUB_LOCAL_POWER`, `wHubStatus.bit1.HUB_OVER_CURRENT`
  - only `bit_name_and_position_only` verification scope
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "tables" / "port_status_bit_matrix.yaml"
DEFAULT_PACKET_DIR = ROOT / "evidence" / "entry_verification_packets"

ALLOWED_PILOT_ENTRIES = {
    "wPortStatus.bit0.PORT_CONNECTION",
    "wPortStatus.bit1.PORT_ENABLE",
    "wPortChange.bit0.C_PORT_CONNECTION",
    "wPortChange.bit1.C_PORT_ENABLE",
    "wHubStatus.bit0.HUB_LOCAL_POWER",
    "wHubStatus.bit1.HUB_OVER_CURRENT",
}
REQUIRED_SCOPE = "bit_name_and_position_only"
REQUIRED_EXCLUDES = {
    "timing behavior",
    "state transition behavior",
    "ClearPortFeature behavior",
    "full USB compliance",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _entry_id(entry: dict[str, Any]) -> str:
    return f"{entry.get('field')}.bit{entry.get('bit')}.{entry.get('name')}"


def _load_packets(packet_dir: Path) -> dict[str, dict[str, Any]]:
    packets: dict[str, dict[str, Any]] = {}
    if not packet_dir.exists():
        return packets
    for path in sorted(packet_dir.glob("*.yaml")):
        doc = _load_yaml(path)
        target = doc.get("target") or {}
        entry_id = target.get("entry_id")
        if isinstance(entry_id, str) and entry_id:
            packets[entry_id] = {"path": path, "doc": doc}
    return packets


def validate(matrix_path: Path, packet_dir: Path) -> tuple[str, list[dict[str, str]]]:
    errors: list[dict[str, str]] = []

    def fail(code: str, message: str) -> None:
        errors.append({"code": code, "message": message})

    matrix = _load_yaml(matrix_path)
    packets = _load_packets(packet_dir)

    if matrix.get("claim_level") == "verified":
        fail(
            "TABLE_LEVEL_VERIFIED_NOT_ALLOWED",
            "table-level claim_level=verified is not allowed; only entry-level promotion may be gated",
        )

    entries = matrix.get("entries") or []
    verified_entries = [entry for entry in entries if isinstance(entry, dict) and entry.get("claim_level") == "verified"]

    for idx, entry in enumerate(verified_entries):
        entry_id = _entry_id(entry)
        loc = f"verified_entry[{idx}] {entry_id}"

        if entry_id not in ALLOWED_PILOT_ENTRIES:
            fail(
                "VERIFIED_ENTRY_NOT_IN_PILOT_SCOPE",
                f"{loc}: only allowed pilot entries {sorted(ALLOWED_PILOT_ENTRIES)} may be promoted in Phase 8J",
            )
            continue

        packet_info = packets.get(entry_id)
        if packet_info is None:
            fail(
                "VERIFIED_ENTRY_MISSING_PACKET",
                f"{loc}: verified promotion requires a matching evidence packet in {packet_dir}",
            )
            continue

        packet = packet_info["doc"]
        result = packet.get("result") or {}
        scope = packet.get("verification_scope") or {}
        target = packet.get("target") or {}

        if target.get("surface") != "governed_table_entry" or target.get("table") != "port_status_bit_matrix":
            fail(
                "PACKET_TARGET_MISMATCH",
                f"{loc}: packet target must be governed_table_entry / port_status_bit_matrix",
            )

        if result.get("eligible_for_verified") is not True:
            fail(
                "PACKET_NOT_ELIGIBLE",
                f"{loc}: packet result.eligible_for_verified must be true before verified promotion",
            )

        if result.get("evidence_status") != "reviewed":
            fail(
                "PACKET_NOT_REVIEWED",
                f"{loc}: packet result.evidence_status must be 'reviewed' before verified promotion",
            )

        if scope.get("claim") != REQUIRED_SCOPE:
            fail(
                "PACKET_SCOPE_TOO_BROAD",
                f"{loc}: packet verification_scope.claim must be '{REQUIRED_SCOPE}'",
            )

        excludes = scope.get("excludes") or []
        if not isinstance(excludes, list):
            fail("PACKET_EXCLUDES_INVALID", f"{loc}: packet verification_scope.excludes must be a list")
        else:
            missing_excludes = sorted(REQUIRED_EXCLUDES - set(excludes))
            if missing_excludes:
                fail(
                    "PACKET_EXCLUDES_INCOMPLETE",
                    f"{loc}: packet excludes missing required boundaries: {missing_excludes}",
                )

    return ("FAIL" if errors else "PASS"), errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--packet-dir", type=Path, default=DEFAULT_PACKET_DIR)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    result, errors = validate(args.matrix, args.packet_dir)

    for e in errors:
        print(f"[FAIL] {e['code']}: {e['message']}")
    print(f"\nEntry verification gate validation {result}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        receipt = {
            "validator": "validate_entry_verification_gate",
            "matrix": str(args.matrix),
            "packet_dir": str(args.packet_dir),
            "result": result,
            "authority_ceiling": "entry_level_verified_gate_only",
            "errors": errors,
            "allowed_pilot_entries": sorted(ALLOWED_PILOT_ENTRIES),
        }
        args.receipt_out.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    sys.exit(0 if result == "PASS" else 1)


if __name__ == "__main__":
    main()
