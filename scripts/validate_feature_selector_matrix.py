#!/usr/bin/env python3
"""Validate USB hub feature selector matrix against governance contracts.

Authority ceiling: feature_selector_namespace_only

Checks structural invariants for feature selector entries.
Derives port selector coverage for namespace 0-22.
Does not verify USB semantic correctness or spec content.

Rules (structural — cause FAIL):
  R1  selector_id must be unique across all entries
  R2  selector_name must be non-empty
  R3  applies_to must be a canonical value
  R4  entries with applies_to=port must have selector_value in 0-22

Advisory findings (recorded but do not cause FAIL):
  A1  port selector namespace 0-22 is partially covered (missing values listed)

Non-goals:
  - Does not fetch USB-IF sources.
  - Does not parse PDF contents.
  - Does not validate SetFeature/ClearFeature behavior.
  - Does not verify port status bit relationships.
  - Does not validate feature selector side effects.
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
DEFAULT_MATRIX = ROOT / "tables" / "feature_selector_matrix.yaml"
DEFAULT_SOURCE_REGISTRY = ROOT / "evidence" / "source_registry.yaml"

VALID_APPLIES_TO = {"hub", "port", "reserved", "hub_and_port", "unknown"}
PORT_SELECTOR_RANGE = set(range(23))  # 0-22 inclusive


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _load_source_registry(path: Path) -> set[str]:
    doc = _load_yaml(path)
    return {s["source_id"] for s in doc.get("sources", [])}


def validate(matrix_path: Path, registry_path: Path) -> tuple[str, list[dict], list[dict], dict]:
    """Return (verdict, errors, advisories, coverage)."""
    errors: list[dict] = []
    advisories: list[dict] = []

    def fail(code: str, msg: str) -> None:
        errors.append({"code": code, "message": msg})

    def advisory(code: str, msg: str) -> None:
        advisories.append({"code": code, "message": msg})

    doc = _load_yaml(matrix_path)
    known_sources = _load_source_registry(registry_path) if registry_path.exists() else set()

    entries = doc.get("entries") or []

    seen_ids: set[str] = set()
    covered_port_values: set[int] = set()

    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            continue

        loc = f"entry[{i}]"
        sid = entry.get("selector_id", "")

        # R1: selector_id unique
        if not sid:
            fail("DUPLICATE_SELECTOR_ID", f"{loc}: selector_id is missing or empty")
        elif sid in seen_ids:
            fail("DUPLICATE_SELECTOR_ID", f"{loc}: selector_id '{sid}' is duplicated")
        else:
            seen_ids.add(sid)

        # R2: selector_name non-empty
        name = entry.get("selector_name", "")
        if not isinstance(name, str) or not name.strip():
            fail("EMPTY_SELECTOR_NAME", f"{loc} ({sid!r}): selector_name is missing or empty")

        # R3: applies_to canonical
        applies_to = entry.get("applies_to")
        if applies_to not in VALID_APPLIES_TO:
            fail(
                "INVALID_APPLIES_TO",
                f"{loc} ({sid!r}): applies_to '{applies_to}' is not a valid value "
                f"(must be one of {sorted(VALID_APPLIES_TO)})",
            )

        # R4: port entries must have selector_value in 0-22
        val = entry.get("selector_value")
        if applies_to == "port":
            if not isinstance(val, int) or val < 0 or val > 22:
                fail(
                    "PORT_SELECTOR_OUT_OF_RANGE",
                    f"{loc} ({sid!r}): applies_to=port but selector_value={val!r} is not in 0-22",
                )
            else:
                covered_port_values.add(val)

        # Track reserved entries that fill namespace gaps
        if applies_to == "reserved" and isinstance(val, int) and 0 <= val <= 22:
            covered_port_values.add(val)

    # A1: port selector namespace coverage
    missing_port_values = sorted(PORT_SELECTOR_RANGE - covered_port_values)
    coverage_status = "complete" if not missing_port_values else "partial"

    if missing_port_values:
        advisory(
            "ADVISORY_PARTIAL_PORT_COVERAGE",
            f"port selector namespace 0-22 is partially covered; "
            f"missing values: {missing_port_values}",
        )

    coverage = {
        "port_selector_count_covered": len(covered_port_values & PORT_SELECTOR_RANGE),
        "port_selector_values_covered": sorted(covered_port_values & PORT_SELECTOR_RANGE),
        "port_selector_values_missing": missing_port_values,
        "coverage_status": coverage_status,
    }

    verdict = "FAIL" if errors else "PASS"
    return verdict, errors, advisories, coverage


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--source-registry", type=Path, default=DEFAULT_SOURCE_REGISTRY)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    verdict, errors, advisories, coverage = validate(args.matrix, args.source_registry)

    for e in errors:
        print(f"[FAIL] {e['code']}: {e['message']}")
    for a in advisories:
        print(f"[ADVISORY] {a['code']}: {a['message']}")

    print(f"\nFeature selector matrix validation {verdict}")
    if verdict == "PASS":
        print(f"- port coverage: {coverage['port_selector_count_covered']}/23")
        print(f"- coverage_status: {coverage['coverage_status']}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        receipt = {
            "validator": "validate_feature_selector_matrix",
            "matrix": str(args.matrix),
            "result": verdict,
            "authority_ceiling": "feature_selector_namespace_only",
            "errors": errors,
            "advisories": advisories,
            "coverage": coverage,
        }
        args.receipt_out.write_text(json.dumps(receipt, indent=2) + "\n")

    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
