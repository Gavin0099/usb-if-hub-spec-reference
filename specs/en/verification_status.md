---
title: Verification Status
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
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
| Hub interrupt endpoint | 4 | 4 | 0 | 0 | 0 |
| Standard device requests | 12 | 12 | 0 | 0 | 0 |
| wHubCharacteristics bit groups | 6 | 5 | 1 | 0 | 0 |
| **Total** | **151** | **105** | **46** | **0** | **0** |

## Evidence Packet Summary

| Artifact type | Count | Status |
|---|---:|---|
| Entry verification packets | 105 | All correspond to promoted verified entries; 46 reviewed entries have no evidence packet |

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
| Hub interrupt endpoint | verified | 4 status change endpoint descriptor fields (bEndpointAddress, bmAttributes, wMaxPacketSize, bInterval) have completed entry-level verified promotion (descriptor field identity scope) |
| Standard device requests | verified | 12 standard USB device requests applicable to hubs have completed entry-level verified promotion (request-linkage identity scope) |
| wHubCharacteristics bit groups | verified / reviewed | 5 wHubCharacteristics bit groups (power switching, compound device, OC mode, TT think time, port indicators) have completed entry-level verified promotion (bit-group name and value-encoding identity scope); 1 reserved high-byte boundary entry is permanent reviewed |

## Reviewed Surface Inventory

The remaining 45 `reviewed` entries represent **permanent boundaries**, not unfinished upgrade work.

### 1 wHubCharacteristics reserved high-byte boundary (no semantic to verify; not upgradeable)

- `usb20_whc_reserved_high` (wHubCharacteristics bits[15:8], spec-defined reserved, shall be zero)

### 4 Port/Hub status-change high-bit boundary placeholders (no semantic to verify; not upgradeable)

These four entries are intentional namespace-closing entries that bound each status word's upper bit range. They do not represent real USB 2.0 bit definitions:

- `PORT_STATUS_HIGH_BIT_BOUNDARY` (wPortStatus bit 15 namespace boundary)
- `PORT_CHANGE_HIGH_BIT_BOUNDARY` (wPortChange bit 15 namespace boundary)
- `HUB_STATUS_HIGH_BIT_BOUNDARY` (wHubStatus bit 15 namespace boundary)
- `HUB_CHANGE_HIGH_BIT_BOUNDARY` (wHubChange bit 15 namespace boundary)

### 41 Reserved bit namespace boundaries (semantically final; should not be upgraded)

USB 2.0 §11.24 / Table 11-19 explicitly defines the following bit positions as reserved (shall be zero). The `reviewed` status for these entries means "the spec position is clear; there is no behavioral semantic left to verify" — not a verification gap:

- wPortStatus reserved: BIT5, BIT6, BIT7, BIT13, BIT14 (5 entries)
- wPortChange reserved: BIT5–BIT14 (10 entries)
- wHubStatus reserved: BIT2–BIT14 (13 entries)
- wHubChange reserved: BIT2–BIT14 (13 entries)

**These 45 reviewed entries are the correct final state.** Promoting them to verified would add no semantic coverage, because reserved bits have no behavioral semantic to verify and boundary placeholder entries are not real bit definitions.

## Verified Entries

105 entries have completed verified promotion (`claim_level: verified`):

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
| usb20_std_get_status_device | `GET_STATUS` device recipient | - | request linkage only |
| usb20_std_get_status_interface | `GET_STATUS` interface recipient | - | request linkage only |
| usb20_std_get_status_endpoint | `GET_STATUS` endpoint recipient | - | request linkage only |
| usb20_std_clear_feature_device | `CLEAR_FEATURE` device recipient | - | request linkage only |
| usb20_std_clear_feature_endpoint | `CLEAR_FEATURE` endpoint recipient | - | request linkage only |
| usb20_std_set_feature_device | `SET_FEATURE` device recipient | - | request linkage only |
| usb20_std_set_address | `SET_ADDRESS` device recipient | - | request linkage only |
| usb20_std_get_descriptor | `GET_DESCRIPTOR` device recipient | - | request linkage only |
| usb20_std_get_configuration | `GET_CONFIGURATION` device recipient | - | request linkage only |
| usb20_std_set_configuration | `SET_CONFIGURATION` device recipient | - | request linkage only |
| usb20_std_get_interface | `GET_INTERFACE` interface recipient | - | request linkage only |
| usb20_std_set_interface | `SET_INTERFACE` interface recipient | - | request linkage only |
| usb20_hub_ep_bEndpointAddress | `bEndpointAddress` hub status-change EP | - | descriptor field identity only |
| usb20_hub_ep_bmAttributes | `bmAttributes` hub status-change EP | - | descriptor field identity only |
| usb20_hub_ep_wMaxPacketSize | `wMaxPacketSize` hub status-change EP | - | descriptor field identity only |
| usb20_hub_ep_bInterval | `bInterval` hub status-change EP | - | descriptor field identity only |
| usb20_whc_power_switching | `wHubCharacteristics` | bits[1:0] | bit-group name and value-encoding identity only |
| usb20_whc_compound_device | `wHubCharacteristics` | bit[2] | bit-group name and value-encoding identity only |
| usb20_whc_over_current_mode | `wHubCharacteristics` | bits[4:3] | bit-group name and value-encoding identity only |
| usb20_whc_tt_think_time | `wHubCharacteristics` | bits[6:5] | bit-group name and value-encoding identity only |
| usb20_whc_port_indicators | `wHubCharacteristics` | bit[7] | bit-group name and value-encoding identity only |
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

