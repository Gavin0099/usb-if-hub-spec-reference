#!/usr/bin/env python3
"""Validate USB 2.0 hub class request family coverage.

Authority ceiling: class_request_family_coverage_structural_only

Checks that coverage declaration is internally consistent and matches
the derived coverage from class_request_matrix.yaml entries.

Coverage unit: request_family (not entry count).

Rules (structural — cause FAIL):
  R1  expected_request_families must not be empty
  R2  derived covered_families (from matrix request_family field) must match
      declared covered_request_families
  R3  invariant: expected == covered + missing
  R4  coverage_status must be 'complete' iff missing is empty, 'partial' otherwise

Advisory findings:
  A1  extra families in matrix (covered not in expected list)

Non-goals:
  - Does not add GET_DESCRIPTOR / SET_DESCRIPTOR entries.
  - Does not parse PDF.
  - Does not upgrade claim_level.
  - Does not validate setup packet semantic correctness.
  - Does not extract feature selectors or status bits.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COVERAGE = ROOT / "evidence" / "class_request_coverage_usb20.json"
DEFAULT_MATRIX = ROOT / "tables" / "class_request_matrix.yaml"


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coverage", default=str(DEFAULT_COVERAGE))
    parser.add_argument("--matrix", default=str(DEFAULT_MATRIX))
    parser.add_argument("--receipt-out")
    args = parser.parse_args()

    def resolve(p: str, fallback: Path) -> Path:
        q = Path(p)
        return q if q.is_absolute() else ROOT / q

    coverage_path = resolve(args.coverage, DEFAULT_COVERAGE)
    matrix_path = resolve(args.matrix, DEFAULT_MATRIX)

    cov = _load_json(coverage_path)
    mat = _load_yaml(matrix_path)

    errors: list[dict[str, str]] = []
    advisories: list[dict[str, str]] = []

    def add_error(code: str, msg: str) -> None:
        errors.append({"code": code, "message": msg})

    def add_advisory(code: str, msg: str) -> None:
        advisories.append({"code": code, "message": msg})

    expected = cov.get("expected_request_families") or []
    declared_covered = cov.get("covered_request_families") or []
    declared_missing = cov.get("missing_request_families") or []
    coverage_status = cov.get("coverage_status", "")

    # R1: expected must not be empty
    if not expected:
        add_error("EXPECTED_FAMILIES_EMPTY",
                  "expected_request_families must not be empty")

    # Derive covered families from matrix request_family fields
    entries = mat.get("entries") or []
    derived_covered: set[str] = set()
    for entry in entries:
        if isinstance(entry, dict):
            rf = entry.get("request_family")
            if rf:
                derived_covered.add(rf)

    expected_set = set(expected)
    declared_covered_set = set(declared_covered)
    declared_missing_set = set(declared_missing)

    # R2: derived covered must match declared covered
    if derived_covered != declared_covered_set:
        only_in_derived = derived_covered - declared_covered_set
        only_in_declared = declared_covered_set - derived_covered
        parts = []
        if only_in_derived:
            parts.append(f"in matrix but not declared covered: {sorted(only_in_derived)}")
        if only_in_declared:
            parts.append(f"declared covered but not in matrix: {sorted(only_in_declared)}")
        add_error("COVERED_FAMILIES_MISMATCH",
                  f"declared covered_request_families does not match matrix: {'; '.join(parts)}")

    # R3: invariant expected == covered + missing
    computed_missing = expected_set - declared_covered_set
    if computed_missing != declared_missing_set:
        add_error(
            "MISSING_FAMILIES_INVARIANT_VIOLATED",
            f"expected == covered + missing violated: "
            f"computed missing={sorted(computed_missing)}, "
            f"declared missing={sorted(declared_missing_set)}",
        )

    # R4: coverage_status must be consistent
    is_complete = len(declared_missing_set) == 0 and len(computed_missing) == 0
    expected_status = "complete" if is_complete else "partial"
    if coverage_status != expected_status:
        add_error(
            "COVERAGE_STATUS_INCONSISTENT",
            f"coverage_status '{coverage_status}' is inconsistent: "
            f"expected '{expected_status}' based on missing list",
        )

    # A1: extra families in matrix (not in expected)
    extra = derived_covered - expected_set
    if extra:
        add_advisory(
            "ADVISORY_EXTRA_FAMILIES_IN_MATRIX",
            f"matrix contains request_family values not in expected list: "
            f"{sorted(extra)} — verify these are intentional",
        )

    passed = len(errors) == 0
    receipt = {
        "validator": "validate_class_request_coverage.py",
        "authority_ceiling": "class_request_family_coverage_structural_only",
        "does_not_validate_semantic_correctness": True,
        "result": "PASS" if passed else "FAIL",
        "coverage_id": cov.get("coverage_id", "<missing>"),
        "expected_count": len(expected),
        "covered_count": len(declared_covered_set),
        "missing_count": len(declared_missing_set),
        "derived_covered": sorted(derived_covered),
        "error_count": len(errors),
        "advisory_count": len(advisories),
        "errors": errors,
        "advisories": advisories,
        "findings": errors + advisories,
    }

    if args.receipt_out:
        rp = Path(args.receipt_out)
        rp = rp if rp.is_absolute() else ROOT / rp
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    if not passed:
        print("Class request coverage validation FAILED")
        for e in errors:
            print(f"- [{e['code']}] {e['message']}")
    else:
        print("Class request coverage validation PASSED")
        cid = cov.get("coverage_id", "?")
        print(f"- coverage_id: {cid}")
        print(f"- {len(expected)} expected / {len(declared_covered_set)} covered / {len(declared_missing_set)} missing")
        print(f"- coverage_status: {coverage_status}")
    if advisories:
        print(f"- {len(advisories)} advisory finding(s):")
        for a in advisories:
            print(f"  ~ [{a['code']}] {a['message']}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
