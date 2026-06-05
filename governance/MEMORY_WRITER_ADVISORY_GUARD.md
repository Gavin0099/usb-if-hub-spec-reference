# Memory Writer Advisory Guard

## Purpose

This repo has observed post-onboarding memory entries written in the old
direct-append format:

```text
- what changed: ...
```

Those entries trigger `non_canonical_writer` in the AI Governance Framework
memory authority guard.

The advisory guard detects old-format memory entries added after the canonical
memory writer onboarding commit.

## Baseline

Baseline ref:

```text
aaf05ca
```

This is the commit that introduced the repo-local canonical memory writer rule
in `AGENTS.md`.

The guard scans:

```text
git diff aaf05ca..HEAD -- memory/*.md
```

and reports added old-format entries:

```text
- what changed:
- what_changed:
```

## Command

Run manually:

```powershell
python scripts/advisory_memory_writer_failure_guard.py --format text
```

Machine-readable output:

```powershell
python scripts/advisory_memory_writer_failure_guard.py --format json
```

Fixture smoke:

```powershell
python scripts/smoke_advisory_memory_writer_failure_guard_fixtures.py
```

## Pre-Commit Advisory Hook

The local `.git/hooks/pre-commit` hook runs the advisory guard before the
existing PLAN freshness check.

The hook is advisory-only:

- it prints findings;
- it never blocks commits;
- it never rewrites memory;
- it never stages or cleans files;
- it never sets #17 thresholds.

## Interpretation

If `finding_count` stays stable, no new post-onboarding old-format memory entry
was detected.

If `finding_count` increases, at least one new old-format memory entry was added
after the onboarding baseline.

This signal supports observation and triage only. It does not prove which agent
wrote the entry.

## Required Writer

New session-derived memory entries should use:

```powershell
python E:/BackUp/Git_EE/ai-governance-framework/governance_tools/memory_record.py `
  --what-changed "..." `
  --commit <git-sha> `
  --test-evidence "..." `
  --next-step "..." `
  --project-root .
```

## Claim Ceiling

CLAIMED:

- advisory detection of post-baseline old-format memory entries;
- local pre-commit advisory visibility;
- fixture coverage for detecting one post-baseline old-format entry.

NOT CLAIMED:

- blocking enforcement;
- historical violation cleanup;
- memory semantic correctness;
- agent attribution;
- canonical writer success;
- #17 threshold readiness;
- hook portability to every clone.
