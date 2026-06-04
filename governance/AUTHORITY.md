# Governance Authority Table

> machine-readable: true
> version: 1.2.0
> updated: 2026-06-04

## Authority Levels

- `canonical`: highest repo-local authority. It defines the controlling rule
  when other surfaces conflict.
- `reference`: supporting authority. It informs agent or reviewer decisions but
  cannot override canonical documents.
- `derived`: generated, adapted, summarized, or cached material derived from
  canonical or reference sources. It cannot create new authority by itself.

## Audience Types

- `agent-runtime`: may be loaded automatically at session start or runtime
  initialization.
- `agent-on-demand`: may be loaded when a task requires the relevant context.
- `human-only`: intended for reviewers or operators. Agents must not treat these
  documents as runtime-loaded policy unless explicitly asked to review them.

## Default Load Modes

- `always`: load at session start or runtime initialization.
- `on-demand`: load only when the current task needs that context.
- `incremental`: load selectively when a specific memory or record is relevant.
- `never`: do not load automatically; human-review surface only.

---

## Authority Table

| document | audience | authority | can_override | overridden_by | default_load |
|----------|----------|-----------|--------------|---------------|--------------|
| `governance/SYSTEM_PROMPT.md` | agent-runtime | canonical | false | ~ | always |
| `governance/AGENT.md` | agent-runtime | canonical | false | ~ | always |
| `governance/PLAN.md` | agent-runtime | canonical | false | ~ | always |
| `governance/ARCHITECTURE.md` | agent-on-demand | reference | false | SYSTEM_PROMPT.md | on-demand |
| `governance/TESTING.md` | agent-on-demand | reference | false | AGENT.md | on-demand |
| `governance/NATIVE-INTEROP.md` | agent-on-demand | reference | false | AGENT.md | on-demand |
| `governance/HUMAN-OVERSIGHT.md` | human-only | reference | false | ~ | never |
| `governance/REVIEW_CRITERIA.md` | human-only | reference | false | ~ | never |
| `governance/RESPONSE_ENVELOPE_CONTRACT.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `governance/TRUST_BOUNDARY_TAXONOMY.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `governance/PHASE_D_CLOSE_AUTHORITY.md` | human-only | canonical | false | ~ | never |
| `AGENTS.md` (workspace) | agent-runtime | derived | false | AGENT.md | always |
| `.github/copilot-instructions.md` | agent-runtime | derived | false | AGENT.md | always |
| `.github/agents/*.agent.md` | agent-on-demand | derived | false | AGENT.md | on-demand |
| `domain contract (full)` | agent-on-demand | canonical | false | ~ | on-demand |
| `domain adapter summary` | agent-runtime | derived | false | domain contract | always |
| `memory/02_project_facts.md` | agent-runtime | canonical | false | ~ | incremental |
| `memory/03_decisions.md` | agent-runtime | canonical | false | ~ | incremental |
| `memory/reviewer_handoff_*` | agent-on-demand | derived | false | 03_decisions.md | on-demand |
| `memory/framework_artifact_*` | agent-on-demand | derived | false | ~ | on-demand |
| `memory/external_repo_aliases` | agent-on-demand | reference | false | ~ | on-demand |

---

## Conflict Resolution Rules

Authority precedence:

```text
canonical > reference > derived
```

Rules:

1. `canonical` wins over `reference`.
2. `canonical` wins over `derived`.
3. `reference` wins over `derived`.
4. Workspace instructions such as `AGENTS.md` and Copilot instructions must not
   override repo canonical governance.
5. `agent-on-demand` surfaces may provide task context, but they must not replace
   always-loaded canonical runtime rules.
6. `derived` material is cache or adaptation only. It must be traced back to its
   governing source before being treated as authority.
7. Phase D completion claims: `PHASE_D_CLOSE_AUTHORITY.md` takes precedence over
   README, PLAN.md, implementation presence, version tags, commit history, and
   all generated summaries. No agent-produced signal may override this contract.

---

## Memory Source Authority

| memory source | authority | promotion policy |
|---------------|-----------|-----------------|
| `02_project_facts.md` | canonical | may be promoted directly |
| `03_decisions.md` | canonical | may be promoted directly |
| `04_patterns.md` | reference | may be promoted case by case |
| reviewer handoff summary | derived | cache only; do not promote as truth |
| framework artifact cache | derived | cache only; do not promote as truth |
| external repo aliases | reference | may be promoted case by case; must still be checked against canonical sources |

---

## Loading Condition Summary

| task_level | always | on-demand | incremental | never |
|------------|--------|-----------|-------------|-------|
| L0 | canonical runtime core | minimal reference only when needed | candidates only | human-only docs |
| L1 | canonical runtime core | boundary, testing, and domain reference | candidates only | human-only docs |
| L2 | canonical runtime core | broader reference plus contract context | candidates only | human-only docs |
| any | canonical runtime core | relevant reference documents | relevant memory records | human-only surfaces |
