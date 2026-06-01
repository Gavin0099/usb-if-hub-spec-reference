#!/usr/bin/env python3
"""Wiki / governed-table cross-reference consistency probe.

Authority ceiling: wiki_specs_governed_table_cross_reference_observation_only

Extracts a set of identifier names from a governed YAML table and checks
whether each name appears as a token in the corresponding specs wiki page.
Emits an observation-only receipt.

This is structural name coverage only — it does NOT:
  - verify USB spec semantic correctness
  - verify that prose descriptions are accurate
  - upgrade claim_level on any page or table
  - assert behavioral compliance

Rules:
  E1  table file must exist and be parseable
  E2  wiki page must exist and be readable

Advisory findings (do not cause FAIL — observation only):
  A1  table name not found as token in wiki page text

Exit code:
  0  always, unless E1/E2 hard error
  1  only on file read/parse error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]

GOVERNANCE_METADATA = {
    "time_bound": True,
    "observation_only": True,
    "does_not_change_claim_level": True,
}


def _load_table(path: Path, name_field: str) -> list[str]:
    """Return deduplicated list of name values from table entries."""
    with path.open("r", encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    entries = doc.get("entries", [])
    seen: set[str] = set()
    names: list[str] = []
    for e in entries:
        val = e.get(name_field)
        if val and str(val) not in seen:
            seen.add(str(val))
            names.append(str(val))
    return names


def _token_in_text(token: str, text: str) -> bool:
    """True if token appears as a whole word/identifier in text."""
    pattern = r"(?<![A-Za-z0-9_])" + re.escape(token) + r"(?![A-Za-z0-9_])"
    return bool(re.search(pattern, text))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cross-reference governed table names against wiki page content."
    )
    parser.add_argument("--table", required=True, help="Governed YAML table file")
    parser.add_argument(
        "--name-field", required=True,
        help="YAML field in each entry whose value is the identifier to check",
    )
    parser.add_argument("--page", required=True, help="Wiki/specs markdown page")
    parser.add_argument("--table-id", default="", help="Human-readable table id for receipt")
    parser.add_argument("--receipt-out", help="Write receipt JSON to this path")
    args = parser.parse_args()

    table_path = Path(args.table) if Path(args.table).is_absolute() else ROOT / args.table
    page_path = Path(args.page) if Path(args.page).is_absolute() else ROOT / args.page
    table_id = args.table_id or table_path.stem

    errors: list[dict] = []
    advisories: list[dict] = []
    names: list[str] = []
    page_text = ""

    # E1: load table
    if not table_path.exists():
        errors.append({"code": "E1_TABLE_NOT_FOUND", "message": f"table file not found: {table_path}"})
    else:
        try:
            names = _load_table(table_path, args.name_field)
        except Exception as exc:
            errors.append({"code": "E1_TABLE_PARSE_ERROR", "message": f"table parse error: {exc}"})

    # E2: load page
    if not page_path.exists():
        errors.append({"code": "E2_PAGE_NOT_FOUND", "message": f"wiki page not found: {page_path}"})
    else:
        try:
            page_text = page_path.read_text(encoding="utf-8")
        except Exception as exc:
            errors.append({"code": "E2_PAGE_READ_ERROR", "message": f"page read error: {exc}"})

    found: list[str] = []
    missing: list[str] = []

    if not errors:
        for name in names:
            if _token_in_text(name, page_text):
                found.append(name)
            else:
                missing.append(name)
                advisories.append({
                    "code": "A1_NAME_NOT_IN_PAGE",
                    "table_id": table_id,
                    "name": name,
                    "page": page_path.name,
                    "message": (
                        f"'{name}' from {table_id} ({args.name_field}) "
                        f"not found as token in {page_path.name}"
                    ),
                })

    has_error = len(errors) > 0
    coverage_pct = (
        round(100 * len(found) / len(names), 1) if names else 100.0
    )

    result = "ERROR" if has_error else "PASS"

    receipt: dict = {
        "probe": "probe_wiki_consistency.py",
        "authority_ceiling": "wiki_specs_governed_table_cross_reference_observation_only",
        "table_id": table_id,
        "table_path": str(table_path.relative_to(ROOT) if table_path.is_relative_to(ROOT) else table_path),
        "wiki_page": str(page_path.relative_to(ROOT) if page_path.is_relative_to(ROOT) else page_path),
        "name_field": args.name_field,
        "result": result,
        "total_names": len(names),
        "found_count": len(found),
        "missing_count": len(missing),
        "coverage_pct": coverage_pct,
        "advisory_count": len(advisories),
        "error_count": len(errors),
        "found": found,
        "missing": missing,
        "advisories": advisories,
        "errors": errors,
        **GOVERNANCE_METADATA,
    }

    if args.receipt_out:
        rp = Path(args.receipt_out) if Path(args.receipt_out).is_absolute() else ROOT / args.receipt_out
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    if has_error:
        print(f"Wiki consistency probe ERROR: {table_id}")
        for e in errors:
            print(f"  [{e['code']}] {e['message']}")
        return 1

    print(
        f"Wiki consistency probe PASS: {table_id} "
        f"({len(found)}/{len(names)} names found in {page_path.name}, "
        f"coverage {coverage_pct}%)"
    )
    if missing:
        print(f"  {len(missing)} advisory — names not found in page:")
        for m in missing:
            print(f"    ~ {m}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
