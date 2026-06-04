---
title: Verification Status
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
semantic_verification_claimed: false
---

# Verification Status

> 本頁是靜態可見性摘要，不是自動產生的 source of truth。
> 受治理的 YAML tables 與 evidence packets 才是權威來源材料。
> 當 table entries 或 packet status 變更時，本頁數字必須手動同步更新。

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

- **Verified**: 已通過 entry-level promotion gate；`claim_level: verified`；scope 明確受限。
- **Reviewed**: Repo-local review 已完成，surface 已收斂成較清楚的 field role、selector boundary 或 request linkage，但尚未提升為 entry-level verified。
- **Inferred**: 已整理但尚未 reviewed 或 verified；`claim_level: inferred`。

## Coverage Map

| Area | Current maturity center | Notes |
|---|---|---|
| Hub descriptor fields | verified | 全部 8 個 tracked hub descriptor fields 已完成 descriptor field identity verified；不驗證 descriptor dumps 或 device behavior |
| Transaction Translator entries | reviewed | 全部 10 個 tracked TT type、think-time 與 request-linkage entries 已有 reviewed reference-boundary surfaces，但未宣告 split-transaction behavior verification |
| Escalation triggers | reviewed | 全部 10 個 E-01 到 E-10 trigger boundaries 已有 reviewed reference surfaces，但 escalation execution 仍由 consuming repos 負責 |
| Class requests | verified | 全部 12 個 tracked class requests 已完成 request-linkage-only verified promotions |
| Feature selectors | reviewed | 全部 25 個 tracked feature selectors 已有 reviewed selector-boundary 或 reserved-boundary surfaces |
| Port status bits | verified / reviewed | 8 個核心 hub/port status-change bits 已完成 entry-level verified promotion；另外 11 個 defined port status/change bits 與 2 個 high-bit boundary placeholders 只是 reviewed namespace/boundary entries |

## Reviewed Surface Inventory

目前 `reviewed` surface 集中在以下項目：

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

這些 `reviewed` surfaces 代表 repo-local boundary 比純 inferred surface 更清楚。
它們不代表這些 surfaces 已完成 entry-level verified promotion。

## Verified Entries

目前共有 20 個 entries 已完成 verified promotion：

| Entry | Field / Request | Scope |
|---|---|---|
| PORT_CONNECTION | `wPortStatus.bit0` | bit name and bit position only |
| PORT_ENABLE | `wPortStatus.bit1` | bit name and bit position only |
| C_PORT_CONNECTION | `wPortChange.bit0` | bit name and bit position only |
| C_PORT_ENABLE | `wPortChange.bit1` | bit name and bit position only |
| HUB_LOCAL_POWER | `wHubStatus.bit0` | bit name and bit position only |
| HUB_OVER_CURRENT | `wHubStatus.bit1` | bit name and bit position only |
| C_HUB_LOCAL_POWER | `wHubChange.bit0` | bit name and bit position only |
| C_HUB_OVER_CURRENT | `wHubChange.bit1` | bit name and bit position only |
| usb20_get_status_hub | GET_STATUS hub request | request linkage only |
| usb20_get_status_port | GET_STATUS port request | request linkage only |
| usb20_set_feature_hub | SET_FEATURE hub request | request linkage only |
| usb20_set_feature_port | SET_FEATURE port request | request linkage only |
| usb20_clear_feature_hub | CLEAR_FEATURE hub request | request linkage only |
| usb20_clear_feature_port | CLEAR_FEATURE port request | request linkage only |
| usb20_clear_tt_buffer | CLEAR_TT_BUFFER request | request linkage only |
| usb20_reset_tt | RESET_TT request | request linkage only |
| usb20_get_tt_state | GET_TT_STATE request | request linkage only |
| usb20_stop_tt | STOP_TT request | request linkage only |
| usb20_get_descriptor_hub | GET_DESCRIPTOR request | request linkage only |
| usb20_set_descriptor_hub | SET_DESCRIPTOR request | request linkage only |

Verified scope 明確只限於 **bit name and bit position** 或 **request linkage**。

以下項目全部不在 verified scope 內：

- Timing behavior
- State transition behavior
- `SetPortFeature` behavior
- `ClearPortFeature` behavior
- Error recovery conditions
- Host-stack interpretation
- Full USB 2.0 compliance

## What This Page Does Not Claim

本頁不宣告：

- USB 2.0 hub behavior 已完整 verified。
- 任何 page-level 或 table-level verification 已完成。
- `PORT_ENABLE` state machine、`SetPortFeature`、`ClearPortFeature` 或 error recovery behavior 已 verified。
- Reviewed entries 可以作為 implementation truth。
- Reviewed coverage 等同於 verified coverage。
- 本 reference 可覆蓋 consuming repositories 中已確認的 project facts。
- 靜態數字是與 YAML tables 自動同步的 source of truth。

## Reference Surface Maintenance Rule

當 verification maturity 或 tracked entry counts 變更時，以下可見 surfaces 必須一起檢查：

- `specs/index.md`: zh-TW homepage 的 tracked / maturity summary
- `specs/en/index.md`: English homepage 的 tracked / maturity summary
- `specs/verification_status.md`: zh-TW verification summary、coverage map、verified entries、non-claims
- `specs/en/verification_status.md`: English verification summary、coverage map、verified entries、non-claims
- Core spec pages: affected entry family 的 `Non-claims` 與 `Governed Linkage` sections

Maintenance rules:

- Wording-only updates 不得改變 YAML source-of-truth semantics。
- 新增或 promoted verified entries 時，verification status pages 與 homepage summaries 必須一起更新。
- 當 surface 從 inferred 移到 reviewed，本頁 maturity breakdown 與 coverage map 也必須同步更新。
- Evidence packet count 變更時，必須更新 evidence packet summary。
- 新增 `section_refs` metadata 不會自動代表 page 或 entry 已 verified。

## Static Numbers Note

本頁 entry counts 與 packet statuses 是手動維護的靜態摘要。

當以下內容變更時，本頁必須手動更新：

- `tables/port_status_bit_matrix.yaml` 任一 entry 的 `claim_level`
- `tables/escalation_trigger_matrix.yaml`、`tables/hub_descriptor_matrix.yaml`、`tables/transaction_translator_matrix.yaml`、`tables/class_request_matrix.yaml` 或 `tables/feature_selector_matrix.yaml` 任一 entry 的 `evidence_status` / `claim_level`
- `evidence/entry_verification_packets/` 新增或修改 packets

受治理的 YAML tables 是 source of truth；本頁只是 visibility summary。
