# Response Envelope Contract v0.1

Repo-local adoption: reporting convention only.

This document is imported from `ai-governance-framework` and sanitized for this
spec-reference repo. It supports structured completion and validation reporting.
It does not add runtime enforcement, semantic validation, firmware authority, or
new CI behavior.

## Purpose

This contract defines the minimum governance fields for structured agent
responses when a response is produced by a recognizable workflow event.

The goal is not compression. The goal is to keep task authority, scope, claim
ceiling, evidence, and risk disclosure separate enough that reviewers can audit
what was done, what was claimed, and what remains unproven.

## Authority Boundary

This contract is a reporting convention and reviewer-facing schema.

It does not change:
- closeout runtime enforcement
- evidence admissibility rules
- claim ceiling semantics
- risk disclosure semantics
- session_end hook behavior
- gate policy behavior
- USB spec interpretation authority
- consuming firmware behavior

## Event-Driven Mode Rule

`mode` must describe the workflow event that produced the response. It must not
be treated as an agent-selected style preference.

Every envelope that includes `mode` must also include `mode_source`.

Allowed initial mode mappings:

| Event | mode | mode_source |
| --- | --- | --- |
| session_end hook completed | `CLOSEOUT` | `session_end_hook` |
| in-progress status update | `PROGRESS` | `intermediate_update` |
| scoped files staged for commit | `PRE_COMMIT` | `git_staged_diff` |
| validation command completed | `VALIDATION` | `validation_command` |
| out-of-scope change detected | `SCOPE_ALERT` | `scope_boundary_check` |

Agents may fill the envelope content, but they must not choose a higher-authority
mode than the event source supports.

## Required Fields

Minimum response envelope:

```yaml
mode: CLOSEOUT
mode_source: session_end_hook
task: verification status presentation cleanup
task_authority: user_request
scope:
  - specs/verification_status.md
  - specs/en/verification_status.md
done:
  - packet statistics moved to a supporting artifact summary
claim_ceiling:
  - reporting convention documented only
  - no runtime enforcement claim
not_claimed:
  - new verified entries
  - generated statistics
  - governance cleanup
evidence_refs:
  - command: python scripts\validate_wiki_frontmatter.py
    result: PASS
  - command: npm.cmd run build
    result: PASS
risk:
  - same-page wording cleanup only; no statistics semantic change claimed
next_action: scoped stage and commit, then review staged diff
```

Required field meanings:
- `mode`: event-derived response mode.
- `mode_source`: source event or command that justifies the mode.
- `task`: bounded task label or short task description.
- `task_authority`: source of authority for the task.
- `scope`: exact files, artifacts, or surfaces covered by the response.
- `done`: completed work inside scope.
- `claim_ceiling`: explicit upper bound on what the response is asserting.
- `not_claimed`: explicit claim ceiling for this response.
- `evidence_refs`: validation commands, artifacts, or reviewer sources supporting
  the `done` claim.
- `risk`: scope drift, incidental cleanup, claim inflation, or evidence maturity
  risks.
- `next_action`: one concrete next step, or `none` when no next action is being
  recommended.

## task_authority Values

Allowed values:
- `user_request`: explicitly requested or authorized by the user.
- `followup`: directly follows a previously authorized task without expanding
  scope.
- `hook_trigger`: produced by a workflow hook or runtime event.
- `autonomous`: initiated by the agent without direct user authorization.

If `task_authority: autonomous`, the response must include a `risk` entry that
explains why the work did not exceed the current DONE boundary.

## evidence_refs Rules

Each evidence reference must include:
- `command` or `artifact`
- `result`

Valid `result` values:
- `PASS`
- `FAIL`
- `NOT RUN`
- `NOT PRESENT`
- `NOT CLAIMED`

`PASS` must include a command, artifact, or source that can be independently
checked. Bare `PASS` is not valid.

`evidence_refs` does not upgrade semantic authority. It records what evidence
exists for the stated claim ceiling.

## Claim Ceiling Preservation

`done`, `claim_ceiling`, and `not_claimed` must remain separate.

Do not merge unverified implications into `done`. If a capability was not
validated, proven, or authorized in the current scope:
- state the positive boundary under `claim_ceiling`
- list the non-asserted items under `not_claimed`
- keep the existing completion report `Cannot claim this session` section when
  using the longer repo completion report

## Risk Disclosure Preservation

The `risk` field is required because incidental work is otherwise easy to hide
inside narrative prose.

Risk entries should disclose:
- incidental cleanup
- scope drift
- claim inflation
- evidence maturity limits
- autonomous work boundary concerns

Do not replace `risk` with confidence scores, effort estimates, or broad impact
analysis.

## Non-Goals

This contract intentionally does not add:
- confidence scores
- effort estimates
- generic impact analysis
- new runtime gates
- automatic semantic verification
- automatic mode inference beyond the listed event mappings
- USB specification validation
- firmware behavior validation

## Relationship To Existing Completion Reports

The existing result-first completion report remains valid.

Use this envelope when a compact event-driven response is needed, or when a
tooling layer needs structured fields before rendering the existing completion
report.

The envelope must preserve the same claim discipline:
- `NOT CLAIMED` means the capability or conclusion is not asserted.
- `NOT PRESENT` means the mechanism, artifact, or enforcement does not exist.
- `PASS` must reference a command or source.
