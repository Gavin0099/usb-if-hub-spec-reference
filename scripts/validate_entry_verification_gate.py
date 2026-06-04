#!/usr/bin/env python3
"""Validate entry-level verified promotion gate for governed table entries.

Authority ceiling: entry_level_verified_gate_only

This validator does not verify USB semantics. It only enforces that any
entry-level `claim_level: verified` promotion is backed by a narrow, explicit,
reviewable evidence packet.

Current scope:
  - `tables/port_status_bit_matrix.yaml`
    - allowed entries: the eight promoted hub/port status-change bit entries
    - required scope: `bit_name_and_position_only`
  - `tables/hub_descriptor_matrix.yaml`
    - allowed entries: the eight tracked USB 2.0 hub descriptor field entries
    - required scope: `descriptor_field_identity_only`
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRICES = [
    ROOT / "tables" / "port_status_bit_matrix.yaml",
    ROOT / "tables" / "hub_descriptor_matrix.yaml",
]
DEFAULT_PACKET_DIR = ROOT / "evidence" / "entry_verification_packets"

TABLE_RULES = {
    "port_status_bit_matrix": {
        "allowed_entries": {
            "wPortStatus.bit0.PORT_CONNECTION",
            "wPortStatus.bit1.PORT_ENABLE",
            "wPortChange.bit0.C_PORT_CONNECTION",
            "wPortChange.bit1.C_PORT_ENABLE",
            "wHubStatus.bit0.HUB_LOCAL_POWER",
            "wHubStatus.bit1.HUB_OVER_CURRENT",
            "wHubChange.bit0.C_HUB_LOCAL_POWER",
            "wHubChange.bit1.C_HUB_OVER_CURRENT",
        },
        "required_scope": "bit_name_and_position_only",
        "required_excludes": {
            "timing behavior",
            "state transition behavior",
            "ClearPortFeature behavior",
            "full USB compliance",
        },
    },
    "hub_descriptor_matrix": {
        "allowed_entries": {
            "usb20_hub_desc_bDescLength",
            "usb20_hub_desc_bDescriptorType",
            "usb20_hub_desc_bNbrPorts",
            "usb20_hub_desc_wHubCharacteristics",
            "usb20_hub_desc_bPwrOn2PwrGood",
            "usb20_hub_desc_bHubContrCurrent",
            "usb20_hub_desc_DeviceRemovable",
            "usb20_hub_desc_PortPwrCtrlMask",
        },
        "required_scope": "descriptor_field_identity_only",
        "required_excludes": {
            "descriptor dump validation",
            "device behavior",
            "board-level timing or current guarantee",
            "full USB compliance",
        },
    },
}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _entry_id(entry: dict[str, Any]) -> str:
    if "field_id" in entry:
        return str(entry.get("field_id"))
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


def _matrix_table_key(matrix_path: Path) -> str:
    return matrix_path.stem


def _validate_matrix(matrix_path: Path, packet_dir: Path, packets: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    def fail(code: str, message: str) -> None:
        errors.append({"code": code, "message": message})

    table_key = _matrix_table_key(matrix_path)
    rule = TABLE_RULES.get(table_key)
    if rule is None:
        fail("MATRIX_NOT_GATED", f"{matrix_path}: no entry verification gate rule is registered")
        return errors

    matrix = _load_yaml(matrix_path)

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

        if entry_id not in rule["allowed_entries"]:
            fail(
                "VERIFIED_ENTRY_NOT_IN_PILOT_SCOPE",
                f"{loc}: only registered entries {sorted(rule['allowed_entries'])} may be promoted for {table_key}",
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

        if target.get("surface") != "governed_table_entry" or target.get("table") != table_key:
            fail(
                "PACKET_TARGET_MISMATCH",
                f"{loc}: packet target must be governed_table_entry / {table_key}",
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

        if scope.get("claim") != rule["required_scope"]:
            fail(
                "PACKET_SCOPE_TOO_BROAD",
                f"{loc}: packet verification_scope.claim must be '{rule['required_scope']}'",
            )

        excludes = scope.get("excludes") or []
        if not isinstance(excludes, list):
            fail("PACKET_EXCLUDES_INVALID", f"{loc}: packet verification_scope.excludes must be a list")
        else:
            missing_excludes = sorted(rule["required_excludes"] - set(excludes))
            if missing_excludes:
                fail(
                    "PACKET_EXCLUDES_INCOMPLETE",
                    f"{loc}: packet excludes missing required boundaries: {missing_excludes}",
                )

    return errors


def validate(matrix_paths: list[Path], packet_dir: Path) -> tuple[str, list[dict[str, str]]]:
    packets = _load_packets(packet_dir)
    errors: list[dict[str, str]] = []
    for matrix_path in matrix_paths:
        errors.extend(_validate_matrix(matrix_path, packet_dir, packets))
    return ("FAIL" if errors else "PASS"), errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, action="append")
    parser.add_argument("--packet-dir", type=Path, default=DEFAULT_PACKET_DIR)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    matrix_paths = args.matrix if args.matrix else DEFAULT_MATRICES
    result, errors = validate(matrix_paths, args.packet_dir)

    for e in errors:
        print(f"[FAIL] {e['code']}: {e['message']}")
    print(f"\nEntry verification gate validation {result}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        receipt = {
            "validator": "validate_entry_verification_gate",
            "matrices": [str(p) for p in matrix_paths],
            "packet_dir": str(args.packet_dir),
            "result": result,
            "authority_ceiling": "entry_level_verified_gate_only",
            "errors": errors,
            "table_rules": {
                key: {
                    "allowed_entries": sorted(rule["allowed_entries"]),
                    "required_scope": rule["required_scope"],
                    "required_excludes": sorted(rule["required_excludes"]),
                }
                for key, rule in TABLE_RULES.items()
            },
        }
        args.receipt_out.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    sys.exit(0 if result == "PASS" else 1)


if __name__ == "__main__":
    main()
