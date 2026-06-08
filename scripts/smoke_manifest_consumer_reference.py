#!/usr/bin/env python3
"""REFERENCE-CONSUMER-SMOKE-1: Manifest v0.3 Consumer Reference Smoke

PURPOSE
-------
This script is a REFERENCE TEMPLATE for consuming repositories that wish to
verify they are reading a known-good version of the usb-if-hub-spec-reference
governed surface manifest (v0.3).

Consuming repositories SHOULD copy or adapt this script into their own CI
pipeline, pointing --repo-root at their pinned checkout of this reference repo.

WHAT THIS SCRIPT ASSERTS
------------------------
1. manifest_version_check   : manifest_version == "0.3"
2. table_count_check        : governed_tables count == 15
3. usb2_stats_check         : USB2 authority_surface tracked/verified/reviewed
4. usb3_stats_check         : USB3 authority_surface tracked=53 / verified=48 / reviewed=5
5. table_paths_exist_check  : all 15 governed table paths exist on disk

WHAT THIS SCRIPT DOES NOT ASSERT
---------------------------------
- Firmware behavior compliance of any kind
- USB-IF certification readiness
- LTSSM / xHCI / electrical / PHY behavior
- Reviewed entries as equivalent to verified
- Semantic correctness of any table entry
- That a consuming firmware repo has adopted this manifest

CLAIM CEILING
-------------
This template can establish:
  "The reference manifest v0.3 is structurally present and passes boundary
   assertions at the pinned checkout."

It CANNOT establish:
  "A consuming firmware repo is compliant with USB 3.2."
  "The downstream firmware correctly implements any governed behavior."
  "Consumer CI is integrated."

ADAPTING FOR A CONSUMING REPO
------------------------------
1. Copy this script into your consuming repo (e.g. scripts/smoke_usb_ref.py).
2. Pin usb-if-hub-spec-reference at commit 537319e (manifest v0.3).
3. Set REPO_ROOT to the absolute path of your pinned checkout.
4. Run: python smoke_usb_ref.py --repo-root /path/to/usb-if-hub-spec-reference

   Example CI snippet:
     git clone https://... usb_ref && git -C usb_ref checkout 537319e
     python scripts/smoke_usb_ref.py --repo-root usb_ref

5. Assert exit code == 0 before consuming any governed entry from the manifest.
6. Do NOT relax the non-claims above when adapting.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")


# ── Expected boundary constants ───────────────────────────────────────────────
# Update these when re-pinning to a newer manifest version.

EXPECTED_MANIFEST_VERSION = "0.3"
EXPECTED_TABLE_COUNT = 15

EXPECTED_USB2_STATS: dict[str, int] = {
    "tracked": 151,
    "verified": 105,
    "reviewed": 46,
}

EXPECTED_USB3_STATS: dict[str, int] = {
    "tracked": 53,
    "verified": 48,
    "reviewed": 5,
}

# ── Receipt output path (relative to repo root) ───────────────────────────────

_RECEIPT_REL = (
    "evidence/validation_receipts/consumer_reference_smoke"
    "/manifest_consumer_reference.json"
)


# ── Individual assertion cases ────────────────────────────────────────────────

def case_manifest_version_check(manifest: dict) -> dict:
    actual = manifest.get("manifest_version")
    passed = actual == EXPECTED_MANIFEST_VERSION
    return {
        "case": "manifest_version_check",
        "note": f"assert manifest_version == {EXPECTED_MANIFEST_VERSION!r}",
        "expected": EXPECTED_MANIFEST_VERSION,
        "actual": actual,
        "result": "PASS" if passed else "FAIL",
    }


def case_table_count_check(manifest: dict) -> dict:
    tables = manifest.get("governed_tables", [])
    actual = len(tables)
    passed = actual == EXPECTED_TABLE_COUNT
    result: dict = {
        "case": "table_count_check",
        "note": f"assert len(governed_tables) == {EXPECTED_TABLE_COUNT}",
        "expected": EXPECTED_TABLE_COUNT,
        "actual": actual,
        "result": "PASS" if passed else "FAIL",
    }
    if not passed:
        result["actual_table_ids"] = [t.get("id") for t in tables]
    return result


def case_usb2_stats_check(manifest: dict) -> dict:
    usb2 = manifest.get("authority_surface", {}).get("usb20", {})
    findings: list[str] = []
    for key, exp in EXPECTED_USB2_STATS.items():
        act = usb2.get(key)
        if act != exp:
            findings.append(f"{key}: expected {exp}, got {act}")
    passed = not findings
    result: dict = {
        "case": "usb2_stats_check",
        "note": "assert USB2 authority_surface tracked/verified/reviewed",
        "expected": EXPECTED_USB2_STATS,
        "actual": {k: usb2.get(k) for k in EXPECTED_USB2_STATS},
        "result": "PASS" if passed else "FAIL",
    }
    if findings:
        result["findings"] = findings
    return result


def case_usb3_stats_check(manifest: dict) -> dict:
    usb3 = manifest.get("authority_surface", {}).get("usb3", {})
    findings: list[str] = []
    for key, exp in EXPECTED_USB3_STATS.items():
        act = usb3.get(key)
        if act != exp:
            findings.append(f"{key}: expected {exp}, got {act}")
    passed = not findings
    result: dict = {
        "case": "usb3_stats_check",
        "note": "assert USB3 authority_surface tracked=53/verified=48/reviewed=5",
        "expected": EXPECTED_USB3_STATS,
        "actual": {k: usb3.get(k) for k in EXPECTED_USB3_STATS},
        "result": "PASS" if passed else "FAIL",
    }
    if findings:
        result["findings"] = findings
    return result


def case_table_paths_exist_check(manifest: dict, repo_root: Path) -> dict:
    tables = manifest.get("governed_tables", [])
    missing: list[str] = []
    for entry in tables:
        path_str = entry.get("path", "")
        if not (repo_root / path_str).exists():
            missing.append(path_str)
    passed = not missing
    result: dict = {
        "case": "table_paths_exist_check",
        "note": f"assert all {EXPECTED_TABLE_COUNT} governed table paths exist on disk",
        "tables_checked": len(tables),
        "result": "PASS" if passed else "FAIL",
    }
    if missing:
        result["missing_paths"] = missing
    return result


# ── Auto-detect repo root ─────────────────────────────────────────────────────

def _detect_repo_root() -> Path:
    """Walk up from this script to find the repo root (contains exports/hub_governed_surface_manifest.yaml)."""
    candidate = Path(__file__).resolve().parent
    for _ in range(5):
        if (candidate / "exports" / "hub_governed_surface_manifest.yaml").exists():
            return candidate
        candidate = candidate.parent
    # Fallback: one level above scripts/
    return Path(__file__).resolve().parents[1]


# ── Main ──────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="REFERENCE-CONSUMER-SMOKE-1: Manifest v0.3 consumer reference smoke"
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        metavar="PATH",
        help=(
            "Path to usb-if-hub-spec-reference checkout "
            "(default: auto-detect from script location)"
        ),
    )
    parser.add_argument(
        "--receipt-out",
        type=Path,
        default=None,
        metavar="PATH",
        help="Path to write JSON receipt (default: <repo-root>/" + _RECEIPT_REL + ")",
    )
    args = parser.parse_args(argv)

    repo_root = args.repo_root or _detect_repo_root()
    manifest_path = repo_root / "exports" / "hub_governed_surface_manifest.yaml"

    if not manifest_path.exists():
        print(f"[ERROR] manifest not found: {manifest_path}", file=sys.stderr)
        print(
            "  If running from a consuming repo, pass --repo-root pointing to "
            "your pinned usb-if-hub-spec-reference checkout.",
            file=sys.stderr,
        )
        return 2

    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))

    cases = [
        case_manifest_version_check(manifest),
        case_table_count_check(manifest),
        case_usb2_stats_check(manifest),
        case_usb3_stats_check(manifest),
        case_table_paths_exist_check(manifest, repo_root),
    ]

    failed = [c for c in cases if c["result"] == "FAIL"]

    receipt: dict = {
        "smoke_runner": "smoke_manifest_consumer_reference.py",
        "phase": "REFERENCE-CONSUMER-SMOKE-1",
        "authority_ceiling": "consumer_reference_template_only",
        "cannot_establish": [
            "consuming_repo_CI_integrated",
            "firmware_behavior_compliance",
            "USB_IF_certification_readiness",
            "LTSSM_xHCI_electrical_validation",
            "reviewed_entries_equivalent_to_verified",
        ],
        "ran_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "repo_root_used": str(repo_root),
        "manifest_path": str(manifest_path),
        "manifest_version_asserted": EXPECTED_MANIFEST_VERSION,
        "total_cases": len(cases),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": cases,
    }

    receipt_out = args.receipt_out or (repo_root / _RECEIPT_REL)
    receipt_out.parent.mkdir(parents=True, exist_ok=True)
    receipt_out.write_text(
        json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
    )

    # Human-readable output
    for c in cases:
        status = c["result"]
        note = c.get("note", c["case"])
        print(f"[{status}] {c['case']} — {note}")
        for finding in c.get("findings", []):
            print(f"  ! {finding}")
        for path in c.get("missing_paths", []):
            print(f"  ! missing: {path}")

    print()
    print("Authority ceiling : consumer_reference_template_only")
    print("Cannot establish  : consuming_repo_CI_integrated | firmware_behavior_compliance")
    print()

    if failed:
        print(
            f"Consumer reference smoke FAILED: "
            f"{len(failed)}/{len(cases)} cases failed"
        )
        return 1

    print(
        f"Consumer reference smoke PASSED: "
        f"{len(cases)}/{len(cases)} cases passed"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
