---
title: 驗證狀態
claim_level: inferred
status: review_required
last_reviewed: "2026-06-02"
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
| 連接埠狀態位元 | `tables/port_status_bit_matrix.yaml` | 10 | 1 | 1 | 8 |
| Evidence packets | `evidence/entry_verification_packets/` | 2 | 1（已 promote） | 1（non-promoting） | — |
| **合計** | | **47** | **1** | **1** | **45** |

數字含義：

- **Verified**：已通過 entry-level promotion gate，`claim_level: verified`，scope 明確限定。
- **Reviewed non-promoting**：review 已完成，evidence packet 存在，但 `eligible_for_verified: false`，promotion 刻意保留。
- **Inferred**：有整理，但尚未進入 reviewed 或 verified 狀態，`claim_level: inferred`。

## 已 Verified 的 Entry

目前只有一筆 entry 完成 verified promotion：

| Entry | 欄位 | 位元 | Verified Scope |
|---|---|---|---|
| PORT_CONNECTION | `wPortStatus` | bit 0 | bit name and bit position only |

Verified scope 明確限定為：**bit 名稱與 bit 位置**。

以下項目在此 verified scope 之外，不適用：

- 任何 timing 行為
- 任何 state transition 行為
- `ClearPortFeature` 行為
- host-stack 解讀
- 完整 USB 2.0 compliance

## Reviewed but Not Promoted

以下 entry 的 evidence packet 已完成 review，但刻意不進入 verified promotion：

| Entry | 欄位 | 位元 | Review 狀態 | 原因 |
|---|---|---|---|---|
| PORT_ENABLE | `wPortStatus` | bit 1 | reviewed | Pilot 推廣邊界目前限定在 `PORT_CONNECTION`；擴展需要獨立 gate 更新 |

**`reviewed` 不等於 `verified`。**

Reviewed 代表 evidence packet 已被建立並 review 完成，但沒有觸發 promotion。

Verified 代表 entry 已通過 Phase 8C promotion gate，`claim_level` 升為 `verified`。

## 本頁不宣告的事項

本頁不宣告：

- USB 2.0 Hub 行為已全面驗證。
- 任何 page-level 或 table-level 驗證已完成。
- `PORT_ENABLE` 已 verified。
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
