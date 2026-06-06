---
title: Verification Status
claim_level: inferred
status: review_required
last_reviewed: "2026-06-05"
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
| Transaction Translator entries | 10 | 10 | 0 | 0 | 0 |
| Escalation triggers | 10 | 10 | 0 | 0 | 0 |
| Class requests | 12 | 12 | 0 | 0 | 0 |
| Feature selectors | 25 | 25 | 0 | 0 | 0 |
| Port status bits | 64 | 19 | 45 | 0 | 0 |
| Hub interrupt endpoint | 4 | 0 | 4 | 0 | 0 |
| Standard device requests | 12 | 0 | 12 | 0 | 0 |
| **Total** | **145** | **84** | **61** | **0** | **0** |

## Evidence Packet Summary

| Artifact type | Count | Status |
|---|---:|---|
| Entry verification packets | 84 | All correspond to promoted verified entries; 61 reviewed entries have no evidence packet |

Term definitions:

- **Verified**: Passed the entry-level promotion gate; `claim_level: verified`; scope is explicitly bounded.
- **Reviewed**: Repo-local review is complete and the surface has been narrowed to a clearer field role, selector boundary, or request linkage, but it has not been promoted to entry-level verified.
- **Inferred**: Organized but not yet reviewed or verified; `claim_level: inferred`.

## Coverage Map

| Area | Current maturity center | Notes |
|---|---|---|
| Hub descriptor fields | verified | All 8 tracked hub descriptor fields have descriptor field identity verified; this does not verify descriptor dumps or device behavior |
| Transaction Translator entries | verified | All 10 tracked TT type, think-time, and request-linkage entries have promoted entry-level verified scope |
| Escalation triggers | verified | All 10 tracked E-01 through E-10 trigger boundaries have promoted entry-level verified scope |
| Class requests | verified | All 12 tracked class requests have request-linkage-only verified promotions |
| Feature selectors | verified | All 25 tracked feature selectors are now verified at selector-name-and-value scope |
| Port status bits | verified / reviewed | 19 core hub/port status-change bits have completed entry-level verified promotion; 4 high-bit boundary placeholders are reviewed; 41 reserved bit entries (wPortStatus, wPortChange, wHubStatus, wHubChange reserved bits) have reviewed namespace boundary |
| Hub interrupt endpoint | reviewed | 4 status change endpoint descriptor fields (bEndpointAddress, bmAttributes, wMaxPacketSize, bInterval) have reviewed field identity; no verified promotion |
| Standard device requests | reviewed | 12 standard USB device requests applicable to hubs have reviewed request-linkage scope; no verified promotion |

## Reviewed Surface Inventory

The current `reviewed` surface is concentrated in these items:

- port status bit boundary placeholders
  - `PORT_STATUS_HIGH_BIT_BOUNDARY`
  - `PORT_CHANGE_HIGH_BIT_BOUNDARY`
  - `HUB_STATUS_HIGH_BIT_BOUNDARY` (new)
  - `HUB_CHANGE_HIGH_BIT_BOUNDARY` (new)
- hub interrupt endpoint descriptor fields
  - `bEndpointAddress`, `bmAttributes`, `wMaxPacketSize`, `bInterval`

These `reviewed` surfaces mean the repo-local boundary is clearer than a purely inferred surface.
They do **not** mean those surfaces have completed entry-level verified promotion.

## Verified Entries

Eighty-four entries have completed verified promotion (`claim_level: verified`); 8 entries have reviewed scope only:

