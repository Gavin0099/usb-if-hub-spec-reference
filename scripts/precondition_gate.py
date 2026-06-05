#!/usr/bin/env python3
"""Emit the entry verification precondition gate as a reusable artifact.

This is the non-smoke execution path for verified-entry promotion preconditions.
It runs the same validator logic as `validate_entry_verification_gate.py` but
writes a structured artifact for downstream audit and CI evidence.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from validate_entry_verification_gate import DEFAULT_MATRICES, ROOT, validate


DEFAULT_RECEIPT = ROOT / "evidence" / "validation_receipt_precondition_gate.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, action="append", default=None, help="Path to a governed table matrix YAML")
    parser.add_argument(
        "--packet-dir",
        type=Path,
        default=ROOT / "evidence" / "entry_verification_packets",
    )
    parser.add_argument("--receipt-out", type=Path, default=DEFAULT_RECEIPT)
    args = parser.parse_args()

    matrix_paths = args.matrix if args.matrix else list(DEFAULT_MATRICES)
    result, errors = validate(matrix_paths, args.packet_dir)

    print(f"\nEntry verification precondition gate {result}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        payload: dict[str, object] = {
            "artifact_type": "precondition_gate",
            "validator": "validate_entry_verification_gate",
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "matrices": [str(p) for p in matrix_paths],
            "packet_dir": str(args.packet_dir),
            "result": result,
            "errors": errors,
            "authority_ceiling": "entry_level_verified_gate_only",
        }
        args.receipt_out.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
