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

> Source scope: USB 2.0 Specification Rev 2.0, Sections 11.17-11.18.  
> This page is a TT behavior summary and does not claim full split-transaction verification.

## 核心概念

Transaction Translator（TT）存在於 high-speed hub，用來橋接主機端高速 split transaction 與實際流向 full-speed / low-speed downstream 的實際傳輸。

- 不具 TT 的 hub 不該宣告 TT 專用請求支援。
- Full-speed-only hub 不該宣告 TT 行為。
- TT 行為綁定 descriptor 宣告的 TT 類型與 TT think time 設定。

## TT 類型與 Think Time

| 項目 | 相關欄位 | 說明 |
|---|---|---|
| Single TT | `wHubCharacteristics` TT type | 一個 TT 服務整個 downstream ports |
| Multiple TT | `wHubCharacteristics` TT type | 每個 port（或 port 群）可有獨立 TT 實例 |
| TT Think Time = `00` | `wHubCharacteristics[6:5]` | 8 FS bit times |
| TT Think Time = `01` | `wHubCharacteristics[6:5]` | 16 FS bit times |
| TT Think Time = `10` | `wHubCharacteristics[6:5]` | 24 FS bit times |
| TT Think Time = `11` | `wHubCharacteristics[6:5]` | 32 FS bit times |

## TT Requests

- `CLEAR_TT_BUFFER`
- `RESET_TT`
- `GET_TT_STATE`
- `STOP_TT`

這些 request 僅適用於具有 embedded TT 的 HS hub。

本 repo 的 reviewed request surface 目前是：

- `CLEAR_TT_BUFFER`：`wValue` 帶 TT buffer selector fields；`wIndex` 選擇 TT port / context
- `RESET_TT`：`wValue = 0x0000`；`wIndex` 選擇 TT port number
- `GET_TT_STATE`：`wValue = 0x0000`；`wIndex` 選擇 TT port / diagnostic context；`wLength` 是 TT state data length
- `STOP_TT`：`wValue = 0x0000`；`wIndex` 選擇 TT port number

這還不足以構成 field-level 的完整 verifier 或 TT 行為語意驗證完成。

## Governed Linkage

- `tables/transaction_translator_matrix.yaml`: TT 類型、think-time、TT request-linkage 的主要治理來源。
- `tables/hub_descriptor_matrix.yaml`: 將 TT think-time 對應到 `wHubCharacteristics[6:5]`。
- `tables/class_request_matrix.yaml`: 將 TT request 名稱映射到 class request setup surface。
- `specs/escalation_table.md`: `E-06`、`E-07`、`E-10` 提供 TT 相關 escalation triggers。

此 TT 表格只是一個 reviewed reference boundary，未驗證 split-transaction timing、TT buffer selector encoding、診斷 payload semantics，或 firmware 支援語意。

## Split Transaction 流程

1. Host 發送 Start Split 給 HS hub。
2. Hub TT 將 request 轉譯給下游 FS/LS 裝置。
3. Host 後續發送 Complete Split。
4. Hub / TT 匯總結果並向上游回報。

## 使用注意

- 本頁不得覆蓋消費 repo 已確認的 Single TT / Multiple TT 架構決策。
- TT think time 與 descriptor 宣告設定不一致是 escalation trigger。
- 若此頁面內容會直接改變 firmware 行為，應先走 architecture review。
