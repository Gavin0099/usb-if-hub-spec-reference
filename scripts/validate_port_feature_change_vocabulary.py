#!/usr/bin/env python3
"""Validate PORT_/C_PORT_* vocabulary pages against the governed matrices.

Authority ceiling: vocabulary_cross_reference_only

This validator only checks naming consistency and page-term synchronization:
  - every scope term in source matrices appears on both vocabulary pages
  - vocabulary pages do not use unknown PORT_/C_PORT_* identifiers
  - zh/en vocabulary pages have consistent identifier sets

It does not validate request timing, state transitions, recovery policy, or
firmware behavior.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EN_PAGE = ROOT / "specs/en/port_feature_change_vocabulary.md"
DEFAULT_ZH_PAGE = ROOT / "specs/port_feature_change_vocabulary.md"
DEFAULT_PORT_STATUS_MATRIX = ROOT / "tables/port_status_bit_matrix.yaml"
DEFAULT_FEATURE_SELECTOR_MATRIX = ROOT / "tables/feature_selector_matrix.yaml"

TERM_RE = re.compile(r"(?<![A-Z0-9_])(?:C_)?PORT_[A-Z0-9_]+(?![A-Z0-9_])")


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    return doc


def _extract_matrix_terms() -> tuple[set[str], set[str], set[str]]:
    """Return (required_terms, allowed_terms, reserved_terms)."""
    port_matrix = _load_yaml(DEFAULT_PORT_STATUS_MATRIX)
    selector_matrix = _load_yaml(DEFAULT_FEATURE_SELECTOR_MATRIX)

    required_terms: set[str] = set()
    allowed_terms: set[str] = set()
    reserved_terms: set[str] = set()

    # Port status matrix contributes status and change terminology.
    for entry in port_matrix.get("entries", []):
        name = str(entry.get("name", "")).strip()
        if not name.startswith("PORT_") and not name.startswith("C_PORT_"):
            continue
        allowed_terms.add(name)

        # Required terms are defined status/change terms and change selectors
        # that are part of the current C_PORT_* family.
        if name.startswith("PORT_"):
            if entry.get("status") == "defined":
                required_terms.add(name)
            if "BOUNDARY" in name or name.startswith("PORT_STATUS_RESERVED_") or name.startswith("PORT_CHANGE_RESERVED_"):
                reserved_terms.add(name)
        elif name.startswith("C_PORT_"):
            required_terms.add(name)

    # Feature selector matrix must cover the same PORT_ and C_PORT_ family.
    for entry in selector_matrix.get("entries", []):
        name = str(entry.get("selector_name", "")).strip()
        if not name.startswith("PORT_") and not name.startswith("C_PORT_"):
            continue
        allowed_terms.add(name)
        required_terms.add(name)

    return required_terms, allowed_terms, reserved_terms


def _extract_page_terms(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return {m for m in TERM_RE.findall(text) if m.startswith("PORT_") or m.startswith("C_PORT_")}


def _fmt_terms(items: Iterable[str]) -> str:
    return ", ".join(sorted(items)) if items else "<none>"


def validate(en_page: Path | None = None, zh_page: Path | None = None) -> tuple[str, list[dict[str, str]], set[str], set[str]]:
    required_terms, allowed_terms, reserved_terms = _extract_matrix_terms()
    en_path = en_page or DEFAULT_EN_PAGE
    zh_path = zh_page or DEFAULT_ZH_PAGE
    en_terms = _extract_page_terms(en_path)
    zh_terms = _extract_page_terms(zh_path)

    errors: list[dict[str, str]] = []

    missing_en = required_terms - en_terms
    missing_zh = required_terms - zh_terms
    unknown_en = en_terms - allowed_terms
    unknown_zh = zh_terms - allowed_terms
    sync_delta = (en_terms ^ zh_terms) - reserved_terms

    def fail(code: str, message: str) -> None:
        errors.append({"code": code, "message": message})

    if missing_en:
        fail(
            "MISSING_REQUIRED_TERM_EN",
            f"English vocabulary page missing required terms: {_fmt_terms(sorted(missing_en))}",
        )
    if missing_zh:
        fail(
            "MISSING_REQUIRED_TERM_ZH",
            f"Chinese vocabulary page missing required terms: {_fmt_terms(sorted(missing_zh))}",
        )
    if unknown_en:
        fail(
            "UNKNOWN_TERM_EN",
            f"English vocabulary page includes unknown identifiers: {_fmt_terms(sorted(unknown_en))}",
        )
    if unknown_zh:
        fail(
            "UNKNOWN_TERM_ZH",
            f"Chinese vocabulary page includes unknown identifiers: {_fmt_terms(sorted(unknown_zh))}",
        )
    if sync_delta:
        fail(
            "LANGUAGE_SYNC_MISMATCH",
            f"Term drift between en/zh vocabulary pages (excluding reserved): {_fmt_terms(sorted(sync_delta))}",
        )

    result = "FAIL" if errors else "PASS"
    return result, errors, required_terms, allowed_terms


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--en-page", default=str(DEFAULT_EN_PAGE))
    parser.add_argument("--zh-page", default=str(DEFAULT_ZH_PAGE))
    parser.add_argument("--receipt-out")
    args = parser.parse_args()

    en_path = Path(args.en_page)
    zh_path = Path(args.zh_page)

    # quick hard checks for expected files
    if not en_path.exists():
        print(f"Vocabulary validation FAIL: missing English page {en_path}")
        sys.exit(1)
    if not zh_path.exists():
        print(f"Vocabulary validation FAIL: missing Chinese page {zh_path}")
        sys.exit(1)

    result, errors, required_terms, allowed_terms = validate(en_path, zh_path)

    if errors:
        print("Port feature/change vocabulary validation FAIL")
        for e in errors:
            print(f"- [{e['code']}] {e['message']}")
    else:
        print("Port feature/change vocabulary validation PASS")

    if args.receipt_out:
        receipt = {
            "validator": "validate_port_feature_change_vocabulary.py",
            "authority_ceiling": "vocabulary_cross_reference_only",
            "result": result,
            "en_page": str(en_path),
            "zh_page": str(zh_path),
            "required_terms": sorted(required_terms),
            "allowed_terms": sorted(allowed_terms),
            "errors": errors,
        }
        out = Path(args.receipt_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    sys.exit(0 if result == "PASS" else 1)


if __name__ == "__main__":
    main()
