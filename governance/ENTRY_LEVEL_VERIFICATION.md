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
