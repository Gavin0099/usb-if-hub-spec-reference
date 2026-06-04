> **Last Updated**: 2026-06-04
> **Owner**: USB-IF Hub Spec Reference
> **Freshness**: Sprint (14d)

# PLAN

This repository is a read-only USB hub specification reference layer. It
clarifies USB hub standard semantics for consuming firmware repositories, but it
does not govern firmware behavior and does not override confirmed project facts.

## Current State

- USB 2.0 LLM wiki/reference surface is complete at reviewed-reference depth.
- Governed tracked entries: 86.
- Entry-level verified entries: 8.
- Reviewed entries: 78.
- Inferred tracked entries: 0.
- Verification scope remains narrow: verified entries are verified only for bit
  name and bit position.
- No page-level, table-level, firmware-behavior, or full USB compliance
  verification is claimed.

## Completed Phases

### Phase 1 - Governance Baseline

- Adopted `ai-governance-framework` baseline.
- Created `contract.yaml`, `AGENTS.md`, and `AGENTS.base.md`.
- Installed repo governance hooks.

Claim ceiling: governance baseline only.

### Phase 2 - USB-IF Spec Reference Tables

- `tables/escalation_trigger_matrix.yaml`: 10 reviewed USB 2.0 standard-side
  escalation trigger-boundary entries.
- `tables/hub_descriptor_matrix.yaml`: 8 reviewed USB 2.0 hub descriptor
  field-role entries.
- `tables/transaction_translator_matrix.yaml`: 10 reviewed USB 2.0 TT type,
  think-time, and TT request-linkage entries.
- `tables/class_request_matrix.yaml`: 12 entries, 9/9 USB 2.0 hub class request
  families covered.
- `tables/feature_selector_matrix.yaml`: 25 entries, standard port selector
  namespace 0-22 covered, including reserved-boundary slots.
- `tables/port_status_bit_matrix.yaml`: 21 tracked hub/port status and change
  entries, including 8 verified entries, 11 reviewed defined port
  status/change namespace entries, and 2 reviewed high-bit boundary
  placeholders.
- Core bilingual spec pages are present under `specs/` and `specs/en/`.

Claim ceiling: structured spec-reference entries only; no firmware behavior.

### Phase 2A - Wiki Frontmatter Bootstrap

- Added required frontmatter to canonical spec pages.
- Established `scripts/validate_wiki_frontmatter.py`.

Claim ceiling: wiki frontmatter structural consistency only.

### Phase 2B - Wiki/Table Consistency Probe

- Added observation-only wiki consistency probe and fixture smoke coverage.
- Real table/page token coverage has been improved through later page deepening.

Claim ceiling: lexical consistency observation only; no semantic proof.

### Phase 3 - Cross-Repo Reference Registration

- Registered this repo as standard-side reference input in the consuming
  firmware contract repo traceability surface.
- Allowed usage: lookup, semantics clarification, escalation support,
  terminology alignment.
- Prohibited usage: overriding project facts, treating inferred/reviewed entries
  as implementation truth.

Claim ceiling: cross-repo reference registered only.

### Phase 4 - Machine-Readable Consumer Access Contract

- Added `exports/usb20_hub_class_request_manifest.yaml`.
- Validators cover class request, feature selector, port status bit, and manifest
  structure.

Claim ceiling: machine-readable namespace and access contract only.

### Phase 5B - Table Fingerprint Drift Observability

- Added `scripts/probe_table_fingerprint.py`.
- Supports `baseline`, `check`, and `compact` modes.
- Current table fingerprint baseline is synchronized: 6 governed tables, 0 drift.

Claim ceiling: table content fingerprint drift only.

### Phase 6 - USB 2.0 Core Reference Deepening

- Deepened core zh-TW and English pages for:
  - hub descriptor
  - hub class requests
  - feature selectors
  - port status bits
  - transaction translator
  - escalation table
  - glossary
