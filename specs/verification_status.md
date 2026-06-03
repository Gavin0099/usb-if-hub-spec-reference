---
title: 驗證狀態
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
semantic_verification_claimed: false
---

# 驗證狀態

> 本頁是靜態可見度摘要，不是自動生成的 source of truth。
> 受管 YAML 表格與 evidence packets 才是資料來源。
> 本頁的數字需在表格或 packet 狀態異動時手動同步。

## 目前驗證摘要

| 範圍 | 表格 | Entries 數量 | Verified | Reviewed non-promoting | Inferred |
|---|---|---|---|---|---|
| Hub 類別請求 | `tables/class_request_matrix.yaml` | 12 | 0 | 0 | 12 |
| 功能選擇器 | `tables/feature_selector_matrix.yaml` | 25 | 0 | 0 | 25 |
| 連接埠狀態位元 | `tables/port_status_bit_matrix.yaml` | 10 | 2 | 0 | 8 |
| Evidence packets | `evidence/entry_verification_packets/` | 2 | 2（已 promote） | 0 | — |
| **合計** | | **47** | **2** | **0** | **45** |

數字含義：

- **Verified**：已通過 entry-level promotion gate，`claim_level: verified`，scope 明確限定。
- **Reviewed non-promoting**：review 已完成，evidence packet 存在，但 `eligible_for_verified: false`，promotion 刻意保留。
- **Inferred**：有整理，但尚未進入 reviewed 或 verified 狀態，`claim_level: inferred`。

## 已 Verified 的 Entry

目前有兩筆 entry 完成 verified promotion（Phase 8E、Phase 8H）：

| Entry | 欄位 | 位元 | Verified Scope |
|---|---|---|---|
| PORT_CONNECTION | `wPortStatus` | bit 0 | bit name and bit position only |
| PORT_ENABLE | `wPortStatus` | bit 1 | bit name and bit position only |

Verified scope 明確限定為：**bit 名稱與 bit 位置**。

以下項目在所有 verified entries 的 scope 之外，不適用：

- 任何 timing 行為
- 任何 state transition 行為
- `SetPortFeature` 行為
- `ClearPortFeature` 行為
- error recovery 條件
- host-stack 解讀
- 完整 USB 2.0 compliance

## Reviewed but Not Promoted

目前沒有 reviewed non-promoting entries。所有 reviewed packets 均已完成 Phase 8H promotion。

## 本頁不宣告的事項

本頁不宣告：

- USB 2.0 Hub 行為已全面驗證。
- 任何 page-level 或 table-level 驗證已完成。
- PORT_ENABLE 的 state machine、SetPortFeature 或 error recovery 行為已 verified。
- Inferred entries 可作為實作真值使用。
- 本參考資料可覆蓋 consuming repo 的確認 project facts。
- 靜態數字會自動隨 YAML 表格同步。

## 靜態數字說明

本頁的 entry 數量與 packet 狀態是手動維護的靜態摘要。

當以下任何項目發生改變時，本頁數字需要手動更新：

- `tables/port_status_bit_matrix.yaml` 的 `claim_level` 異動
- `tables/class_request_matrix.yaml` 或 `tables/feature_selector_matrix.yaml` 新增或更新 entries
- `evidence/entry_verification_packets/` 目錄下新增或修改 packets

受管 YAML 表格本身才是 source of truth；本頁只是可視化摘要。
