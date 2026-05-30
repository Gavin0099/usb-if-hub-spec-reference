#!/usr/bin/env python3
"""Validate USB hub class request matrix against governance contracts.

Authority ceiling: class_request_matrix_structural_validation_only

Checks structural invariants for extraction table entries.
Does not verify USB semantic correctness or spec content.

Rules (structural — cause FAIL):
  R1  matrix_id and entries fields must be present
  R2  each entry must have required fields
  R3  usb_version_scope values must be valid
  R4  claim_level must be valid
  R5  verified/normative entry must have non-empty section_anchor
  R6  each source_ref must exist in source_registry
  R7  verified/normative entry must have ≥1 normative_official source_ref
  R8  request_id must be unique across all entries

Non-goals:
  - Does not fetch USB-IF sources.
  - Does not parse PDF contents.
  - Does not verify bmRequestType bit patterns.
  - Does not validate USB 3.2 / USB4 deltas.
  - Does not extract or compare spec sections.
  - Does not auto-populate missing entries.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "tables" / "class_request_matrix.yaml"
DEFAULT_SOURCE_REGISTRY = ROOT / "evidence" / "source_registry.yaml"

VALID_USB_SCOPES = {"usb20", "usb21", "usb32", "usb4"}
VALID_CLAIM_LEVELS = {"normative", "verified", "inferred", "provisional", "draft", "rejected"}
HIGH_CLAIM_LEVELS = {"normative", "verified"}
NORMATIVE_OFFICIAL = "normative_official"
VALID_APPLIES_TO = {"all_hubs", "hub_only", "port_only", "hub_with_tt_only", "reserved_or_unsupported"}
REQUIRED_ENTRY_FIELDS = {
    "request_id", "request_name", "usb_version_scope", "setup",
    "recipient", "topic", "source_refs", "authority_level",
    "claim_level", "evidence_status", "drift_status",
}
AUTHORITY_RANK = {
    "normative_official": 100,
    "official_validation": 80,
    "official_index": 50,
    "community_reference": 30,
    "archive_fallback": 20,
}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _load_source_registry(path: Path) -> dict[str, str]:
    doc = _load_yaml(path)
    return {s["source_id"]: s["authority_level"] for s in doc.get("sources", [])}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", default=str(DEFAULT_MATRIX))
    parser.add_argument("--source-registry", default=str(DEFAULT_SOURCE_REGISTRY))
    parser.add_argument("--receipt-out")
    args = parser.parse_args()

    def resolve(p: str, fallback: Path) -> Path:
        q = Path(p)
        return q if q.is_absolute() else ROOT / q

    matrix_path = resolve(args.matrix, DEFAULT_MATRIX)
    registry_path = resolve(args.source_registry, DEFAULT_SOURCE_REGISTRY)

    source_registry = _load_source_registry(registry_path)
    matrix = _load_yaml(matrix_path)

    errors: list[dict[str, str]] = []

    def add_error(code: str, msg: str) -> None:
        errors.append({"code": code, "message": msg})

    # R1: top-level structure
    if "matrix_id" not in matrix:
        add_error("MATRIX_ID_MISSING", "matrix is missing required field 'matrix_id'")
    if "entries" not in matrix:
        add_error("ENTRIES_FIELD_MISSING", "matrix is missing required field 'entries'")
        entries = []
    else:
        entries = matrix["entries"]
        if not isinstance(entries, list):
            add_error("ENTRIES_NOT_LIST", "'entries' must be a list")
            entries = []

    seen_ids: set[str] = set()
    for idx, entry in enumerate(entries):
        if not isinstance(entry, dict):
            add_error("ENTRY_NOT_MAPPING", f"entries[{idx}] must be a mapping")
            continue

        eid = entry.get("request_id", f"<missing@{idx}>")

        # R2: required fields
        missing = [f for f in sorted(REQUIRED_ENTRY_FIELDS) if f not in entry]
        if missing:
            add_error("REQUIRED_FIELD_MISSING", f"{eid}: missing required field(s): {', '.join(missing)}")

        # R3: valid usb_version_scope
        scopes = entry.get("usb_version_scope", [])
        if not isinstance(scopes, list) or not scopes:
            add_error("USB_VERSION_SCOPE_EMPTY", f"{eid}: usb_version_scope must be a non-empty list")
        else:
            invalid = [s for s in scopes if s not in VALID_USB_SCOPES]
            if invalid:
                add_error("USB_VERSION_SCOPE_INVALID", f"{eid}: invalid usb_version_scope: {', '.join(invalid)}")

        # R4: valid claim_level
        claim_level = entry.get("claim_level", "")
        if claim_level not in VALID_CLAIM_LEVELS:
            add_error("CLAIM_LEVEL_INVALID", f"{eid}: claim_level '{claim_level}' is not valid")

        source_refs = entry.get("source_refs") or []
        if not isinstance(source_refs, list):
            source_refs = []
        authority_level = entry.get("authority_level", "")
        section_anchor = entry.get("section_anchor")

        # R5: verified/normative must have section_anchor
        if claim_level in HIGH_CLAIM_LEVELS and not section_anchor:
            add_error(
                "HIGH_CLAIM_LEVEL_MISSING_SECTION_ANCHOR",
                f"{eid}: claim_level '{claim_level}' requires a non-empty section_anchor",
            )

        has_normative_official = False
        for ref in source_refs:
            ref_authority = source_registry.get(ref)

            # R6: source_ref must exist in registry
            if ref_authority is None:
                add_error("SOURCE_REF_NOT_IN_REGISTRY", f"{eid}: source_ref '{ref}' not found in source_registry")
                continue

            if ref_authority == NORMATIVE_OFFICIAL:
                has_normative_official = True

        # R7: verified/normative must have normative_official source
        if claim_level in HIGH_CLAIM_LEVELS and source_refs and not has_normative_official:
            add_error(
                "HIGH_CLAIM_LEVEL_NO_NORMATIVE_OFFICIAL_SOURCE",
                f"{eid}: claim_level '{claim_level}' requires ≥1 source_ref with authority_level 'normative_official'",
            )

        # R9: applies_to must be valid enum if present
        applies_to = entry.get("applies_to")
        if applies_to is not None and applies_to not in VALID_APPLIES_TO:
            add_error(
                "APPLIES_TO_INVALID",
                f"{eid}: applies_to '{applies_to}' is not a valid value "
                f"(expected one of: {', '.join(sorted(VALID_APPLIES_TO))})",
            )

        # R8: unique request_id
        if eid in seen_ids:
            add_error("DUPLICATE_REQUEST_ID", f"{eid}: request_id is duplicated")
        seen_ids.add(eid)

    passed = len(errors) == 0
    receipt = {
        "validator": "validate_class_request_matrix.py",
        "authority_ceiling": "class_request_matrix_structural_validation_only",
        "does_not_fetch_network": True,
        "does_not_parse_pdf": True,
        "does_not_validate_usb_semantics": True,
        "result": "PASS" if passed else "FAIL",
        "matrix_id": matrix.get("matrix_id", "<missing>"),
        "entry_count": len(entries),
        "error_count": len(errors),
        "errors": errors,
        "findings": errors,
    }

    if args.receipt_out:
        rp = Path(args.receipt_out)
        rp = rp if rp.is_absolute() else ROOT / rp
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    if not passed:
        print("Class request matrix validation FAILED")
        for e in errors:
            print(f"- [{e['code']}] {e['message']}")
        return 1

    print("Class request matrix validation PASSED")
    print(f"- matrix_id: {matrix.get('matrix_id', '<missing>')}")
    print(f"- entries: {len(entries)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
