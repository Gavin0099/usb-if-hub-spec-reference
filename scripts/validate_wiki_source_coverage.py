#!/usr/bin/env python3
"""Validate wiki page source_refs authority coverage.

Authority ceiling: wiki_source_reference_coverage_only

Checks that verified/normative wiki claims are structurally bound to registered
sources with sufficient authority. Does not verify semantic correctness.

Rules (structural — cause FAIL):
  R1  verified/normative page must have non-empty source_refs
  R2  each source_ref must exist in source_registry
  R3  source_ref authority_level must satisfy page authority_required
  R4  verified/normative page must include at least one normative_official source_ref

Advisory findings (recorded, do not cause FAIL):
  A1  draft/provisional page has no source_refs

Non-goals:
  - Does not fetch USB-IF sources.
  - Does not parse PDF contents.
  - Does not compare wiki prose with source text.
  - Does not auto-add missing source_refs.
  - Does not change claim_level.
  - Does not validate section-level correctness.
  - Does not extract descriptor/request/status tables.
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
DEFAULT_SOURCE_REGISTRY = ROOT / "evidence" / "source_registry.yaml"
DEFAULT_WIKI_DIR = ROOT / "wiki"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
HIGH_CLAIM_LEVELS = {"normative", "verified"}
LOW_CLAIM_LEVELS = {"draft", "provisional"}
AUTHORITY_RANK = {
    "normative_official": 100,
    "official_validation": 80,
    "official_index": 50,
    "community_reference": 30,
    "archive_fallback": 20,
}
NORMATIVE_OFFICIAL = "normative_official"


def _load_source_registry(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    return {s["source_id"]: s["authority_level"] for s in doc.get("sources", [])}


def _parse_frontmatter(path: Path) -> dict[str, Any] | None:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    return yaml.safe_load(m.group(1)) if m else None


def _evaluate_page(
    path: Path,
    source_registry: dict[str, str],
) -> tuple[list[dict], list[dict]]:
    errors: list[dict[str, str]] = []
    advisories: list[dict[str, str]] = []
    name = path.name

    fm = _parse_frontmatter(path)
    if not fm or not isinstance(fm, dict):
        return errors, advisories

    claim_level = fm.get("claim_level", "")
    authority_required = fm.get("authority_required")
    source_refs = fm.get("source_refs") or []
    if not isinstance(source_refs, list):
        source_refs = []

    # R1: verified/normative must have source_refs
    if claim_level in HIGH_CLAIM_LEVELS and not source_refs:
        errors.append({
            "code": "HIGH_CLAIM_LEVEL_MISSING_SOURCE_REFS",
            "message": f"{name}: claim_level '{claim_level}' requires non-empty source_refs",
        })
        return errors, advisories  # no point checking further

    # A1: draft/provisional with no source_refs → advisory
    if claim_level in LOW_CLAIM_LEVELS and not source_refs:
        advisories.append({
            "code": "ADVISORY_LOW_CLAIM_WITHOUT_SOURCE_REFS",
            "message": f"{name}: claim_level '{claim_level}' has no source_refs — acceptable for drafts",
        })

    has_normative_official = False
    for ref in source_refs:
        ref_authority = source_registry.get(ref)

        # R2: source_ref must exist in registry
        if ref_authority is None:
            errors.append({
                "code": "SOURCE_REF_NOT_IN_REGISTRY",
                "message": f"{name}: source_ref '{ref}' not found in source_registry",
            })
            continue

        if ref_authority == NORMATIVE_OFFICIAL:
            has_normative_official = True

        # R3: source authority must satisfy authority_required
        if authority_required:
            req_rank = AUTHORITY_RANK.get(authority_required, 0)
            ref_rank = AUTHORITY_RANK.get(ref_authority, 0)
            if ref_rank < req_rank:
                errors.append({
                    "code": "SOURCE_REF_INSUFFICIENT_AUTHORITY",
                    "message": (
                        f"{name}: source_ref '{ref}' has authority_level '{ref_authority}' "
                        f"which does not satisfy authority_required '{authority_required}'"
                    ),
                })

    # R4: verified/normative must have at least one normative_official source_ref
    if claim_level in HIGH_CLAIM_LEVELS and source_refs and not has_normative_official:
        errors.append({
            "code": "HIGH_CLAIM_LEVEL_NO_NORMATIVE_OFFICIAL_SOURCE",
            "message": (
                f"{name}: claim_level '{claim_level}' requires at least one "
                "source_ref with authority_level 'normative_official'"
            ),
        })

    return errors, advisories


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-registry", default=str(DEFAULT_SOURCE_REGISTRY))
    parser.add_argument("--wiki-dir")
    parser.add_argument("--wiki-file")
    parser.add_argument("--receipt-out")
    args = parser.parse_args()

    def resolve(p: str, fallback: Path) -> Path:
        q = Path(p)
        return q if q.is_absolute() else ROOT / q

    registry_path = resolve(args.source_registry, DEFAULT_SOURCE_REGISTRY)
    source_registry = _load_source_registry(registry_path)

    if args.wiki_file:
        wf = Path(args.wiki_file)
        pages = [wf if wf.is_absolute() else ROOT / wf]
    else:
        wiki_dir = Path(args.wiki_dir) if args.wiki_dir else DEFAULT_WIKI_DIR
        wiki_dir = wiki_dir if wiki_dir.is_absolute() else ROOT / wiki_dir
        pages = sorted(p for p in wiki_dir.rglob("*.md") if p.name != "index.md")

    all_errors: list[dict] = []
    all_advisories: list[dict] = []
    checked_pages: list[str] = []

    for page in pages:
        checked_pages.append(page.name)
        errs, advs = _evaluate_page(page, source_registry)
        all_errors.extend(errs)
        all_advisories.extend(advs)

    passed = len(all_errors) == 0
    receipt = {
        "validator": "validate_wiki_source_coverage.py",
        "authority_ceiling": "wiki_source_reference_coverage_only",
        "does_not_fetch_network": True,
        "does_not_parse_pdf": True,
        "does_not_modify_wiki": True,
        "does_not_validate_semantic_correctness": True,
        "result": "PASS" if passed else "FAIL",
        "checked_pages": checked_pages,
        "error_count": len(all_errors),
        "advisory_count": len(all_advisories),
        "errors": all_errors,
        "advisories": all_advisories,
        "findings": all_errors + all_advisories,
    }

    if args.receipt_out:
        rp = Path(args.receipt_out)
        rp = rp if rp.is_absolute() else ROOT / rp
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    if not passed:
        print("Wiki source coverage validation FAILED")
        for e in all_errors:
            print(f"- [{e['code']}] {e['message']}")
    else:
        print("Wiki source coverage validation PASSED")
        print(f"- checked pages: {len(checked_pages)}")

    if all_advisories:
        print(f"- {len(all_advisories)} advisory finding(s):")
        for a in all_advisories:
            print(f"  ~ [{a['code']}] {a['message']}")

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
