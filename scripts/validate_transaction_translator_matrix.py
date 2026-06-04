#!/usr/bin/env python3
"""Validate USB 2.0 Transaction Translator reference matrix structure.

Authority ceiling: transaction_translator_reference_boundary_only

Structural checks only:
  R1 tt_id must be unique
  R2 category must be one of the tracked TT categories
  R3 required TT type, think-time, and request entries must be present
  R4 source_refs must exist in source_registry
  R5 claim_level=verified/normative is not allowed by this validator
  R6 TT request entries must point at existing class request IDs

Non-goals:
  - Does not fetch USB-IF sources.
  - Does not parse PDF contents.
  - Does not validate split-transaction timing or behavior.
  - Does not verify TT buffer selector field encodings.
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
DEFAULT_MATRIX = ROOT / "tables" / "transaction_translator_matrix.yaml"
DEFAULT_SOURCE_REGISTRY = ROOT / "evidence" / "source_registry.yaml"
DEFAULT_CLASS_REQUEST_MATRIX = ROOT / "tables" / "class_request_matrix.yaml"

VALID_CATEGORIES = {"tt_type", "tt_think_time", "tt_request", "split_transaction_boundary"}
VALID_CLAIM_LEVELS = {"inferred", "provisional", "draft", "rejected"}
VALID_EVIDENCE_STATUS = {"reviewed", "review_required", "unverified"}
EXPECTED_TT_TYPES = {"Single TT", "Multiple TT"}
EXPECTED_THINK_VALUES = {"00", "01", "10", "11"}
EXPECTED_TT_REQUESTS = {"CLEAR_TT_BUFFER", "RESET_TT", "GET_TT_STATE", "STOP_TT"}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _load_source_registry(path: Path) -> set[str]:
    doc = _load_yaml(path)
    return {s["source_id"] for s in doc.get("sources", [])}


def _load_class_request_ids(path: Path) -> set[str]:
    doc = _load_yaml(path)
    return {e["request_id"] for e in doc.get("entries", []) if isinstance(e, dict) and e.get("request_id")}


def validate(
    matrix_path: Path,
    registry_path: Path,
    class_request_matrix_path: Path,
) -> tuple[str, list[dict[str, str]], dict[str, Any]]:
    errors: list[dict[str, str]] = []

    def fail(code: str, message: str) -> None:
        errors.append({"code": code, "message": message})

    doc = _load_yaml(matrix_path)
    entries = doc.get("entries") or []
    known_sources = _load_source_registry(registry_path) if registry_path.exists() else set()
    class_request_ids = _load_class_request_ids(class_request_matrix_path)

    if doc.get("matrix_id") != "usb20_transaction_translator_matrix":
        fail("INVALID_MATRIX_ID", "matrix_id must be usb20_transaction_translator_matrix")
    if not isinstance(entries, list) or not entries:
        fail("MISSING_ENTRIES", "entries must be a non-empty list")
        entries = []

    seen_ids: set[str] = set()
    tt_types: set[str] = set()
    think_values: set[str] = set()
    tt_requests: set[str] = set()

    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            fail("ENTRY_NOT_MAPPING", f"entry[{i}] must be a mapping")
            continue

        loc = f"entry[{i}]"
        tt_id = entry.get("tt_id")
        category = entry.get("category")
        value = entry.get("value")
        name = entry.get("name")

        if not isinstance(tt_id, str) or not tt_id.strip():
            fail("MISSING_TT_ID", f"{loc}: tt_id is required")
        elif tt_id in seen_ids:
            fail("DUPLICATE_TT_ID", f"{loc}: duplicate tt_id '{tt_id}'")
        else:
            seen_ids.add(tt_id)

        if category not in VALID_CATEGORIES:
            fail("INVALID_CATEGORY", f"{loc}: category '{category}' is invalid")

        if category == "tt_type" and isinstance(name, str):
            tt_types.add(name)
        if category == "tt_think_time" and isinstance(value, str):
            think_values.add(value)
            if entry.get("related_field") != "wHubCharacteristics[6:5]":
                fail("THINK_TIME_FIELD_MISMATCH", f"{loc}: tt_think_time must use wHubCharacteristics[6:5]")
        if category == "tt_request" and isinstance(value, str):
            tt_requests.add(value)
            request_ref = entry.get("request_ref")
            if request_ref not in class_request_ids:
                fail("REQUEST_REF_NOT_FOUND", f"{loc}: request_ref '{request_ref}' not found in class request matrix")

        claim_level = entry.get("claim_level")
        if claim_level not in VALID_CLAIM_LEVELS:
            fail(
                "CLAIM_LEVEL_NOT_ALLOWED",
                f"{loc}: claim_level '{claim_level}' is not allowed for TT reference validation",
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

    missing_tt_types = sorted(EXPECTED_TT_TYPES - tt_types)
    missing_think_values = sorted(EXPECTED_THINK_VALUES - think_values)
    missing_tt_requests = sorted(EXPECTED_TT_REQUESTS - tt_requests)

    if missing_tt_types:
        fail("MISSING_TT_TYPES", f"missing TT type entries: {missing_tt_types}")
    if missing_think_values:
        fail("MISSING_THINK_TIME_VALUES", f"missing TT think-time entries: {missing_think_values}")
    if missing_tt_requests:
        fail("MISSING_TT_REQUESTS", f"missing TT request entries: {missing_tt_requests}")

    coverage = {
        "tt_type_count": len(tt_types & EXPECTED_TT_TYPES),
        "tt_think_time_count": len(think_values & EXPECTED_THINK_VALUES),
        "tt_request_count": len(tt_requests & EXPECTED_TT_REQUESTS),
        "expected_tt_type_count": len(EXPECTED_TT_TYPES),
        "expected_tt_think_time_count": len(EXPECTED_THINK_VALUES),
        "expected_tt_request_count": len(EXPECTED_TT_REQUESTS),
    }
    return ("FAIL" if errors else "PASS"), errors, coverage


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--source-registry", type=Path, default=DEFAULT_SOURCE_REGISTRY)
    parser.add_argument("--class-request-matrix", type=Path, default=DEFAULT_CLASS_REQUEST_MATRIX)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    result, errors, coverage = validate(args.matrix, args.source_registry, args.class_request_matrix)

    for e in errors:
        print(f"[FAIL] {e['code']}: {e['message']}")
    print(f"\nTransaction Translator matrix validation {result}")
    if result == "PASS":
        print(
            "- coverage: "
            f"tt_type {coverage['tt_type_count']}/{coverage['expected_tt_type_count']}, "
            f"think_time {coverage['tt_think_time_count']}/{coverage['expected_tt_think_time_count']}, "
            f"tt_request {coverage['tt_request_count']}/{coverage['expected_tt_request_count']}"
        )

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        receipt = {
            "validator": "validate_transaction_translator_matrix",
            "matrix": str(args.matrix),
            "result": result,
            "authority_ceiling": "transaction_translator_reference_boundary_only",
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
