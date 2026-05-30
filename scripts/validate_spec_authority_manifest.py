#!/usr/bin/env python3
"""Validate a spec authority manifest against structural governance contracts.

Authority ceiling: spec_authority_manifest_structural_validation_only

Checks that the manifest correctly declares its access path and claim ceiling.
Does not verify that consuming repos use the manifest, or that referenced tables
contain correct USB spec content.

Rules (structural — cause FAIL):
  R1  manifest_id must be present and non-empty
  R2  export_type must be a canonical allowed value
  R3  authority_surface.table_path must point to an existing file (relative to repo root)
  R4  authority_surface.schema_path must point to an existing file (relative to repo root)
  R5  authority_surface.validator_path must point to an existing file (relative to repo root)
  R6  claim_ceiling.default must be spec_reference_only
  R7  claim_ceiling.cannot_establish must include firmware_behavior,
      project_specific_truth, and observed_device_behavior
  R8  authority_surface.usb_version_scope must use canonical version strings
  R9  evidence_state.semantic_pdf_verification must be false when claim_level is inferred

Non-goals:
  - Does not verify consuming repo uses this manifest.
  - Does not verify project evidence in the consuming repo.
  - Does not enforce consumer-side claim ceiling.
  - Does not parse or validate USB spec content.
  - Does not upgrade claim_level.
  - Does not validate the referenced table contents.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "exports" / "usb20_hub_class_request_manifest.yaml"

ALLOWED_EXPORT_TYPES = {"governed_table_reference"}
VALID_USB_SCOPES = {"usb20", "usb21", "usb32", "usb4"}
REQUIRED_CANNOT_ESTABLISH = {
    "firmware_behavior",
    "project_specific_truth",
    "observed_device_behavior",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def validate(manifest_path: Path) -> tuple[str, list[str], list[str]]:
    """Return (verdict, failures, advisories). verdict is PASS or FAIL."""
    failures: list[str] = []
    advisories: list[str] = []

    doc = _load_yaml(manifest_path)

    # R1: manifest_id present and non-empty
    manifest_id = doc.get("manifest_id", "")
    if not manifest_id or not str(manifest_id).strip():
        failures.append("R1: manifest_id is missing or empty")

    # R2: export_type is canonical
    export_type = doc.get("export_type", "")
    if export_type not in ALLOWED_EXPORT_TYPES:
        failures.append(
            f"R2: export_type '{export_type}' not in allowed set {sorted(ALLOWED_EXPORT_TYPES)}"
        )

    # R3–R5: authority_surface file paths must exist
    surface = doc.get("authority_surface", {})
    for rule, field in [("R3", "table_path"), ("R4", "schema_path"), ("R5", "validator_path")]:
        rel = surface.get(field, "")
        if not rel:
            failures.append(f"{rule}: authority_surface.{field} is missing")
        else:
            target = ROOT / rel
            if not target.exists():
                failures.append(f"{rule}: authority_surface.{field} = '{rel}' does not exist (resolved: {target})")

    # R6: claim_ceiling.default must be spec_reference_only
    ceiling = doc.get("claim_ceiling", {})
    if ceiling.get("default") != "spec_reference_only":
        failures.append(
            f"R6: claim_ceiling.default must be 'spec_reference_only', got '{ceiling.get('default')}'"
        )

    # R7: cannot_establish must include required terms
    cannot_establish = set(ceiling.get("cannot_establish") or [])
    missing_terms = REQUIRED_CANNOT_ESTABLISH - cannot_establish
    if missing_terms:
        failures.append(
            f"R7: claim_ceiling.cannot_establish is missing required terms: {sorted(missing_terms)}"
        )

    # R8: usb_version_scope canonical values
    scopes = surface.get("usb_version_scope") or []
    invalid_scopes = [s for s in scopes if s not in VALID_USB_SCOPES]
    if invalid_scopes:
        failures.append(
            f"R8: authority_surface.usb_version_scope contains invalid values: {invalid_scopes}"
        )
    if not scopes:
        failures.append("R8: authority_surface.usb_version_scope is empty or missing")

    # R9: semantic_pdf_verification must be false when claim_level is inferred
    ev = doc.get("evidence_state", {})
    if ev.get("claim_level") == "inferred" and ev.get("semantic_pdf_verification") is not False:
        failures.append(
            "R9: evidence_state.semantic_pdf_verification must be false when claim_level is inferred"
        )

    verdict = "FAIL" if failures else "PASS"
    return verdict, failures, advisories


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    verdict, failures, advisories = validate(args.manifest)

    for f in failures:
        print(f"[FAIL] {f}")
    for a in advisories:
        print(f"[ADVISORY] {a}")
    print(f"\nResult: {verdict} — {args.manifest.name}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        receipt = {
            "validator": "validate_spec_authority_manifest",
            "manifest": str(args.manifest),
            "verdict": verdict,
            "failures": failures,
            "advisories": advisories,
            "authority_ceiling": "spec_authority_manifest_structural_validation_only",
        }
        args.receipt_out.write_text(json.dumps(receipt, indent=2))

    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
