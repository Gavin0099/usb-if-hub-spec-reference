---
title: Verification Status
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
semantic_verification_claimed: false
---

# Verification Status

> 本頁是靜態 visibility summary，不是自動產生的 source of truth。
> Governed YAML tables 與 evidence packets 才是 authoritative source materials。
> 當 table entries 或 packet status 改變時，本頁數字必須手動更新。

## Current Verification Summary

| Area | Tracked entries | Verified | Reviewed | Inferred | Missing |
|---|---:|---:|---:|---:|---:|
| Class requests | 12 | 0 | 12 | 0 | 0 |
| Feature selectors | 25 | 0 | 15 | 10 | 0 |
| Port status bits | 10 | 8 | 0 | 2 | 0 |
| **Total** | **47** | **8** | **27** | **12** | **0** |

## Evidence Packet Summary

| Artifact type | Count | Status |
|---|---:|---|
| Entry verification packets | 8 | All correspond to promoted verified entries |

Term definitions:

- **Verified**: 已通過 entry-level promotion gate；`claim_level: verified`；scope 已明確限制。
- **Reviewed**: Repo-local review 已完成，surface 已收斂到較清楚的 field role、selector boundary 或 request linkage，但尚未 promoted to entry-level verified。
- **Inferred**: 已整理但尚未 reviewed / verified；`claim_level: inferred`。

## Coverage Map

| Area | Current maturity center | Notes |
|---|---|---|
| Class requests | reviewed | 12 筆 tracked class requests 全部已有 reviewed request-linkage surfaces，但尚未有 entry-level verified promotions |
| Feature selectors | reviewed / inferred mixed | `PORT_CONNECTION`、`PORT_ENABLE`、`PORT_SUSPEND`、`PORT_OVER_CURRENT`、`PORT_RESET`、`PORT_POWER`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED`、`C_HUB_LOCAL_POWER`、`C_HUB_OVER_CURRENT`、`C_PORT_CONNECTION`、`C_PORT_ENABLE`、`C_PORT_SUSPEND`、`C_PORT_OVER_CURRENT`、`C_PORT_RESET` 已有 reviewed linkage；其餘 selector coverage 仍是 inferred |
| Port status bits | verified-heavy | 8 筆核心 hub/port status-change bits 已完成 entry-level verified promotion；剩餘 2 筆 boundary placeholders 仍是 inferred |

## Reviewed Surface Inventory

目前 `reviewed` surface 主要集中在這些項目：

- class requests
  - `GET_STATUS` hub / port
  - `SET_FEATURE` hub / port
  - `CLEAR_FEATURE` hub / port
  - `CLEAR_TT_BUFFER`
  - `RESET_TT`
  - `GET_TT_STATE`
  - `STOP_TT`
  - `GET_DESCRIPTOR`
  - `SET_DESCRIPTOR`
- feature selectors
  - `PORT_CONNECTION`
  - `PORT_OVER_CURRENT`
  - `PORT_LOW_SPEED`
  - `PORT_HIGH_SPEED`
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

這些 `reviewed` surfaces 代表 repo-local boundary 比純 inferred surface 更清楚。
它們不代表已完成 entry-level verified promotion。

## Verified Entries

目前有 8 筆 entries 已完成 verified promotion（Phase 8E、Phase 8H、Phase 8I、Phase 8J、Phase 8K）：

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

Verified scope 明確限制在 **bit name and bit position**。

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
- Reviewed 或 inferred entries 可直接當作 implementation truth。
- 本 reference 可覆蓋 consuming repositories 中已確認的 project facts。
- Static counts 是與 YAML tables 自動同步的 source of truth。

## Reference Surface Maintenance Rule

當 verification maturity 或 tracked entry counts 改變時，以下 visible surfaces 必須一起檢查：

- `specs/index.md`: zh-TW homepage 的 tracked / maturity summary
- `specs/en/index.md`: English homepage 的 tracked / maturity summary
- `specs/verification_status.md`: zh-TW verification summary、coverage map、verified entries、non-claims
- `specs/en/verification_status.md`: English verification summary、coverage map、verified entries、non-claims
- Core spec pages: affected entry family 的 `Non-claims` 與 `Governed Linkage` sections

Maintenance rules:

- Wording-only updates 不得改變 YAML source-of-truth semantics。
- 新增或 promoted verified entries 時，verification status pages 與 homepage summaries 必須同步更新。
- Surface 從 inferred 升到 reviewed 時，本頁 verification summary 與 coverage map 的 maturity breakdown 也要同步更新。
- Evidence packet count 改變時，evidence packet summary 必須同步更新。
- 新增 `section_refs` metadata 不會自動宣告 page 或 entry 已 verified。

## Static Numbers Note

本頁的 entry counts 與 packet statuses 是手動維護的 static summary。

以下項目改變時，本頁必須手動更新：

- `tables/port_status_bit_matrix.yaml` 中任何 entry 的 `claim_level`
- `tables/class_request_matrix.yaml` 或 `tables/feature_selector_matrix.yaml` 中的 `evidence_status` / `claim_level`
- `evidence/entry_verification_packets/` 中新增或修改 packets

Governed YAML tables 是 source of truth；本頁只是 visibility summary。
