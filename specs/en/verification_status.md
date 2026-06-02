---
title: Verification Status
claim_level: inferred
status: review_required
last_reviewed: "2026-06-02"
semantic_verification_claimed: false
---

# Verification Status

> This page is a static visibility summary, not an automatically generated source of truth.
> The governed YAML tables and evidence packets are the authoritative source materials.
> Numbers on this page must be updated manually whenever table entries or packet status changes.

## Current Verification Summary

| Area | Table | Entries | Verified | Reviewed non-promoting | Inferred |
|---|---|---|---|---|---|
| Hub class requests | `tables/class_request_matrix.yaml` | 12 | 0 | 0 | 12 |
| Feature selectors | `tables/feature_selector_matrix.yaml` | 25 | 0 | 0 | 25 |
| Port status bits | `tables/port_status_bit_matrix.yaml` | 10 | 1 | 1 | 8 |
| Evidence packets | `evidence/entry_verification_packets/` | 2 | 1 (promoted) | 1 (non-promoting) | — |
| **Total** | | **47** | **1** | **1** | **45** |

Term definitions:

- **Verified**: Passed the entry-level promotion gate; `claim_level: verified`; scope is explicitly bounded.
- **Reviewed non-promoting**: Review complete; evidence packet exists; `eligible_for_verified: false`; promotion is deliberately withheld.
- **Inferred**: Organized but not yet reviewed or verified; `claim_level: inferred`.

## Verified Entries

Only one entry has completed verified promotion:

| Entry | Field | Bit | Verified Scope |
|---|---|---|---|
| PORT_CONNECTION | `wPortStatus` | bit 0 | bit name and bit position only |

The verified scope is explicitly limited to **bit name and bit position**.

The following are outside this verified scope:

- Timing behavior
- State transition behavior
- `ClearPortFeature` behavior
- Host-stack interpretation
- Full USB 2.0 compliance

## Reviewed but Not Promoted

The following entry has a completed reviewed evidence packet but has not been promoted to verified:

| Entry | Field | Bit | Review Status | Reason |
|---|---|---|---|---|
| PORT_ENABLE | `wPortStatus` | bit 1 | reviewed | Pilot promotion boundary is currently limited to `PORT_CONNECTION`; expansion requires a separate gate update |

**`reviewed` is not the same as `verified`.**

Reviewed means an evidence packet was created and reviewed, but no promotion was triggered.

Verified means the entry passed the Phase 8C promotion gate and `claim_level` was upgraded to `verified`.

## What This Page Does Not Claim

This page does not claim:

- USB 2.0 hub behavior is fully verified.
- Any page-level or table-level verification is complete.
- `PORT_ENABLE` is verified.
- Inferred entries are safe to use as implementation truth.
- This reference overrides confirmed project facts in consuming repositories.
- Static counts are an automated source of truth synchronized with the YAML tables.

## Static Numbers Note

The entry counts and packet statuses on this page are a manually maintained static summary.

This page must be updated manually when any of the following change:

- `claim_level` on any entry in `tables/port_status_bit_matrix.yaml`
- Entries added or updated in `tables/class_request_matrix.yaml` or `tables/feature_selector_matrix.yaml`
- Packets added or modified in `evidence/entry_verification_packets/`

The governed YAML tables are the source of truth; this page is a visibility summary only.
