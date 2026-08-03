#!/usr/bin/env python3
"""Validate the structural boundary of the USB3 semantic quarantine."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUARANTINE = ROOT / "contract" / "usb3_semantic_quarantine.yaml"
DEFAULT_SPECS_DIR = ROOT / "specs" / "usb3"
EXPECTED_CLAIM_LEVEL = "inferred"
EXPECTED_SEMANTIC_FLAG = False
BOUNDARY_HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return value


def _parse_frontmatter(path: Path) -> dict[str, Any] | None:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return None

    closing_index = next(
        (index for index, line in enumerate(lines[1:], start=1) if line == "---"),
        None,
    )
    if closing_index is None:
        return None

    value = yaml.safe_load("\n".join(lines[1:closing_index]))
    return value if isinstance(value, dict) else None


def _error(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def _relative_page_path(page_path: Path, repo_root: Path) -> str:
    try:
        return page_path.relative_to(repo_root).as_posix()
    except ValueError:
        return page_path.as_posix()


def _boundary_section(page_path: Path, headings: list[str]) -> str | None:
    lines = page_path.read_text(encoding="utf-8").splitlines()
    expected_headings = {heading.casefold() for heading in headings}
    start_index: int | None = None
    for index, line in enumerate(lines):
        match = BOUNDARY_HEADING_RE.match(line.strip())
        if match and match.group(1).casefold() in expected_headings:
            start_index = index + 1
            break
    if start_index is None:
        return None

    end_index = len(lines)
    for index in range(start_index, len(lines)):
        if BOUNDARY_HEADING_RE.match(lines[index].strip()):
            end_index = index
            break
    return "\n".join(lines[start_index:end_index])


def _validate_behavioral_boundary_audit(
    document: dict[str, Any],
    repo_root: Path,
    declared_paths: set[str],
    actual_paths: set[str],
) -> list[dict[str, str]]:
    audit = document.get("behavioral_boundary_audit")
    errors: list[dict[str, str]] = []
    audit_path = "contract/usb3_semantic_quarantine.yaml"
    if not isinstance(audit, dict):
        return [_error(
            "BEHAVIORAL_AUDIT_MISSING",
            audit_path,
            "behavioral_boundary_audit must be a mapping",
        )]

    headings = audit.get("boundary_headings")
    topic_terms = audit.get("topic_terms")
    pages = audit.get("pages")
    if (
        not isinstance(headings, list)
        or not all(isinstance(value, str) for value in headings)
        or not isinstance(topic_terms, dict)
        or not isinstance(pages, list)
    ):
        return [_error(
            "BEHAVIORAL_AUDIT_INVALID",
            audit_path,
            "audit requires boundary_headings, topic_terms, and pages",
        )]

    audit_entries: dict[str, dict[str, Any]] = {}
    for entry in pages:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            errors.append(_error(
                "BEHAVIORAL_AUDIT_ENTRY_INVALID",
                audit_path,
                "each audit page must contain a path",
            ))
            continue
        path = Path(entry["path"]).as_posix()
        if path in audit_entries:
            errors.append(_error(
                "BEHAVIORAL_AUDIT_PATH_DUPLICATE",
                path,
                "behavioral audit contains duplicate paths",
            ))
            continue
        topics = entry.get("topics")
        if not isinstance(topics, list) or not all(isinstance(value, str) for value in topics):
            errors.append(_error(
                "BEHAVIORAL_AUDIT_TOPICS_INVALID",
                path,
                "audit topics must be a list of strings",
            ))
            continue
        audit_entries[path] = {"topics": topics}

    audit_paths = set(audit_entries)
    for path in sorted(declared_paths - audit_paths):
        errors.append(_error(
            "BEHAVIORAL_AUDIT_PAGE_MISSING",
            path,
            "quarantined page has no behavioral audit entry",
        ))
    for path in sorted(audit_paths - declared_paths):
        errors.append(_error(
            "BEHAVIORAL_AUDIT_PAGE_EXTRA",
            path,
            "behavioral audit page is not in quarantined_pages",
        ))

    known_topics = set(topic_terms)
    for path, entry in sorted(audit_entries.items()):
        page_topics = entry["topics"]
        for topic in page_topics:
            terms = topic_terms.get(topic)
            if not isinstance(terms, list) or not all(isinstance(value, str) for value in terms):
                errors.append(_error(
                    "BEHAVIORAL_TOPIC_INVALID",
                    path,
                    f"topic {topic!r} is not defined in topic_terms",
                ))
                continue
            if path not in actual_paths:
                continue
            page_path = repo_root / Path(path)
            section = _boundary_section(page_path, headings)
            if section is None:
                errors.append(_error(
                    "BEHAVIORAL_BOUNDARY_SECTION_MISSING",
                    path,
                    "behavioral page has no registered non-claim boundary heading",
                ))
                continue
            section_folded = section.casefold()
            if not any(term.casefold() in section_folded for term in terms):
                errors.append(_error(
                    "BEHAVIORAL_BOUNDARY_TERM_MISSING",
                    path,
                    f"boundary does not name topic {topic!r}",
                ))

        unknown_topics = set(page_topics) - known_topics
        for topic in sorted(unknown_topics):
            errors.append(_error(
                "BEHAVIORAL_TOPIC_INVALID",
                path,
                f"topic {topic!r} is not defined in topic_terms",
            ))
    return errors


def validate(quarantine_path: Path, repo_root: Path, specs_dir: Path) -> dict[str, Any]:
    document = _load_yaml(quarantine_path)
    entries = document.get("quarantined_pages")
    errors: list[dict[str, str]] = []

    if not isinstance(entries, list):
        errors.append(_error(
            "QUARANTINE_REGISTRY_INVALID",
            _relative_page_path(quarantine_path, repo_root),
            "quarantined_pages must be a list",
        ))
        entries = []

    registry_paths: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            errors.append(_error(
                "QUARANTINE_ENTRY_INVALID",
                _relative_page_path(quarantine_path, repo_root),
                "each quarantined_pages entry must contain a path",
            ))
            continue

        relative_path = Path(entry["path"])
        registry_path = relative_path.as_posix()
        registry_paths.append(registry_path)
        if entry.get("claim_level") != EXPECTED_CLAIM_LEVEL:
            errors.append(_error(
                "REGISTRY_CLAIM_LEVEL_INVALID",
                registry_path,
                f"registry claim_level must be {EXPECTED_CLAIM_LEVEL!r}",
            ))
        if entry.get("semantic_verification_claimed") is not EXPECTED_SEMANTIC_FLAG:
            errors.append(_error(
                "REGISTRY_SEMANTIC_VERIFICATION_CLAIMED_INVALID",
                registry_path,
                "registry semantic_verification_claimed must be false",
            ))

    if len(registry_paths) != len(set(registry_paths)):
        errors.append(_error(
            "QUARANTINE_PATH_DUPLICATE",
            _relative_page_path(quarantine_path, repo_root),
            "quarantined_pages contains duplicate paths",
        ))

    actual_paths = {
        _relative_page_path(path, repo_root)
        for path in sorted(specs_dir.rglob("*.md"))
    } if specs_dir.exists() else set()
    declared_paths = set(registry_paths)

    for path in sorted(declared_paths - actual_paths):
        errors.append(_error("QUARANTINE_PAGE_MISSING", path, "registry page does not exist"))
    for path in sorted(actual_paths - declared_paths):
        errors.append(_error("QUARANTINE_PAGE_UNREGISTERED", path, "USB3 page is not listed in quarantine registry"))

    pages_checked = 0
    pages_valid = 0
    for registry_path in sorted(declared_paths & actual_paths):
        page_path = repo_root / Path(registry_path)
        pages_checked += 1
        frontmatter = _parse_frontmatter(page_path)
        if frontmatter is None:
            errors.append(_error("FRONTMATTER_MISSING", registry_path, "page has no YAML frontmatter mapping"))
            continue

        page_error_count = len(errors)
        if frontmatter.get("claim_level") != EXPECTED_CLAIM_LEVEL:
            errors.append(_error(
                "CLAIM_LEVEL_INVALID",
                registry_path,
                f"frontmatter claim_level must be {EXPECTED_CLAIM_LEVEL!r}",
            ))
        if frontmatter.get("semantic_verification_claimed") is not EXPECTED_SEMANTIC_FLAG:
            errors.append(_error(
                "SEMANTIC_VERIFICATION_CLAIMED_INVALID",
                registry_path,
                "frontmatter semantic_verification_claimed must be false",
            ))
        if len(errors) == page_error_count:
            pages_valid += 1

    errors.extend(_validate_behavioral_boundary_audit(
        document,
        repo_root,
        declared_paths,
        actual_paths,
    ))

    return {
        "validator": "validate_usb3_semantic_quarantine.py",
        "quarantine_yaml": _relative_page_path(quarantine_path, repo_root),
        "specs_dir": _relative_page_path(specs_dir, repo_root),
        "authority_ceiling": "structural_frontmatter_and_behavioral_boundary_presence",
        "note": "PASS verifies quarantine coverage, frontmatter markers, and registered non-claim boundary terms only; it does not verify USB3 semantic claims.",
        "result": "PASS" if not errors else "FAIL",
        "registry_pages": len(registry_paths),
        "pages_checked": pages_checked,
        "pages_valid": pages_valid,
        "error_count": len(errors),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quarantine", default=str(DEFAULT_QUARANTINE))
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--specs-dir")
    parser.add_argument("--receipt-out")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    quarantine_path = Path(args.quarantine)
    if not quarantine_path.is_absolute():
        quarantine_path = repo_root / quarantine_path
    specs_dir = Path(args.specs_dir) if args.specs_dir else repo_root / "specs" / "usb3"
    if not specs_dir.is_absolute():
        specs_dir = repo_root / specs_dir

    try:
        receipt = validate(quarantine_path.resolve(), repo_root, specs_dir.resolve())
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"[QUARANTINE_VALIDATION_ERROR] {exc}")
        return 1

    if args.receipt_out:
        receipt_path = Path(args.receipt_out)
        if not receipt_path.is_absolute():
            receipt_path = repo_root / receipt_path
        try:
            receipt_path.parent.mkdir(parents=True, exist_ok=True)
            receipt_path.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
        except OSError as exc:
            print(f"[RECEIPT_WRITE_ERROR] {exc}")
            return 2

    if receipt["result"] == "PASS":
        print("USB3 semantic quarantine validation: PASS")
        print(f"- registry pages: {receipt['registry_pages']}")
        print(f"- pages checked: {receipt['pages_checked']}")
    else:
        print("USB3 semantic quarantine validation: FAIL")
        for finding in receipt["errors"]:
            print(f"- [{finding['code']}] {finding['path']}: {finding['message']}")
    return 0 if receipt["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
