---
title: USB Transfer Types
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# USB Transfer Types

> 來源範圍：USB 2.0 Specification Rev 2.0，§5.4–§5.7。  
> 本頁是 USB 2.0 四種傳輸類型及其對 hub 操作的相關性的 reviewed reference summary。

## 頁面目的

本頁回答：

- USB 2.0 的四種傳輸類型是什麼，各有哪些特性。
- USB 2.0 hub 使用哪些傳輸類型。
- 每種傳輸類型如何對應到特定的 endpoint 類型。

## USB 2.0 四種傳輸類型

| 傳輸類型 | `bmAttributes[1:0]` | 方向 | 錯誤恢復 | 時序保證 | Hub 用途 |
|---|---|---|---|---|---|
| **Control** | `00` | 雙向（setup+data+status）| 有（重試）| 無 | Endpoint 0 — 所有請求 |
| **Isochronous** | `01` | IN 或 OUT | 無（不重試）| 保證頻寬 | 無 |
| **Bulk** | `10` | IN 或 OUT | 有（重試）| 無（盡力而為）| 無 |
| **Interrupt** | `11` | IN 或 OUT | 有（重試）| 有界延遲 | Status change endpoint |

## Control Transfer

**Hub 使用**：是 — Endpoint 0 處理所有標準和 hub class 請求。

結構：
- **SETUP 階段**：Host 向 endpoint 0 傳送 8-byte setup packet。
- **DATA 階段**（選用）：Host 或設備傳輸資料 payload。
- **STATUS 階段**：設備（或 IN 時的 host）確認完成。

特性：
- 保證傳遞：錯誤觸發重試。
- HS 最多 64 bytes/封包（LS: 8 bytes，FS: 8/16/32/64）。
- Host 排程器為 control transfer 分配最多 10% 的 bus 頻寬。

Hub 角色：在 endpoint 0 回應標準請求（`GET_DESCRIPTOR`、`SET_ADDRESS`、`SET_CONFIGURATION`）和 hub class 請求（`GET_STATUS`、`SET_FEATURE`、`CLEAR_FEATURE`、TT requests）。

## Interrupt Transfer

**Hub 使用**：是 — 唯一的 interrupt IN endpoint 是 status change endpoint。

特性：
- 週期性：host 以 `bInterval` 為間隔輪詢 endpoint。
- 有界延遲：transfer 在可用後的有界時間內完成。
- 錯誤恢復：錯誤在同一週期內觸發重試。
- FS：`bInterval` = 1–255 ms polling interval。
- HS：`bInterval` = 2^(`bInterval`–1) × 125µs（編碼指數）。

Hub 角色：Hub 透過此 endpoint 上的單一 status change bitmap 回報 port 狀態變化（連接、斷開、過電流、reset 完成等）。請見 `specs/hub_interrupt_endpoint.md`。

## Bulk Transfer

**Hub 使用**：否。Hub 沒有 bulk endpoint。

特性：
- 大型可靠資料傳輸，無時序保證。
- 在其他傳輸類型服務後填充可用 bus 頻寬。
- FS 最大 64 bytes/封包；HS 最大 512 bytes/封包。

Hub 沒有 bulk endpoint，不使用此傳輸類型。

## Isochronous Transfer

**Hub 使用**：否。Hub 沒有 isochronous endpoint。

特性：
- 即時、固定速率傳輸。
- 無錯誤恢復——遺失的資料不重傳。
- 保留頻寬分配保證傳遞時序。
- 用於音訊、視訊及其他即時 class 設備。

Hub 沒有 isochronous endpoint，不使用此傳輸類型。

## 傳輸類型與 Endpoint Descriptor

Endpoint descriptor 中的 `bmAttributes[1:0]` 欄位宣告傳輸類型：

| `bmAttributes[1:0]` | 傳輸類型 |
|---|---|
| `00` | Control（僅限 endpoint 0；不在 endpoint descriptor 中編碼）|
| `01` | Isochronous |
| `10` | Bulk |
| `11` | Interrupt |

Hub endpoint 0 固定為 Control；唯一的附加 hub endpoint 的 `bmAttributes=0x03`（Interrupt）。

## Split Transactions 與傳輸類型

對於連接到 HS hub 的 FS/LS 下行設備，hub 的 Transaction Translator（TT）將 HS split transaction 轉換為 FS/LS transaction。這適用於 FS/LS 設備的 control 和 bulk transaction；isochronous transaction 也被 split 但有特殊處理。請見 `specs/transaction_translator.md`。

## Governed Linkage

- `specs/hub_interrupt_endpoint.md`：Hub status change interrupt endpoint descriptor 欄位
- `specs/hub_configuration.md`：hub configuration 情境中的 endpoint descriptor
- `specs/transaction_translator.md`：TT 如何橋接 HS 和 FS/LS 的傳輸時序

## Non-claims

- 本頁不宣告傳輸類型實作已針對實體 hub 驗證。
- 本頁不定義完整的 USB 2.0 排程器或頻寬分配演算法。
- 本頁不覆蓋 consuming repo 已確認的 project facts。
