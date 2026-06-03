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

| Area | Tracked entries | Verified | Reviewed / inferred | Missing |
|---|---:|---:|---:|---:|
| Class requests | 12 | 0 | 12 | 0 |
| Feature selectors | 25 | 0 | 25 | 0 |
| Port status bits | 10 | 2 | 8 | 0 |
| **Total** | **47** | **2** | **45** | **0** |

## Evidence Packet Summary

| Artifact type | Count | Status |
|---|---:|---|
| Entry verification packets | 2 | Both correspond to promoted verified entries |

Term definitions:

- **Verified**: Passed the entry-level promotion gate; `claim_level: verified`; scope is explicitly bounded.
- **Reviewed non-promoting**: Review complete; evidence packet exists; `eligible_for_verified: false`; promotion is deliberately withheld.
- **Inferred**: Organized but not yet reviewed or verified; `claim_level: inferred`.

## Verified Entries

Two entries have completed verified promotion (Phase 8E and Phase 8H):

| Entry | Field | Bit | Verified Scope |
|---|---|---|---|
| PORT_CONNECTION | `wPortStatus` | bit 0 | bit name and bit position only |
| PORT_ENABLE | `wPortStatus` | bit 1 | bit name and bit position only |

The verified scope is explicitly limited to **bit name and bit position**.

The following are outside the verified scope for all entries:

- Timing behavior
- State transition behavior
- `SetPortFeature` behavior
- `ClearPortFeature` behavior
- Error recovery conditions
- Host-stack interpretation
- Full USB 2.0 compliance

## Reviewed but Not Promoted

No reviewed non-promoting entries currently exist. All reviewed packets have already been promoted through Phase 8H.

## What This Page Does Not Claim

This page does not claim:

- USB 2.0 hub behavior is fully verified.
- Any page-level or table-level verification is complete.
- PORT_ENABLE state machine, SetPortFeature, or error recovery behavior is verified.
- Inferred entries are safe to use as implementation truth.
- This reference overrides confirmed project facts in consuming repositories.
- Static counts are an automated source of truth synchronized with the YAML tables.

## Reference Surface Maintenance Rule

When verification maturity or tracked entry counts change, the following visible surfaces must be checked together:

- `specs/index.md`: tracked / verified summary on the zh-TW homepage
- `specs/en/index.md`: tracked / verified summary on the English homepage
- `specs/verification_status.md`: zh-TW verification summary, verified entries, and non-claims
- `specs/en/verification_status.md`: English verification summary, verified entries, and non-claims
- Core spec pages: `Non-claims` and `Governed Linkage` sections for the affected entry family

Maintenance rules:

- Wording-only updates must not change YAML source-of-truth semantics.
- New or promoted verified entries must update the verification status pages and homepage summaries together.
- Evidence packet count changes must update the evidence packet summary.
- Adding `section_refs` metadata must not automatically claim that a page or entry is verified.

## Static Numbers Note

The entry counts and packet statuses on this page are a manually maintained static summary.

This page must be updated manually when any of the following change:

- `claim_level` on any entry in `tables/port_status_bit_matrix.yaml`
- Entries added or updated in `tables/class_request_matrix.yaml` or `tables/feature_selector_matrix.yaml`
- Packets added or modified in `evidence/entry_verification_packets/`

The governed YAML tables are the source of truth; this page is a visibility summary only.
