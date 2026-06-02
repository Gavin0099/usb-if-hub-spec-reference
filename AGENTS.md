# AGENTS.md — USB-IF Hub Spec Reference

<!-- governance:memory_authority -->
memory_root: memory/
external_memory_allowed: false
operational_records_must_stay_under_memory_root: true

## Purpose

This repository is a **read-only spec reference layer**.

Its only permitted role is to clarify the semantics of USB 2.0 hub class specifications for consuming firmware repositories.

It does **not** govern firmware behavior directly. It does **not** override confirmed project facts.

## Usage Boundary

This repository may be used to:

- Clarify field definitions (descriptor fields, port status bits, hub class requests)
- Confirm standard-mandated behavior for comparison with project implementation
- Provide the authoritative source for Standard Conflict Detection (see AGENTS.md in consuming repos)

This repository must **not** be used to:

- Replace a confirmed project fact with a generic standard interpretation
- Override architecture decisions in consuming firmware repos
- Serve as the source of truth for project-specific behavior

## Standard Conflict Resolution

When a consuming repo detects a conflict between this spec reference and a confirmed project fact, the consuming repo's Standard Escalation Mode applies.

This repo does not resolve those conflicts. It only provides the standard-side input.

## Governance Calibration

<!-- governance:key=critical_path -->
The most dangerous path in this repo is misuse: content here must never silently replace
a confirmed project fact in a consuming firmware repo. The boundary is clarification only.

<!-- governance:key=critical_path_verification -->
Verify by checking consuming repos — any firmware change citing this repo as authority
(not as reference) for overriding a confirmed fact must be flagged immediately.

<!-- governance:key=l2_escalation -->
Escalate to L2 (consuming repo architecture review) when:
- A consuming repo proposes to change firmware behavior based solely on this spec content
- A conflict is found between this spec and a confirmed project fact
- A new spec interpretation is introduced that affects port status bits or TT behavior

<!-- governance:key=forbidden_shortcuts -->
Forbidden in this repo:
- Adding project-specific implementation guidance (belongs in the firmware contract repo)
- Marking any spec interpretation as "required" without noting it as USB-IF standard, not project fact
- Overwriting or amending existing spec content without tracing to the USB-IF source section number

## Document Relationship

- `specs/hub_descriptor.md` — Hub class descriptor field definitions (USB 2.0 spec 11.23)
- `specs/port_status_bits.md` — Port status and change bit definitions (USB 2.0 spec 11.24.2.7)
- `specs/hub_class_requests.md` — Hub class request semantics (USB 2.0 spec 11.24.2)
- `specs/transaction_translator.md` — TT rules summary
- `specs/escalation_table.md` — Standard Escalation trigger table for consuming repos

## Review Tasks

If the agent is asked to perform `review` or `audit` work:

- The agent must read `governance/REVIEW_CRITERIA.md` before producing review output.
- The agent must not skip that read step.
- The final review output must include a `Review Inputs Checked` block.

## Commit Checkpoint (Reporting Convention)

This is a reporting convention only, not a mandatory pause gate.

When reporting a completed work chunk, include:

- `Commit Checkpoint: <short hash or NO_COMMIT>`
- `Scope: <files or area covered>`
- `Validation: <checks run or NONE>`
- `Risk: <open risk or NONE>`

## Rule 4 Language Note

When using the Rule 4 structured completion format for this repo:

- The session language may follow the user language (for example, Chinese).
- Fixed field labels remain in English:
  - `structural`
  - `build`
  - `semantic`
  - `behavioral`
  - `ext evidence`
  - `scope drift`
  - `claim inflation`
  - `evidence maturity`
- Fixed status tokens also remain in English:
  - `PASS`
  - `FAIL`
  - `NOT RUN`
  - `NOT CLAIMED`
  - `NOT PRESENT`
- `Cannot claim this session` must always be present, even in Chinese sessions.

## Canonical Memory Writer Rule

Only canonical session closeout is allowed to write under `memory/`.

- Non-closeout phases must not write memory records.
- If closeout evidence is missing, memory write claims are non-admissible.
- Any attempt to bypass canonical closeout memory write flow is a governance violation.
