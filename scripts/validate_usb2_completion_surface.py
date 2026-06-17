#!/usr/bin/env python3
"""Validate the USB2 LLM wiki completion surface.

Authority ceiling: usb2_completion_surface_consistency_only

This aggregate validator does not verify USB semantics. It runs the existing
navigation, entry-gate, claim-partition, statistics, and frontmatter validators
as a single completion-surface guard.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class CommandSpec:
    name: str
    command: list[str]
    authority_ceiling: str


DEFAULT_COMMANDS = [
    CommandSpec(
        name="usb2_reference_navigation",
        command=[
            "scripts/validate_usb2_reference_navigation.py",
            "--zh-page",
            "specs/usb2.md",
            "--en-page",
            "specs/en/usb2.md",
        ],
        authority_ceiling="usb2_navigation_consistency_only",
    ),
    CommandSpec(
        name="usb2_topic_cross_references",
        command=["scripts/validate_usb2_topic_cross_references.py"],
        authority_ceiling="usb2_core_topic_cross_reference_consistency_only",
    ),
    CommandSpec(
        name="usb2_topic_pair_reachability",
        command=["scripts/validate_usb2_topic_pair_reachability.py"],
        authority_ceiling="usb2_noncore_topic_pair_reachability_only",
    ),
    CommandSpec(
        name="entry_verification_precondition_gate",
        command=["scripts/precondition_gate.py"],
        authority_ceiling="entry_verification_precondition_only",
    ),
    CommandSpec(
        name="entry_verification_gate",
        command=["scripts/validate_entry_verification_gate.py"],
        authority_ceiling="entry_level_verified_gate_only",
    ),
    CommandSpec(
        name="entry_gate_coverage",
        command=["scripts/validate_entry_gate_coverage.py"],
        authority_ceiling="gate_coverage_consistency_only",
    ),
    CommandSpec(
        name="reviewed_boundary_lock",
        command=["scripts/validate_reviewed_boundary_lock.py"],
        authority_ceiling="reviewed_boundary_lock_only",
    ),
    CommandSpec(
        name="usb2_claim_partition",
        command=["scripts/validate_usb2_claim_partition.py"],
        authority_ceiling="usb2_claim_partition_consistency_only",
    ),
    CommandSpec(
        name="usb2_claim_partition_packet",
        command=["scripts/validate_usb2_claim_partition_packet.py"],
        authority_ceiling="usb2_claim_partition_packet_consistency_only",
    ),
    CommandSpec(
        name="reference_surface_statistics",
        command=["scripts/validate_reference_surface_statistics.py"],
        authority_ceiling="visible_statistics_consistency_only",
    ),
    CommandSpec(
        name="wiki_frontmatter",
        command=["scripts/validate_wiki_frontmatter.py", "--dir", "specs/"],
        authority_ceiling="wiki_frontmatter_shape_only",
    ),
]


def run_command_specs(command_specs: list[CommandSpec], cwd: Path = ROOT) -> tuple[str, list[dict[str, Any]]]:
    results: list[dict[str, Any]] = []
    for spec in command_specs:
        completed = subprocess.run(
            [sys.executable, "-X", "utf8", *spec.command],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )
        results.append({
            "name": spec.name,
            "command": [sys.executable, "-X", "utf8", *spec.command],
            "authority_ceiling": spec.authority_ceiling,
            "exit_code": completed.returncode,
            "result": "PASS" if completed.returncode == 0 else "FAIL",
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        })
    return ("FAIL" if any(result["exit_code"] != 0 for result in results) else "PASS"), results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    result, command_results = run_command_specs(DEFAULT_COMMANDS)
    failed = [item for item in command_results if item["result"] != "PASS"]

    for item in command_results:
        print(f"[{item['result']}] {item['name']}")
        if item["result"] != "PASS":
            print(f"  exit_code: {item['exit_code']}")
            if item["stdout"]:
                print(f"  stdout: {item['stdout']}")
            if item["stderr"]:
                print(f"  stderr: {item['stderr']}")

    print(f"\nUSB2 completion surface validation {result}")
    print(f"- validators: {len(command_results)}")
    print(f"- failed: {len(failed)}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "validator": "validate_usb2_completion_surface",
            "result": result,
            "authority_ceiling": "usb2_completion_surface_consistency_only",
            "does_not_verify_usb_semantics": True,
            "does_not_change_claim_level": True,
            "does_not_promote_entries": True,
            "command_count": len(command_results),
            "failed_count": len(failed),
            "commands": command_results,
        }
        args.receipt_out.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
