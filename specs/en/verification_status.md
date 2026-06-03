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
| Class requests | 12 | 0 | 10 | 2 | 0 |
| Feature selectors | 25 | 0 | 4 | 21 | 0 |
| Port status bits | 10 | 8 | 0 | 2 | 0 |
| **Total** | **47** | **8** | **14** | **25** | **0** |

## Evidence Packet Summary

| Artifact type | Count | Status |
|---|---:|---|
| Entry verification packets | 8 | All correspond to promoted verified entries |

Term definitions:

- **Verified**: Passed the entry-level promotion gate; `claim_level: verified`; scope is explicitly bounded.
- **Reviewed**: Repo-local review is complete and the surface has been narrowed to a clearer field role, selector boundary, or request linkage, but it has not been promoted to entry-level verified.
- **Inferred**: Organized but not yet reviewed or verified; `claim_level: inferred`.

## Coverage Map

| Area | Current maturity center | Notes |
|---|---|---|
| Class requests | reviewed-heavy | `SET_FEATURE` / `CLEAR_FEATURE`, TT request families, and `GET_DESCRIPTOR` / `SET_DESCRIPTOR` have reviewed surfaces, but no entry-level verified promotions yet |
| Feature selectors | inferred-heavy with reviewed anchors | `C_HUB_LOCAL_POWER`, `C_HUB_OVER_CURRENT`, `C_PORT_CONNECTION`, and `C_PORT_ENABLE` have reviewed linkage; most remaining selector coverage is still inferred |
| Port status bits | verified-heavy | 8 core hub/port status-change bits have completed entry-level verified promotion; the remaining 2 boundary placeholders are still inferred |

## Reviewed Surface Inventory

The current `reviewed` surface is concentrated in these items:

- class requests
  - `SET_FEATURE` hub / port
  - `CLEAR_FEATURE` hub / port
  - `CLEAR_TT_BUFFER`
  - `RESET_TT`
  - `GET_TT_STATE`
  - `STOP_TT`
  - `GET_DESCRIPTOR`
  - `SET_DESCRIPTOR`
- feature selectors
  - `C_HUB_LOCAL_POWER`
  - `C_HUB_OVER_CURRENT`
  - `C_PORT_CONNECTION`
  - `C_PORT_ENABLE`

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
- Reviewed or inferred entries are safe to use as implementation truth.
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
- `evidence_status` / `claim_level` on entries in `tables/class_request_matrix.yaml` or `tables/feature_selector_matrix.yaml`
- Packets added or modified in `evidence/entry_verification_packets/`

The governed YAML tables are the source of truth; this page is a visibility summary only.