## USB 3.x Governed Surface Statistics

> USB 3.x entries and evidence packets are tracked independently and are **not included** in the USB 2.0 151/105/46 freeze statistics.

| Area | Tracked entries | Verified | Reviewed | Inferred | Missing |
|---|---:|---:|---:|---:|---:|
| SS hub descriptor fields | 9 | 9 | 0 | 0 | 0 |
| SS hub class requests | 10 | 10 | 0 | 0 | 0 |
| SS port status bits | 19 | 15 | 4 | 0 | 0 |
| SS feature selectors (USB3-FS-2) | 6 | 6 | 0 | 0 | 0 |
| **USB 3.x Total** | **44** | **40** | **4** | **0** | **0** |

| Artifact type | Count | Status |
|---|---:|---|
| USB 3.x evidence packets | 40 | `evidence/entry_verification_packets/usb3/`; 9 for SS hub descriptor (USB3-3A), 10 for SS hub class requests (USB3-3B), 15 for SS port status bits (USB3-3C), 6 for SS feature selectors (USB3-FS-2) |

The SS port status bit matrix USB3-3C pilot is complete: 15 defined entries promoted to verified. The SS feature selector matrix USB3-FS-2 pilot is complete: 6 SS-only port feature selector entries promoted to verified (selector name/value/applicability/recipient identity only); 4 port status reserved boundary entries remain reviewed (permanent boundaries).

## What This Page Does Not Claim

This page does not claim:

- USB 2.0 hub behavior is fully verified.
- Any page-level or table-level verification is complete.
- `PORT_ENABLE` state machine, `SET_FEATURE`, `CLEAR_FEATURE`, or error recovery behavior is verified.
- Reviewed entries are safe to use as implementation truth.
- Reviewed coverage is the same as verified coverage.
- This reference overrides confirmed project facts in consuming repositories.
- Static counts are an automated source of truth synchronized with the YAML tables.

## USB 3.x Governed Matrix Closeout State (separate from USB 2.0 statistics)

The following statistics are **fully independent of the USB 2.0 totals (151/105/46)** and are not added to the USB 2.0 counts.

| Table | Tracked | Verified | Reviewed | State |
|---|---:|---:|---:|---|
| SS port status bits | 19 | 15 | 4 | **CLOSED** (15/19 defined verified; 4 reserved boundary, permanent) |
| SS hub class requests | 10 | 10 | 0 | **CLOSED** (10/10 verified) |
| SS hub descriptor fields | 9 | 9 | 0 | **CLOSED** (9/9 verified) |
| **USB 3.x total** | **38** | **34** | **4** | matrix-level closeout |

All three USB 3.x matrices are at matrix-level closeout. 34 entries have completed entry-level verified promotion; 4 reserved boundary entries remain reviewed (permanent boundaries, no verifiable semantics).

### USB 3.x Governed Matrix Closeout Details

The USB 3.x governed matrix surface is now stable (as of Phase USB3-3C completion):

- **All defined entries across the three matrices have completed entry-level verified promotion**: SS hub descriptor 9/9, SS hub class requests 10/10, SS port status/change bits 15/19.
- **The remaining 4 reviewed entries are reserved boundaries only**, not pending-promotion gaps: wPortStatus bit4, bit15; wPortChange bit1, bits[15:7].
- **No defined USB 3.x matrix entry is pending semantic promotion.**

### USB 3.x Non-Claims (fixed boundaries)

The following are outside the verified scope for all USB 3.x entries, now and permanently:

- Does not claim LTSSM runtime state transition behavior is verified.
- Does not claim xHCI port state management or xHCI enumeration behavior is verified.
- Does not claim SuperSpeed hub firmware compliance truth.
- Does not claim electrical, timing, or interoperability compliance.
- Does not claim USB-IF certification completeness.
- `PORT_LINK_STATE` verified scope is **limited to** bit range [8:5] and 12-value encoding table identity only; does not cover LTSSM transition behavior or U-state semantics.
- `PORT_SPEED` verified scope is **limited to** bit range [12:10] and 6-value encoding table identity only; does not cover speed detection hardware or link training outcome.
- USB 3.x reference surface covers the current three governed matrices only; **this is not complete USB 3.x spec coverage** and is not equivalent to the USB 2.0 28 topic-pair reference surface.
- USB 3.x entries are not counted in the USB 2.0 evidence packet total (USB 2.0 remains at 105 packets).

