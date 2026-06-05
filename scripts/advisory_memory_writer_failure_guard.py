#!/usr/bin/env python3
"""Advisory guard for post-onboarding non-canonical memory writes.

Claim ceiling:
- Detects old-format memory entries added after a configured baseline commit.
- Advisory only: does not block, rewrite memory, or validate semantic truth.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASELINE_REF = "aaf05ca"
OLD_FORMAT_RE = re.compile(r"^\+\s*-\s*(what changed|what_changed):\s*", re.IGNORECASE)


def _run_git(repo_root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )


def _scan_added_old_format_entries(repo_root: Path, baseline_ref: str) -> dict[str, Any]:
    result = _run_git(
        repo_root,
        [
            "diff",
            "--unified=0",
            f"{baseline_ref}..HEAD",
            "--",
            "memory/*.md",
        ],
    )
    if result.returncode != 0:
        return {
            "ok": False,
            "error": "git_diff_failed",
            "baseline_ref": baseline_ref,
            "stderr": result.stderr.strip(),
            "findings": [],
            "finding_count": 0,
        }

    findings: list[dict[str, str]] = []
    current_file = ""
    current_line = ""
    for line in result.stdout.splitlines():
        if line.startswith("+++ b/"):
            current_file = line.removeprefix("+++ b/")
            current_line = ""
            continue
        if line.startswith("@@ "):
            current_line = line
            continue
        if OLD_FORMAT_RE.match(line):
            findings.append(
                {
                    "file": current_file,
                    "diff_hunk": current_line,
                    "entry_preview": line[1:].strip()[:240],
                    "code": "post_onboarding_old_format_memory_entry",
                    "severity": "advisory",
                }
            )

    return {
        "ok": True,
        "guard": "advisory_memory_writer_failure_guard",
        "mode": "advisory",
        "baseline_ref": baseline_ref,
        "finding_count": len(findings),
        "findings": findings,
        "claim_ceiling": "detects post-baseline old-format memory entries only",
        "not_claimed": [
            "blocking enforcement",
            "historical violation cleanup",
            "memory semantic correctness",
            "agent attribution",
            "#17 threshold readiness",
        ],
    }


def _print_text(payload: dict[str, Any]) -> None:
    print("[advisory_memory_writer_failure_guard]")
    print(f"mode={payload.get('mode', 'advisory')}")
    print(f"baseline_ref={payload.get('baseline_ref')}")
    print(f"finding_count={payload.get('finding_count')}")
    for finding in payload.get("findings", []):
        print(
            "finding="
            f"{finding.get('code')} file={finding.get('file')} "
            f"entry={finding.get('entry_preview')}"
        )
    print("blocking=NOT PRESENT")
    print("cleanup=NOT CLAIMED")
    print("threshold=NOT CLAIMED")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Advisory post-onboarding memory writer failure guard."
    )
    parser.add_argument("--repo-root", default=str(ROOT), help="Repository root.")
    parser.add_argument(
        "--baseline-ref",
        default=DEFAULT_BASELINE_REF,
        help="Baseline ref after which old-format memory entries are advisory findings.",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    payload = _scan_added_old_format_entries(Path(args.repo_root), args.baseline_ref)
    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        _print_text(payload)

    # Advisory-only guard: findings do not block.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
