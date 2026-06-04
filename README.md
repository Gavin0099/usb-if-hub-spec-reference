# USB-IF Hub Spec Reference

Governed USB hub specification reference and LLM wiki surface.

## Purpose

This repository provides controlled reference content from USB-IF hub-related
specifications for consumption by firmware governance contracts.

It does **not** govern firmware behavior. It clarifies standard semantics only.
It must not override confirmed project facts in consuming firmware repositories.

## Current USB 2.0 Status

- Canonical visible reference surface: `specs/` and `specs/en/`.
- Governed tracked entries: 86.
- Entry-level verified entries: 31.
- Reviewed entries: 55.
- Inferred tracked entries: 0.
- Verified scope is limited to descriptor field identity for 8 hub descriptor
  entries and bit name/position for 11 promoted port/hub status-change entries.
- No page-level, table-level, firmware-behavior, or full USB compliance
  verification is claimed.

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

- `tables/`: governed structured matrices for escalation triggers, hub
  descriptor fields, Transaction Translator entries, class requests, feature
  selectors, and port status bits.
- `exports/usb20_hub_class_request_manifest.yaml`: consumer-facing access
  manifest for governed tables.
- `evidence/entry_verification_packets/`: entry-level verification packets for
  promoted verified entries.
- `evidence/table_fingerprint_baseline.jsonl`: content-hash baseline for
  governed table drift observation.
- `scripts/validate_reference_surface_statistics.py`: consistency check for
  manually maintained visible counts across README, PLAN, homepages, and
  verification status pages.

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

Common repo-local checks:

```powershell
python scripts\validate_wiki_frontmatter.py
python scripts\validate_wiki_source_coverage.py
python scripts\validate_feature_selector_matrix.py
python scripts\validate_port_status_bit_matrix.py
python scripts\validate_class_request_matrix.py
python scripts\validate_class_request_coverage.py --matrix tables\class_request_matrix.yaml
python scripts\probe_table_fingerprint.py --mode check --manifest exports\usb20_hub_class_request_manifest.yaml --baseline-in evidence\table_fingerprint_baseline.jsonl
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
