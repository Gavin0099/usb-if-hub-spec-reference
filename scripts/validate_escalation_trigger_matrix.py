#!/usr/bin/env python3
"""Validate USB 2.0 standard escalation trigger matrix structure.

Authority ceiling: escalation_trigger_reference_boundary_only

Structural checks only:
  R1 trigger_id must be unique
  R2 trigger IDs E-01 through E-10 must be present
  R3 escalation_required must be true for every tracked trigger
  R4 related_surface must be one of the canonical USB2 reference surfaces
  R5 source_refs must exist in source_registry
  R6 claim_level=verified is allowed when authorized by an evidence packet; normative is not allowed

Non-goals:
  - Does not execute escalation in consuming repos.
  - Does not resolve project facts.
  - Does not fetch USB-IF sources.
  - Does not parse PDF contents.
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
DEFAULT_MATRIX = ROOT / "tables" / "escalation_trigger_matrix.yaml"
DEFAULT_SOURCE_REGISTRY = ROOT / "evidence" / "source_registry.yaml"

EXPECTED_TRIGGERS = {f"E-{i:02d}" for i in range(1, 11)}
VALID_RELATED_SURFACES = {
    "hub_descriptor",
    "hub_class_requests",
    "feature_selectors",
    "port_status_bits",
    "transaction_translator",
}
VALID_CLAIM_LEVELS = {"inferred", "provisional", "draft", "rejected", "verified"}
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

    if doc.get("matrix_id") != "usb20_escalation_trigger_matrix":
        fail("INVALID_MATRIX_ID", "matrix_id must be usb20_escalation_trigger_matrix")
    if not isinstance(entries, list) or not entries:
        fail("MISSING_ENTRIES", "entries must be a non-empty list")
        entries = []

    seen_ids: set[str] = set()
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            fail("ENTRY_NOT_MAPPING", f"entry[{i}] must be a mapping")
            continue

        loc = f"entry[{i}]"
        trigger_id = entry.get("trigger_id")

        if not isinstance(trigger_id, str) or not trigger_id.strip():
            fail("MISSING_TRIGGER_ID", f"{loc}: trigger_id is required")
        elif trigger_id in seen_ids:
            fail("DUPLICATE_TRIGGER_ID", f"{loc}: duplicate trigger_id '{trigger_id}'")
        else:
            seen_ids.add(trigger_id)

        if entry.get("escalation_required") is not True:
            fail("ESCALATION_REQUIRED_NOT_TRUE", f"{loc}: escalation_required must be true")

        related_surface = entry.get("related_surface")
        if related_surface not in VALID_RELATED_SURFACES:
            fail("INVALID_RELATED_SURFACE", f"{loc}: related_surface '{related_surface}' is invalid")

        claim_level = entry.get("claim_level")
        if claim_level not in VALID_CLAIM_LEVELS:
            fail(
                "CLAIM_LEVEL_NOT_ALLOWED",
                f"{loc}: claim_level '{claim_level}' is not allowed for escalation trigger validation",
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

    missing = sorted(EXPECTED_TRIGGERS - seen_ids)
    extra = sorted(seen_ids - EXPECTED_TRIGGERS)
    if missing:
        fail("MISSING_EXPECTED_TRIGGERS", f"missing trigger IDs: {missing}")
    if extra:
        fail("UNKNOWN_TRIGGER_IDS", f"unknown trigger IDs: {extra}")

    coverage = {
        "trigger_count": len(seen_ids & EXPECTED_TRIGGERS),
        "expected_trigger_count": len(EXPECTED_TRIGGERS),
        "coverage_status": "complete" if not missing and not extra else "review_required",
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
    print(f"\nEscalation trigger matrix validation {result}")
    if result == "PASS":
        print(f"- trigger coverage: {coverage['trigger_count']}/{coverage['expected_trigger_count']}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        receipt = {
            "validator": "validate_escalation_trigger_matrix",
            "matrix": str(args.matrix),
            "result": result,
            "authority_ceiling": "escalation_trigger_reference_boundary_only",
            "does_not_execute_consuming_repo_escalation": True,
            "does_not_resolve_project_facts": True,
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
