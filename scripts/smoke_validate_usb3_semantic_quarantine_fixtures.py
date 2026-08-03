#!/usr/bin/env python3
"""Smoke test the USB3 semantic quarantine validator with temporary fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_usb3_semantic_quarantine.py"
RECEIPT_OUT = ROOT / "evidence" / "validation_receipt_usb3_semantic_quarantine_fixtures.json"

CASES = [
    {
        "name": "valid",
        "pages": {"page_one.md": ("inferred", False), "page_two.md": ("inferred", False)},
        "registry": ["page_one.md", "page_two.md"],
        "topics": {"page_two.md": ["ltssm_transitions"]},
        "expected_exit": 0,
        "expected_codes": [],
    },
    {
        "name": "behavioral_boundary_missing",
        "pages": {"page_one.md": ("inferred", False)},
        "registry": ["page_one.md"],
        "topics": {"page_one.md": ["ltssm_transitions"]},
        "omit_boundary": True,
        "expected_exit": 1,
        "expected_codes": ["BEHAVIORAL_BOUNDARY_SECTION_MISSING"],
    },
    {
        "name": "missing_page",
        "pages": {"page_one.md": ("inferred", False)},
        "registry": ["page_one.md", "missing.md"],
        "expected_exit": 1,
        "expected_codes": ["QUARANTINE_PAGE_MISSING"],
    },
    {
        "name": "wrong_claim_level",
        "pages": {"page_one.md": ("verified", False)},
        "registry": ["page_one.md"],
        "expected_exit": 1,
        "expected_codes": ["CLAIM_LEVEL_INVALID"],
    },
    {
        "name": "semantic_verification_claimed",
        "pages": {"page_one.md": ("inferred", True)},
        "registry": ["page_one.md"],
        "expected_exit": 1,
        "expected_codes": ["SEMANTIC_VERIFICATION_CLAIMED_INVALID"],
    },
    {
        "name": "missing_frontmatter",
        "pages": {"page_one.md": None},
        "registry": ["page_one.md"],
        "expected_exit": 1,
        "expected_codes": ["FRONTMATTER_MISSING"],
    },
    {
        "name": "duplicate_path",
        "pages": {"page_one.md": ("inferred", False)},
        "registry": ["page_one.md", "page_one.md"],
        "expected_exit": 1,
        "expected_codes": ["QUARANTINE_PATH_DUPLICATE"],
    },
    {
        "name": "embedded_delimiter",
        "pages": {"page_one.md": ("inferred", False)},
        "registry": ["page_one.md"],
        "embedded_delimiter": True,
        "expected_exit": 0,
        "expected_codes": [],
    },
]


def _write_page(
    path: Path,
    values: tuple[str, bool] | None,
    embedded_delimiter: bool,
    topics: list[str],
    omit_boundary: bool,
) -> None:
    if values is None:
        path.write_text("Fixture content without frontmatter.\n", encoding="utf-8")
        return

    claim_level, semantic_verification_claimed = values
    notes = "notes: |\n  ---\n" if embedded_delimiter else ""
    body = "Fixture content.\n"
    if topics and not omit_boundary:
        body += "\n## 本頁不宣告\n\n"
        for topic in topics:
            marker = {
                "ltssm_transitions": "LTSSM runtime behavior is not claimed.",
                "link_power_behavior": "U1/U2/U3 link power behavior is not claimed.",
                "hub_enumeration": "SET_HUB_DEPTH enumeration ordering is not claimed.",
            }[topic]
            body += f"- {marker}\n"
    path.write_text(
        "---\n"
        "title: Fixture page\n"
        f"{notes}"
        f"claim_level: {claim_level}\n"
        "status: review_required\n"
        "last_reviewed: '2026-08-03'\n"
        f"semantic_verification_claimed: {'true' if semantic_verification_claimed else 'false'}\n"
        "---\n\n" + body,
        encoding="utf-8",
    )


def run_case(case: dict) -> dict:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        specs_dir = root / "specs" / "usb3"
        quarantine_path = root / "contract" / "usb3_semantic_quarantine.yaml"
        specs_dir.mkdir(parents=True)
        quarantine_path.parent.mkdir(parents=True)

        topics = case.get("topics", {})
        for name, values in case["pages"].items():
            _write_page(
                specs_dir / name,
                values,
                case.get("embedded_delimiter", False),
                topics.get(name, []),
                case.get("omit_boundary", False),
            )

        registry = {
            "schema_version": 1,
            "quarantine_status": "active",
            "quarantined_pages": [
                {
                    "path": f"specs/usb3/{name}",
                    "claim_level": "inferred",
                    "semantic_verification_claimed": False,
                }
                for name in case["registry"]
            ],
            "behavioral_boundary_audit": {
                "version": 1,
                "boundary_headings": ["本頁不宣告", "Non-claims", "不宣告"],
                "topic_terms": {
                    "ltssm_transitions": ["LTSSM"],
                    "link_power_behavior": ["U1", "U2", "U3", "LPM", "timeout", "latency"],
                    "hub_enumeration": ["SET_HUB_DEPTH", "enumeration"],
                },
                "pages": [
                    {
                        "path": f"specs/usb3/{name}",
                        "topics": topics.get(name, []),
                    }
                    for name in dict.fromkeys(case["registry"])
                ],
            },
        }
        quarantine_path.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")
        receipt_path = root / "receipt.json"
        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--repo-root",
                str(root),
                "--quarantine",
                str(quarantine_path),
                "--specs-dir",
                str(specs_dir),
                "--receipt-out",
                str(receipt_path),
            ],
            capture_output=True,
            text=True,
        )
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

    actual_codes = [finding["code"] for finding in receipt.get("errors", [])]
    expected_codes = case["expected_codes"]
    passed = (
        result.returncode == case["expected_exit"]
        and sorted(actual_codes) == sorted(expected_codes)
    )
    return {
        "name": case["name"],
        "expected_exit": case["expected_exit"],
        "actual_exit": result.returncode,
        "expected_codes": expected_codes,
        "actual_codes": actual_codes,
        "result": "PASS" if passed else "FAIL",
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def main() -> int:
    results = [run_case(case) for case in CASES]
    failed = [result for result in results if result["result"] == "FAIL"]
    summary = {
        "validator": "validate_usb3_semantic_quarantine.py",
        "smoke_runner": "smoke_validate_usb3_semantic_quarantine_fixtures.py",
        "authority_ceiling": "structural_frontmatter_and_behavioral_boundary_presence",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }
    RECEIPT_OUT.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    for result in results:
        print(f"[{result['result']}] {result['name']}")
        if result["result"] == "FAIL":
            print(f"  expected_exit={result['expected_exit']} actual_exit={result['actual_exit']}")
            print(f"  expected_codes={result['expected_codes']}")
            print(f"  actual_codes={result['actual_codes']}")

    if failed:
        print(f"\nSmoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1
    print(f"\nSmoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
