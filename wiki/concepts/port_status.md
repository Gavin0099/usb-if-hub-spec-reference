---
title: Port Status and Change Bits
topic: port_status
usb_versions:
  - usb_2_0
  - usb_3_2
authority_required: normative_official
claim_level: inferred
source_refs:
  - usb20_spec
status: review_required
last_reviewed: 2026-06-03
forbidden_assumptions:
  - status_bits_equal_change_bits
  - usb4_direct_mapping_without_evidence
---

# Port Status and Change Bits

This legacy concept page is an orientation note only.

Use the canonical `specs/` surface for current repo-local status/change boundaries:

- `specs/port_status_bits.md`
- `specs/en/port_status_bits.md`
- `tables/port_status_bit_matrix.yaml`

## Boundary

- Do not treat this page as an independent status-bit truth table.
- Status bits and change bits are different categories and must not be merged.
- SuperSpeed and USB4 mappings require explicit versioned evidence before reuse.
- Do not use this legacy page to override governed YAML tables or consuming-repo project facts.
