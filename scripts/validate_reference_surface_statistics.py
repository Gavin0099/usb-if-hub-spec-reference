#!/usr/bin/env python3
"""Validate visible USB 2.0 reference-surface statistics.

Authority ceiling: visible_statistics_consistency_only

Checks that manually maintained visible statistics match governed source files.
Does not generate documentation, change claim levels, or verify USB semantics.
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

TABLES = {
    "hub_descriptor": ROOT / "tables" / "hub_descriptor_matrix.yaml",
    "transaction_translator": ROOT / "tables" / "transaction_translator_matrix.yaml",
    "escalation_triggers": ROOT / "tables" / "escalation_trigger_matrix.yaml",
    "class_requests": ROOT / "tables" / "class_request_matrix.yaml",
    "feature_selectors": ROOT / "tables" / "feature_selector_matrix.yaml",
    "port_status_bits": ROOT / "tables" / "port_status_bit_matrix.yaml",
}
VISIBLE_FILES = [
    ROOT / "README.md",
    ROOT / "PLAN.md",
    ROOT / "specs" / "index.md",
    ROOT / "specs" / "en" / "index.md",
    ROOT / "specs" / "verification_status.md",
    ROOT / "specs" / "en" / "verification_status.md",
]
PACKET_DIR = ROOT / "evidence" / "entry_verification_packets"


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _entry_counts(path: Path) -> dict[str, int]:
    doc = _load_yaml(path)
    entries = doc.get("entries") or []
    counts = {"tracked": len(entries), "verified": 0, "reviewed": 0, "inferred": 0, "missing": 0}

    for entry in entries:
        if not isinstance(entry, dict):
            counts["missing"] += 1
            continue

        claim_level = entry.get("claim_level")
        evidence_status = entry.get("evidence_status")

        if claim_level == "verified":
            counts["verified"] += 1
        elif evidence_status == "reviewed":
            counts["reviewed"] += 1
        elif claim_level == "inferred":
            counts["inferred"] += 1
        else:
            counts["missing"] += 1

    return counts


def compute_statistics() -> dict[str, Any]:
    areas = {name: _entry_counts(path) for name, path in TABLES.items()}
    total = {
        key: sum(area[key] for area in areas.values())
        for key in ("tracked", "verified", "reviewed", "inferred", "missing")
    }
    packet_count = len(list(PACKET_DIR.glob("*.yaml"))) if PACKET_DIR.exists() else 0
    return {"areas": areas, "total": total, "evidence_packets": packet_count}


def _visible_expected_patterns(stats: dict[str, Any]) -> list[tuple[str, str]]:
    total = stats["total"]
    packet_count = stats["evidence_packets"]
    patterns = [
        ("tracked", rf"\b{total['tracked']}\b"),
        ("verified", rf"\b{total['verified']}\b"),
        ("reviewed", rf"\b{total['reviewed']}\b"),
        ("inferred", rf"\b{total['inferred']}\b"),
    ]
    if packet_count:
        patterns.append(("evidence_packets", rf"\b{packet_count}\b"))
    return patterns


def _is_redirect_page(path: Path, text: str) -> bool:
    rel = path.relative_to(ROOT)
    if rel != Path("specs/index.md"):
        return False
    return "window.location.replace" in text and "./en/" in text


def validate(stats: dict[str, Any], visible_files: list[Path]) -> tuple[str, list[dict[str, str]]]:
    errors: list[dict[str, str]] = []
    total = stats["total"]

    if total["tracked"] != total["verified"] + total["reviewed"] + total["inferred"] + total["missing"]:
        errors.append({
            "code": "TOTAL_BREAKDOWN_MISMATCH",
            "message": "tracked total does not equal verified+reviewed+inferred+missing",
        })

    if stats["evidence_packets"] != total["verified"]:
        errors.append({
            "code": "PACKET_VERIFIED_COUNT_MISMATCH",
            "message": (
                f"evidence packet count {stats['evidence_packets']} != "
                f"verified entry count {total['verified']}"
            ),
        })

    for path in visible_files:
        if not path.exists():
            errors.append({"code": "VISIBLE_FILE_MISSING", "message": str(path)})
            continue
        text = path.read_text(encoding="utf-8")
        if _is_redirect_page(path, text):
            continue
        for label, pattern in _visible_expected_patterns(stats):
            if not re.search(pattern, text):
                rel = path.relative_to(ROOT)
                errors.append({
                    "code": "VISIBLE_COUNT_MISSING",
                    "message": f"{rel}: expected {label} count matching /{pattern}/",
                })

    return ("FAIL" if errors else "PASS"), errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    stats = compute_statistics()
    result, errors = validate(stats, VISIBLE_FILES)

    for e in errors:
        print(f"[FAIL] {e['code']}: {e['message']}")

    total = stats["total"]
    print(f"\nReference surface statistics validation {result}")
    print(
        "- totals: "
        f"tracked={total['tracked']}, verified={total['verified']}, "
        f"reviewed={total['reviewed']}, inferred={total['inferred']}, missing={total['missing']}"
    )
    print(f"- evidence packets: {stats['evidence_packets']}")

    if args.receipt_out:
        receipt_path = args.receipt_out if args.receipt_out.is_absolute() else ROOT / args.receipt_out
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt = {
            "validator": "validate_reference_surface_statistics",
            "result": result,
            "authority_ceiling": "visible_statistics_consistency_only",
            "does_not_generate_statistics": True,
            "does_not_change_claim_level": True,
            "does_not_validate_usb_semantics": True,
            "statistics": stats,
            "visible_files": [str(p.relative_to(ROOT)) for p in VISIBLE_FILES],
            "errors": errors,
        }
        receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    sys.exit(0 if result == "PASS" else 1)


if __name__ == "__main__":
    main()
