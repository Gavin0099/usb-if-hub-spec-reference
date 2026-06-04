---
title: Verification Status
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
semantic_verification_claimed: false
---

# Verification Status

> 本頁是靜態的 visibility summary，不是自動生成的 source of truth。  
> 真正受治理的權威來源仍是 YAML tables 與 evidence packets。  
> 只要 table entries 或 packet status 有變動，這頁數字就必須手動同步更新。

## Current Verification Summary

| Area | Tracked entries | Verified | Reviewed | Inferred | Missing |
|---|---:|---:|---:|---:|---:|
| Hub descriptor fields | 8 | 8 | 0 | 0 | 0 |
| Transaction Translator entries | 10 | 0 | 10 | 0 | 0 |
| Escalation triggers | 10 | 0 | 10 | 0 | 0 |
| Class requests | 12 | 12 | 0 | 0 | 0 |
| Feature selectors | 25 | 0 | 25 | 0 | 0 |
| Port status bits | 21 | 11 | 10 | 0 | 0 |
| **Total** | **86** | **31** | **55** | **0** | **0** |

## Evidence Packet Summary

| Artifact type | Count | Status |
|---|---:|---|
| Entry verification packets | 31 | 全部對應到已 promoted 的 verified entries |

名詞定義：

- **Verified**：已通過 entry-level promotion gate；`claim_level: verified`；scope 有明確邊界。
- **Reviewed**：repo-local review 已完成，surface 已收斂成較清楚的 field role、selector boundary 或 request linkage，但尚未升級為 entry-level verified。
- **Inferred**：已整理但尚未完成 reviewed 或 verified；`claim_level: inferred`。

## Coverage Map

| Area | Current maturity center | Notes |
|---|---|---|
| Hub descriptor fields | verified | 全部 8 個 tracked hub descriptor fields 都已完成 descriptor field identity verified；這不代表 descriptor dumps 或 device behavior 已驗證 |
| Transaction Translator entries | reviewed | 全部 10 個 tracked TT type、think-time、request-linkage entries 都已達到 reviewed reference-boundary surface，但未驗證 split-transaction behavior |
| Escalation triggers | reviewed | 全部 10 個 tracked E-01 到 E-10 trigger boundaries 都已達到 reviewed reference surface，但 escalation execution 仍由 consuming repos 負責 |
| Class requests | verified | 全部 12 個 tracked class requests 都已完成 request-linkage-only verified promotion |
| Feature selectors | reviewed | 全部 25 個 tracked feature selectors 都已具備 reviewed selector-boundary 或 reserved-boundary surfaces |
| Port status bits | verified / reviewed | 9 個核心 hub/port status-change bits 已完成 entry-level verified promotion；另有 10 個已定義的 port status/change bits 與 2 個 high-bit boundary placeholders 仍屬 reviewed namespace/boundary entries |

## Reviewed Surface Inventory

目前 `reviewed` surface 主要集中在這些項目：

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

這些 `reviewed` surfaces 代表 repo-local boundary 已經比單純 inferred 更清楚。  
它們**不代表**已完成 entry-level verified promotion。

## Verified Entries

目前共有 29 個 entries 已完成 verified promotion（`claim_level: verified`）：

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
| C_PORT_CONNECTION | `wPortChange` | bit 0 | bit name and bit position only |
| C_PORT_ENABLE | `wPortChange` | bit 1 | bit name and bit position only |
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

所有 verified entries 的 verified scope 都明確限制在 **bit name and bit position**。

以下內容對所有 entries 都仍然在 verified scope 之外：

- Timing behavior
- State transition behavior
- `SET_FEATURE` behavior
- `CLEAR_FEATURE` behavior
- Error recovery conditions
- Host-stack interpretation
- Full USB 2.0 compliance

## What This Page Does Not Claim

本頁不宣告：

- USB 2.0 hub behavior 已全面 verified。
- 任何 page-level 或 table-level verification 已完成。
- `PORT_ENABLE` state machine、`SET_FEATURE`、`CLEAR_FEATURE` 或 error recovery behavior 已驗證。
- Reviewed entries 可以直接當 implementation truth 使用。
- Reviewed coverage 等同於 verified coverage。
- 本 reference 可以覆蓋 consuming repositories 中已確認的 project facts。
- 這些靜態數字已與 YAML tables 自動同步，並可作為 source of truth。

## Reference Surface Maintenance Rule

當 verification maturity 或 tracked entry counts 有變化時，以下 visible surfaces 必須一起檢查：

- `specs/index.md`：zh-TW homepage 的 tracked / maturity summary
- `specs/en/index.md`：English homepage 的 tracked / maturity summary
- `specs/verification_status.md`：zh-TW verification summary、coverage map、verified entries、non-claims
- `specs/en/verification_status.md`：English verification summary、coverage map、verified entries、non-claims
- Core spec pages：受影響 entry family 的 `Non-claims` 與 `Governed Linkage` sections

維護規則：

- 單純 wording update 不得改變 YAML source-of-truth semantics。
- 任何新的或 promoted verified entries，都必須同步更新 verification status pages 與 homepage summaries。
- 若某個 surface 從 inferred 轉成 reviewed，本頁與 coverage map 的 maturity breakdown 也必須一起更新。
- Evidence packet count 變動時，evidence packet summary 也必須同步更新。
- 新增 `section_refs` metadata，不得自動宣告頁面或 entry 已 verified。

## Static Numbers Note

本頁的 entry counts 與 packet statuses 都是人工維護的靜態 summary。

只要下列任一來源有變化，本頁都必須手動更新：

- `tables/port_status_bit_matrix.yaml` 中任一 entry 的 `claim_level`
- `tables/escalation_trigger_matrix.yaml`、`tables/hub_descriptor_matrix.yaml`、`tables/transaction_translator_matrix.yaml`、`tables/class_request_matrix.yaml`、`tables/feature_selector_matrix.yaml` 中 entries 的 `evidence_status` / `claim_level`
- `evidence/entry_verification_packets/` 中新增或修改的 packets

真正的 source of truth 是 governed YAML tables；本頁只是 visibility summary。
