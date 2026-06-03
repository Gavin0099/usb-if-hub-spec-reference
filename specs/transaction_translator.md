---
title: Transaction Translator
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Transaction Translator

> 來源範圍：USB 2.0 Specification Rev 2.0，第 11.17-11.18 節。
> 本頁為 TT 行為摘要，不代表已完成所有 split transaction 細節的逐段驗證。

## 核心概念

Transaction Translator（TT）存在於 high-speed hub 中，用來橋接 host 發出的 high-speed split transaction，與 full-speed / low-speed downstream 裝置之間的實際傳輸。

- 沒有 TT 的 hub，不應宣稱支援 TT 專屬請求。
- Full-speed-only hub 不應出現 TT 行為；若出現，屬於 escalation trigger。
- TT 行為與 `wHubCharacteristics` 中的 TT 類型與 think time 設定密切相關。

## TT 類型與 think time

| 項目 | 對應欄位 | 摘要 |
|---|---|---|
| Single TT | `wHubCharacteristics` TT type | 所有 downstream port 共用同一個 TT |
| Multiple TT | `wHubCharacteristics` TT type | 每個 port 或 port 群組具獨立 TT |
| TT Think Time = `00` | `wHubCharacteristics[6:5]` | 8 FS bit times |
| TT Think Time = `01` | `wHubCharacteristics[6:5]` | 16 FS bit times |
| TT Think Time = `10` | `wHubCharacteristics[6:5]` | 24 FS bit times |
| TT Think Time = `11` | `wHubCharacteristics[6:5]` | 32 FS bit times |

## TT 相關請求

- `CLEAR_TT_BUFFER`：清除 TT 緩衝狀態
- `RESET_TT`：重設 TT
- `GET_TT_STATE`：讀取 TT 診斷狀態
- `STOP_TT`：停止 TT split transaction 處理

這些請求只適用於具內建 TT 的 HS hub。

本 repo 目前已收斂的 reviewed request surface 是：

- `CLEAR_TT_BUFFER`: `wValue` 是 TT buffer selector fields；`wIndex` 是 TT port / context
- `RESET_TT`: `wValue = 0x0000`；`wIndex` 是 TT port number
- `GET_TT_STATE`: `wValue = 0x0000`；`wIndex` 是 TT port / diagnostic context；`wLength` 是 TT state data length
- `STOP_TT`: `wValue = 0x0000`；`wIndex` 是 TT port number

這不等於完整 field-level verified encoding，也不等於 TT behavior 已完成 semantic verification。

## Split transaction 摘要

1. Host 對 HS hub 發出 Start Split。
2. Hub 內的 TT 轉換為對 FS/LS 裝置可用的交易。
3. Host 之後再以 Complete Split 取回結果或完成階段。
4. Hub / TT 彙整結果並回傳 upstream。

## 使用注意

- 如果專案已確認使用 Single TT 或 Multiple TT，不能僅憑本 repo 的一般標準摘要覆蓋它。
- TT Think Time 若與 descriptor 宣告不一致，屬於 escalation trigger。
- consuming repo 若要依本頁內容調整 TT 行為，應先經過標準衝突檢查與 architecture review。
