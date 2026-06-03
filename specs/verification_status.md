---
title: Verification Status
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
semantic_verification_claimed: false
---

# Verification Status

> 本頁是靜態可見性摘要，不是自動產生的 source of truth。  
> governed YAML tables 與 evidence packets 才是 authoritative source materials。  
> 只要 table entries 或 packet 狀態有變，本頁數字都必須手動同步更新。

## Current Verification Summary

| Area | Tracked entries | Verified | Reviewed | Inferred | Missing |
|---|---:|---:|---:|---:|---:|
| Class requests | 12 | 0 | 10 | 2 | 0 |
| Feature selectors | 25 | 0 | 11 | 14 | 0 |
| Port status bits | 10 | 8 | 0 | 2 | 0 |
| **Total** | **47** | **8** | **21** | **18** | **0** |

## Evidence Packet Summary

| Artifact type | Count | Status |
|---|---:|---|
| Entry verification packets | 8 | All correspond to promoted verified entries |

Term definitions:

- **Verified**: 已通過 entry-level promotion gate；`claim_level: verified`；scope 仍受明確邊界限制。
- **Reviewed**: repo-local review 已完成，對應 surface 已收斂到較清楚的欄位角色、selector boundary 或 request linkage，但尚未升成 entry-level verified。
- **Inferred**: 已整理但尚未 reviewed / verified；`claim_level: inferred`。

## Coverage Map

| Area | Current maturity center | Notes |
|---|---|---|
| Class requests | reviewed-heavy | `SET_FEATURE` / `CLEAR_FEATURE`、TT request families、`GET_DESCRIPTOR` / `SET_DESCRIPTOR` 已有 reviewed surface，但尚未有 entry-level verified promotion |
| Feature selectors | reviewed / inferred mixed | `PORT_ENABLE`、`PORT_SUSPEND`、`PORT_RESET`、`PORT_POWER`、`C_HUB_LOCAL_POWER`、`C_HUB_OVER_CURRENT`、`C_PORT_CONNECTION`、`C_PORT_ENABLE`、`C_PORT_SUSPEND`、`C_PORT_OVER_CURRENT`、`C_PORT_RESET` 已有 reviewed linkage；其餘 selector coverage 仍是 inferred |
| Port status bits | verified-heavy | 8 筆核心 hub/port status-change bits 已完成 entry-level verified promotion；剩餘 2 筆 boundary placeholders 仍是 inferred |

## Reviewed Surface Inventory

目前 `reviewed` surface 主要集中在這些項目：

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
  - `C_PORT_SUSPEND`
  - `C_PORT_OVER_CURRENT`
  - `C_PORT_RESET`
  - `PORT_ENABLE`
  - `PORT_SUSPEND`
  - `PORT_RESET`
  - `PORT_POWER`

這些 `reviewed` surfaces 代表 repo-local boundary 已比純 inferred surface 更明確，
但不代表這些 surfaces 已完成 entry-level verified promotion。

## Verified Entries

目前共有 8 筆 entries 完成 verified promotion（Phase 8E、Phase 8H、Phase 8I、Phase 8J、Phase 8K）：

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

verified scope 目前仍明確限制在 **bit name** 與 **bit position**。

以下內容都不在 verified scope 內：

- Timing behavior
- State transition behavior
- `SetPortFeature` behavior
- `ClearPortFeature` behavior
- Error recovery conditions
- Host-stack interpretation
- Full USB 2.0 compliance

## What This Page Does Not Claim

本頁不宣告：

- USB 2.0 hub behavior 已整體 verified
- 任何 page-level 或 table-level verification 已完成
- `PORT_ENABLE` state machine、`SetPortFeature`、`ClearPortFeature`、error recovery behavior 已 verified
- reviewed 或 inferred entries 可以直接當作 implementation truth
- 這個 reference 可以覆蓋 consuming repos 的 confirmed project facts
- 靜態數字會自動和 YAML tables 同步

## Reference Surface Maintenance Rule

當 verification maturity 或 tracked entry count 改變時，下列 visible surfaces 必須一起檢查：

- `specs/index.md`: zh-TW 首頁的 tracked / maturity 摘要
- `specs/en/index.md`: English 首頁的 tracked / maturity 摘要
- `specs/verification_status.md`: zh-TW verification summary、coverage map、verified entries、non-claims
- `specs/en/verification_status.md`: English verification summary、coverage map、verified entries、non-claims
- 核心 spec pages：受影響 entry family 的 `Non-claims` 與 `Governed Linkage`

維護規則：

- 只改 visible wording，不得改變 YAML source-of-truth semantics。
- 新增或升級 verified entry 時，首頁摘要與 verification status 必須一起更新。
- surface 從 inferred 升到 reviewed 時，verification summary 與 coverage map 的 maturity breakdown 也要同步更新。
- evidence packet count 改變時，evidence packet summary 也要同步更新。
- 新增 `section_refs` metadata，不得自動宣告 page 或 entry 已 verified。

## Static Numbers Note

本頁的 entry counts 與 packet statuses 都是手工維護的靜態摘要。

下列任一來源有變時，本頁都必須手動更新：

- `tables/port_status_bit_matrix.yaml` 內任一 entry 的 `claim_level`
- `tables/class_request_matrix.yaml` 與 `tables/feature_selector_matrix.yaml` 的 `evidence_status` / `claim_level`
- `evidence/entry_verification_packets/` 新增或修改 packet

governed YAML tables 才是 source of truth；本頁只是 visibility summary。