| Entry | Field | Bit | Verified Scope |
|---|---|---|---|
| bDescLength | `wHubDescriptor.bDescLength` | - | descriptor field identity only |
| bDescriptorType | `wHubDescriptor.bDescriptorType` | - | descriptor field identity only |
| bNbrPorts | `wHubDescriptor.bNbrPorts` | - | descriptor field identity only |
| wHubCharacteristics | `wHubDescriptor.wHubCharacteristics` | - | descriptor field identity only |
| bPwrOn2PwrGood | `wHubDescriptor.bPwrOn2PwrGood` | - | descriptor field identity only |
| bHubContrCurrent | `wHubDescriptor.bHubContrCurrent` | - | descriptor field identity only |
| DeviceRemovable | `wHubDescriptor.DeviceRemovable` | - | descriptor field identity only |
| PortPwrCtrlMask | `wHubDescriptor.PortPwrCtrlMask` | - | descriptor field identity only |
| PORT_CONNECTION | `wPortStatus` | bit 0 | bit name and bit position only |
| PORT_ENABLE | `wPortStatus` | bit 1 | bit name and bit position only |
| PORT_SUSPEND | `wPortStatus` | bit 2 | bit name and bit position only |
| PORT_OVER_CURRENT | `wPortStatus` | bit 3 | bit name and bit position only |
| PORT_RESET | `wPortStatus` | bit 4 | bit name and bit position only |
| PORT_POWER | `wPortStatus` | bit 8 | bit name and bit position only |
| PORT_LOW_SPEED | `wPortStatus` | bit 9 | bit name and bit position only |
| PORT_HIGH_SPEED | `wPortStatus` | bit 10 | bit name and bit position only |
| PORT_TEST | `wPortStatus` | bit 11 | bit name and bit position only |
| PORT_INDICATOR | `wPortStatus` | bit 12 | bit name and bit position only |
| C_PORT_CONNECTION | `wPortChange` | bit 0 | bit name and bit position only |
| C_PORT_ENABLE | `wPortChange` | bit 1 | bit name and bit position only |
| C_PORT_SUSPEND | `wPortChange` | bit 2 | bit name and bit position only |
| C_PORT_OVER_CURRENT | `wPortChange` | bit 3 | bit name and bit position only |
| C_PORT_RESET | `wPortChange` | bit 4 | bit name and bit position only |
| HUB_LOCAL_POWER | `wHubStatus` | bit 0 | bit name and bit position only |
| HUB_OVER_CURRENT | `wHubStatus` | bit 1 | bit name and bit position only |
| C_HUB_LOCAL_POWER | `wHubChange` | bit 0 | bit name and bit position only |
| C_HUB_OVER_CURRENT | `wHubChange` | bit 1 | bit name and bit position only |
| usb20_get_status_hub | `GET_STATUS` hub recipient | - | request linkage only |
| usb20_get_status_port | `GET_STATUS` port recipient | - | request linkage only |
| usb20_set_feature_hub | `SET_FEATURE` hub recipient | - | request linkage only |
| usb20_set_feature_port | `SET_FEATURE` port recipient | - | request linkage only |
| usb20_clear_feature_hub | `CLEAR_FEATURE` hub recipient | - | request linkage only |
| usb20_clear_feature_port | `CLEAR_FEATURE` port recipient | - | request linkage only |
| usb20_clear_tt_buffer | `CLEAR_TT_BUFFER` TT-capable hub recipient | - | request linkage only |
| usb20_reset_tt | `RESET_TT` TT-capable hub recipient | - | request linkage only |
| usb20_get_tt_state | `GET_TT_STATE` TT-capable hub recipient | - | request linkage only |
| usb20_stop_tt | `STOP_TT` TT-capable hub recipient | - | request linkage only |
| usb20_get_descriptor_hub | `GET_DESCRIPTOR` hub recipient | - | request linkage only |
| usb20_set_descriptor_hub | `SET_DESCRIPTOR` hub recipient | - | request linkage only |
| usb20_tt_type_single | `wHubCharacteristics` | - | TT type boundary only |
| usb20_tt_type_multiple | `wHubCharacteristics` | - | TT type boundary only |
| usb20_tt_think_time_00 | `wHubCharacteristics` | 00 | TT think-time boundary only |
| usb20_tt_think_time_01 | `wHubCharacteristics` | 01 | TT think-time boundary only |
| usb20_tt_think_time_10 | `wHubCharacteristics` | 10 | TT think-time boundary only |
| usb20_tt_think_time_11 | `wHubCharacteristics` | 11 | TT think-time boundary only |
| usb20_tt_request_clear_tt_buffer | `hub_class_request` | - | TT request-linkage boundary only |
| usb20_tt_request_reset_tt | `hub_class_request` | - | TT request-linkage boundary only |
| usb20_tt_request_get_tt_state | `hub_class_request` | - | TT request-linkage boundary only |
| usb20_tt_request_stop_tt | `hub_class_request` | - | TT request-linkage boundary only |
| E-01 | `Escalation trigger` | - | escalation trigger boundary only |
| E-02 | `Escalation trigger` | - | escalation trigger boundary only |
| E-03 | `Escalation trigger` | - | escalation trigger boundary only |
| E-04 | `Escalation trigger` | - | escalation trigger boundary only |
| E-05 | `Escalation trigger` | - | escalation trigger boundary only |
| E-06 | `Escalation trigger` | - | escalation trigger boundary only |
| E-07 | `Escalation trigger` | - | escalation trigger boundary only |
| E-08 | `Escalation trigger` | - | escalation trigger boundary only |
| E-09 | `Escalation trigger` | - | escalation trigger boundary only |
| E-10 | `Escalation trigger` | - | escalation trigger boundary only |

