---
title: Verification Status
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
semantic_verification_claimed: false
---

# Verification Status

> 本頁是靜態可見性摘要，不是自動產生的 source of truth。  
> Governed YAML tables 與 evidence packets 才是權威來源。  
> 只要 table entries 或 packet status 有變動，本頁數字就必須手動更新。

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
| Entry verification packets | 28 | 全部對應到已 promoted 的 verified entries |

術語定義：

- **Verified**：已通過 entry-level promotion gate；`claim_level: verified`；scope 有明確邊界。
- **Reviewed**：repo-local review 已完成，surface 已被收斂成較清楚的 field role、selector boundary 或 request linkage，但尚未升級為 entry-level verified。
- **Inferred**：已整理，但尚未 review 或 verified；`claim_level: inferred`。

## Coverage Map

| Area | Current maturity center | Notes |
|---|---|---|
| Hub descriptor fields | verified | 8 個 tracked hub descriptor fields 都已完成 descriptor field identity verified；但這不驗證 descriptor dumps 或 device behavior |
| Transaction Translator entries | reviewed | 10 個 tracked TT type、think-time 與 request-linkage entries 都已有 reviewed reference-boundary surfaces，但不驗證 split-transaction behavior |
| Escalation triggers | reviewed | 10 個 tracked E-01 到 E-10 trigger boundaries 都已有 reviewed reference surfaces，但 escalation execution 仍由 consuming repos 負責 |
| Class requests | verified | 12 個 tracked class requests 都已完成 request-linkage-only verified promotion |
| Feature selectors | reviewed | 25 個 tracked feature selectors 都已有 reviewed selector-boundary 或 reserved-boundary surfaces |
| Port status bits | verified / reviewed | 8 個核心 hub/port status-change bits 已完成 entry-level verified promotion；另有 11 個 defined port status/change bits 與 2 個 high-bit boundary placeholders 仍是 reviewed namespace/boundary entries |

## Reviewed Surface Inventory

目前 `reviewed` surface 主要集中在下列項目：

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

這些 `reviewed` surfaces 代表 repo-local boundary 已比純 `inferred` surface 更清楚。  
它們**不代表**這些 surfaces 已完成 entry-level verified promotion。

## Verified Entries

目前共有 28 個 entries 已完成 verified promotion（`claim_level: verified`）：

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
| C_PORT_CONNECTION | `wPortChange` | bit 0 | bit name and bit position only |
| C_PORT_ENABLE | `wPortChange` | bit 1 | bit name and bit position only |
| HUB_LOCAL_POWER | `wHubStatus` | bit 0 | bit name and bit position only |
| HUB_OVER_CURRENT | `wHubStatus` | bit 1 | bit name and bit position only |
| C_HUB_LOCAL_POWER | `wHubChange` | bit 0 | bit name and bit position only |
| C_HUB_OVER_CURRENT | `wHubChange` | bit 1 | bit name and bit position only |

Verified scope 明確限制為 **bit name and bit position**。

對所有 entries 而言，下列內容都仍在 verified scope 之外：

- Timing behavior
- State transition behavior
- `SET_FEATURE` behavior
- `CLEAR_FEATURE` behavior
- Error recovery conditions
- Host-stack interpretation
- Full USB 2.0 compliance

## What This Page Does Not Claim

本頁不宣告：

- USB 2.0 hub behavior 已完整 verified
- 任何 page-level 或 table-level verification 已完成
- `PORT_ENABLE` state machine、`SET_FEATURE`、`CLEAR_FEATURE` 或 error recovery behavior 已驗證
- Reviewed entries 可安全直接當作 implementation truth
- Reviewed coverage 等同於 verified coverage
- 這份 reference 可覆蓋 consuming repositories 中已確認的 project facts
- 靜態統計數字是與 YAML tables 自動同步的 source of truth

## Reference Surface Maintenance Rule

當 verification maturity 或 tracked entry counts 變動時，下列 visible surfaces 必須一起檢查：

- `specs/index.md`：zh-TW homepage 上的 tracked / maturity summary
- `specs/en/index.md`：English homepage 上的 tracked / maturity summary
- `specs/verification_status.md`：zh-TW verification summary、coverage map、verified entries 與 non-claims
- `specs/en/verification_status.md`：English verification summary、coverage map、verified entries 與 non-claims
- Core spec pages：受影響 entry family 的 `Non-claims` 與 `Governed Linkage` sections

維護規則：

- 純 wording update 不得改變 YAML source-of-truth semantics。
- 新增或提升 verified entries 時，必須同步更新 verification status pages 與 homepage summaries。
- 當 surface 從 inferred 變為 reviewed 時，本頁的 maturity breakdown 與 coverage map 也必須同步更新。
- Evidence packet count 變動時，必須同步更新 evidence packet summary。
- 新增 `section_refs` metadata 不得自動宣稱某個 page 或 entry 已 verified。

## Static Numbers Note

本頁的 entry counts 與 packet statuses 是人工維護的靜態摘要。

只要下列任一項變動，本頁就必須手動更新：

- `tables/port_status_bit_matrix.yaml` 中任一 entry 的 `claim_level`
- `tables/escalation_trigger_matrix.yaml`、`tables/hub_descriptor_matrix.yaml`、`tables/transaction_translator_matrix.yaml`、`tables/class_request_matrix.yaml` 或 `tables/feature_selector_matrix.yaml` 中 entries 的 `evidence_status` / `claim_level`
- `evidence/entry_verification_packets/` 中新增或修改 packets

Governed YAML tables 才是 source of truth；本頁只是 visibility summary。
