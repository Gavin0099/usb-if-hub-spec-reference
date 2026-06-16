#!/usr/bin/env python3
"""Validate USB2 topic cross-reference consistency for selected core pages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_PAGES = [
    "specs/feature_selectors.md",
    "specs/en/feature_selectors.md",
    "specs/port_status_bits.md",
    "specs/en/port_status_bits.md",
    "specs/port_feature_change_vocabulary.md",
    "specs/en/port_feature_change_vocabulary.md",
    "specs/hub_class_requests.md",
    "specs/en/hub_class_requests.md",
    "specs/hub_descriptor.md",
    "specs/en/hub_descriptor.md",
]

REQUIRED_LINKS = {
    "specs/feature_selectors.md": {
        "specs/port_status_bits.md",
        "specs/port_feature_change_vocabulary.md",
    },
    "specs/en/feature_selectors.md": {
        "specs/en/port_status_bits.md",
        "specs/en/port_feature_change_vocabulary.md",
    },
    "specs/port_status_bits.md": {
        "specs/feature_selectors.md",
        "specs/port_feature_change_vocabulary.md",
    },
    "specs/en/port_status_bits.md": {
        "specs/en/feature_selectors.md",
        "specs/en/port_feature_change_vocabulary.md",
    },
    "specs/port_feature_change_vocabulary.md": {
        "specs/feature_selectors.md",
        "specs/port_status_bits.md",
        "specs/hub_class_requests.md",
    },
    "specs/en/port_feature_change_vocabulary.md": {
        "specs/en/feature_selectors.md",
        "specs/en/port_status_bits.md",
        "specs/en/hub_class_requests.md",
    },
    "specs/hub_class_requests.md": {
        "specs/hub_descriptor.md",
        "specs/usb2.md",
    },
    "specs/en/hub_class_requests.md": {
        "specs/en/hub_descriptor.md",
        "specs/en/usb2.md",
    },
    "specs/hub_descriptor.md": {
        "specs/hub_class_requests.md",
        "specs/usb2.md",
    },
    "specs/en/hub_descriptor.md": {
        "specs/en/hub_class_requests.md",
        "specs/en/usb2.md",
    },
}

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PATH_TOKEN_RE = re.compile(r"(specs/(?:en/)?[a-z0-9_/-]+\.md)")


def _normalize_link_target(raw: str) -> str:
    href = raw.strip()
    if not href or href.startswith("http://") or href.startswith("https://"):
        return ""
    href = href.split("#", 1)[0].split("?", 1)[0]
    href = href.strip()
    while href.endswith("/"):
        href = href[:-1]
    return href


def _extract_links(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    links: set[str] = set()
    for match in LINK_RE.finditer(text):
        target = _normalize_link_target(match.group(1))
        if target:
            links.add(target)
    for match in PATH_TOKEN_RE.finditer(text):
        target = _normalize_link_target(match.group(1))
        if target:
            links.add(target)
    return links


def _normalize_core_slug(link: str) -> str:
    # Convert both zh and en variants to the same base slug for language parity checks.
    if link.startswith("./"):
        link = link[2:]
    if link.startswith("/"):
        link = link[1:]
    if link.startswith("specs/en/"):
        link = link[len("specs/en/") :]
    elif link.startswith("specs/"):
        link = link[len("specs/") :]
    return link.lower()


def _file_path(rel: str) -> Path:
    return ROOT / rel


def _is_markdown_file(path: str) -> bool:
    return path.endswith(".md") and path.startswith("specs/")


def _check_required_links(target: str, links: set[str]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    required = REQUIRED_LINKS[target]
    missing = sorted(required - links)

    # Keep raw link checks language-specific.
    for miss in missing:
        findings.append({
            "code": "REQUIRED_CROSS_LINK_MISSING",
            "message": f"{target}: missing required reference '{miss}'",
        })

    for req in required:
        # Keep validator robust if referenced page is stale.
        if req.startswith("specs/"):
            if not _file_path(req).exists():
                findings.append({
                    "code": "REQUIRED_TARGET_MISSING",
                    "message": f"{target}: required reference target not found '{req}'",
                })
    return findings


def _validate_pair_parity(left: str, right: str, links_left: set[str], links_right: set[str]) -> list[dict[str, str]]:
    def _to_local_core_set(link_set: set[str]) -> set[str]:
        return {
            _normalize_core_slug(x)
            for x in link_set
            if x.startswith("specs/")
        }

    left_core = _to_local_core_set(links_left)
    right_core = _to_local_core_set(links_right)
    findings: list[dict[str, str]] = []

    req_left_core = {_normalize_core_slug(x) for x in REQUIRED_LINKS[left]}
    req_right_core = {_normalize_core_slug(x) for x in REQUIRED_LINKS[right]}
    if req_left_core != req_right_core:
        findings.append({
            "code": "REQUIRED_LINK_PARITY_MISMATCH",
            "message": (
                f"Required cross-reference targets are not language-equivalent "
                f"between {left} and {right}: "
                f"zh={sorted(req_left_core)}, en={sorted(req_right_core)}"
            ),
        })
    if left_core != right_core:
        findings.append({
            "code": "LINK_PARITY_MISMATCH",
            "message": (
                f"Observed cross-reference core targets differ between {left} and {right}: "
                f"left={sorted(left_core)}, right={sorted(right_core)}"
            ),
        })
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate USB2 topic cross-reference consistency for selected pages."
    )
    parser.add_argument("--receipt-out")
    args = parser.parse_args()

    errors: list[dict[str, str]] = []
    link_map: dict[str, set[str]] = {}
    for page in DEFAULT_PAGES:
        p = ROOT / page
        if not p.exists():
            errors.append({
                "code": "TOPIC_PAGE_MISSING",
                "message": f"Missing required topic page: {page}",
            })
            link_map[page] = set()
            continue
        link_map[page] = _extract_links(p)

    if not errors:
        for page in DEFAULT_PAGES:
            page_errors = _check_required_links(page, link_map[page])
            errors.extend(page_errors)

    if not errors:
        pairs = [
            ("specs/feature_selectors.md", "specs/en/feature_selectors.md"),
            ("specs/port_status_bits.md", "specs/en/port_status_bits.md"),
            ("specs/port_feature_change_vocabulary.md", "specs/en/port_feature_change_vocabulary.md"),
            ("specs/hub_class_requests.md", "specs/en/hub_class_requests.md"),
            ("specs/hub_descriptor.md", "specs/en/hub_descriptor.md"),
        ]
        for left, right in pairs:
            errors.extend(_validate_pair_parity(left, right, link_map[left], link_map[right]))

    passed = len(errors) == 0
    if args.receipt_out:
        out = Path(args.receipt_out)
        out = out if out.is_absolute() else ROOT / out
        out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "validator": "validate_usb2_topic_cross_references.py",
            "result": "PASS" if passed else "FAIL",
            "error_count": len(errors),
            "checked_files": DEFAULT_PAGES,
            "errors": errors,
        }
        out.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    if not passed:
        print("USB2 topic cross-reference consistency validation FAILED")
        for item in errors:
            print(f"- [{item['code']}] {item['message']}")
        return 1

    print("USB2 topic cross-reference consistency validation PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
