#!/usr/bin/env python3
"""Validate source registry URL reachability and authority metadata consistency.

Authority ceiling: source_reachability_and_metadata_consistency_only
- PASS does not imply source correctness or normative content accuracy.
- Reachability results are advisory; they do not change any claim_level.
- Results are time-bound: a URL reachable now may not be reachable later.

Checks:
1. url_type is consistent with authority_level (whitelist matrix from contract)
2. URL is reachable (HTTP HEAD/GET, advisory only, skipped with --skip-network)
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUTHORITY_FILE = ROOT / "contract" / "authority_levels.yaml"
DEFAULT_REGISTRY_FILE = ROOT / "evidence" / "source_registry.yaml"

NETWORK_TIMEOUT_SECONDS = 10


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


def _check_url_reachability(url: str) -> dict[str, Any]:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "usb-if-hub-spec-reference/1.0"})
        with urllib.request.urlopen(req, timeout=NETWORK_TIMEOUT_SECONDS) as resp:
            return {"reachability_status": "reachable", "http_status": resp.status}
    except urllib.error.HTTPError as e:
        if e.code in (200, 301, 302, 403, 405, 429):
            status = "reachable" if e.code < 400 else "reachable_with_restriction"
            return {"reachability_status": status, "http_status": e.code}
        return {"reachability_status": "unreachable", "http_status": e.code, "error": str(e)}
    except urllib.error.URLError as e:
        return {"reachability_status": "unreachable", "http_status": None, "error": str(e.reason)}
    except Exception as e:  # noqa: BLE001
        return {"reachability_status": "indeterminate", "http_status": None, "error": str(e)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authority-file", help="path to authority_levels.yaml")
    parser.add_argument("--registry-file", help="path to source_registry fixture or real registry")
    parser.add_argument("--receipt-out", help="write machine-readable receipt JSON")
    parser.add_argument(
        "--skip-network",
        action="store_true",
        default=False,
        help="skip live URL checks (use for fixtures and CI; reachability marked as skipped)",
    )
    args = parser.parse_args()

    authority_file = _resolve_path(args.authority_file, DEFAULT_AUTHORITY_FILE)
    registry_file = _resolve_path(args.registry_file, DEFAULT_REGISTRY_FILE)

    metadata_errors: list[dict[str, str]] = []
    reachability_results: list[dict[str, Any]] = []
    findings: list[dict[str, str]] = []

    def add_metadata_error(code: str, message: str) -> None:
        metadata_errors.append({"code": code, "message": message})
        findings.append({"code": code, "message": message})

    authority_doc = _load_yaml(authority_file)
    url_type_allowlist: dict[str, list[str]] = authority_doc.get("url_type_allowlist", {})

    registry_doc = _load_yaml(registry_file)
    sources = registry_doc.get("sources", [])
    if not isinstance(sources, list):
        add_metadata_error("SOURCES_NOT_LIST", "source_registry 'sources' must be a list")
        sources = []

    for source in sources:
        if not isinstance(source, dict):
            continue
        sid = source.get("source_id", "<missing>")
        authority_level = source.get("authority_level", "")
        url_type = source.get("url_type", "")
        url = source.get("url", "")

        # Check 1: url_type vs authority_level whitelist
        allowed_url_types = url_type_allowlist.get(authority_level)
        if allowed_url_types is None:
            add_metadata_error(
                "URL_TYPE_ALLOWLIST_MISSING",
                f"{sid}: no url_type_allowlist entry for authority_level '{authority_level}'",
            )
        elif url_type not in allowed_url_types:
            add_metadata_error(
                "URL_TYPE_NOT_ALLOWED_FOR_AUTHORITY",
                f"{sid}: url_type '{url_type}' not in allowlist for authority_level '{authority_level}' "
                f"(allowed: {', '.join(allowed_url_types)})",
            )

        # Check 2: URL reachability (advisory only)
        if args.skip_network or not url:
            reach = {"reachability_status": "skipped", "http_status": None}
        else:
            reach = _check_url_reachability(url)

        reachability_results.append({
            "source_id": sid,
            "url": url,
            **reach,
            "claim_effect": "advisory_only",
            "does_not_change_claim_level": True,
        })

    metadata_passed = len(metadata_errors) == 0
    receipt = {
        "validator": "validate_source_reachability.py",
        "authority_ceiling": "source_reachability_and_metadata_consistency_only",
        "validation_surface": "source_reachability_metadata_consistency",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "time_bound": True,
        "skip_network": args.skip_network,
        "result": "PASS" if metadata_passed else "FAIL",
        "note": (
            "PASS does not imply source correctness or normative content accuracy. "
            "Reachability results are advisory and time-bound."
        ),
        "metadata_error_count": len(metadata_errors),
        "metadata_errors": metadata_errors,
        "reachability_results": reachability_results,
        "findings": findings,
    }

    if args.receipt_out:
        receipt_path = _resolve_path(
            args.receipt_out,
            ROOT / "evidence" / "validation_receipt_source_reachability.json",
        )
        _write_receipt(receipt_path, receipt)

    if not metadata_passed:
        print("Metadata validation FAILED")
        for e in metadata_errors:
            print(f"- [{e['code']}] {e['message']}")
        return 1

    print("Metadata validation PASSED")
    print(f"- checked sources: {len(reachability_results)}")
    if not args.skip_network:
        unreachable = [r for r in reachability_results if r["reachability_status"] == "unreachable"]
        if unreachable:
            print(f"- advisory: {len(unreachable)} source(s) unreachable (does not affect PASS/FAIL)")
            for r in unreachable:
                print(f"  - {r['source_id']}: {r.get('error', '')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
