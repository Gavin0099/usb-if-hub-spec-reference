#!/usr/bin/env python3
"""Validate source authority registry against governance contract scaffolds.

Checks:
1. source authority_level exists in contract/authority_levels.yaml
2. required source fields are present and non-empty
3. usb_version_scope values are legal
4. claim_usage constraints by authority level
5. URL format sanity checks
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUTHORITY_FILE = ROOT / "contract" / "authority_levels.yaml"
DEFAULT_REGISTRY_FILE = ROOT / "evidence" / "source_registry.yaml"

VALID_USB_SCOPES = {"usb20", "usb21", "usb32", "usb4"}
FORBID_NORMATIVE_CLAIM_USAGE = {
    "official_index",
    "community_reference",
    "archive_fallback",
}
NORMATIVE_CLAIM_USAGES = {"allowed_normative", "normative"}
REQUIRED_SOURCE_FIELDS = {
    "source_id",
    "title",
    "authority_level",
    "usb_version_scope",
    "topics",
    "url",
    "url_type",
    "monitor_status",
    "claim_usage",
}
CLAIM_USAGE_POLICY = {
    "normative_official": {
        "allowed_normative",
        "delta_only",
        "fallback_only",
        "boundary_context_only",
        "non_normative_only",
    },
    "official_validation": {
        "validation_only",
        "non_normative_only",
    },
    "official_index": {
        "discovery_only",
        "discovery_only_until_download_registered",
        "boundary_context_only",
    },
    "community_reference": {
        "non_normative_only",
    },
    "archive_fallback": {
        "fallback_only",
        "non_normative_only",
    },
}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a YAML object")
    return data


def _resolve_path(path_arg: str | None, fallback: Path) -> Path:
    if not path_arg:
        return fallback
    p = Path(path_arg)
    return p if p.is_absolute() else ROOT / p


def _write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authority-file", help="path to authority_levels.yaml")
    parser.add_argument("--registry-file", help="path to source_registry fixture")
    parser.add_argument("--receipt-out", help="write machine-readable validation receipt JSON")
    args = parser.parse_args()

    authority_file = _resolve_path(args.authority_file, DEFAULT_AUTHORITY_FILE)
    registry_file = _resolve_path(args.registry_file, DEFAULT_REGISTRY_FILE)

    errors: list[str] = []
    findings: list[dict[str, str]] = []

    def add_error(code: str, message: str) -> None:
        errors.append(message)
        findings.append({"code": code, "message": message})

    authority_doc = _load_yaml(authority_file)
    authority_levels = authority_doc.get("authority_levels", {})
    if not isinstance(authority_levels, dict) or not authority_levels:
        add_error(
            "AUTHORITY_LEVELS_MAP_MISSING",
            "authority_levels.yaml missing non-empty authority_levels map",
        )
        authority_level_keys = set()
    else:
        authority_level_keys = set(authority_levels.keys())

    registry_doc = _load_yaml(registry_file)
    sources = registry_doc.get("sources", [])
    if not isinstance(sources, list):
        add_error("SOURCES_NOT_LIST", "source_registry.yaml 'sources' must be a list")
        sources = []

    for idx, source in enumerate(sources):
        loc = f"sources[{idx}]"
        if not isinstance(source, dict):
            add_error("SOURCE_ENTRY_NOT_MAPPING", f"{loc} must be a mapping")
            continue

        sid = source.get("source_id", f"<missing@{idx}>")
        authority_level = source.get("authority_level")
        claim_usage = source.get("claim_usage")
        usb_scopes = source.get("usb_version_scope", [])
        title = source.get("title")
        url = source.get("url")
        topics = source.get("topics")

        missing_fields = [k for k in REQUIRED_SOURCE_FIELDS if k not in source]
        if missing_fields:
            add_error(
                "REQUIRED_FIELD_MISSING",
                f"{sid}: missing required field(s): {', '.join(sorted(missing_fields))}",
            )

        if not isinstance(title, str) or not title.strip():
            add_error("TITLE_INVALID", f"{sid}: title must be a non-empty string")

        if authority_level not in authority_level_keys:
            add_error(
                "UNKNOWN_AUTHORITY_LEVEL",
                f"{sid}: authority_level '{authority_level}' not defined in contract/authority_levels.yaml"
            )

        if not isinstance(usb_scopes, list) or not usb_scopes:
            add_error("USB_VERSION_SCOPE_EMPTY", f"{sid}: usb_version_scope must be a non-empty list")
        else:
            invalid_scopes = [s for s in usb_scopes if s not in VALID_USB_SCOPES]
            if invalid_scopes:
                add_error(
                    "USB_VERSION_SCOPE_INVALID",
                    f"{sid}: invalid usb_version_scope value(s): {', '.join(invalid_scopes)}"
                )

        if not isinstance(topics, list) or not topics:
            add_error("TOPICS_EMPTY", f"{sid}: topics must be a non-empty list")
        elif any((not isinstance(t, str) or not t.strip()) for t in topics):
            add_error("TOPICS_ITEM_INVALID", f"{sid}: topics list contains empty/non-string item")

        if not isinstance(url, str) or not url.strip():
            add_error("URL_EMPTY", f"{sid}: url must be a non-empty string")
        elif not (url.startswith("https://") or url.startswith("http://")):
            add_error("URL_SCHEME_INVALID", f"{sid}: url must start with http:// or https://")

        if authority_level in FORBID_NORMATIVE_CLAIM_USAGE and claim_usage in NORMATIVE_CLAIM_USAGES:
            add_error(
                "NORMATIVE_CLAIM_USAGE_FOR_NON_NORMATIVE_AUTHORITY",
                f"{sid}: claim_usage '{claim_usage}' is not allowed for authority_level '{authority_level}'"
            )

        allowed_claim_usages = CLAIM_USAGE_POLICY.get(authority_level)
        if (
            allowed_claim_usages is not None
            and claim_usage not in allowed_claim_usages
            and not (
                authority_level in FORBID_NORMATIVE_CLAIM_USAGE
                and claim_usage in NORMATIVE_CLAIM_USAGES
            )
        ):
            errors.append(
                f"{sid}: claim_usage '{claim_usage}' not allowed for authority_level '{authority_level}'"
            )
            findings.append(
                {
                    "code": "CLAIM_USAGE_NOT_ALLOWED_FOR_AUTHORITY",
                    "message": f"{sid}: claim_usage '{claim_usage}' not allowed for authority_level '{authority_level}'",
                }
            )

    passed = not errors
    receipt = {
        "validator": "validate_source_registry.py",
        "authority_file": str(authority_file),
        "registry_file": str(registry_file),
        "authority_ceiling": "structural_registry_validation_only",
        "result": "PASS" if passed else "FAIL",
        "checked_authority_levels": len(authority_level_keys),
        "checked_sources": len(sources),
        "error_count": len(errors),
        "errors": errors,
        "findings": findings,
    }

    if args.receipt_out:
        receipt_path = _resolve_path(args.receipt_out, ROOT / "evidence" / "validation_receipt_source_registry.json")
        _write_receipt(receipt_path, receipt)

    if not passed:
        print("Validation FAILED")
        for e in errors:
            print(f"- {e}")
        return 1

    print("Validation PASSED")
    print(f"- checked authority levels: {len(authority_level_keys)}")
    print(f"- checked sources: {len(sources)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
