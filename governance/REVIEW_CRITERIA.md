---
audience: human-only
authority: reference
can_override: false
overridden_by: ~
default_load: never
---

# REVIEW_CRITERIA.md

**Code Review / Audit Protocol - v1.2**

> **Version**: 1.2 | **Priority**: 3

This document defines how review or audit work must be performed in this repo.
It is reviewer-facing guidance. It does not override canonical runtime
governance or the repo root `AGENTS.md`.

## 0. Activation

This protocol applies whenever the user asks for `review`, `audit`, pull request
review, governance review, or equivalent change assessment.

When active, the agent must:

- Switch to a skeptical verifier posture rather than an implementer posture.
- Read this file before producing review output.
- Focus on bugs, regressions, governance boundary violations, missing evidence,
  and missing tests.
- Put findings before summaries.
- Include a `Review Inputs Checked` block in the final review output.

## 1. Review Philosophy

Review work must answer these questions:

- Does the change preserve this repo's read-only spec-reference boundary?
- Does the change create claim inflation or authority drift?
- Does the change risk misleading consuming firmware repositories?
- Does the validation evidence match the risk of the change?
- Are unrelated dirty worktree changes being mixed into the review scope?

Do not approve a change only because it builds. Build success is evidence, not
correctness.

## 2. Verdict Model

| Verdict | Meaning | Use When |
|---|---|---|
| `APPROVED` | No blocking governance, correctness, or validation issue found | Remaining risk is acceptable and disclosed |
| `CHANGES_REQUESTED` | At least one blocking issue must be fixed | The change would merge with unacceptable risk |
| `ESCALATED` | Risk or ownership is ambiguous enough to need higher-level decision | The reviewer cannot safely decide from current evidence |

### 2.1 Finding Levels

| Level | Meaning |
|---|---|
| `BLOCKING` | Must be fixed before approval; correctness, safety, or governance boundary issue |
| `WARNING` | Important risk or missing evidence; may be acceptable only if explicitly accepted |
| `SUGGESTION` | Non-blocking improvement or cleanup |

Do not use `ESCALATED` as a substitute for a concrete `BLOCKING` finding. Use it
when the issue is a decision/ownership ambiguity rather than a directly fixable
defect.

## 3. Mandatory Audit Checklist

### 3.1 Boundary and Architecture

Check whether the change:

- Treats this repo as firmware truth instead of standard-side reference input.
- Adds project-specific implementation guidance that belongs in a consuming repo.
- Adds fleet governance, runtime enforcement, or CI authority outside this repo's
  spec-reference role.
- Changes authority hierarchy, load mode, or memory promotion policy.
- Introduces a new interpretation affecting port status bits or Transaction
  Translator behavior without adequate source tracing.

### 3.2 Physical and Native Safety

For native interop, C/C++, firmware, ABI, memory ownership, or hardware-facing
changes, check:

- Ownership and lifetime rules.
- ABI layout and packing assumptions.
- Panic/fail-fast versus recoverable error handling.
- Whether the change belongs in this reference repo at all.

If not applicable, mark `N/A`.

### 3.3 Quality and Verification

Check whether:

- Validation commands match the risk of the change.
- Failure paths are tested or explicitly out of scope.
- Evidence supports behavior rather than implementation trivia.
- Documentation-only changes avoid semantic or claim-level drift.
- Generated receipts or baselines are intentional and scoped.

### 3.4 Thread Safety and Async Safety

For UI, async, scheduled, or delegated execution paths, check:

- Thread or task ownership.
- Failure and cancellation paths.
- Whether the change introduces side effects through automation or agents.

If not applicable, mark `N/A`.

### 3.5 Dirty Worktree and Scope Hygiene

Check whether:

- Unrelated dirty files are mixed into the review.
- The reviewed diff overlaps with uncommitted user changes.
- The commit boundary is coherent and small enough to review.
- Memory writes follow the canonical closeout rule.

## 4. Knowledge Base Cross-Check

If a relevant knowledge base or prior review log is available, check for:

- Known anti-patterns.
- Regression notes.
- Prior unresolved findings.

If no applicable knowledge base exists or it is not readable, state that in the
review output instead of silently skipping it.

## 5. Legacy Refactor Review Addendum

For refactor, rollback, or baseline reset work, additionally check:

- The authoritative baseline remains buildable or is explicitly marked
  unverified.
- The canonical toolchain is still clear.
- The change does not label a reset as a clean refactor when baseline evidence is
  missing.
- Any baseline instability is reported as at least a `WARNING`; escalate if the
  correct baseline cannot be determined.

## 6. Review Output Format

Use this structure for review output:

```markdown
### Review Inputs Checked
- governance/REVIEW_CRITERIA.md
- <additional documents or commands checked>

### Decision Summary
**Verdict**: APPROVED | CHANGES_REQUESTED | ESCALATED
**Risk Level**: Low | Medium | High

### Governance Audit
- Architecture: ...
- Native Safety: ... | N/A
- Test Integrity: ...
- Thread Safety: ... | N/A
- Baseline Status: Stable | Unverified | Unstable | N/A

### Technical Findings
1. [BLOCKING|WARNING|SUGGESTION] Title
   - Location: `path:line`
   - Evidence: ...
   - Rule Reference: ...
   - Fix Required / Reasoning: ...

### Knowledge Base Alignment
- Anti-patterns checked: N
- Regression notes checked: N
- Result: Pass | Conflict Found | Not Available
```

Every non-trivial finding must include:

- Location.
- Evidence.
- Rule reference.
- Required fix or reviewer reasoning.

## 7. Post-Review Memory Actions

Memory writes are not automatic during review.

Only canonical closeout may write under `memory/`. If a review result needs a
memory record, it must be written as part of the canonical closeout flow and
must preserve the repo's memory authority rules.

Do not write `memory/04_review_log.md` or any other memory file as an incidental
side effect of a non-closeout review.

## 8. C++ Build Boundary Addendum

When review touches C++ project files, header layout, or build configuration:

- Check that include directories do not depend on private peer-project trees.
- Check that cross-project private headers are not used to force a build pass.
- If a header must be shared, check ownership and shared boundary rules.

Treat this as a boundary issue, not a style issue.

## 9. Final Principle

No evidence means no review approval.

Ambiguous ownership or authority should be escalated. A directly evidenced bug,
regression, or governance violation should be reported as a finding.
