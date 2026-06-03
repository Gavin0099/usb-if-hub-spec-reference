---
title: 驗證狀態
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
semantic_verification_claimed: false
---

# 驗證狀態

> 本頁是靜態可見性摘要，不是自動生成的 source of truth。  
> governed YAML tables 與 evidence packets 才是權威來源。  
> 只要 table entry 或 packet 狀態有變動，本頁數字就必須手動更新。

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

- **Verified**: 已通過 entry-level promotion gate，`claim_level: verified`，scope 有明確上限。
- **Reviewed non-promoting**: review 已完成，evidence packet 存在，但 `eligible_for_verified: false`，promotion 刻意保留。
- **Inferred**: 已整理，但尚未進入 reviewed 或 verified 狀態，`claim_level: inferred`。

## Verified Entries

目前有兩筆 entry 完成 verified promotion（Phase 8E、Phase 8H）：

| Entry | Field | Bit | Verified Scope |
|---|---|---|---|
| PORT_CONNECTION | `wPortStatus` | bit 0 | bit name and bit position only |
| PORT_ENABLE | `wPortStatus` | bit 1 | bit name and bit position only |

Verified scope 明確限定為：**bit 名稱與 bit 位置**。

以下都不在 verified scope 內：

- Timing behavior
- State transition behavior
- `SetPortFeature` behavior
- `ClearPortFeature` behavior
- Error recovery conditions
- Host-stack interpretation
- Full USB 2.0 compliance

## Reviewed but Not Promoted

目前沒有 reviewed non-promoting entries。所有 reviewed packets 都已在 Phase 8H 前後完成 promotion。

## What This Page Does Not Claim

本頁不宣告：

- USB 2.0 hub behavior 已完整 verified
- 任何 page-level 或 table-level verification 已完成
- PORT_ENABLE 的 state machine、SetPortFeature 或 error recovery behavior 已 verified
- inferred entries 可以直接當成 implementation truth
- 本 reference 可以覆蓋 consuming repo 裡已確認的 project facts
- 這些靜態數字是與 YAML tables 自動同步的

## Static Numbers Note

本頁的 entry 數量與 packet 狀態是人工維護的靜態摘要。

只要以下任何一項變動，本頁就必須手動更新：

- `tables/port_status_bit_matrix.yaml` 中任何 entry 的 `claim_level`
- `tables/class_request_matrix.yaml` 或 `tables/feature_selector_matrix.yaml` 的 entry 數量或狀態
- `evidence/entry_verification_packets/` 中 packet 的新增、刪除或狀態變更

governed YAML tables 是 source of truth；本頁只是 visibility summary。
