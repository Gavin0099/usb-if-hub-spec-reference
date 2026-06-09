# USB-IF Hub Spec Reference

A reference guide for USB hub specification details — descriptor fields, class requests,
and status bit definitions for USB 2.0 and USB 3.2 hubs.

## What Is This?

### The Problem

Writing firmware for a USB hub requires precise knowledge of specific details from the
USB specification: which bit in a status register means "device connected", what value
a feature selector should have, what fields a hub descriptor must contain. The USB spec
is a large PDF document spanning hundreds of pages, and getting these details wrong leads
to subtle firmware bugs that are hard to trace.

Two things make this harder in practice:

- Relevant details are scattered across many spec sections.
- USB 2.0 and USB 3.2 hubs have different rules, and it is easy to apply the wrong
  version's rules by mistake.

### What This Repo Provides

- A **structured, searchable reference** for USB 2.0 and USB 3.2 hub descriptor fields,
  class requests, port status bits, and feature selectors.
- Clear **claim boundaries**: each entry states exactly what is verified and what is out
  of scope. This prevents the reference from claiming more than the spec actually says.
- An **escalation guide** (`specs/escalation_table.md`): a checklist of conditions where
  firmware behavior may conflict with the spec and requires a closer review.
- **Machine-readable tables** that a CI system can use to detect unexpected changes in
  the reference content.

### What This Repo Does Not Cover

- How hubs behave at runtime (state machines, timing, error recovery sequences).
- Host-side driver behavior (Windows, Linux, xHCI controller internals).
- USB electrical compliance or certification testing.
- USB4 or Thunderbolt hub semantics.

This repo clarifies what the spec says. It does not make decisions about firmware
implementation, and it does not override engineering judgment on project-specific behavior.

## Purpose (Technical Summary)

## Governed Surface Status

### USB 2.0 — Freeze

- Canonical visible reference surface: `specs/` and `specs/en/`.
- Governed tracked entries: 151.
- Entry-level verified entries: 105.
- Reviewed entries: 46 (reserved bits and boundary-only placeholders; not pending promotion).
- Verified scope: selector-name/value, descriptor field identity, bit name/position,
  request-linkage identity, bit-group name and value-encoding identity.
- No page-level, table-level, firmware-behavior, or full USB compliance verification is claimed.

### USB 3.x / SuperSpeed Hub — Governed Surface (USB3-IEP-1)

- Six governed matrices: SS hub descriptor (9 verified), SS hub class requests (10 verified),
  SS port status/change bits (15 verified, 4 reviewed reserved boundary),
  SS feature selectors (6 verified, USB3-FS-2),
  SS wHubCharacteristics bit groups (4 verified, 1 reviewed reserved, USB3-WHC-1),
  SS hub interrupt endpoint (4 verified, USB3-IEP-1).
- Governed tracked entries: 53. Entry-level verified: 48. Reviewed: 5.
- Reference surface is matrix-defined only; not equivalent to full USB 3.x spec coverage.
- No LTSSM, xHCI, electrical, or USB-IF certification claims.

See:
- [specs/verification_status.md](specs/verification_status.md)
- [specs/en/verification_status.md](specs/en/verification_status.md)
- [PLAN.md](PLAN.md)

## Canonical Reference Pages

| Document | Scope | Description |
|----------|-------|-------------|
| [specs/hub_descriptor.md](specs/hub_descriptor.md) | USB 2.0 section 11.23 | Hub descriptor field definitions |
| [specs/port_status_bits.md](specs/port_status_bits.md) | USB 2.0 section 11.24.2.7 | Port, hub, and change-bit reference surface |
| [specs/hub_class_requests.md](specs/hub_class_requests.md) | USB 2.0 section 11.24.2 | Hub class request semantics and setup-field linkage |
| [specs/transaction_translator.md](specs/transaction_translator.md) | USB 2.0 TT reference surface | Transaction Translator summary and non-claims |
| [specs/escalation_table.md](specs/escalation_table.md) | Standard escalation policy | Escalation triggers for consuming repos |
| [specs/version_source_map.md](specs/version_source_map.md) | Multi-version source map | USB 2.0 / 2.1 / 3.2 / 4.0 hub-focused source mapping |

English pages are available under [specs/en/](specs/en/).

## Machine-Readable Surfaces

