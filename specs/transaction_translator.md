---
title: Transaction Translator (TT) 規則
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Transaction Translator (TT) 規則

> 來源：USB 2.0 規格書 Revision 2.0，第 11.17–11.18 節
> 用途：僅供語意參考層使用。不可用於覆蓋已確認的專案事實。

## 用途說明

Transaction Translator（TT）是高速能力 hub 的必要元件，允許低速與全速
裝置連接至高速匯流排。

TT 負責緩衝全速／低速交易，並將其轉換為高速上行埠格式。

## TT 組態

| 組態項目 | wHubCharacteristics 位元 6:5 | 說明 |
|---------|------------------------------|------|
| Single TT | — | Hub 所有連接埠共用一個 TT |
| Multiple TT | — | Hub 每個連接埠各有一個 TT |
| TT Think Time | 00 | 8 FS 位元時間 |
| TT Think Time | 01 | 16 FS 位元時間 |
| TT Think Time | 10 | 24 FS 位元時間 |
| TT Think Time | 11 | 32 FS 位元時間 |

## TT 請求行為

- **CLEAR_TT_BUFFER**：清除特定端點的 TT 緩衝區。在 TT 交易 halt 後
  用於錯誤恢復。
- **RESET_TT**：將 TT 重置至已知狀態。Hub 必須完成進行中的交易後才能重置。
- **GET_TT_STATE**：回傳 TT 狀態，供診斷用途。
- **STOP_TT**：停止 TT 處理指定埠上的分割交易（Split Transaction）。

## 分割交易概述（Split Transaction）

高速 hub 上的全速／低速流量透過分割交易處理：

1. Host 向 Hub 發出 Start Split（SSPLIT）
2. Hub 緩衝全速／低速交易
3. Host 發出 Complete Split（CSPLIT）取回結果
4. Hub 回傳交易狀態或資料

## 標準衝突說明

- 若專案的 hub 為**全速專用**（無高速上行埠）：TT 不適用。
  此情況下不應要求 TT 支援。
- 若專案使用 Single TT，但描述符回報 Multiple TT（或相反）：
  須觸發 Standard Escalation Mode。
- TT Think Time 必須符合下行裝置的實際匯流排時序需求。
  未經硬體驗證證據，不可更改此值。
