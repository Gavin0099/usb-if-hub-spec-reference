---
title: USB 2.0 Version Scope
topic: version_scope
usb_versions:
  - usb_2_0
authority_required: normative_official
claim_level: inferred
source_refs:
  - usb20_spec
status: review_required
last_reviewed: 2026-06-03
---

# USB 2.0

USB 2.0 is the baseline hub class model in this repository.

This legacy page is not the canonical visible LLM wiki surface.
Use the `specs/` pages for current repo-local claim boundaries:

- `specs/hub_class_requests.md`
- `specs/feature_selectors.md`
- `specs/port_status_bits.md`
- `specs/hub_descriptor.md`
- `specs/transaction_translator.md`
- `specs/verification_status.md`

## Included Baseline Areas

- Hub descriptor fields
- Port status and change bits
- Hub class-specific requests
- Transaction Translator (TT) behavior for HS hubs

## Claim Boundary

- This page is an orientation note, not an independent normative authority surface.
- USB 2.0 reviewed reference coverage is represented in `specs/verification_status.md`.
- Entry-level verified coverage remains limited to explicitly promoted entries and their stated scopes.
- This page must not be used to override confirmed project facts in consuming repositories.
