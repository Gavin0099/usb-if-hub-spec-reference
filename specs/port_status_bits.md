---
title: 連接埠狀態與變更位元
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# 連接埠狀態與變更位元

> 來源：USB 2.0 規格書 Revision 2.0，第 11.24.2.7.1 與 11.24.2.7.2 節
> 用途：僅供語意參考層使用。不可用於覆蓋已確認的專案事實。

## 連接埠狀態欄位（wPortStatus）

由 GET_PORT_STATUS 請求回傳，16 位元欄位。

| 位元 | 名稱 | 設定時的含義 |
|------|------|------------|
| 0 | PORT_CONNECTION | 此連接埠已連接裝置 |
| 1 | PORT_ENABLE | 連接埠已啟用 |
| 2 | PORT_SUSPEND | 連接埠已暫停 |
| 3 | PORT_OVER_CURRENT | 偵測到過電流狀態 |
| 4 | PORT_RESET | 連接埠正在重置 |
| 7:5 | 保留 | 必須為 0 |
| 8 | PORT_POWER | 連接埠電源已開啟 |
| 9 | PORT_LOW_SPEED | 已連接低速裝置（0 = 全速） |
| 10 | PORT_HIGH_SPEED | 已連接高速裝置 |
| 11 | PORT_TEST | 連接埠處於測試模式 |
| 12 | PORT_INDICATOR | 連接埠指示燈由軟體控制 |
| 15:13 | 保留 | 必須為 0 |

## 連接埠變更欄位（wPortChange）

記錄自上次讀取以來的狀態變更，由 CLEAR_FEATURE 清除。

| 位元 | 名稱 | 清除方式 |
|------|------|---------|
| 0 | C_PORT_CONNECTION | C_PORT_CONNECTION feature |
| 1 | C_PORT_ENABLE | C_PORT_ENABLE feature |
| 2 | C_PORT_SUSPEND | C_PORT_SUSPEND feature |
| 3 | C_PORT_OVER_CURRENT | C_PORT_OVER_CURRENT feature |
| 4 | C_PORT_RESET | C_PORT_RESET feature |
| 15:5 | 保留 | — |

## 標準衝突說明

- **位元 3（PORT_OVER_CURRENT）**：規格定義為硬體偵測到的過電流狀態。
  若專案將此位元用於內部級聯 hub 狀態訊號，屬於已確認的 Project Implementation
  Constraint，不可以通用標準行為替換。
- **位元 15:13 與 7:5**：USB-IF 保留這些位元，必須為 0。若專案將
  任何保留位元用於廠商自訂目的，須觸發 Standard Escalation Mode。
- **PORT_HIGH_SPEED（位元 10）**：僅適用於高速能力的 hub。全速專用
  hub 的韌體不得設定或測試此位元。
