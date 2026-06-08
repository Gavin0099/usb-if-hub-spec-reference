#!/usr/bin/env python3
"""Validate the unified hub governed surface manifest.

Authority ceiling: manifest_structural_integrity_only.
Does not re-validate table contents — use per-table validators for that.

Checks:
  R1  manifest_id present
  R2  governed_tables list not empty
  R3  each entry has id, spec_family, path, state
  R4  each table path exists on disk
  R5  spec_family must be usb20 or usb3
  R6  state must be a known value (freeze, matrix_level_closeout)
  R7  entry ids unique
  R8  per-family verified/reviewed sums match authority_surface summary
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "exports" / "hub_governed_surface_manifest.yaml"

VALID_SPEC_FAMILIES = {"usb20", "usb3"}
VALID_STATES = {"freeze", "matrix_level_closeout", "partial_verified"}


def main() -> int:
    if not MANIFEST_PATH.exists():
        print(f"FAIL: manifest not found: {MANIFEST_PATH}")
        return 1

    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}

    errors: list[str] = []

    # R1
    if not doc.get("manifest_id"):
        errors.append("R1: manifest_id missing or empty")

    entries = doc.get("governed_tables") or []

    # R2
    if not entries:
        errors.append("R2: governed_tables list missing or empty")

    seen_ids: set[str] = set()
    family_verified: dict[str, int] = {}
    family_reviewed: dict[str, int] = {}

    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"R3: entry[{i}] is not a dict")
            continue

        eid = entry.get("id", f"<entry[{i}]>")

        # R7
        if eid in seen_ids:
            errors.append(f"R7: duplicate entry id {eid!r}")
        seen_ids.add(eid)

        # R3
        for fld in ("id", "spec_family", "path", "state"):
            if fld not in entry:
                errors.append(f"R3: entry {eid!r} missing required field '{fld}'")

        # R4
        raw_path = entry.get("path", "")
        tpath = ROOT / raw_path
        if raw_path and not tpath.exists():
            errors.append(f"R4: entry {eid!r} path does not exist: {tpath}")

        # R5
        sf = entry.get("spec_family", "")
        if sf not in VALID_SPEC_FAMILIES:
            errors.append(f"R5: entry {eid!r} spec_family {sf!r} not in {VALID_SPEC_FAMILIES}")

        # R6
        st = entry.get("state", "")
        if st not in VALID_STATES:
            errors.append(f"R6: entry {eid!r} state {st!r} not in {VALID_STATES}")

        # Accumulate for R8
        if sf in VALID_SPEC_FAMILIES:
            family_verified[sf] = family_verified.get(sf, 0) + int(entry.get("verified", 0))
            family_reviewed[sf] = family_reviewed.get(sf, 0) + int(entry.get("reviewed", 0))

    # R8 — cross-check sums against authority_surface
    authority = doc.get("authority_surface") or {}
    for sf in VALID_SPEC_FAMILIES:
        surface = authority.get(sf) or {}
        expected_verified = surface.get("verified")
        expected_reviewed = surface.get("reviewed")
        actual_verified = family_verified.get(sf, 0)
        actual_reviewed = family_reviewed.get(sf, 0)

        if expected_verified is not None and actual_verified != expected_verified:
            errors.append(
                f"R8: {sf} verified sum mismatch: "
                f"authority_surface.verified={expected_verified}, "
                f"governed_tables sum={actual_verified}"
            )
        if expected_reviewed is not None and actual_reviewed != expected_reviewed:
            errors.append(
                f"R8: {sf} reviewed sum mismatch: "
                f"authority_surface.reviewed={expected_reviewed}, "
                f"governed_tables sum={actual_reviewed}"
            )

    if errors:
        print("FAIL: hub_governed_surface_manifest validation")
        for e in errors:
            print(f"  {e}")
        return 1

    usb20_tables = [e for e in entries if e.get("spec_family") == "usb20"]
    usb3_tables = [e for e in entries if e.get("spec_family") == "usb3"]
    print("PASS: hub_governed_surface_manifest validation")
    print(f"  manifest_id: {doc.get('manifest_id')}")
    print(f"  governed_tables: {len(entries)} "
          f"(usb20={len(usb20_tables)}, usb3={len(usb3_tables)})")
    auth = doc.get("authority_surface") or {}
    for sf in ("usb20", "usb3"):
        s = auth.get(sf) or {}
        print(f"  {sf}: state={s.get('state')} "
              f"tracked={s.get('tracked')} "
              f"verified={s.get('verified')} "
              f"reviewed={s.get('reviewed')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
