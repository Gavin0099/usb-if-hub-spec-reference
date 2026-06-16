#!/usr/bin/env python3
"""Validate non-core USB2 index topic pair reachability and navigation links."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE_SLUGS = {
    "hub_descriptor",
    "hub_class_requests",
    "feature_selectors",
    "port_status_bits",
    "port_feature_change_vocabulary",
}


def _extract_internal_links(text: str) -> list[str]:
    links: list[str] = []
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        links.append(match.group(1).strip())
    return links


def _collect_index_topics(index_path: Path, language: str) -> set[str]:
    text = index_path.read_text(encoding="utf-8")
    links = _extract_internal_links(text)
    topics = set()
    for href in links:
        if not href.startswith("/"):
            continue
        if href.startswith("/en/"):
            if language == "zh":
                continue
            slug = href[4:].strip("/").split("#", 1)[0]
        else:
            if language != "zh":
                continue
            slug = href[1:].strip("/").split("#", 1)[0]
        if not slug or slug == "usb3" or slug.startswith("usb3/"):
            continue
        if slug in CORE_SLUGS:
            continue
        candidate = ROOT / ("specs/en/" if language == "en" else "specs/") / f"{slug}.md"
        if candidate.exists():
            topics.add(slug)
    return topics


def _has_any(text: str, patterns: list[str]) -> bool:
    return any(p in text for p in patterns)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate non-core USB2 topic pair reachability and links."
    )
    parser.add_argument("--receipt-out", help="Path for JSON receipt.")
    args = parser.parse_args()

    zh_topics = _collect_index_topics(ROOT / "specs/usb2.md", language="zh")
    en_topics = _collect_index_topics(ROOT / "specs/en/usb2.md", language="en")

    errors: list[dict[str, str]] = []
    if zh_topics != en_topics:
        missing_in_en = sorted(zh_topics - en_topics)
        missing_in_zh = sorted(en_topics - zh_topics)
        if missing_in_en:
            errors.append({
                "code": "INDEX_PAIR_MISMATCH",
                "message": f"Topics present only in zh USB2 index: {', '.join(missing_in_en)}",
            })
        if missing_in_zh:
            errors.append({
                "code": "INDEX_PAIR_MISMATCH",
                "message": f"Topics present only in en USB2 index: {', '.join(missing_in_zh)}",
            })

    noncore_topics = sorted(zh_topics & en_topics)

    for slug in noncore_topics:
        zh_path = ROOT / "specs" / f"{slug}.md"
        en_path = ROOT / "specs/en" / f"{slug}.md"
        zh_text = zh_path.read_text(encoding="utf-8")
        en_text = en_path.read_text(encoding="utf-8")

        zh_backlink_ok = _has_any(
            zh_text,
            [
                "specs/usb2.md",
                "/usb2",
                "/en/usb2",
                "/usb2.md",
            ],
        )
        en_backlink_ok = _has_any(
            en_text,
            [
                "specs/en/usb2.md",
                "/en/usb2",
                "/usb2",
                "/en/usb2.md",
            ],
        )

        zh_counterpart_ok = _has_any(
            zh_text,
            [
                f"specs/en/{slug}.md",
                f"/en/{slug}",
                f"/en/{slug}.md",
            ],
        )
        en_counterpart_ok = _has_any(
            en_text,
            [
                f"specs/{slug}.md",
                f"/{slug}",
                f"/{slug}.md",
            ],
        )

        if not zh_backlink_ok:
            errors.append({
                "code": "MISSING_USB2_BACKLINK",
                "message": f"{slug}.zh: missing backlink to USB2 index.",
            })
        if not en_backlink_ok:
            errors.append({
                "code": "MISSING_USB2_BACKLINK",
                "message": f"{slug}.en: missing backlink to USB2 index.",
            })
        if not zh_counterpart_ok:
            errors.append({
                "code": "MISSING_LANGUAGE_PAIR_LINK",
                "message": f"{slug}.zh: missing link to en/{slug}.",
            })
        if not en_counterpart_ok:
            errors.append({
                "code": "MISSING_LANGUAGE_PAIR_LINK",
                "message": f"{slug}.en: missing link to /{slug}.",
            })

    passed = len(errors) == 0
    if args.receipt_out:
        out = Path(args.receipt_out)
        if not out.is_absolute():
            out = ROOT / out
        out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "validator": "validate_usb2_topic_pair_reachability.py",
            "result": "PASS" if passed else "FAIL",
            "error_count": len(errors),
            "checked_topics": len(noncore_topics),
            "errors": errors,
        }
        out.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    if passed:
        print("USB2 topic pair reachability validation PASSED")
        return 0

    print("USB2 topic pair reachability validation FAILED")
    for item in errors:
        print(f"- [{item['code']}] {item['message']}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