## USB 3.x Feature Selector Expansion (USB3-FS-2)

> This section is **independent of and separate from** the 38/34/4 matrix-level closeout baseline above.
> It does not change USB 3.x closeout numbers.
> Verified gate: PARTIAL / allowlist-only (USB3-FS-2 pilot, all 6 entries promoted).

Phase USB3-FS-2 completes verified promotion for the fourth USB 3.x governed matrix:
all six SS-only port feature selectors not present in the USB 2.0 feature selector namespace.

| Selector | Value | Recipient | Claim level | Verified scope |
|---|---|---|---|---|
| PORT_U1_ENABLE | 17 (0x11) | port | **verified** | selector name/value/applicability/recipient identity only |
| PORT_U2_ENABLE | 18 (0x12) | port | **verified** | selector name/value/applicability/recipient identity only |
| PORT_U1_TIMEOUT | 23 (0x17) | port | **verified** | selector name/value/applicability/recipient identity only |
| PORT_U2_TIMEOUT | 24 (0x18) | port | **verified** | selector name/value/applicability/recipient identity only |
| PORT_REMOTE_WAKE_MASK | 27 (0x1B) | port | **verified** | selector name/value/applicability/recipient identity only |
| BH_PORT_RESET | 28 (0x1C) | port | **verified** | selector name/value/applicability/recipient identity only |
| **Total** | | | **6 verified / 0 reviewed** | gate: **PARTIAL (allowlist, all 6)** |

Evidence packets (6 total, `evidence/entry_verification_packets/usb3/`):
`ss_feature_selector_usb3_port_u1_enable.yaml`, `ss_feature_selector_usb3_port_u2_enable.yaml`,
`ss_feature_selector_usb3_port_u1_timeout.yaml`, `ss_feature_selector_usb3_port_u2_timeout.yaml`,
`ss_feature_selector_usb3_port_remote_wake_mask.yaml`, `ss_feature_selector_usb3_port_bh_port_reset.yaml`.

**Non-claims for all SS feature selector entries (fixed boundaries):**
- Does not verify U1/U2 power state entry or exit behavior.
- Does not verify LTSSM transition behavior triggered by U1/U2 enable or BH reset.
- Does not verify xHCI port power policy or xHCI warm reset behavior.
- Does not verify U1/U2 timeout encoding semantics or wValue field behavior.
- Does not verify remote wake event routing, platform wake policy, or OS power management.
- Does not verify BH/warm reset sequence timing, LFPS signaling, or link recovery outcome.
- Manifest/baseline inclusion requires EXPORT-CONTRACT-1.1.

## Export Contract Surface

The hub governed surface now has a complete machine-readable export contract for consuming repo CI use.

| Component | Path | Role |
|---|---|---|
| Unified manifest | `exports/hub_governed_surface_manifest.yaml` | Governed truth index: authority surface, claim ceiling, and consumer usage contract for all 12 tables |
| Fingerprint baseline | `evidence/table_fingerprint_baseline.jsonl` | Content-hash baseline for all 12 governed tables for CI drift detection |
| Consumer contract | `docs/CONSUMER_INTEGRATION_CONTRACT.md` | Allowed / forbidden usage, failure interpretation, governance layer model |
| Manifest validator | `scripts/validate_hub_governed_surface_manifest.py` | Consistency gate between manifest summary and actual table entries (R1–R8) |
| Fingerprint probe | `scripts/probe_table_fingerprint.py --mode check` | Table content drift gate (exit 1 + names the drifted table) |
| Consumer smoke | `scripts/smoke_consumer_integration_fixtures.py` | Smoke-tested: manifest PASS, no-drift PASS, drift FAIL with table attribution |

**Consuming repo two-step CI gate:**

```
Step 1  python scripts/validate_hub_governed_surface_manifest.py
        → PASS: 12 tables, usb20 freeze, usb3 matrix_level_closeout

Step 2  python scripts/probe_table_fingerprint.py --mode check \
          --manifest exports/hub_governed_surface_manifest.yaml \
          --baseline-in evidence/table_fingerprint_baseline.jsonl
        → PASS: 12 tables, 0 drift
```

**Export contract non-claims:**
- Does not establish firmware compliance truth
- Does not claim LTSSM / xHCI runtime behavior is verified
- Does not claim USB-IF certification
- Cannot override confirmed project facts in consuming repositories

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
