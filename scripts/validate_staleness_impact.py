#!/usr/bin/env python3
"""Evaluate staleness impact of USB-IF source drift on wiki claim levels.

Authority ceiling: drift_to_claim_level_impact_only

Reads:
  contract/staleness_rules.yaml
  evidence/source_registry.yaml
  evidence/drift_events.jsonl
  wiki/**/*.md (frontmatter)

Rules:
  R1  unresolved normative_official drift + wiki source_ref + claim_level normative/verified
      → structural_fail (staleness_rules.yaml: claim_level_max = provisional)
  R2  unresolved official_index drift + normative wiki claim
      → advisory only (claim_level_max = verified, not normative; no structural fail)
  R3  community_reference / archive_fallback drift → no impact on any claim level
  R4  resolved drift (resolution_status != unresolved) → no impact

Non-goals:
  - Does not fetch USB-IF sources.
  - Does not create new drift events.
  - Does not parse PDF contents.
  - Does not semantically compare spec sections.
  - Does not automatically edit wiki claim_level.
  - Does not resolve drift events.
  - Does not extract USB descriptor/request/status tables.
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
DEFAULT_DRIFT_EVENTS = ROOT / "evidence" / "drift_events.jsonl"
DEFAULT_SOURCE_REGISTRY = ROOT / "evidence" / "source_registry.yaml"
DEFAULT_STALENESS_RULES = ROOT / "contract" / "staleness_rules.yaml"
DEFAULT_WIKI_DIR = ROOT / "wiki"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
HIGH_CLAIM_LEVELS = {"normative", "verified"}
CLAIM_LEVEL_RANK = {"normative": 100, "verified": 80, "inferred": 60, "provisional": 40, "draft": 20, "rejected": 0}
UNRESOLVED_STATUS = "unresolved"


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            events.append(json.loads(line))
    return events


def _parse_frontmatter(path: Path) -> dict[str, Any] | None:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    return yaml.safe_load(m.group(1)) if m else None


def _build_source_authority_map(registry: dict) -> dict[str, str]:
    return {s["source_id"]: s["authority_level"] for s in registry.get("sources", [])}


def _build_unresolved_drift_map(events: list[dict]) -> dict[str, list[dict]]:
    unresolved: dict[str, list[dict]] = {}
    for e in events:
        if e.get("resolution_status", UNRESOLVED_STATUS) == UNRESOLVED_STATUS:
            sid = e.get("source_id", "")
            unresolved.setdefault(sid, []).append(e)
    return unresolved


def _build_staleness_policy(rules: dict) -> dict[str, dict]:
    """Build map of authority_level → {impact_type, effect}.

    impact_type 'structural' → compare claim_level_max; fail if exceeded.
    impact_type 'advisory'   → always advisory, never structural fail.
    Absent entry             → no impact.
    """
    policy: dict[str, dict] = {}
    for _rule_name, rule in rules.get("staleness_rules", {}).items():
        impact_type = rule.get("impact_type", "structural")
        effect = rule.get("effect", {})
        for level in rule.get("applies_to_authority_levels", []):
            policy[level] = {"impact_type": impact_type, "effect": effect}
    return policy


def _evaluate_page(
    path: Path,
    source_authority: dict[str, str],
    unresolved_drift: dict[str, list[dict]],
    staleness_policy: dict[str, dict],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    fm = _parse_frontmatter(path)
    if not fm or not isinstance(fm, dict):
        return results

    page_claim_level = fm.get("claim_level", "")
    page_source_refs = fm.get("source_refs", [])
    if not isinstance(page_source_refs, list):
        page_source_refs = []

    for source_ref in page_source_refs:
        authority_level = source_authority.get(source_ref)
        if not authority_level:
            continue

        drift_events = unresolved_drift.get(source_ref, [])
        if not drift_events:
            continue

        policy = staleness_policy.get(authority_level)
        if not policy:
            continue  # no staleness rule for this authority_level → no impact

        impact_type = policy.get("impact_type", "structural")
        effect = policy.get("effect", {})
        max_claim_level = effect.get("claim_level_max", "provisional")
        max_rank = CLAIM_LEVEL_RANK.get(max_claim_level, 0)
        current_rank = CLAIM_LEVEL_RANK.get(page_claim_level, 0)

        if impact_type == "advisory":
            results.append({
                "page": path.name,
                "page_path": str(path),
                "source_ref": source_ref,
                "source_authority_level": authority_level,
                "current_claim_level": page_claim_level,
                "drift_event_count": len(drift_events),
                "impact": "advisory",
                "reason": (
                    f"source '{source_ref}' (authority: {authority_level}) has unresolved drift; "
                    "advisory only — does not block this claim level"
                ),
            })
        elif impact_type == "structural" and current_rank > max_rank:
            results.append({
                "page": path.name,
                "page_path": str(path),
                "source_ref": source_ref,
                "source_authority_level": authority_level,
                "current_claim_level": page_claim_level,
                "max_allowed_claim_level": max_claim_level,
                "drift_event_count": len(drift_events),
                "impact": "structural_fail",
                "reason": (
                    f"claim_level '{page_claim_level}' exceeds max allowed '{max_claim_level}' "
                    f"due to unresolved drift on '{source_ref}' (authority: {authority_level})"
                ),
            })

    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--drift-events", default=str(DEFAULT_DRIFT_EVENTS))
    parser.add_argument("--source-registry", default=str(DEFAULT_SOURCE_REGISTRY))
    parser.add_argument("--staleness-rules", default=str(DEFAULT_STALENESS_RULES))
    parser.add_argument("--wiki-dir", help="wiki directory (default: wiki/)")
    parser.add_argument("--wiki-file", help="single wiki page to validate")
    parser.add_argument("--receipt-out")
    args = parser.parse_args()

    def resolve(p: str, fallback: Path) -> Path:
        q = Path(p)
        return q if q.is_absolute() else ROOT / q

    drift_path = resolve(args.drift_events, DEFAULT_DRIFT_EVENTS)
    registry_path = resolve(args.source_registry, DEFAULT_SOURCE_REGISTRY)
    rules_path = resolve(args.staleness_rules, DEFAULT_STALENESS_RULES)

    registry = _load_yaml(registry_path)
    rules = _load_yaml(rules_path)
    events = _load_jsonl(drift_path)

    source_authority = _build_source_authority_map(registry)
    unresolved_drift = _build_unresolved_drift_map(events)
    staleness_policy = _build_staleness_policy(rules)

    if args.wiki_file:
        wf = Path(args.wiki_file)
        pages = [wf if wf.is_absolute() else ROOT / wf]
    else:
        wiki_dir = Path(args.wiki_dir) if args.wiki_dir else DEFAULT_WIKI_DIR
        wiki_dir = wiki_dir if wiki_dir.is_absolute() else ROOT / wiki_dir
        pages = sorted(p for p in wiki_dir.rglob("*.md") if p.name != "index.md")

    all_results: list[dict] = []
    checked_pages: list[str] = []

    for page in pages:
        checked_pages.append(page.name)
        results = _evaluate_page(page, source_authority, unresolved_drift, staleness_policy)
        all_results.extend(results)

    structural_fails = [r for r in all_results if r["impact"] == "structural_fail"]
    advisories = [r for r in all_results if r["impact"] == "advisory"]
    passed = len(structural_fails) == 0

    receipt = {
        "validator": "validate_staleness_impact.py",
        "authority_ceiling": "drift_to_claim_level_impact_only",
        "does_not_fetch_network": True,
        "does_not_parse_pdf": True,
        "does_not_modify_wiki": True,
        "uses_observed_drift_events": True,
        "time_bound": True,
        "result": "PASS" if passed else "FAIL",
        "checked_pages": checked_pages,
        "total_unresolved_drift_sources": len(unresolved_drift),
        "structural_fail_count": len(structural_fails),
        "advisory_count": len(advisories),
        "structural_fails": structural_fails,
        "advisories": advisories,
        "findings": all_results,
    }

    if args.receipt_out:
        rp = Path(args.receipt_out)
        rp = rp if rp.is_absolute() else ROOT / rp
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    if not passed:
        print("Staleness impact validation FAILED")
        for r in structural_fails:
            print(f"- [structural_fail] {r['page']}: {r['reason']}")
    else:
        print("Staleness impact validation PASSED")
        print(f"- checked pages: {len(checked_pages)}")
        print(f"- unresolved drift sources: {len(unresolved_drift)}")

    if advisories:
        print(f"- {len(advisories)} advisory finding(s):")
        for a in advisories:
            print(f"  ~ [advisory] {a['page']}: {a['reason']}")

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
