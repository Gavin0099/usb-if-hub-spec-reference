#!/usr/bin/env python3
"""Validate the repository's public specification-copy policy structure.

Authority ceiling: policy_structure_only.

This validator checks that the repository policy retains its explicit
prohibitions, permitted independently-authored forms, attribution boundary,
official source links, and licensing boundary. It does not assess legal
compliance, copyrightability, or similarity to an external specification.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POLICY = ROOT / "governance" / "PUBLIC_SPEC_COPY_POLICY.md"

REQUIRED_HEADINGS = [
    "# Public Spec Copy Policy",
    "## Boundary",
    "## MUST NOT",
    "## MAY",
    "## Attribution and authority",
    "## Licensing boundary",
    "## Review gate",
]

REQUIRED_MUST_NOT = [
    "reproduce full specification sections",
    "copy specification paragraphs verbatim",
    "reproduce original figures",
    "reproduce original diagrams",
    "reproduce large original tables",
    "reconstruct the complete specification sequentially",
]

REQUIRED_MAY = [
    "state protocol constants",
    "state field names",
    "state bit positions",
    "state request IDs",
    "summarize semantics in original wording",
    "create independently designed comparison tables",
    "cite specification section or table anchors",
    "explain engineering implications",
]

REQUIRED_AUTHORITY = [
    "independent, unofficial engineering reference",
    "not affiliated with or endorsed by USB",
    "authoritative source",
    "https://www.usb.org/document-library/usb-20-specification",
    "https://www.usb.org/document-library",
]

REQUIRED_LICENSING = [
    "Third-party standards and trademarks are not licensed",
    "blanket statement",
    "file-specific license",
]


def validate(policy_path: Path) -> tuple[str, list[dict[str, str]]]:
    errors: list[dict[str, str]] = []

    def fail(code: str, message: str) -> None:
        errors.append({"code": code, "message": message})

    if not policy_path.is_file():
        fail("POLICY_MISSING", f"policy file does not exist: {policy_path}")
        return "FAIL", errors

    text = policy_path.read_text(encoding="utf-8")
    lowered = text.casefold()
    normalized = re.sub(r"\s+", " ", lowered)

    for heading in REQUIRED_HEADINGS:
        if heading.casefold() not in lowered:
            fail("MISSING_REQUIRED_HEADING", f"missing required heading: {heading}")

    for phrase in REQUIRED_MUST_NOT:
        if phrase.casefold() not in normalized:
            fail("MISSING_MUST_NOT_RULE", f"missing MUST NOT rule: {phrase}")

    for phrase in REQUIRED_MAY:
        if phrase.casefold() not in normalized:
            fail("MISSING_MAY_RULE", f"missing MAY rule: {phrase}")

    for phrase in REQUIRED_AUTHORITY:
        if phrase.casefold() not in normalized:
            fail("MISSING_AUTHORITY_ANCHOR", f"missing authority/attribution anchor: {phrase}")

    for phrase in REQUIRED_LICENSING:
        if phrase.casefold() not in normalized:
            fail("MISSING_LICENSING_BOUNDARY", f"missing licensing boundary: {phrase}")

    return ("FAIL" if errors else "PASS"), errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    result, errors = validate(args.policy)
    for error in errors:
        print(f"[FAIL] {error['code']}: {error['message']}")
    print(f"\nPublic Spec copy policy validation {result}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        receipt = {
            "validator": "validate_public_spec_copy_policy",
            "policy": str(args.policy),
            "result": result,
            "authority_ceiling": "policy_structure_only",
            "legal_review": "NOT CLAIMED",
            "semantic_copy_detection": "NOT CLAIMED",
            "errors": errors,
        }
        args.receipt_out.write_text(
            json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
        )

    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
