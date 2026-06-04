#!/usr/bin/env python3
"""Validate USB 2.0 hub descriptor field matrix structure.

Authority ceiling: hub_descriptor_field_role_only

Structural checks only:
  R1 field_id must be unique
  R2 field_name must be one of the tracked USB 2.0 hub descriptor fields
  R3 offset must match the tracked field-role surface
  R4 source_refs must exist in source_registry
  R5 claim_level=verified/normative is not allowed by this validator
  R6 wHubCharacteristics must include the reviewed bit-group boundaries

Non-goals:
  - Does not fetch USB-IF sources.
  - Does not parse PDF contents.
  - Does not validate descriptor dump values.
  - Does not verify wHubCharacteristics bit-pattern semantics.
  - Does not upgrade claim_level.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "tables" / "hub_descriptor_matrix.yaml"
DEFAULT_SOURCE_REGISTRY = ROOT / "evidence" / "source_registry.yaml"

EXPECTED_FIELDS: dict[str, int | str] = {
    "bDescLength": 0,
    "bDescriptorType": 1,
    "bNbrPorts": 2,
    "wHubCharacteristics": 3,
    "bPwrOn2PwrGood": 5,
    "bHubContrCurrent": 6,
    "DeviceRemovable": 7,
    "PortPwrCtrlMask": "variable_after_DeviceRemovable",
}
EXPECTED_BIT_GROUPS = {"1:0", "2", "4:3", "6:5", "7", "15:8"}
VALID_CLAIM_LEVELS = {"inferred", "provisional", "draft", "rejected"}
VALID_EVIDENCE_STATUS = {"reviewed", "review_required", "unverified"}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _load_source_registry(path: Path) -> set[str]:
    doc = _load_yaml(path)
    return {s["source_id"] for s in doc.get("sources", [])}


def validate(matrix_path: Path, registry_path: Path) -> tuple[str, list[dict[str, str]], dict[str, Any]]:
    errors: list[dict[str, str]] = []

    def fail(code: str, message: str) -> None:
        errors.append({"code": code, "message": message})

    doc = _load_yaml(matrix_path)
    entries = doc.get("entries") or []
    known_sources = _load_source_registry(registry_path) if registry_path.exists() else set()

    if doc.get("matrix_id") != "usb20_hub_descriptor_field_matrix":
        fail("INVALID_MATRIX_ID", "matrix_id must be usb20_hub_descriptor_field_matrix")
    if not isinstance(entries, list) or not entries:
        fail("MISSING_ENTRIES", "entries must be a non-empty list")
        entries = []

    seen_ids: set[str] = set()
    seen_fields: set[str] = set()

    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            fail("ENTRY_NOT_MAPPING", f"entry[{i}] must be a mapping")
            continue

        loc = f"entry[{i}]"
        field_id = entry.get("field_id")
        field_name = entry.get("field_name")
        offset = entry.get("offset")

        if not isinstance(field_id, str) or not field_id.strip():
            fail("MISSING_FIELD_ID", f"{loc}: field_id is required")
        elif field_id in seen_ids:
            fail("DUPLICATE_FIELD_ID", f"{loc}: duplicate field_id '{field_id}'")
        else:
            seen_ids.add(field_id)

        if field_name not in EXPECTED_FIELDS:
            fail("UNKNOWN_FIELD_NAME", f"{loc}: field_name '{field_name}' is not tracked")
        else:
            seen_fields.add(field_name)
            expected_offset = EXPECTED_FIELDS[field_name]
            if offset != expected_offset:
                fail(
                    "OFFSET_MISMATCH",
                    f"{loc}: field_name '{field_name}' offset {offset!r} != expected {expected_offset!r}",
                )

        claim_level = entry.get("claim_level")
        if claim_level not in VALID_CLAIM_LEVELS:
            fail(
                "CLAIM_LEVEL_NOT_ALLOWED",
                f"{loc}: claim_level '{claim_level}' is not allowed for descriptor field-role validation",
            )

        evidence_status = entry.get("evidence_status")
        if evidence_status not in VALID_EVIDENCE_STATUS:
            fail("INVALID_EVIDENCE_STATUS", f"{loc}: evidence_status '{evidence_status}' is invalid")

        source_refs = entry.get("source_refs") or []
        if not isinstance(source_refs, list) or not source_refs:
            fail("MISSING_SOURCE_REFS", f"{loc}: source_refs must be a non-empty list")
            source_refs = []
        for ref in source_refs:
            if ref not in known_sources:
                fail("SOURCE_REF_NOT_IN_REGISTRY", f"{loc}: source_ref '{ref}' not found in source_registry")

        if field_name == "bDescriptorType" and entry.get("expected_value") != "0x29":
            fail("DESCRIPTOR_TYPE_BOUNDARY_MISMATCH", f"{loc}: bDescriptorType expected_value must be 0x29")

        if field_name == "wHubCharacteristics":
            bit_groups = entry.get("bit_groups") or []
            bits = {g.get("bits") for g in bit_groups if isinstance(g, dict)}
            missing = sorted(EXPECTED_BIT_GROUPS - bits)
            if missing:
                fail("MISSING_BIT_GROUPS", f"{loc}: missing wHubCharacteristics bit groups: {missing}")

    missing_fields = sorted(set(EXPECTED_FIELDS) - seen_fields)
    if missing_fields:
        fail("MISSING_DESCRIPTOR_FIELDS", f"missing descriptor field entries: {missing_fields}")

    coverage = {
        "tracked_field_count": len(seen_fields),
        "expected_field_count": len(EXPECTED_FIELDS),
        "missing_fields": missing_fields,
    }
    return ("FAIL" if errors else "PASS"), errors, coverage


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--source-registry", type=Path, default=DEFAULT_SOURCE_REGISTRY)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    result, errors, coverage = validate(args.matrix, args.source_registry)

    for e in errors:
        print(f"[FAIL] {e['code']}: {e['message']}")
    print(f"\nHub descriptor matrix validation {result}")
    if result == "PASS":
        print(f"- field coverage: {coverage['tracked_field_count']}/{coverage['expected_field_count']}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        receipt = {
            "validator": "validate_hub_descriptor_matrix",
            "matrix": str(args.matrix),
            "result": result,
            "authority_ceiling": "hub_descriptor_field_role_only",
            "does_not_fetch_network": True,
            "does_not_parse_pdf": True,
            "does_not_validate_usb_semantics": True,
            "errors": errors,
            "coverage": coverage,
        }
        args.receipt_out.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    sys.exit(0 if result == "PASS" else 1)


if __name__ == "__main__":
    main()
