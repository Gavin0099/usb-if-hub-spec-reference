# Entry-Level Verification

> Written: 2026-06-02  
> Status: DRAFT  
> Canonical schema file: `contract/entry_verification_packet_schema.yaml`

## Purpose

This document defines the minimum evidence packet expected before an entry-level
verified promotion is even considered.

It exists to enforce the sequence:

1. anchor attachment
2. evidence packet
3. promotion gate

and to block the shortcut:

`section_refs exists -> therefore verified`

## Core Rule

> An evidence packet is necessary for later promotion review, but it is not
> sufficient to promote an entry by itself.

That means the following is valid and expected:

- target entry still `claim_level: inferred`
- target entry still `evidence_status: review_required`
- packet exists and is reviewable

## Minimum Packet Shape

```yaml
target:
  surface: governed_table_entry
  table: port_status_bit_matrix
  entry_id: wPortStatus.bit0.PORT_CONNECTION

evidence:
  spec: usb20
  section: "11.24.2.7.1"
  page: null
  quoted_surface: short_reference_only
  reviewer_note: ""

verification_scope:
  claim: bit_name_and_position_only
  excludes:
    - timing behavior
    - state transition behavior
    - ClearPortFeature behavior
    - full USB compliance

result:
  eligible_for_verified: false
  evidence_status: review_required
```

## Why These Fields Exist

### `target`

Defines the exact evidence surface.

This prevents ambiguous claims like "the page was reviewed" when the intended
unit is only one governed table entry.

### `evidence`

Captures where the reviewer looked and how much of the source surface is being
claimed.

The packet is intentionally conservative:

- `quoted_surface` may remain `short_reference_only`
- `reviewer_note` may be empty in the earliest structural stage

This supports a narrow pilot without pretending extraction is complete.

### `verification_scope`

This is the most important boundary field.

It records exactly what is being checked and, equally importantly, what is not.

For the first pilot, the intended safe claim is:

- `bit_name_and_position_only`

not:

- timing behavior
- state transition semantics
- host-stack behavior
- full USB compliance

### `result`

This field records the current gate state.

For Phase 8A:

- `eligible_for_verified: false`
- `evidence_status: review_required`

These are the expected defaults.

## Pilot Packet Inventory

The first non-promoting pilot packet is:

- `evidence/entry_verification_packets/port_status_wPortStatus.bit0.PORT_CONNECTION.yaml`

This pilot exists to prove that a packet can be attached to one governed table
entry without changing `claim_level` or `evidence_status`.

## What This Phase Does Not Allow

Phase 8A/8B do not allow:

- entry promotion to `verified`
- page-level verified claims
- table-level verified claims
- "PDF-backed" wording beyond the existence of a structured packet format
- semantic closure of escalation triggers

## Intended Follow-up

The first intended packet targets:

- `wPortStatus.bit0.PORT_CONNECTION`

Its first iteration remains non-promoting and review-required.

## Phase 8C Promotion Gate

The next gate is intentionally narrow.

Current allowed promotion scope:

- governed table only: `tables/port_status_bit_matrix.yaml`
- entry only: `wPortStatus.bit0.PORT_CONNECTION`
- verification scope only: `bit_name_and_position_only`

Promotion is still disallowed unless all of the following are true:

- a matching evidence packet exists
- `result.eligible_for_verified` is `true`
- `result.evidence_status` is `reviewed`
- the packet exclusions still explicitly rule out timing behavior, state-transition behavior, `ClearPortFeature` behavior, and full USB compliance

No page-level or table-level verified promotion is allowed in this phase.

## Phase 8D Human-Reviewable Packet Pilot

The next safe step is to improve one pilot packet into a human-reviewable
evidence artifact without changing the live governed table.

Recommended additions for a Phase 8D packet:

- `document_ref` to name the preferred source and any fallback source
- `quoted_surface_summary` as a short reviewer paraphrase
- `review_checklist` so a human can verify the packet boundaries
- `promotion_note` explaining why promotion is still blocked or deferred

Phase 8D still does **not** allow:

- direct table promotion
- page-level verified claims
- table-level verified claims
- timing or state-transition verification

The intended Phase 8D target remains:

- `wPortStatus.bit0.PORT_CONNECTION`

## Phase 8E First Entry-Level Verified Promotion

The first live promotion remains intentionally narrow.

Allowed live verified surface:

- governed table: `tables/port_status_bit_matrix.yaml`
- entry: `wPortStatus.bit0.PORT_CONNECTION`
- scope: `bit_name_and_position_only`

Required promotion conditions:

- packet result sets `eligible_for_verified: true`
- packet result sets `evidence_status: reviewed`
- packet scope remains `bit_name_and_position_only`
- packet exclusions still include timing behavior, state transition behavior, `ClearPortFeature` behavior, and full USB compliance

Phase 8E still does **not** allow:

- any second verified entry
- page-level verified claims
- table-level verified claims
- TT behavior verification
- reset, debounce, timing, or host-side semantic verification

## Phase 8I Expanded Change-Bit Pilot

The live verified set remains narrow, but now includes the first two
`wPortChange` entries alongside the existing `wPortStatus` pair.

Allowed live verified surface:

- governed table: `tables/port_status_bit_matrix.yaml`
- entries:
  - `wPortStatus.bit0.PORT_CONNECTION`
  - `wPortStatus.bit1.PORT_ENABLE`
  - `wPortChange.bit0.C_PORT_CONNECTION`
  - `wPortChange.bit1.C_PORT_ENABLE`
- scope: `bit_name_and_position_only`

Required promotion conditions remain unchanged:

- matching evidence packet exists
- packet result sets `eligible_for_verified: true`
- packet result sets `evidence_status: reviewed`
- packet scope remains `bit_name_and_position_only`
- packet exclusions still include timing behavior, state transition behavior,
  `ClearPortFeature` behavior, and full USB compliance

Phase 8I still does **not** allow:

- page-level verified claims
- table-level verified claims
- timing, debounce, or event-ordering verification
- `ClearPortFeature` behavioral verification
- TT behavior verification

## Phase 8J Hub-Status Pilot Expansion

The live verified set remains narrow, but now includes two hub-level status bits
alongside the existing `wPortStatus` and `wPortChange` pilot entries.

Allowed live verified surface:

- governed table: `tables/port_status_bit_matrix.yaml`
- entries:
  - `wPortStatus.bit0.PORT_CONNECTION`
  - `wPortStatus.bit1.PORT_ENABLE`
  - `wPortChange.bit0.C_PORT_CONNECTION`
  - `wPortChange.bit1.C_PORT_ENABLE`
  - `wHubStatus.bit0.HUB_LOCAL_POWER`
  - `wHubStatus.bit1.HUB_OVER_CURRENT`
- scope: `bit_name_and_position_only`

Required promotion conditions remain unchanged:

- matching evidence packet exists
- packet result sets `eligible_for_verified: true`
- packet result sets `evidence_status: reviewed`
- packet scope remains `bit_name_and_position_only`
- packet exclusions still include timing behavior, state transition behavior,
  `ClearPortFeature` behavior, and full USB compliance

Phase 8J still does **not** allow:

- page-level verified claims
- table-level verified claims
- hub-power policy or over-current behavior verification
- timing, debounce, or event-ordering verification
- `ClearPortFeature` behavioral verification
- TT behavior verification
