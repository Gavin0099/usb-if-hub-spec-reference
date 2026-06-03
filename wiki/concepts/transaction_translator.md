---
title: Transaction Translator
topic: transaction_translator
usb_versions:
  - usb_2_0
  - usb_2_1
authority_required: normative_official
claim_level: inferred
source_refs:
  - usb20_spec
status: review_required
last_reviewed: 2026-06-03
---

# Transaction Translator

This legacy concept page is an orientation note only.

Use the canonical `specs/` surface for current repo-local TT boundaries:

- `specs/transaction_translator.md`
- `specs/en/transaction_translator.md`
- `specs/hub_descriptor.md`
- `specs/en/hub_descriptor.md`

## Boundary

- Do not treat this page as an independent TT behavior truth table.
- TT semantics are anchored in USB 2.0 high-speed hub behavior.
- Any USB 2.1-related TT interpretation must be presented as ECN/addendum delta against USB 2.0 baseline.
- Do not infer TT-equivalent semantics in USB4 context without explicit normative evidence.
