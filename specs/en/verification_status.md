---
title: Verification Status
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
semantic_verification_claimed: false
---

# Verification Status

> This page is a static visibility summary, not an automatically generated source of truth.  
> The governed YAML tables and evidence packets are the authoritative source materials.  
> Numbers on this page must be updated manually whenever table entries or packet status changes.

## Current Verification Summary

| Area | Tracked entries | Verified | Reviewed | Inferred | Missing |
|---|---:|---:|---:|---:|---:|
| Hub descriptor fields | 8 | 8 | 0 | 0 | 0 |
| Transaction Translator entries | 10 | 0 | 10 | 0 | 0 |
| Escalation triggers | 10 | 0 | 10 | 0 | 0 |
| Class requests | 12 | 12 | 0 | 0 | 0 |
| Feature selectors | 25 | 0 | 25 | 0 | 0 |
| Port status bits | 21 | 8 | 13 | 0 | 0 |
| **Total** | **86** | **28** | **58** | **0** | **0** |

## Evidence Packet Summary

| Artifact type | Count | Status |
|---|---:|---|
| Entry verification packets | 28 | All correspond to promoted verified entries |

Term definitions:

- **Verified**: Passed the entry-level promotion gate; `claim_level: verified`; scope is explicitly bounded.
- **Reviewed**: Repo-local review is complete and the surface has been narrowed to a clearer field role, selector boundary, or request linkage, but it has not been promoted to entry-level verified.
- **Inferred**: Organized but not yet reviewed or verified; `claim_level: inferred`.

## Coverage Map

| Area | Current maturity center | Notes |
|---|---|---|
| Hub descriptor fields | verified | All 8 tracked hub descriptor fields have descriptor field identity verified; this does not verify descriptor dumps or device behavior |
| Transaction Translator entries | reviewed | All 10 tracked TT type, think-time, and request-linkage entries have reviewed reference-boundary surfaces, but no split-transaction behavior verification |
| Escalation triggers | reviewed | All 10 tracked E-01 through E-10 trigger boundaries have reviewed reference surfaces, but escalation execution remains owned by consuming repos |
| Class requests | verified | All 12 tracked class requests have request-linkage-only verified promotions |
| Feature selectors | reviewed | All 25 tracked feature selectors now have reviewed selector-boundary or reserved-boundary surfaces |
| Port status bits | verified / reviewed | 8 core hub/port status-change bits have completed entry-level verified promotion; 11 additional defined port status/change bits and 2 high-bit boundary placeholders are reviewed namespace/boundary entries only |

## Reviewed Surface Inventory

The current `reviewed` surface is concentrated in these items:

- transaction translator entries
  - Single TT / Multiple TT
  - TT think-time values `00`, `01`, `10`, `11`
  - `CLEAR_TT_BUFFER`
  - `RESET_TT`
  - `GET_TT_STATE`
  - `STOP_TT`
- escalation triggers
  - `E-01` through `E-10`
- feature selectors
  - `PORT_CONNECTION`
  - `PORT_OVER_CURRENT`
  - `PORT_LOW_SPEED`
  - `PORT_HIGH_SPEED`
  - reserved selector slots `5-7`
  - reserved selector slots `11-15`
  - `C_HUB_LOCAL_POWER`
  - `C_HUB_OVER_CURRENT`
  - `C_PORT_CONNECTION`
  - `C_PORT_ENABLE`
  - `C_PORT_SUSPEND`
  - `C_PORT_OVER_CURRENT`
  - `C_PORT_RESET`
  - `PORT_ENABLE`
  - `PORT_SUSPEND`
  - `PORT_RESET`
  - `PORT_POWER`
  - `PORT_TEST`
  - `PORT_INDICATOR`
