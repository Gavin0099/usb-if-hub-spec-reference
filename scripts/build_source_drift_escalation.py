#!/usr/bin/env python3
"""Build an operator-facing report for unresolved source drift events.

Authority ceiling: source_drift_escalation_observation_only.

This report classifies existing drift events for review. It does not fetch
sources, compare semantic content, modify claims, or create GitHub issues.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DRIFT_EVENTS = ROOT / "evidence" / "drift_events.jsonl"
DEFAULT_SOURCE_REGISTRY = ROOT / "evidence" / "source_registry.yaml"
DEFAULT_STALENESS_RULES = ROOT / "contract" / "staleness_rules.yaml"


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a YAML object")
    return data


def _load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines() if path.exists() else []:
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path} contains a non-object event")
            events.append(value)
    return events


def _resolve(path_arg: str | None, fallback: Path) -> Path:
    if not path_arg:
        return fallback
    path = Path(path_arg)
    return path if path.is_absolute() else ROOT / path


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def _write_summary(path: Path, receipt: dict[str, Any]) -> None:
    lines = [
        "## Source Drift Escalation",
        "",
        f"- Status: **{receipt['status']}**",
        f"- Unresolved events: {receipt['unresolved_event_count']}",
        f"- Blocking review signals: {receipt['blocking_review_count']}",
        f"- Advisory review signals: {receipt['advisory_review_count']}",
        "",
        "This is observation-only output. It does not change claim levels or create issues.",
    ]
    for finding in receipt["findings"]:
        lines.extend(
            [
                "",
                f"- `{finding['code']}` `{finding['source_id']}`: {finding['required_action']}",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--drift-events")
    parser.add_argument("--source-registry")
    parser.add_argument("--staleness-rules")
    parser.add_argument("--receipt-out")
    parser.add_argument("--summary-out")
    args = parser.parse_args()

    drift_path = _resolve(args.drift_events, DEFAULT_DRIFT_EVENTS)
    source_path = _resolve(args.source_registry, DEFAULT_SOURCE_REGISTRY)
    rules_path = _resolve(args.staleness_rules, DEFAULT_STALENESS_RULES)
    source_doc = _load_yaml(source_path)
    rules_doc = _load_yaml(rules_path)
    source_map = {
        source.get("source_id"): source.get("authority_level")
        for source in source_doc.get("sources", [])
        if isinstance(source, dict) and source.get("source_id")
    }
    policy_by_authority: dict[str, dict[str, Any]] = {}
    for rule in rules_doc.get("staleness_rules", {}).values():
        for authority in rule.get("applies_to_authority_levels", []):
            policy_by_authority[authority] = rule

    findings: list[dict[str, Any]] = []
    unresolved_count = 0
    blocking_count = 0
    advisory_count = 0
    errors: list[str] = []
    for event in _load_events(drift_path):
        source_id = event.get("source_id", "<missing>")
        if event.get("resolution_status", "unresolved") != "unresolved":
            continue
        unresolved_count += 1
        authority = source_map.get(source_id)
        if authority is None:
            code = "DRIFT_SOURCE_UNREGISTERED"
            action = "registry error: register the source before interpreting drift"
            errors.append(f"{source_id}: unresolved drift source is not registered")
        else:
            rule = policy_by_authority.get(authority, {})
            impact_type = rule.get("impact_type", "advisory")
            if authority == "normative_official" and impact_type == "structural":
                code = "NORMATIVE_DRIFT_ESCALATION"
                action = "blocking review: stop new normative claims and review dependent claims"
                blocking_count += 1
            elif impact_type == "advisory":
                code = "OFFICIAL_INDEX_DRIFT_ADVISORY"
                action = "advisory review: inspect affected references; no automatic claim block"
                advisory_count += 1
            elif impact_type == "structural":
                code = "STRUCTURAL_DRIFT_REVIEW_REQUIRED"
                action = "review required: apply the configured staleness rule before claim use"
                blocking_count += 1
            else:
                code = "DRIFT_NO_ESCALATION_RULE"
                action = "review registry policy: no configured escalation rule applies"
                errors.append(f"{source_id}: no escalation rule for authority '{authority}'")
        findings.append(
            {
                "code": code,
                "source_id": source_id,
                "authority_level": authority,
                "event_id": event.get("event_id"),
                "required_action": action,
                "observation_only": True,
                "does_not_change_claim_level": True,
            }
        )

    if errors:
        status = "ERROR"
    elif blocking_count:
        status = "ESCALATION_REQUIRED"
    elif advisory_count:
        status = "ADVISORY"
    else:
        status = "CLEAR"
    receipt = {
        "validator": "build_source_drift_escalation.py",
        "authority_ceiling": "source_drift_escalation_observation_only",
        "drift_events": str(drift_path),
        "source_registry": str(source_path),
        "staleness_rules": str(rules_path),
        "status": status,
        "result": "FAIL" if errors or blocking_count else "PASS",
        "unresolved_event_count": unresolved_count,
        "blocking_review_count": blocking_count,
        "advisory_review_count": advisory_count,
        "errors": errors,
        "findings": findings,
        "does_not_fetch_sources": True,
        "does_not_change_claim_level": True,
        "does_not_create_issues": True,
    }
    if args.receipt_out:
        _write_json(_resolve(args.receipt_out, ROOT / "evidence" / "validation_receipt_source_drift_escalation.json"), receipt)
    if args.summary_out:
        _write_summary(_resolve(args.summary_out, ROOT / "evidence" / "source_drift_escalation.md"), receipt)

    print(f"Source drift escalation: {status}")
    print(f"- unresolved events: {unresolved_count}")
    print(f"- blocking review signals: {blocking_count}")
    print(f"- advisory review signals: {advisory_count}")
    for error in errors:
        print(f"- {error}")
    return 1 if errors or blocking_count else 0


if __name__ == "__main__":
    sys.exit(main())