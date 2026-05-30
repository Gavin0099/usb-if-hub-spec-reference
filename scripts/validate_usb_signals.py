#!/usr/bin/env python3
"""Validate USB signal claim authority invariants.

Authority ceiling: claim_authority_invariants_only
- Checks structural claim/source/drift invariants; does not verify USB spec content.
- PASS does not imply USB-IF normative correctness.

Rules:
  R1  normative claim requires authority_level == normative_official
  R2  verified claim requires non-empty section_anchor
  R3  usb21 in usb_version_scope requires scope_role != base
  R4  usb4 in usb_version_scope with assumption_type == hub_class_equivalence is invalid (MVP)
  R5  drift_status == unresolved is incompatible with claim_level normative or verified
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SIGNAL_FILE = ROOT / "examples" / "sample_signal.json"

HIGH_CLAIM_LEVELS = {"normative", "verified"}
NORMATIVE_AUTHORITY = "normative_official"


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def _validate_signal(signal: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    def add_error(code: str, message: str) -> None:
        errors.append({"code": code, "message": message})

    sid = signal.get("signal_id", "<missing>")
    authority_level = signal.get("authority_level", "")
    claim_level = signal.get("claim_level", "")
    drift_status = signal.get("drift_status", "")
    usb_version_scope = signal.get("usb_version_scope", [])
    scope_role = signal.get("scope_role")
    assumption_type = signal.get("assumption_type")
    section_anchor = signal.get("section_anchor")

    # R1: normative claim must come from normative_official
    if claim_level == "normative" and authority_level != NORMATIVE_AUTHORITY:
        add_error(
            "NORMATIVE_CLAIM_REQUIRES_NORMATIVE_OFFICIAL",
            f"{sid}: claim_level 'normative' requires authority_level 'normative_official', "
            f"got '{authority_level}'",
        )

    # R2: verified claim must have section_anchor
    if claim_level == "verified" and not section_anchor:
        add_error(
            "VERIFIED_CLAIM_MISSING_SECTION_ANCHOR",
            f"{sid}: claim_level 'verified' requires a non-empty section_anchor",
        )

    # R3: USB 2.1 scope_role must not be base
    if "usb21" in usb_version_scope and scope_role == "base":
        add_error(
            "USB21_SCOPE_ROLE_MUST_NOT_BE_BASE",
            f"{sid}: usb21 in usb_version_scope requires scope_role != 'base' "
            "(usb21 is a delta, not a standalone base spec)",
        )

    # R4: USB4 + hub_class_equivalence is invalid at MVP
    if "usb4" in usb_version_scope and assumption_type == "hub_class_equivalence":
        add_error(
            "USB4_HUB_CLASS_EQUIVALENCE_INVALID",
            f"{sid}: usb4 scope with assumption_type 'hub_class_equivalence' is not supported "
            "until section-level evidence is registered",
        )

    # R5: unresolved drift is incompatible with normative/verified claim level
    if drift_status == "unresolved" and claim_level in HIGH_CLAIM_LEVELS:
        add_error(
            "UNRESOLVED_DRIFT_INCOMPATIBLE_WITH_CLAIM_LEVEL",
            f"{sid}: drift_status 'unresolved' is incompatible with claim_level '{claim_level}'",
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="path to a single signal JSON file")
    parser.add_argument("--dir", help="path to a directory of signal JSON files")
    parser.add_argument("--receipt-out", help="write machine-readable receipt JSON")
    args = parser.parse_args()

    if args.dir:
        signal_dir = Path(args.dir) if Path(args.dir).is_absolute() else ROOT / args.dir
        signal_files = sorted(signal_dir.glob("*.json"))
    elif args.file:
        signal_files = [Path(args.file) if Path(args.file).is_absolute() else ROOT / args.file]
    else:
        signal_files = [DEFAULT_SIGNAL_FILE]

    all_errors: list[dict[str, str]] = []
    checked_signals: list[str] = []

    for signal_path in signal_files:
        try:
            signal = _load_json(signal_path)
        except Exception as e:
            all_errors.append({
                "code": "SIGNAL_LOAD_ERROR",
                "message": f"{signal_path.name}: failed to load — {e}",
            })
            continue

        if not isinstance(signal, dict):
            all_errors.append({
                "code": "SIGNAL_NOT_OBJECT",
                "message": f"{signal_path.name}: signal must be a JSON object",
            })
            continue

        checked_signals.append(signal.get("signal_id", signal_path.name))
        errors = _validate_signal(signal)
        all_errors.extend(errors)

    passed = len(all_errors) == 0
    receipt = {
        "validator": "validate_usb_signals.py",
        "authority_ceiling": "claim_authority_invariants_only",
        "note": (
            "PASS does not imply USB-IF normative content correctness. "
            "Checks structural claim/source/drift invariants only."
        ),
        "result": "PASS" if passed else "FAIL",
        "checked_signals": checked_signals,
        "error_count": len(all_errors),
        "errors": all_errors,
        "findings": all_errors,
    }

    if args.receipt_out:
        receipt_path = (
            Path(args.receipt_out) if Path(args.receipt_out).is_absolute()
            else ROOT / args.receipt_out
        )
        _write_receipt(receipt_path, receipt)

    if not passed:
        print("Signal authority validation FAILED")
        for e in all_errors:
            print(f"- [{e['code']}] {e['message']}")
        return 1

    print("Signal authority validation PASSED")
    print(f"- checked signals: {len(checked_signals)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
