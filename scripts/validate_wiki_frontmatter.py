#!/usr/bin/env python3
"""Validate wiki page YAML frontmatter against governance contracts.

Authority ceiling: wiki_frontmatter_structural_consistency_only
- Validates frontmatter fields; does not verify USB spec content accuracy.

Rules (structural — cause FAIL):
  R1  required fields present and non-empty: title, claim_level, status, last_reviewed
  R2  claim_level must be a valid value
  R3  status must be a valid value
  R4  authority_required (if present) must be a canonical authority level name
  R5  usb_versions (if present) must contain valid version strings

Advisory findings (recorded but do not cause FAIL):
  A1  claim_level == normative with status == draft
  A2  claim_level == verified with status == draft
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WIKI_DIR = ROOT / "wiki"
CONTRACT_DIR = ROOT / "contract"

VALID_CLAIM_LEVELS = {"normative", "verified", "inferred", "provisional", "draft", "index", "rejected"}
VALID_STATUSES = {"draft", "review_required", "complete", "deprecated"}
VALID_USB_VERSIONS = {"usb_2_0", "usb_2_1", "usb_3_2", "usb4"}
REQUIRED_FIELDS = {"title", "claim_level", "status", "last_reviewed"}
HIGH_CLAIM_LEVELS = {"normative", "verified"}

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def _load_authority_levels() -> set[str]:
    path = CONTRACT_DIR / "authority_levels.yaml"
    try:
        with path.open("r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)
        return set(doc.get("authority_levels", {}).keys())
    except Exception:
        return set()


def _parse_frontmatter(path: Path) -> dict[str, Any] | None:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    return yaml.safe_load(m.group(1)) or {}


def _validate_page(path: Path, authority_level_keys: set[str]) -> tuple[list[dict], list[dict]]:
    errors: list[dict[str, str]] = []
    advisories: list[dict[str, str]] = []
    name = path.name

    fm = _parse_frontmatter(path)
    if fm is None:
        errors.append({"code": "FRONTMATTER_MISSING", "message": f"{name}: no YAML frontmatter block found"})
        return errors, advisories

    if not isinstance(fm, dict):
        errors.append({"code": "FRONTMATTER_NOT_MAPPING", "message": f"{name}: frontmatter must be a YAML mapping"})
        return errors, advisories

    # R1: required fields
    for field in sorted(REQUIRED_FIELDS):
        val = fm.get(field)
        if val is None or (isinstance(val, str) and not val.strip()):
            errors.append({"code": "REQUIRED_FIELD_MISSING", "message": f"{name}: missing or empty required field '{field}'"})

    claim_level = fm.get("claim_level", "")
    status = fm.get("status", "")

    # R2: valid claim_level
    if claim_level and claim_level not in VALID_CLAIM_LEVELS:
        errors.append({"code": "CLAIM_LEVEL_INVALID", "message": f"{name}: claim_level '{claim_level}' is not valid (expected one of: {', '.join(sorted(VALID_CLAIM_LEVELS))})"})

    # R3: valid status
    if status and status not in VALID_STATUSES:
        errors.append({"code": "STATUS_INVALID", "message": f"{name}: status '{status}' is not valid (expected one of: {', '.join(sorted(VALID_STATUSES))})"})

    # R4: authority_required must be canonical
    authority_required = fm.get("authority_required")
    if authority_required is not None:
        if authority_required not in authority_level_keys:
            errors.append({"code": "AUTHORITY_REQUIRED_INVALID", "message": f"{name}: authority_required '{authority_required}' is not a canonical authority level (expected one of: {', '.join(sorted(authority_level_keys))})"})

    # R5: usb_versions must be valid
    usb_versions = fm.get("usb_versions")
    if usb_versions is not None:
        if not isinstance(usb_versions, list):
            errors.append({"code": "USB_VERSIONS_NOT_LIST", "message": f"{name}: usb_versions must be a list"})
        else:
            invalid = [v for v in usb_versions if v not in VALID_USB_VERSIONS]
            if invalid:
                errors.append({"code": "USB_VERSION_INVALID", "message": f"{name}: invalid usb_versions value(s): {', '.join(invalid)} (expected subset of: {', '.join(sorted(VALID_USB_VERSIONS))})"})

    # A1/A2: high claim_level with draft status (advisory)
    if claim_level in HIGH_CLAIM_LEVELS and status == "draft":
        advisories.append({"code": f"ADVISORY_{claim_level.upper()}_CLAIM_WITH_DRAFT_STATUS", "message": f"{name}: claim_level '{claim_level}' with status 'draft' — consider promoting status when claim is ready"})

    return errors, advisories


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help="wiki directory to validate (default: wiki/)")
    parser.add_argument("--file", help="single markdown file to validate")
    parser.add_argument("--receipt-out", help="write machine-readable receipt JSON")
    args = parser.parse_args()

    authority_level_keys = _load_authority_levels()

    if args.file:
        pages = [Path(args.file) if Path(args.file).is_absolute() else ROOT / args.file]
    else:
        wiki_dir = Path(args.dir) if args.dir else DEFAULT_WIKI_DIR
        wiki_dir = wiki_dir if wiki_dir.is_absolute() else ROOT / wiki_dir
        pages = sorted(p for p in wiki_dir.rglob("*.md") if p.name != "index.md")

    all_errors: list[dict] = []
    all_advisories: list[dict] = []
    checked_pages: list[str] = []

    for page in pages:
        errs, advs = _validate_page(page, authority_level_keys)
        all_errors.extend(errs)
        all_advisories.extend(advs)
        checked_pages.append(page.name)

    passed = len(all_errors) == 0
    receipt = {
        "validator": "validate_wiki_frontmatter.py",
        "authority_ceiling": "wiki_frontmatter_structural_consistency_only",
        "note": "PASS does not imply USB spec content accuracy. Validates frontmatter structure only.",
        "result": "PASS" if passed else "FAIL",
        "checked_pages": checked_pages,
        "error_count": len(all_errors),
        "advisory_count": len(all_advisories),
        "errors": all_errors,
        "advisories": all_advisories,
        "findings": all_errors + all_advisories,
    }

    if args.receipt_out:
        receipt_path = Path(args.receipt_out) if Path(args.receipt_out).is_absolute() else ROOT / args.receipt_out
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    if not passed:
        print("Wiki frontmatter validation FAILED")
        for e in all_errors:
            print(f"- [{e['code']}] {e['message']}")
    else:
        print("Wiki frontmatter validation PASSED")
        print(f"- checked pages: {len(checked_pages)}")

    if all_advisories:
        print(f"- {len(all_advisories)} advisory finding(s):")
        for a in all_advisories:
            print(f"  ~ [{a['code']}] {a['message']}")

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
