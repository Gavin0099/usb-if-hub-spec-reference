#!/usr/bin/env python3
"""Validate source authority registry and monitor configuration parity.

Authority ceiling: source_monitor_registry_parity_only.

The authority registry remains the source of claim metadata. The monitor
registry is the runtime observation configuration and must map explicitly to
authority sources; names are never matched heuristically.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_REGISTRY = ROOT / "evidence" / "source_registry.yaml"
DEFAULT_MONITOR_REGISTRY = ROOT / "monitor" / "monitored_sources.yaml"
VALID_MONITOR_STATUSES = {"active", "planned", "optional", "not_required"}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a YAML object")
    return data


def _resolve_path(path_arg: str | None, fallback: Path) -> Path:
    if not path_arg:
        return fallback
    path = Path(path_arg)
    return path if path.is_absolute() else ROOT / path


def _write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-registry", help="path to authority source_registry.yaml")
    parser.add_argument("--monitor-registry", help="path to monitored_sources.yaml")
    parser.add_argument("--receipt-out", help="write machine-readable validation receipt JSON")
    args = parser.parse_args()

    source_registry_path = _resolve_path(args.source_registry, DEFAULT_SOURCE_REGISTRY)
    monitor_registry_path = _resolve_path(args.monitor_registry, DEFAULT_MONITOR_REGISTRY)
    errors: list[str] = []
    findings: list[dict[str, str]] = []

    def add_error(code: str, message: str) -> None:
        errors.append(message)
        findings.append({"code": code, "message": message})

    source_doc = _load_yaml(source_registry_path)
    monitor_doc = _load_yaml(monitor_registry_path)
    source_entries = source_doc.get("sources", [])
    monitor_entries = monitor_doc.get("sources", [])

    if not isinstance(source_entries, list):
        add_error("SOURCE_REGISTRY_SOURCES_NOT_LIST", "source registry 'sources' must be a list")
        source_entries = []
    if not isinstance(monitor_entries, list):
        add_error("MONITOR_REGISTRY_SOURCES_NOT_LIST", "monitor registry 'sources' must be a list")
        monitor_entries = []

    sources_by_id: dict[str, dict[str, Any]] = {}
    for index, source in enumerate(source_entries):
        if not isinstance(source, dict):
            add_error("SOURCE_ENTRY_NOT_MAPPING", f"source registry sources[{index}] must be a mapping")
            continue
        source_id = source.get("source_id")
        if not isinstance(source_id, str) or not source_id.strip():
            add_error("SOURCE_ID_MISSING", f"source registry sources[{index}] is missing source_id")
            continue
        if source_id in sources_by_id:
            add_error("SOURCE_ID_DUPLICATE", f"duplicate source_id: {source_id}")
            continue
        sources_by_id[source_id] = source
        status = source.get("monitor_status")
        if status not in VALID_MONITOR_STATUSES:
            add_error("MONITOR_STATUS_INVALID", f"{source_id}: invalid monitor_status '{status}'")

    monitor_mappings: dict[str, list[str]] = {}
    monitor_ids: set[str] = set()
    for index, monitor in enumerate(monitor_entries):
        if not isinstance(monitor, dict):
            add_error("MONITOR_ENTRY_NOT_MAPPING", f"monitor registry sources[{index}] must be a mapping")
            continue
        monitor_id = monitor.get("id")
        if not isinstance(monitor_id, str) or not monitor_id.strip():
            add_error("MONITOR_ID_MISSING", f"monitor registry sources[{index}] is missing id")
            continue
        if monitor_id in monitor_ids:
            add_error("MONITOR_ID_DUPLICATE", f"duplicate monitor id: {monitor_id}")
        monitor_ids.add(monitor_id)

        source_id = monitor.get("source_registry_id")
        if not isinstance(source_id, str) or not source_id.strip():
            add_error("MONITOR_SOURCE_MAPPING_MISSING", f"{monitor_id}: source_registry_id is required")
            continue
        if source_id not in sources_by_id:
            add_error("MONITOR_SOURCE_MAPPING_UNKNOWN", f"{monitor_id}: unknown source_registry_id '{source_id}'")
            continue
        monitor_mappings.setdefault(source_id, []).append(monitor_id)
        source = sources_by_id[source_id]
        if source.get("monitor_status") != "active":
            add_error(
                "MONITOR_SOURCE_STATUS_NOT_ACTIVE",
                f"{monitor_id}: mapped source '{source_id}' has monitor_status '{source.get('monitor_status')}', not active",
            )
        for field in ("url", "authority_level"):
            if monitor.get(field) != source.get(field):
                add_error(
                    "MONITOR_METADATA_MISMATCH",
                    f"{monitor_id}: {field} does not match source registry '{source_id}'",
                )

    for source_id, source in sources_by_id.items():
        mappings = monitor_mappings.get(source_id, [])
        if source.get("monitor_status") == "active" and len(mappings) == 0:
            add_error("ACTIVE_SOURCE_UNMONITORED", f"{source_id}: active source has no monitor mapping")
        if len(mappings) > 1:
            add_error(
                "ACTIVE_SOURCE_MULTIPLE_MONITORS",
                f"{source_id}: source has multiple monitor mappings: {', '.join(sorted(mappings))}",
            )

    passed = not errors
    receipt = {
        "validator": "validate_source_monitor_parity.py",
        "authority_ceiling": "source_monitor_registry_parity_only",
        "source_registry": str(source_registry_path),
        "monitor_registry": str(monitor_registry_path),
        "result": "PASS" if passed else "FAIL",
        "checked_sources": len(source_entries),
        "checked_monitors": len(monitor_entries),
        "error_count": len(errors),
        "errors": errors,
        "findings": findings,
    }
    if args.receipt_out:
        receipt_path = _resolve_path(
            args.receipt_out,
            ROOT / "evidence" / "validation_receipt_source_monitor_parity.json",
        )
        _write_receipt(receipt_path, receipt)

    if not passed:
        print("Source/monitor parity validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Source/monitor parity validation PASSED")
    print(f"- checked sources: {len(source_entries)}")
    print(f"- checked monitors: {len(monitor_entries)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())