- `tables/`: governed structured matrices for USB 2.0 (9 tables) and USB 3.x (6 tables).
- `exports/hub_governed_surface_manifest.yaml`: unified consumer-facing manifest
  covering all 15 governed tables with per-family authority surface, claim ceiling,
  and consumer usage contract. Supersedes `exports/usb20_hub_class_request_manifest.yaml`.
- `evidence/entry_verification_packets/`: entry-level verification packets for promoted
  verified entries (105 USB 2.0 + 48 USB 3.x packets).
- `evidence/table_fingerprint_baseline.jsonl`: content-hash baseline for all 15 governed
  table drift detection.
- `scripts/validate_reference_surface_statistics.py`: consistency check for manually
  maintained visible counts across README, PLAN, homepages, and verification status pages.

## Consumer Integration

Consuming repositories can integrate this governed surface through a two-step CI gate:

```powershell
# Step 1 — Manifest structural integrity
python scripts\validate_hub_governed_surface_manifest.py

# Step 2 — Table content drift detection
python scripts\probe_table_fingerprint.py --mode check `
  --manifest exports\hub_governed_surface_manifest.yaml `
  --baseline-in evidence\table_fingerprint_baseline.jsonl
```

Both steps must PASS before treating the governed surface as stable. The contract
documents allowed usage, forbidden usage, and failure interpretation:
- [`docs/CONSUMER_INTEGRATION_CONTRACT.md`](docs/CONSUMER_INTEGRATION_CONTRACT.md)

This contract is smoke-tested. The smoke fixture verifies manifest integrity, zero drift
on 12 governed tables, and drift detection with table-level attribution when a hash is
corrupted.

## Governance Layers

- `contract/`: machine-readable authority, claim, evidence, version, and
  staleness rules.
- `governance/`: repo-local governance documents and imported reporting
  conventions.
- `specs/`: canonical human/LLM reference pages.
- `wiki/`: legacy orientation notes only; not the canonical authority surface.
- `evidence/`: source registry, validation receipts, drift snapshots, and
  evidence packets.
- `monitor/`: USB-IF source drift detection scripts/config.

## Source Drift Principle

Source monitoring detects **staleness risk** and triggers review.
It does **not** automatically validate semantic correctness or auto-upgrade
claims.

## Usage Boundary

This repo may be used to **clarify standard semantics**. It may **not** be used
to override confirmed project facts in consuming firmware repos.

When a conflict is detected between this spec reference and a confirmed project
fact, the consuming repo's Standard Escalation Mode must be activated. This repo
provides standard-side input only; the consuming repo owns project-specific
behavior decisions.

## Governance Import Status

Adopted baseline: [ai-governance-framework](https://github.com/Gavin0099/ai-governance-framework)
v1.2.0.

Current repo-local import includes reporting and reviewer-facing boundary
surfaces only. It does not enable fleet governance, runtime profile validation,
or response envelope enforcement.

## Validation

Core repo-local checks:

```powershell
# USB 2.0 + USB 3.x matrix validators
python scripts\validate_hub_descriptor_matrix.py
python scripts\validate_feature_selector_matrix.py
python scripts\validate_port_status_bit_matrix.py
python scripts\validate_class_request_matrix.py
python scripts\validate_standard_device_request_matrix.py
python scripts\validate_wHubCharacteristics_bit_matrix.py
python scripts\validate_ss_hub_descriptor_matrix.py
python scripts\validate_ss_hub_class_request_matrix.py
python scripts\validate_ss_port_status_bit_matrix.py

# Export contract validators
python scripts\validate_hub_governed_surface_manifest.py
python scripts\probe_table_fingerprint.py --mode check `
  --manifest exports\hub_governed_surface_manifest.yaml `
  --baseline-in evidence\table_fingerprint_baseline.jsonl

# Consumer integration smoke
python scripts\smoke_consumer_integration_fixtures.py

# Static site build
npm.cmd run build
```

## Non-Claims

This repository does not claim:

- USB 2.0 hub behavior is fully verified.
- All entries are PDF-semantically verified.
- Reviewed coverage is equivalent to verified coverage.
- Firmware implementation behavior is established here.
- This repo can override consuming firmware project facts.
- Fleet governance or runtime enforcement is active.
- LTSSM runtime state transitions are verified.
- xHCI port state management or xHCI enumeration behavior is verified.
- USB 3.x governed matrix surface is equivalent to full USB 3.x spec coverage.
- The export contract establishes firmware compliance truth or USB-IF certification.
