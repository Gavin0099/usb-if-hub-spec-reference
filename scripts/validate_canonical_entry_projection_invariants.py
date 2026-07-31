#!/usr/bin/env python3
"""Enforce canonical entry projection losslessness + export freshness (P2').

This is a GATE, not a report. It fails if either:

  (a) PROJECTION_NOT_LOSSLESS — the live three-column projection
      (entry_id / claim_level / source_ref) over the 15 governed tables is
      no longer lossless: an adapter broke, or a table lost the
      identity/claim/source-ref convention the projection relies on. Same
      check as scripts/probe_canonical_entry_projection.py's own exit code,
      re-run here as a named, receipted invariant.

  (b) EXPORT_STALE / EXPORT_MISSING — the committed
      exports/canonical_entry_index.yaml no longer matches a fresh
      regeneration from the current governed tables and
      contract/projection_adapters.yaml. This is the actual drift gate: if
      someone edits a governed table or an adapter and forgets to
      regenerate the export, this fails even though the projection itself
      might still be lossless.

This validator never modifies any governed table or the export; it only
measures drift between the governed tables (source of truth) and the
derivative export. Regenerate the export with
scripts/export_canonical_entry_index.py, then re-run this validator.

Usage:
    python scripts/validate_canonical_entry_projection_invariants.py
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

from export_canonical_entry_index import EXPORT_PATH, build_export

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_committed_export(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def validate(export_path: Path = EXPORT_PATH) -> tuple[str, list[str]]:
    errors: list[str] = []
    live = build_export()

    if not live["invariants"]["lossless_projection"]:
        errors.append(
            "PROJECTION_NOT_LOSSLESS: live projection over the governed "
            f"tables is no longer lossless: {live['invariants']}"
        )

    committed = _load_committed_export(export_path)
    if committed is None:
        errors.append(
            f"EXPORT_MISSING: {export_path} does not exist; run "
            "scripts/export_canonical_entry_index.py and commit the result."
        )
    elif committed != live:
        errors.append(
            "EXPORT_STALE: exports/canonical_entry_index.yaml no longer "
            "matches a fresh regeneration of the governed tables/adapters; "
            "run scripts/export_canonical_entry_index.py and commit the result."
        )

    return ("FAIL" if errors else "PASS"), errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export", type=Path, default=EXPORT_PATH)
    parser.add_argument("--receipt-out", type=Path, default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result, errors = validate(args.export)

    for e in errors:
        print(f"[FAIL] {e}")
    print(f"\nCanonical entry projection invariants: {result}")

    if args.receipt_out:
        receipt = {
            "validator": "validate_canonical_entry_projection_invariants",
            "authority_ceiling": "derivative_export_freshness_only",
            "result": result,
            "errors": errors,
        }
        try:
            args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
            args.receipt_out.write_text(
                json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
            )
        except OSError as exc:
            # Keep receipt-write I/O failures out of the PASS/FAIL exit-code
            # space (0/1) — see scripts/validate_entry_verification_gate.py.
            print(f"[RECEIPT_WRITE_ERROR] failed to write receipt to {args.receipt_out}: {exc}", file=sys.stderr)
            return 2

    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