- Current core pages are readable reference summaries with explicit non-claims.

Claim ceiling: readable reference surface only; not semantic verification.

### Phase 7 - Section Anchor Metadata

- Added section anchor schema and governance documentation.
- Attached section references to selected pilot entries.
- Clarified that section references are evidence metadata and do not upgrade
  claim level by themselves.

Claim ceiling: section-ref metadata only.

### Phase 8 - Entry-Level Verification Pilot

- Added entry verification packet schema and governance guidance.
- Added promotion gate for a bounded pilot set.
- Current verified entries:
  - `wPortStatus.bit0.PORT_CONNECTION`
  - `wPortStatus.bit1.PORT_ENABLE`
  - `wPortChange.bit0.C_PORT_CONNECTION`
  - `wPortChange.bit1.C_PORT_ENABLE`
  - `wHubStatus.bit0.HUB_LOCAL_POWER`
  - `wHubStatus.bit1.HUB_OVER_CURRENT`
  - `wHubChange.bit0.C_HUB_LOCAL_POWER`
  - `wHubChange.bit1.C_HUB_OVER_CURRENT`
- Verified scope for all 8 entries: bit name and bit position only.

Claim ceiling: entry-level verified gate only.

### Phase 9 - LLM Wiki Reference Surface Completion

- Canonical visible wiki surface is under `specs/` and `specs/en/`.
- Legacy `wiki/` pages have been demoted to orientation notes.
- Homepage and verification status surfaces align to 86 tracked entries, 8
  verified entries, 78 reviewed entries, and 0 inferred tracked entries.

Claim ceiling: LLM reference readability and boundary clarity only.

### Phase 10 - ai-governance Repo-Local Import

- Pulled latest `ai-governance-framework` state at
  `a0d42d15a43cf98be33dc8618deae8153d69ff62`.
- Imported only repo-local reporting and reviewer-facing surfaces:
  - `governance/RESPONSE_ENVELOPE_CONTRACT.md`
  - `governance/TRUST_BOUNDARY_TAXONOMY.md`
- Registered retained files in `governance/AUTHORITY.md`, `contract.yaml`, and
  `governance/framework.lock.json`.
- Excluded framework memory, artifacts, runtime profile validator, fleet
  governance, and new CI workflow surfaces.

Claim ceiling: reporting/reference governance surface only.

## Active Validators

- `python scripts\validate_wiki_frontmatter.py`
- `python scripts\validate_wiki_source_coverage.py`
- `python scripts\validate_escalation_trigger_matrix.py`
- `python scripts\validate_hub_descriptor_matrix.py`
- `python scripts\validate_transaction_translator_matrix.py`
- `python scripts\validate_feature_selector_matrix.py`
- `python scripts\validate_port_status_bit_matrix.py`
- `python scripts\validate_class_request_matrix.py`
- `python scripts\validate_class_request_coverage.py --matrix tables\class_request_matrix.yaml`
- `python scripts\probe_table_fingerprint.py --mode check --manifest exports\usb20_hub_class_request_manifest.yaml --baseline-in evidence\table_fingerprint_baseline.jsonl`
- `npm.cmd run build`

## Open Work

1. Audit visible README/governance copy for stale or mojibake reference wording.
2. Decide whether to add a generated statistics validator for verification
   counts; do not add it until the verified promotion workflow is stable enough
   to define a durable contract.
3. Continue entry-level verification only when narrow evidence packets and gate
   scope are explicit.
4. Keep consuming-repo integration as reference-only; any firmware behavior
   change still belongs in the consuming repo's Standard Escalation Mode.

## Cannot Claim

- USB 2.0 hub behavior is fully verified.
- All entries are PDF-semantically verified.
- Reviewed coverage is the same as verified coverage.
- This repo can override consuming firmware project facts.
- Fleet governance is enabled.
- Runtime profile validation or response envelope enforcement is active.
