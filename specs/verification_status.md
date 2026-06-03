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
> 只要 table entries 或 packet 狀態改變，本頁數字都必須手動更新。

## Current Verification Summary

| Area | Tracked entries | Verified | Reviewed / inferred | Missing |
|---|---:|---:|---:|---:|
| Class requests | 12 | 0 | 12 | 0 |
| Feature selectors | 25 | 0 | 25 | 0 |
| Port status bits | 10 | 4 | 6 | 0 |
| **Total** | **47** | **4** | **43** | **0** |

## Evidence Packet Summary

| Artifact type | Count | Status |
|---|---:|---|
| Entry verification packets | 4 | All correspond to promoted verified entries |

Term definitions:

- **Verified**: 已通過 entry-level promotion gate；`claim_level: verified`；scope 有明確邊界。
- **Reviewed non-promoting**: review 已完成；evidence packet 存在；`eligible_for_verified: false`；刻意不做 promotion。
- **Inferred**: 已整理但尚未進入 reviewed / verified；`claim_level: inferred`。

## Verified Entries

目前有 4 個 entries 已完成 verified promotion（Phase 8E、Phase 8H、Phase 8I）：

| Entry | Field | Bit | Verified Scope |
|---|---|---|---|
| PORT_CONNECTION | `wPortStatus` | bit 0 | bit name and bit position only |
| PORT_ENABLE | `wPortStatus` | bit 1 | bit name and bit position only |
| C_PORT_CONNECTION | `wPortChange` | bit 0 | bit name and bit position only |
| C_PORT_ENABLE | `wPortChange` | bit 1 | bit name and bit position only |

verified scope 明確限制在 **bit name** 與 **bit position**。

以下內容都不在 verified scope 內：

- Timing behavior
- State transition behavior
- `SetPortFeature` behavior
- `ClearPortFeature` behavior
- Error recovery conditions
- Host-stack interpretation
- Full USB 2.0 compliance

## Reviewed but Not Promoted

目前沒有 reviewed non-promoting entries。現有 reviewed packets 都已在 Phase 8H 前後完成 promotion。

## What This Page Does Not Claim

本頁不宣告：

- USB 2.0 hub behavior 已完整 verified
- 任何 page-level 或 table-level verification 已完成
- PORT_ENABLE state machine、SetPortFeature、error recovery behavior 已 verified
- inferred entries 可直接當 implementation truth 使用
- 這份 reference 可覆蓋 consuming repos 的 confirmed project facts
- 靜態數字已和 YAML tables 自動同步

## Reference Surface Maintenance Rule

當 verification maturity 或 tracked entry count 改變時，以下 visible surfaces 必須一起檢查：

- `specs/index.md`: 首頁上的 tracked / verified 摘要
- `specs/en/index.md`: 英文首頁上的 tracked / verified 摘要
- `specs/verification_status.md`: 中文 verification summary、verified entries、non-claims
- `specs/en/verification_status.md`: 英文 verification summary、verified entries、non-claims
- 核心 spec pages: 與該 entry family 相關的 `Non-claims` 與 `Governed Linkage`

維護規則：

- 若只改 visible wording，不得改變 YAML source-of-truth 語意
- 若新增或提升 verified entry，必須同步更新 verification status 與首頁摘要
- 若 evidence packet count 改變，必須同步更新 evidence packet summary
- 若只新增 section_refs metadata，不得自動宣告該 page 或 entry 已 verified

## Static Numbers Note

本頁的 entry counts 與 packet statuses 都是人工維護的靜態摘要。

只要以下任一項改變，本頁都必須手動更新：

- `tables/port_status_bit_matrix.yaml` 中任一 entry 的 `claim_level`
- `tables/class_request_matrix.yaml` 或 `tables/feature_selector_matrix.yaml` 的 entries 數量或狀態
- `evidence/entry_verification_packets/` 中新增或修改 packet

governed YAML tables 才是 source of truth；本頁只是 visibility summary。
