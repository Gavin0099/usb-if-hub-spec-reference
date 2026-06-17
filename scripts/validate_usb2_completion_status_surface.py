#!/usr/bin/env python3
"""Validate USB2 completion guard visibility on verification status pages.

Authority ceiling: usb2_completion_status_visibility_only

This validator checks visible status-page wording only. It does not verify USB
semantics, update statistics, or promote entries.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ZH_PAGE = ROOT / "specs" / "verification_status.md"
DEFAULT_EN_PAGE = ROOT / "specs" / "en" / "verification_status.md"

REQUIRED_SHARED_LITERALS = [
    "USB2 Completion Surface Guard",
    "Entry verification gate",
    "Entry gate coverage",
    "Reviewed boundary lock",
    "Claim partition guard",
    "Completion surface aggregate",
    "151 = 105 verified + 46 reviewed + 0 inferred + 0 missing",
]

REQUIRED_ZH_LITERALS = [
    "USB2 LLM wiki",
    "reference surface",
    "claim partition",
    "firmware correctness",
    "host-stack behavior",
]

REQUIRED_EN_LITERALS = [
    "USB2 LLM wiki",
    "reference surface",
    "claim partition",
    "firmware correctness",
    "host-stack behavior",
]


def validate_text(text: str, required_literals: list[str], page_label: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for literal in required_literals:
        if literal not in text:
            errors.append({
                "code": "STATUS_REQUIRED_LITERAL_MISSING",
                "page": page_label,
                "literal": literal,
                "message": f"{page_label}: missing required literal: {literal}",
            })
    return errors


def validate(
    zh_page: Path = DEFAULT_ZH_PAGE,
    en_page: Path = DEFAULT_EN_PAGE,
) -> tuple[str, list[dict[str, Any]], dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    pages = {"zh": zh_page, "en": en_page}
    for label, path in pages.items():
        if not path.exists():
            errors.append({
                "code": "STATUS_PAGE_MISSING",
                "page": label,
                "message": f"{label}: status page missing: {path}",
            })
            continue
        text = path.read_text(encoding="utf-8")
        page_literals = REQUIRED_SHARED_LITERALS + (
            REQUIRED_ZH_LITERALS if label == "zh" else REQUIRED_EN_LITERALS
        )
        errors.extend(validate_text(text, page_literals, label))

    coverage = {
        "zh_page": str(zh_page),
        "en_page": str(en_page),
        "required_shared_literals": len(REQUIRED_SHARED_LITERALS),
        "required_language_literals": len(REQUIRED_ZH_LITERALS),
    }
    return ("FAIL" if errors else "PASS"), errors, coverage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zh-page", type=Path, default=DEFAULT_ZH_PAGE)
    parser.add_argument("--en-page", type=Path, default=DEFAULT_EN_PAGE)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    result, errors, coverage = validate(args.zh_page, args.en_page)

    for error in errors:
        print(f"[FAIL] {error['code']}: {error['message']}")

    print(f"\nUSB2 completion status surface validation {result}")
    print(f"- zh page: {coverage['zh_page']}")
    print(f"- en page: {coverage['en_page']}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "validator": "validate_usb2_completion_status_surface",
            "result": result,
            "authority_ceiling": "usb2_completion_status_visibility_only",
            "coverage": coverage,
            "errors": errors,
        }
        args.receipt_out.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
