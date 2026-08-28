#!/usr/bin/env python3
"""Validate accounting and metadata for the public specification surface.

Authority ceiling: public_page_boundary_inventory_structural_only.

This validator proves that every Markdown page under the configured public
root is accounted for and that inventory source metadata agrees with page
frontmatter. It does not inspect an external specification, compare prose,
detect plagiarism, decide copyrightability, or grant legal clearance.
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
DEFAULT_INVENTORY = ROOT / "governance" / "public_spec_boundary_inventory.yaml"
DEFAULT_SOURCE_REGISTRY = ROOT / "evidence" / "source_registry.yaml"
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.DOTALL)

ALLOWED_RISK_CLASSES = {
    "index_or_notice",
    "engineering_summary",
    "normative_prose",
    "structured_spec_reproduction",
    "high_density_normative_table",
}
ALLOWED_REVIEW_STATES = {"pending", "reviewed", "cleared", "blocked"}
HIGH_RISK_CLASSES = {"structured_spec_reproduction", "high_density_normative_table"}


def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def normalize_repo_path(value: Any) -> str:
    return Path(str(value)).as_posix()


def is_safe_relative_path(value: Any) -> bool:
    path = Path(str(value))
    return not path.is_absolute() and ".." not in path.parts


def load_yaml(path: Path) -> tuple[Any, str | None]:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, f"file does not exist: {path}"
    except (OSError, yaml.YAMLError) as exc:
        return None, f"could not read YAML {path}: {exc}"


def parse_frontmatter(page_path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        text = page_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return None, f"could not read page: {exc}"
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, "page has no YAML frontmatter"
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, f"invalid YAML frontmatter: {exc}"
    if not isinstance(data, dict):
        return None, "frontmatter must be a mapping"
    return data, None


def source_ids(source_registry: Any) -> set[str]:
    if not isinstance(source_registry, dict):
        return set()
    sources = source_registry.get("sources")
    if not isinstance(sources, list):
        return set()
    return {
        str(source.get("source_id"))
        for source in sources
        if isinstance(source, dict) and source.get("source_id")
    }


def validate(
    repo_root: Path,
    inventory_path: Path,
    source_registry_path: Path,
) -> tuple[str, list[dict[str, str]], dict[str, Any]]:
    errors: list[dict[str, str]] = []

    def fail(code: str, message: str) -> None:
        errors.append({"code": code, "message": message})

    inventory, inventory_error = load_yaml(inventory_path)
    if inventory_error:
        fail("INVENTORY_MISSING", inventory_error)
        return "FAIL", errors, {"public_pages": [], "inventory_pages": []}
    if not isinstance(inventory, dict):
        fail("INVENTORY_SCHEMA_INVALID", "inventory root must be a mapping")
        return "FAIL", errors, {"public_pages": [], "inventory_pages": []}

    if inventory.get("schema_version") != 1:
        fail("INVENTORY_SCHEMA_INVALID", "schema_version must be 1")

    if inventory.get("legal_clearance") != "not_claimed":
        fail(
            "LEGAL_CLEARANCE_CLAIM",
            "inventory legal_clearance must remain exactly 'not_claimed'",
        )

    public_root_value = inventory.get("public_root")
    if not isinstance(public_root_value, str) or not is_safe_relative_path(public_root_value):
        fail("PUBLIC_ROOT_INVALID", "public_root must be a safe repository-relative path")
        public_root = repo_root / "__invalid_public_root__"
    else:
        public_root = repo_root / public_root_value

    if not public_root.is_dir():
        fail("PUBLIC_ROOT_MISSING", f"public_root directory does not exist: {public_root}")

    public_pages = (
        sorted(
            path.relative_to(repo_root).as_posix()
            for path in public_root.rglob("*")
            if path.is_file() and path.suffix.casefold() == ".md"
        )
        if public_root.is_dir()
        else []
    )
    public_page_set = set(public_pages)

    source_registry, source_error = load_yaml(source_registry_path)
    if source_error:
        fail("SOURCE_REGISTRY_MISSING", source_error)
    valid_source_ids = source_ids(source_registry)

    entries = inventory.get("entries")
    if not isinstance(entries, list):
        fail("INVENTORY_SCHEMA_INVALID", "entries must be a list")
        entries = []

    allowed_no_source = inventory.get("no_source_allowed_pages", [])
    if not isinstance(allowed_no_source, list) or not all(
        isinstance(page, str) and is_safe_relative_path(page) for page in allowed_no_source
    ):
        fail(
            "INVENTORY_SCHEMA_INVALID",
            "no_source_allowed_pages must be a list of safe repository-relative paths",
        )
        allowed_no_source = []
    allowed_no_source_set = {normalize_repo_path(page) for page in allowed_no_source}

    inventory_pages: list[str] = []
    entry_by_page: dict[str, dict[str, Any]] = {}

    for index, entry in enumerate(entries):
        location = f"entries[{index}]"
        if not isinstance(entry, dict):
            fail("INVENTORY_SCHEMA_INVALID", f"{location} must be a mapping")
            continue

        page_value = entry.get("page")
        if not isinstance(page_value, str) or not is_safe_relative_path(page_value):
            fail("PAGE_OUTSIDE_PUBLIC_ROOT", f"{location}.page must be safe and relative")
            continue
        page = normalize_repo_path(page_value)
        inventory_pages.append(page)
        if page in entry_by_page:
            fail("DUPLICATE_INVENTORY_PAGE", f"page appears more than once: {page}")
        entry_by_page[page] = entry

        if not page.startswith(f"{normalize_repo_path(public_root_value)}/"):
            fail("PAGE_OUTSIDE_PUBLIC_ROOT", f"page is outside public_root: {page}")

        page_path = repo_root / Path(page)
        if not page_path.is_file():
            fail("INVENTORY_PAGE_MISSING", f"inventory page does not exist: {page}")

        refs = entry.get("source_refs")
        if not isinstance(refs, list) or not all(isinstance(ref, str) for ref in refs):
            fail("MISSING_SOURCE_METADATA", f"{page}: source_refs must be a list of source IDs")
            refs = []
        if len(refs) != len(set(refs)):
            fail("SOURCE_REFS_INVALID", f"{page}: source_refs contains duplicates")

        source_scope = entry.get("source_scope")
        if not isinstance(source_scope, str) or not source_scope.strip():
            fail("MISSING_SOURCE_METADATA", f"{page}: source_scope is required")
            source_scope = ""

        risk_class = entry.get("risk_class")
        if risk_class not in ALLOWED_RISK_CLASSES:
            fail("INVALID_RISK_CLASS", f"{page}: unsupported risk_class: {risk_class!r}")

        review_status = entry.get("review_status")
        if review_status not in ALLOWED_REVIEW_STATES:
            fail("INVALID_REVIEW_STATE", f"{page}: unsupported review_status: {review_status!r}")

        if entry.get("legal_clearance") not in (None, "not_claimed", "NOT CLAIMED"):
            fail("LEGAL_CLEARANCE_CLAIM", f"{page}: legal clearance cannot be claimed")

        if review_status in {"reviewed", "cleared"}:
            evidence = entry.get("review_evidence")
            if not evidence or (isinstance(evidence, list) and not any(str(item).strip() for item in evidence)):
                fail("CLEARED_REQUIRES_EVIDENCE", f"{page}: {review_status} requires review_evidence")

        if refs:
            unknown = sorted(set(refs) - valid_source_ids)
            for source_id in unknown:
                fail("UNKNOWN_SOURCE_REF", f"{page}: unknown source_refs ID: {source_id}")
            if "usb20_spec" in refs and "USB 2.0" not in source_scope:
                fail("SOURCE_SCOPE_MISMATCH", f"{page}: usb20_spec requires USB 2.0 in source_scope")
            if "usb20_spec" not in refs and "USB 2.0" in source_scope:
                fail("SOURCE_SCOPE_MISMATCH", f"{page}: source_scope names USB 2.0 without usb20_spec")
            if "usb32_spec" in refs and "USB 3.2" not in source_scope:
                fail("SOURCE_SCOPE_MISMATCH", f"{page}: usb32_spec requires USB 3.2 in source_scope")
            if "usb32_spec" not in refs and "USB 3.2" in source_scope:
                fail("SOURCE_SCOPE_MISMATCH", f"{page}: source_scope names USB 3.2 without usb32_spec")
        elif page not in allowed_no_source_set:
            fail(
                "MISSING_SOURCE_METADATA",
                f"{page}: source_refs are empty but the page is not in no_source_allowed_pages",
            )
        elif risk_class != "index_or_notice":
            fail("INVALID_RISK_CLASS", f"{page}: no-source pages must be index_or_notice")

        if page_path.is_file():
            frontmatter, frontmatter_error = parse_frontmatter(page_path)
            if frontmatter_error:
                fail("PAGE_FRONTMATTER_INVALID", f"{page}: {frontmatter_error}")
            else:
                actual_refs = frontmatter.get("source_refs", [])
                if actual_refs is None:
                    actual_refs = []
                if not isinstance(actual_refs, list) or not all(
                    isinstance(ref, str) for ref in actual_refs
                ):
                    fail("SOURCE_REFS_MISMATCH", f"{page}: page frontmatter source_refs is not a list")
                    actual_refs = []
                # The four navigation/notice pages intentionally have no
                # frontmatter source_refs; their explicit allowlist entry is
                # the machine-readable exception.
                if refs != actual_refs and not (
                    not refs and page in allowed_no_source_set and "source_refs" not in frontmatter
                ):
                    fail(
                        "SOURCE_REFS_MISMATCH",
                        f"{page}: inventory source_refs={refs!r}, page frontmatter source_refs={actual_refs!r}",
                    )

    inventory_page_set = set(inventory_pages)
    for page in sorted(public_page_set - inventory_page_set):
        fail("UNTRACKED_PUBLIC_PAGE", f"public page is not in inventory: {page}")
    for page in sorted(inventory_page_set - public_page_set):
        fail("INVENTORY_PAGE_MISSING", f"inventory page is not a public page: {page}")

    if allowed_no_source_set - public_page_set:
        for page in sorted(allowed_no_source_set - public_page_set):
            fail("INVENTORY_PAGE_MISSING", f"no-source allowlist page does not exist: {page}")
    if allowed_no_source_set != {
        page for page, entry in entry_by_page.items() if entry.get("source_refs") == []
    }:
        fail(
            "MISSING_SOURCE_METADATA",
            "no_source_allowed_pages must exactly match inventory entries with empty source_refs",
        )

    metadata = {
        "public_pages": public_pages,
        "inventory_pages": sorted(inventory_page_set),
        "public_page_count": len(public_pages),
        "inventory_page_count": len(inventory_page_set),
    }
    return ("FAIL" if errors else "PASS"), errors, metadata


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--source-registry", type=Path, default=DEFAULT_SOURCE_REGISTRY)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    inventory_path = resolve_path(repo_root, args.inventory)
    source_registry_path = resolve_path(repo_root, args.source_registry)
    result, errors, metadata = validate(repo_root, inventory_path, source_registry_path)

    for error in errors:
        print(f"[FAIL] {error['code']}: {error['message']}")
    print(f"\nPublic Spec boundary inventory validation {result}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        receipt = {
            "validator": "validate_public_spec_boundary_inventory",
            "inventory": str(inventory_path),
            "source_registry": str(source_registry_path),
            "result": result,
            "authority_ceiling": "public_page_boundary_inventory_structural_only",
            "legal_clearance": "NOT CLAIMED",
            "semantic_copy_detection": "NOT CLAIMED",
            "does_not_modify_public_content": True,
            "checked_pages": metadata["public_page_count"],
            "inventory_pages": metadata["inventory_page_count"],
            "errors": errors,
        }
        args.receipt_out.write_text(
            json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
        )

    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
