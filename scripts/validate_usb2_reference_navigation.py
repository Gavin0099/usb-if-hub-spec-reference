#!/usr/bin/env python3
"""Validate USB 2.0 navigation consistency between zh/en index and vocabulary backlinks.

Authority ceiling: USB 2.0 navigation consistency only.
- This validator only checks wiki routing presence and mutual backlink policy.
- It does not verify USB spec semantic content.
- It does not change claim levels.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ZH_USB2_PAGE = ROOT / "specs" / "usb2.md"
DEFAULT_EN_USB2_PAGE = ROOT / "specs" / "en" / "usb2.md"
DEFAULT_VOCAB_PAGE = ROOT / "specs" / "port_feature_change_vocabulary.md"
DEFAULT_EN_VOCAB_PAGE = ROOT / "specs" / "en" / "port_feature_change_vocabulary.md"

SECTION_RE = re.compile(r"^##\s+(?P<name>.+?)\s*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

TOPIC_PAGES_REQUIRED_LINK_BACK_TO_VOCAB = {
    "specs/feature_selectors.md",
    "specs/port_status_bits.md",
}
TOPIC_PAGES_REQUIRED_LINK_BACK_TO_VOCAB_EN = {
    "specs/en/feature_selectors.md",
    "specs/en/port_status_bits.md",
}
VOCAB_TOPIC_LINKS = {
    "specs/feature_selectors.md",
    "specs/port_status_bits.md",
}
VOCAB_TOPIC_LINKS_EN = {
    "specs/en/feature_selectors.md",
    "specs/en/port_status_bits.md",
}
REQUIRED_SECTIONS = [
    "Hub Class Topics",
    "USB 2.0 Protocol Foundation",
    "Reference & Governance",
]


def _normalize_link_target(href: str) -> str:
    href = href.strip()
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href or href.startswith("http://") or href.startswith("https://"):
        return ""
    href = href.rstrip("/")
    if href.startswith("/en/"):
        href = href[len("/en/") :]
    elif href.startswith("/"):
        href = href[1:]
    return href


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_index_links(path: Path) -> dict[str, set[str]]:
    text = _read_text(path)
    current_section = None
    sections: dict[str, set[str]] = {}

    for raw_line in text.splitlines():
        line = raw_line.strip()
        section_match = SECTION_RE.match(line)
        if section_match:
            current_section = section_match.group("name").strip()
            sections.setdefault(current_section, set())
            continue

        if current_section and line.startswith("|") and "](" in line:
            for match in LINK_RE.finditer(line):
                target = _normalize_link_target(match.group(1))
                if target:
                    sections[current_section].add(Path(target).name.removesuffix(".md"))

    return sections


def _extract_links(path: Path) -> set[str]:
    text = _read_text(path)
    targets: set[str] = set()
    for match in LINK_RE.finditer(text):
        target = _normalize_link_target(match.group(1))
        if target:
            targets.add(target)
    return targets


def _has_reference_text(path: Path, token: str) -> bool:
    text = _read_text(path).lower()
    return token.lower() in text


def _check_links_exist(section_map: dict[str, set[str]], page: Path, language: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for section, slugs in section_map.items():
        for slug in sorted(slugs):
            rel_path = Path("specs") / language / f"{slug}.md"
            if language == "":
                rel_path = Path("specs") / f"{slug}.md"
            candidate = ROOT / rel_path
            if not candidate.exists():
                findings.append({
                    "code": "LINK_TARGET_NOT_FOUND",
                    "message": f"{page}: link target '{slug}' in section '{section}' points to missing page '{rel_path}'",
                })
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate USB2 index topic consistency across zh/en and vocabulary backlinks."
    )
    parser.add_argument("--zh-page", default=str(DEFAULT_ZH_USB2_PAGE))
    parser.add_argument("--en-page", default=str(DEFAULT_EN_USB2_PAGE))
    parser.add_argument("--receipt-out")
    args = parser.parse_args()

    zh_page = Path(args.zh_page)
    en_page = Path(args.en_page)
    if not zh_page.is_absolute():
        zh_page = ROOT / zh_page
    if not en_page.is_absolute():
        en_page = ROOT / en_page

    errors: list[dict[str, str]] = []
    advisories: list[dict[str, str]] = []

    if not zh_page.exists():
        errors.append({"code": "ZH_PAGE_MISSING", "message": f"{zh_page} is missing"})
    if not en_page.exists():
        errors.append({"code": "EN_PAGE_MISSING", "message": f"{en_page} is missing"})

    if errors:
        for e in errors:
            print(f"- [{e['code']}] {e['message']}")
        return 1

    zh_sections = _extract_index_links(zh_page)
    en_sections = _extract_index_links(en_page)

    if not zh_sections:
        errors.append({"code": "ZH_SECTION_NOT_FOUND", "message": f"{zh_page} does not contain any index sections"})
    if not en_sections:
        errors.append({"code": "EN_SECTION_NOT_FOUND", "message": f"{en_page} does not contain any index sections"})

    # Validate section names
    if zh_sections and en_sections:
        for section in REQUIRED_SECTIONS:
            if section not in zh_sections:
                errors.append({
                    "code": "ZH_SECTION_MISSING",
                    "message": f"{zh_page}: missing required section '{section}'",
                })
            if section not in en_sections:
                errors.append({
                    "code": "EN_SECTION_MISSING",
                    "message": f"{en_page}: missing required section '{section}'",
                })

    if zh_sections and en_sections and set(zh_sections.keys()) != set(en_sections.keys()):
        errors.append({
            "code": "SECTION_SET_MISMATCH",
            "message": (
                f"{zh_page.name}/{en_page.name}: section header set mismatch, "
                f"zh={sorted(zh_sections.keys())}, en={sorted(en_sections.keys())}"
            ),
        })
    if not errors:
        for section in sorted(zh_sections.keys() & en_sections.keys()):
            if zh_sections[section] != en_sections[section]:
                errors.append({
                    "code": "SECTION_LINKS_MISMATCH",
                    "message": (
                        f"{section}: zh topics {sorted(zh_sections[section])} != en topics {sorted(en_sections[section])}"
                    ),
                })

    errors.extend(_check_links_exist(zh_sections, zh_page, ""))
    errors.extend(_check_links_exist(en_sections, en_page, "en"))

    zh_links = _extract_links(zh_page)
    en_links = _extract_links(en_page)
    zh_vocab_slug = Path("port_feature_change_vocabulary.md").name.removesuffix(".md")
    en_vocab_slug = zh_vocab_slug

    for p in TOPIC_PAGES_REQUIRED_LINK_BACK_TO_VOCAB:
        q = ROOT / p
        if not q.exists():
            errors.append({"code": "TOPIC_PAGE_MISSING", "message": f"{p} is missing"})
            continue
        if not _has_reference_text(q, zh_vocab_slug):
            errors.append({
                "code": "TOPIC_PAGE_MISSING_VOCAB_LINK",
                "message": f"{q} does not link back to {zh_vocab_slug} vocabulary page",
            })

    for p in TOPIC_PAGES_REQUIRED_LINK_BACK_TO_VOCAB_EN:
        q = ROOT / p
        if not q.exists():
            errors.append({"code": "TOPIC_PAGE_MISSING", "message": f"{p} is missing"})
            continue
        if not _has_reference_text(q, en_vocab_slug):
            errors.append({
                "code": "TOPIC_PAGE_MISSING_VOCAB_LINK",
                "message": f"{p} does not link back to {en_vocab_slug} vocabulary page",
            })

    # Vocabulary pages should remain reachable from topic pages.
    zh_vocab_links = _extract_links(DEFAULT_VOCAB_PAGE)
    en_vocab_links = _extract_links(DEFAULT_EN_VOCAB_PAGE)
    for target in VOCAB_TOPIC_LINKS:
        if target not in zh_vocab_links and not _has_reference_text(DEFAULT_VOCAB_PAGE, target):
            errors.append({
                "code": "VOCAB_PAGE_MISSING_BACKLINK",
                "message": f"{DEFAULT_VOCAB_PAGE}: missing backlink to {target}",
            })
    for target in VOCAB_TOPIC_LINKS_EN:
        if target not in en_vocab_links and not _has_reference_text(DEFAULT_EN_VOCAB_PAGE, target):
            errors.append({
                "code": "VOCAB_PAGE_MISSING_BACKLINK",
                "message": f"{DEFAULT_EN_VOCAB_PAGE}: missing backlink to {target}",
            })

    # Advisory: ensure index includes vocabulary in both language variants
    if zh_vocab_slug not in zh_links:
        advisories.append({
            "code": "ADVISORY_ZH_INDEX_MISSING_VOCAB",
            "message": f"{zh_page}: hub index does not contain {zh_vocab_slug} link",
        })
    if en_vocab_slug not in en_links:
        advisories.append({
            "code": "ADVISORY_EN_INDEX_MISSING_VOCAB",
            "message": f"{en_page}: hub index does not contain {en_vocab_slug} link",
        })

    passed = len(errors) == 0
    receipt = {
        "validator": "validate_usb2_reference_navigation.py",
        "authority_ceiling": "usb2_reference_navigation_consistency_only",
        "result": "PASS" if passed else "FAIL",
        "error_count": len(errors),
        "advisory_count": len(advisories),
        "checked_files": [
            str(zh_page.relative_to(ROOT)),
            str(en_page.relative_to(ROOT)),
            "specs/feature_selectors.md",
            "specs/port_status_bits.md",
            "specs/en/feature_selectors.md",
            "specs/en/port_status_bits.md",
        ],
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
        print("USB2 reference navigation validation FAILED")
        for e in errors:
            print(f"- [{e['code']}] {e['message']}")
        if advisories:
            print(f"- {len(advisories)} advisory finding(s):")
            for a in advisories:
                print(f"  ~ [{a['code']}] {a['message']}")
        return 1

    print("USB2 reference navigation validation PASSED")
    print(f"- checked sections: {len(en_sections)}")
    if advisories:
        print(f"- {len(advisories)} advisory finding(s):")
        for a in advisories:
            print(f"  ~ [{a['code']}] {a['message']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
