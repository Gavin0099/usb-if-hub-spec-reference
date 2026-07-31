#!/usr/bin/env python3
"""Read-only canonical projection pilot (contract.yaml P1 precondition).

Reads all 15 governed tables listed in
``exports/hub_governed_surface_manifest.yaml`` and projects each entry into a
three-column canonical view: ``entry_id``, ``claim_level``, ``source_ref``.

REPORT MODE ONLY. Per the 2026-07-31 governance review round 1 (commit
6ff1c56, finding 3 [WARNING] "不要直接 migration 15 張表"), this script does
not modify any of the 15 original tables. It exists to prove — or disprove —
that a lossless three-column projection is possible before any real schema
unification is attempted.

Tables whose identity/source-ref convention isn't recognized by the generic
heuristic are handled through an explicit, reviewed adapter registered in
``contract/projection_adapters.yaml`` instead of a silent guess or a bulk
edit of the original table. This addresses governance review round 2
(commit 6ff1c56, findings 1/2 [BLOCKING]):

  1. A table can have a stable, unique per-entry identity even without a
     dedicated ``*_id`` field, if an existing validator/evidence-packet
     convention already defines one (e.g. ``{field}.bit{bit}.{name}`` for
     ``port_status_bit_matrix.yaml``). Adapters encode that convention
     explicitly instead of the generic script guessing a different one.
  2. ``source_ref`` (a normative spec source ID) must never be silently
     replaced by an evidence-packet path or free-text evidence description.
     Those are kept in a separate ``evidence_ref`` field so normative source,
     section anchor, and verification evidence stay distinguishable.

Any row that still cannot get a governed identity/source_ref (no adapter,
no recognized field) is emitted with an explicit gap flag rather than
silently coerced. This script does not decide whether migration should
proceed; it only measures the gap and validates the adapters it has.

Usage:
    python scripts/probe_canonical_entry_projection.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "exports" / "hub_governed_surface_manifest.yaml"
ADAPTERS_PATH = REPO_ROOT / "contract" / "projection_adapters.yaml"
SOURCE_REGISTRY_PATH = REPO_ROOT / "evidence" / "source_registry.yaml"
OUTPUT_PATH = (
    REPO_ROOT / "artifacts" / "governance" / "canonical_entry_projection_report.json"
)

# Identity key field names observed across the 15 governed tables, in
# priority order. Not every table uses the same name (this inconsistency is
# exactly what P1 is measuring).
IDENTITY_KEY_CANDIDATES = [
    "field_id",
    "trigger_id",
    "selector_id",
    "request_id",
    "tt_id",
    "id",
]


def load_adapters() -> dict[str, dict[str, Any]]:
    if not ADAPTERS_PATH.exists():
        return {}
    doc = yaml.safe_load(ADAPTERS_PATH.read_text(encoding="utf-8")) or {}
    return doc.get("adapters", {}) or {}


def load_registered_source_ids() -> set[str]:
    if not SOURCE_REGISTRY_PATH.exists():
        return set()
    doc = yaml.safe_load(SOURCE_REGISTRY_PATH.read_text(encoding="utf-8")) or {}
    return {s.get("source_id") for s in doc.get("sources", []) or [] if s.get("source_id")}


def resolve_entry_id(
    entry: dict[str, Any], table_id: str, index: int, adapter: dict[str, Any] | None
) -> tuple[str, bool, str]:
    """Return (entry_id, was_synthesized_without_governed_rule, source_label)."""
    identity = (adapter or {}).get("identity")
    if identity and identity.get("strategy") == "composite":
        fields = identity.get("fields", [])
        fmt = identity.get("format", "")
        values = {f: entry.get(f) for f in fields}
        if all(v is not None for v in values.values()):
            return fmt.format(**values), False, "adapter:composite"

    for key in IDENTITY_KEY_CANDIDATES:
        value = entry.get(key)
        if value:
            return str(value), False, f"field:{key}"

    # No recognized identity key and no adapter covers this row — this is a
    # real gap, not a governed convention. Synthesize a best-effort value so
    # the report still shows every row, but flag it plainly.
    parts = [str(entry[k]) for k in ("field", "bit", "name") if entry.get(k) is not None]
    if parts:
        return f"{table_id}::{'.'.join(parts)}", True, "ungoverned_synthesis"
    return f"{table_id}::entry_{index}", True, "ungoverned_synthesis"


def resolve_claim_level(
    entry: dict[str, Any], table_default: str | None
) -> tuple[str | None, bool]:
    """Return (claim_level, was_defaulted_from_table_level)."""
    value = entry.get("claim_level")
    if value:
        return value, False
    if table_default:
        return table_default, True
    return None, True


def resolve_source_ref(
    entry: dict[str, Any], adapter: dict[str, Any] | None
) -> tuple[str | None, bool, str | None]:
    """Return (source_ref, is_gap, evidence_ref).

    ``source_ref`` is only ever a normative spec source ID (a
    ``source_registry.yaml`` ``source_id``, or the raw ``source_refs``/
    ``source_ref`` field already on the entry). Evidence-packet paths or
    free-text evidence descriptions are returned separately as
    ``evidence_ref`` and are never substituted for ``source_ref`` — that
    conflation was governance review round 2 finding 2 [BLOCKING].
    """
    source_rule = (adapter or {}).get("source")
    if source_rule and source_rule.get("strategy") == "section_spec_mapping":
        wanted_spec = source_rule.get("section_spec")
        for ref in entry.get("section_refs") or []:
            if isinstance(ref, dict) and ref.get("spec") == wanted_spec:
                return source_rule.get("source_ref"), False, None
        # Adapter registered for this table but this specific row didn't
        # match the expected section spec — a real gap, not covered by the
        # adapter's stated evidence.
        return None, True, None

    refs = entry.get("source_refs")
    if refs:
        return (",".join(refs) if isinstance(refs, list) else str(refs)), False, None
    ref = entry.get("source_ref")
    if ref:
        return str(ref), False, None

    evidence_ref = None
    evidence = entry.get("evidence")
    if isinstance(evidence, dict):
        if evidence.get("verification_packet"):
            evidence_ref = f"evidence_packet:{evidence['verification_packet']}"
        elif evidence.get("source"):
            evidence_ref = f"evidence_source_text:{evidence['source']}"
    return None, True, evidence_ref


def project_table(
    table: dict[str, Any], adapters: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    table_id = table["id"]
    table_path = REPO_ROOT / table["path"]
    data = yaml.safe_load(table_path.read_text(encoding="utf-8")) or {}
    entries = data.get("entries", []) or []
    table_default_claim_level = data.get("claim_level")

    # Adapters are keyed by manifest table id (e.g.
    # usb20_hub_port_status_bit_matrix), matching hub_governed_surface_manifest.yaml.
    adapter = adapters.get(table_id)

    rows: list[dict[str, Any]] = []
    synthesized_count = 0
    defaulted_claim_count = 0
    source_gap_count = 0

    for index, entry in enumerate(entries):
        entry_id, id_synthesized, id_source = resolve_entry_id(entry, table_id, index, adapter)
        claim_level, claim_defaulted = resolve_claim_level(entry, table_default_claim_level)
        source_ref, source_gap, evidence_ref = resolve_source_ref(entry, adapter)

        if id_synthesized:
            synthesized_count += 1
        if claim_defaulted:
            defaulted_claim_count += 1
        if source_gap:
            source_gap_count += 1

        rows.append(
            {
                "entry_id": entry_id,
                "claim_level": claim_level,
                "source_ref": source_ref,
                "evidence_ref": evidence_ref,
                "gaps": {
                    "identity_key_ungoverned": id_synthesized,
                    "claim_level_defaulted_from_table": claim_defaulted,
                    "source_ref_gap": source_gap,
                },
                "identity_source": id_source,
            }
        )

    return {
        "table_id": table_id,
        "path": table["path"],
        "spec_family": table.get("spec_family"),
        "adapter_applied": adapter is not None,
        "entry_count": len(entries),
        "identity_key_ungoverned_count": synthesized_count,
        "claim_level_defaulted_count": defaulted_claim_count,
        "source_ref_gap_count": source_gap_count,
        "rows": rows,
    }


def validate_adapters(
    adapters: dict[str, dict[str, Any]],
    projected_by_table_id: dict[str, dict[str, Any]],
    registered_source_ids: set[str],
) -> list[dict[str, Any]]:
    """Self-validate each registered adapter against its projected rows.

    Checks (per governance review round 2's explicit ask):
      - all generated composite IDs for the adapted table are unique
      - the adapter's source_ref is a registered source_id
      - every existing evidence-packet target.entry_id for the table's
        evidence_packet_glob matches one of the generated IDs (format
        consistency; packets need not cover every entry)
    """
    results: list[dict[str, Any]] = []

    for table_id, adapter in adapters.items():
        projected = projected_by_table_id.get(table_id)
        checks: dict[str, Any] = {}

        if projected is None:
            checks["table_found_in_manifest"] = False
            results.append({"table_id": table_id, "checks": checks, "passed": False})
            continue
        checks["table_found_in_manifest"] = True

        ids = [row["entry_id"] for row in projected["rows"]]
        checks["identity_count"] = len(ids)
        checks["identity_unique_count"] = len(set(ids))
        checks["all_ids_unique"] = len(ids) == len(set(ids))

        source_ref = (adapter.get("source") or {}).get("source_ref")
        checks["source_ref"] = source_ref
        checks["source_ref_registered"] = source_ref in registered_source_ids

        glob_pattern = adapter.get("evidence_packet_glob")
        if glob_pattern:
            packet_ids: set[str] = set()
            for path in REPO_ROOT.glob(glob_pattern):
                packet_doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
                target = packet_doc.get("target") or {}
                entry_id = target.get("entry_id")
                if entry_id:
                    packet_ids.add(str(entry_id))
            checks["evidence_packet_count"] = len(packet_ids)
            checks["evidence_packets_matching_projection"] = len(packet_ids & set(ids))
            checks["evidence_packets_not_matching_projection"] = sorted(packet_ids - set(ids))
            checks["evidence_packet_format_consistent"] = not checks[
                "evidence_packets_not_matching_projection"
            ]
        else:
            checks["evidence_packet_format_consistent"] = None

        passed = (
            checks["all_ids_unique"]
            and checks["source_ref_registered"]
            and checks["evidence_packet_format_consistent"] is not False
        )
        results.append({"table_id": table_id, "checks": checks, "passed": passed})

    return results


def main() -> int:
    manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    tables = manifest.get("governed_tables", [])
    adapters = load_adapters()
    registered_source_ids = load_registered_source_ids()

    projected_tables = [project_table(table, adapters) for table in tables]
    projected_by_table_id = {t["table_id"]: t for t in projected_tables}

    adapter_validation = validate_adapters(adapters, projected_by_table_id, registered_source_ids)
    adapter_validation_passed = all(r["passed"] for r in adapter_validation)

    total_entries = sum(t["entry_count"] for t in projected_tables)
    total_ungoverned_id = sum(t["identity_key_ungoverned_count"] for t in projected_tables)
    total_default_claim = sum(t["claim_level_defaulted_count"] for t in projected_tables)
    total_source_gap = sum(t["source_ref_gap_count"] for t in projected_tables)

    report = {
        "report_id": "canonical_entry_projection_pilot",
        "mode": "report_only_read_only",
        "modifies_original_tables": False,
        "origin": (
            "governance review commit 6ff1c56, round 1 finding 3 [WARNING] + "
            "round 2 findings 1/2 [BLOCKING]"
        ),
        "manifest_source": "exports/hub_governed_surface_manifest.yaml",
        "adapters_source": "contract/projection_adapters.yaml",
        "summary": {
            "table_count": len(projected_tables),
            "total_entries": total_entries,
            "total_identity_key_ungoverned": total_ungoverned_id,
            "total_claim_level_defaulted": total_default_claim,
            "total_source_ref_gaps": total_source_gap,
            "adapter_validation_passed": adapter_validation_passed,
            "lossless_projection": (
                total_ungoverned_id == 0
                and total_default_claim == 0
                and total_source_gap == 0
                and adapter_validation_passed
            ),
        },
        "adapter_validation": adapter_validation,
        "tables": projected_tables,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    summary = report["summary"]
    print("Canonical entry projection pilot — report_only, no tables modified.")
    print(f"Tables: {summary['table_count']}  Entries: {summary['total_entries']}")
    print(f"Ungoverned/synthesized identity keys: {summary['total_identity_key_ungoverned']}")
    print(f"Claim levels defaulted from table-level: {summary['total_claim_level_defaulted']}")
    print(f"Source-ref gaps: {summary['total_source_ref_gaps']}")
    for result in adapter_validation:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"Adapter [{result['table_id']}]: {status} — {result['checks']}")
    print(f"Lossless 3-column projection: {summary['lossless_projection']}")
    print(f"Full report written to: {OUTPUT_PATH.relative_to(REPO_ROOT)}")

    if not summary["lossless_projection"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
