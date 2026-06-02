# Section Anchor Schema

> Written: 2026-06-02  
> Status: DRAFT  
> Canonical schema file: `contract/section_anchor_schema.yaml`

## Purpose

`section_refs` is the next-step evidence shape for this repo.

Its job is narrow:

- record future USB 2.0 section/page anchors in a structured form
- allow wiki pages and governed-table entries to carry reviewable anchor metadata
- prepare for entry-level verification pilots

It does **not**:

- auto-upgrade `claim_level`
- make a page or table entry `verified`
- replace human review

## Why This Exists

This repo already carries scalar `section_anchor` fields in some governed tables.
Those fields are useful, but they are too narrow for the next phase because they do
not express:

- multiple anchors for one claim
- page-level vs claim-block vs entry-level scope
- evidence state per anchor

`section_refs` is the additive future shape. It exists so that Phase 7 verification
work can attach anchors without over-claiming.

## Required Boundary

The following rule is mandatory:

> A `section_refs` block is evidence metadata only. Its presence does not upgrade
> `claim_level`, does not prove semantic correctness, and does not bypass
> review-required status.

This means the following is admissible:

- `claim_level: inferred`
- `evidence_status: review_required`
- `section_refs: [...]`

All three can coexist without contradiction.

## Canonical Minimal Shape

```yaml
section_refs:
  - spec: usb20
    section: "11.24.2.7.1"
    anchor_type: section
    evidence_status: review_required
```

Required fields per anchor:

- `spec`
- `section`
- `anchor_type`
- `evidence_status`

Optional fields:

- `page`
- `note`
- `applies_to`
- `quoted_surface`

## Allowed Embedding Surfaces

### 1. Wiki page claim blocks

Use when a page contains a bounded claim block that should later be reviewed against
the USB 2.0 PDF.

Example:

```yaml
section_refs:
  - spec: usb20
    section: "11.24.2.7.1"
    anchor_type: section
    evidence_status: review_required
    applies_to: "PORT_LOW_SPEED / PORT_HIGH_SPEED combined decoding summary"
```

### 2. Governed table entries

Use when a single table entry needs one or more anchors without promoting the whole
table or page.

Example:

```yaml
request_id: usb20_get_status_port
claim_level: inferred
evidence_status: review_required
section_refs:
  - spec: usb20
    section: "11.24.2"
    anchor_type: section
    evidence_status: review_required
    applies_to: "request family summary"
```

## Legacy Compatibility

Existing scalar `section_anchor` fields remain allowed during transition.

That means:

- existing tables do **not** need immediate migration
- existing validators do **not** need immediate change
- future work may gradually add `section_refs` where entry-level review becomes useful

During transition:

- `section_anchor` = legacy scalar field
- `section_refs` = preferred future structured field

## What Phase 7A Does Not Do

Phase 7A does not:

- retrofit every current page
- edit every governed table
- introduce a new validator
- mark any entry as `verified`
- claim PDF verification has happened

## Expected Next Step

The first intended consumer is the future verification pilot for
`specs/port_status_bits.md`.

That pilot should use `section_refs` at entry-level or bounded-claim-block level,
not page-level blanket promotion.