- port status bit boundary placeholders
  - `PORT_SUSPEND`
  - `PORT_OVER_CURRENT`
  - `PORT_RESET`
  - `PORT_POWER`
  - `PORT_LOW_SPEED`
  - `PORT_HIGH_SPEED`
  - `PORT_TEST`
  - `PORT_INDICATOR`
  - `C_PORT_SUSPEND`
  - `C_PORT_OVER_CURRENT`
  - `C_PORT_RESET`
  - `PORT_STATUS_HIGH_BIT_BOUNDARY`
  - `PORT_CHANGE_HIGH_BIT_BOUNDARY`

These `reviewed` surfaces mean the repo-local boundary is clearer than a purely inferred surface.
They do **not** mean those surfaces have completed entry-level verified promotion.

## Verified Entries

Eight entries have completed verified promotion (Phase 8E, Phase 8H, Phase 8I, Phase 8J, and Phase 8K):

| Entry | Field | Bit | Verified Scope |
|---|---|---|---|
| PORT_CONNECTION | `wPortStatus` | bit 0 | bit name and bit position only |
| PORT_ENABLE | `wPortStatus` | bit 1 | bit name and bit position only |
| C_PORT_CONNECTION | `wPortChange` | bit 0 | bit name and bit position only |
| C_PORT_ENABLE | `wPortChange` | bit 1 | bit name and bit position only |
| HUB_LOCAL_POWER | `wHubStatus` | bit 0 | bit name and bit position only |
| HUB_OVER_CURRENT | `wHubStatus` | bit 1 | bit name and bit position only |
| C_HUB_LOCAL_POWER | `wHubChange` | bit 0 | bit name and bit position only |
| C_HUB_OVER_CURRENT | `wHubChange` | bit 1 | bit name and bit position only |

The verified scope is explicitly limited to **bit name and bit position**.

The following are outside the verified scope for all entries:

- Timing behavior
- State transition behavior
- `SetPortFeature` behavior
- `ClearPortFeature` behavior
- Error recovery conditions
- Host-stack interpretation
- Full USB 2.0 compliance

## What This Page Does Not Claim

This page does not claim:

- USB 2.0 hub behavior is fully verified.
- Any page-level or table-level verification is complete.
- `PORT_ENABLE` state machine, `SetPortFeature`, `ClearPortFeature`, or error recovery behavior is verified.
- Reviewed entries are safe to use as implementation truth.
- Reviewed coverage is the same as verified coverage.
- This reference overrides confirmed project facts in consuming repositories.
- Static counts are an automated source of truth synchronized with the YAML tables.

## Reference Surface Maintenance Rule

When verification maturity or tracked entry counts change, the following visible surfaces must be checked together:

- `specs/index.md`: tracked / maturity summary on the zh-TW homepage
- `specs/en/index.md`: tracked / maturity summary on the English homepage
- `specs/verification_status.md`: zh-TW verification summary, coverage map, verified entries, and non-claims
- `specs/en/verification_status.md`: English verification summary, coverage map, verified entries, and non-claims
- Core spec pages: `Non-claims` and `Governed Linkage` sections for the affected entry family

Maintenance rules:

- Wording-only updates must not change YAML source-of-truth semantics.
- New or promoted verified entries must update the verification status pages and homepage summaries together.
- When a surface moves from inferred to reviewed, the maturity breakdown on this page and its coverage map must also be updated.
- Evidence packet count changes must update the evidence packet summary.
- Adding `section_refs` metadata must not automatically claim that a page or entry is verified.

## Static Numbers Note

The entry counts and packet statuses on this page are a manually maintained static summary.

This page must be updated manually when any of the following change:

- `claim_level` on any entry in `tables/port_status_bit_matrix.yaml`
- `evidence_status` / `claim_level` on entries in `tables/escalation_trigger_matrix.yaml`, `tables/hub_descriptor_matrix.yaml`, `tables/transaction_translator_matrix.yaml`, `tables/class_request_matrix.yaml`, or `tables/feature_selector_matrix.yaml`
- Packets added or modified in `evidence/entry_verification_packets/`

The governed YAML tables are the source of truth; this page is a visibility summary only.