| C_HUB_LOCAL_POWER | `feature_selector_matrix` | 0 | selector name and value only |
| C_HUB_OVER_CURRENT | `feature_selector_matrix` | 1 | selector name and value only |
| PORT_CONNECTION | `feature_selector_matrix` | 0 | selector name and value only |
| PORT_ENABLE | `feature_selector_matrix` | 1 | selector name and value only |
| PORT_SUSPEND | `feature_selector_matrix` | 2 | selector name and value only |
| PORT_OVER_CURRENT | `feature_selector_matrix` | 3 | selector name and value only |
| PORT_RESET | `feature_selector_matrix` | 4 | selector name and value only |
| reserved | `feature_selector_matrix` | 5 | selector name and value only |
| reserved | `feature_selector_matrix` | 6 | selector name and value only |
| reserved | `feature_selector_matrix` | 7 | selector name and value only |
| PORT_POWER | `feature_selector_matrix` | 8 | selector name and value only |
| PORT_LOW_SPEED | `feature_selector_matrix` | 9 | selector name and value only |
| PORT_HIGH_SPEED | `feature_selector_matrix` | 10 | selector name and value only |
| reserved | `feature_selector_matrix` | 11 | selector name and value only |
| reserved | `feature_selector_matrix` | 12 | selector name and value only |
| reserved | `feature_selector_matrix` | 13 | selector name and value only |
| reserved | `feature_selector_matrix` | 14 | selector name and value only |
| reserved | `feature_selector_matrix` | 15 | selector name and value only |
| C_PORT_CONNECTION | `feature_selector_matrix` | 16 | selector name and value only |
| C_PORT_ENABLE | `feature_selector_matrix` | 17 | selector name and value only |
| C_PORT_SUSPEND | `feature_selector_matrix` | 18 | selector name and value only |
| C_PORT_OVER_CURRENT | `feature_selector_matrix` | 19 | selector name and value only |
| C_PORT_RESET | `feature_selector_matrix` | 20 | selector name and value only |
| PORT_TEST | `feature_selector_matrix` | 21 | selector name and value only |
| PORT_INDICATOR | `feature_selector_matrix` | 22 | selector name and value only |

The verified scope is explicitly limited to each entry's stated scope in the table below.

The following are outside the verified scope for all entries:

- Timing behavior
- State transition behavior
- `SET_FEATURE` behavior
- `CLEAR_FEATURE` behavior
- Error recovery conditions
- Host-stack interpretation
- Full USB 2.0 compliance

## What This Page Does Not Claim

This page does not claim:

- USB 2.0 hub behavior is fully verified.
- Any page-level or table-level verification is complete.
- `PORT_ENABLE` state machine, `SET_FEATURE`, `CLEAR_FEATURE`, or error recovery behavior is verified.
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
