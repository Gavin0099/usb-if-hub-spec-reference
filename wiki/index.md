---
title: Legacy USB Hub Wiki
scope: legacy_reference
governance_mode: superseded_by_specs
claim_level: index
source_refs:
  - usb_if_document_library
status: review_required
last_reviewed: 2026-06-03
---

# Legacy USB Hub Wiki

This `wiki/` tree is a legacy human/LLM reference layer.

The canonical visible LLM wiki surface is now under `specs/` and is rendered by VitePress:

- `specs/index.md`
- `specs/hub_class_requests.md`
- `specs/feature_selectors.md`
- `specs/port_status_bits.md`
- `specs/hub_descriptor.md`
- `specs/transaction_translator.md`
- `specs/escalation_table.md`
- `specs/version_source_map.md`
- `specs/verification_status.md`
- `specs/glossary.md`

## Boundary

- Do not treat this legacy tree as an independent authority surface.
- Do not use legacy version pages to override `specs/` pages or governed YAML tables.
- When prose and governed tables conflict, use the governed YAML tables and the `specs/` reference pages.
- High-confidence USB 2.0 behavior is not implied by this legacy index.

## Legacy Pages

The legacy pages may still be useful as orientation notes:

- `wiki/versions/usb20.md`
- `wiki/versions/usb21.md`
- `wiki/versions/usb32.md`
- `wiki/versions/usb4.md`
- `wiki/concepts/class_specific_requests.md`
- `wiki/concepts/hub_descriptor.md`
- `wiki/concepts/port_status.md`
- `wiki/concepts/transaction_translator.md`
