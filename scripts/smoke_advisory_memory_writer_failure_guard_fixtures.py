#!/usr/bin/env python3
"""Smoke test advisory_memory_writer_failure_guard.py against a temp git repo."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "scripts" / "advisory_memory_writer_failure_guard.py"


def _run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )


def _git(repo: Path, *args: str) -> None:
    result = _run(["git", *args], cwd=repo)
    if result.returncode != 0:
        raise AssertionError(
            f"git {' '.join(args)} failed\nstdout={result.stdout}\nstderr={result.stderr}"
        )


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    tmp = tempfile.TemporaryDirectory(prefix="usbif-memory-guard-")
    repo = Path(tmp.name) / "repo"
    repo.mkdir(parents=True)

    _git(repo, "init")
    _git(repo, "config", "user.email", "smoke@example.invalid")
    _git(repo, "config", "user.name", "Smoke Test")

    memory_file = repo / "memory" / "2026-06-05.md"
    _write(
        memory_file,
        """# 2026-06-05

- memory_type: session-derived
  record_format_version: 1.0
  writer: governance_tools.memory_record
  what_changed: baseline canonical entry
  commit: baseline
  commit_hash: baseline
  session_id: baseline-session
  next_step: continue
""",
    )
    _git(repo, "add", "memory/2026-06-05.md")
    _git(repo, "commit", "-m", "baseline")
    baseline = _run(["git", "rev-parse", "--short", "HEAD"], cwd=repo).stdout.strip()

    _write(
        memory_file,
        memory_file.read_text(encoding="utf-8")
        + """
- what changed: post-baseline old-format entry
  session_id: bad-session

- memory_type: session-derived
  record_format_version: 1.0
  writer: governance_tools.memory_record
  what_changed: post-baseline canonical entry
  commit: canonical
  commit_hash: canonical
  session_id: canonical-session
  next_step: continue
""",
    )
    _git(repo, "add", "memory/2026-06-05.md")
    _git(repo, "commit", "-m", "post baseline entries")

    result = _run(
        [
            sys.executable,
            str(GUARD),
            "--repo-root",
            str(repo),
            "--baseline-ref",
            baseline,
            "--format",
            "json",
        ],
        cwd=ROOT,
    )
    if result.returncode != 0:
        raise AssertionError(f"guard exited nonzero: {result.returncode}\n{result.stderr}")

    payload = json.loads(result.stdout)
    findings = payload.get("findings", [])
    assert payload["mode"] == "advisory"
    assert payload["finding_count"] == 1
    assert findings[0]["code"] == "post_onboarding_old_format_memory_entry"
    assert "post-baseline old-format entry" in findings[0]["entry_preview"]
    assert "canonical entry" not in findings[0]["entry_preview"]

    print(
        json.dumps(
            {
                "ok": True,
                "guard_exit": result.returncode,
                "finding_count": payload["finding_count"],
                "mode": payload["mode"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
