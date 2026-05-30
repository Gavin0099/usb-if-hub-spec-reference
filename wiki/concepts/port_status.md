---
title: Port Status and Change Bits
topic: port_status
usb_versions:
  - usb_2_0
  - usb_3_2
authority_required: normative_official
claim_level: draft
source_refs:
  - usb20_spec
status: draft
last_reviewed: 2026-05-30
forbidden_assumptions:
  - status_bits_equal_change_bits
  - usb4_direct_mapping_without_evidence
---

# Port Status and Change Bits

This page separates current status from change indicators and scopes them by USB version.

## Baseline Rule

USB 2.0 definitions are baseline for classic hub port status and change flags.

## Common Confusion

Status bits and change bits are different categories and must not be merged.

## Boundary

SuperSpeed and USB4 mappings require explicit versioned evidence before reuse.
