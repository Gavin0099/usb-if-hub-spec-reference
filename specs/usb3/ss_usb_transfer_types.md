---
title: SS USB 傳輸類型
claim_level: inferred
spec_family: usb3
status: review_required
last_reviewed: "2026-06-08"
usb_versions:
  - usb_3_2
source_refs:
  - usb32_spec
semantic_verification_claimed: false
---

# SS USB 傳輸類型

> 來源範圍：USB 3.2 Specification Rev 1.0，§8（Transaction Layer）/ Chapter 5。
> 本頁是 USB 3.x SuperSpeed 四種傳輸類型及其對 SS hub 操作相關性的 reviewed reference summary。

## 頁面目的

本頁回答：

- USB 3.x 的四種傳輸類型是什麼，與 USB 2.0 有何差異。
- SS hub 使用哪些傳輸類型。
- NRDY/ERDY flow control 如何影響 SS 傳輸效率。

本頁不回答：

- 傳輸層 runtime 行為或重傳機制 —— 請見 `specs/usb3/ss_transactions.md`。
- NRDY/ERDY 的 runtime flow control 行為。
- xHCI SS 傳輸排程實作。

## USB 3.x 四種傳輸類型

USB 3.x 保留與 USB 2.0 相同的四種傳輸類型，但底層機制根本不同：

| 傳輸類型 | `bmAttributes[1:0]` | SS Hub 用途 | 關鍵 USB 3.x 差異 |
|---|---|---|---|
| **Control** | `00` | Endpoint 0 — 所有請求 | 最大封包 512 bytes（vs HS 64 bytes）|
| **Interrupt** | `11` | Status change endpoint | 週期性，有界延遲；使用 NRDY/ERDY |
| **Bulk** | `10` | 無（hub 不使用）| 最大封包 1024 bytes（vs HS 512 bytes）|
| **Isochronous** | `01` | 無（hub 不使用）| 使用 ITP 取代 SOF 作為時序基準 |

## Control Transfer

**SS Hub 使用**：是 — Endpoint 0 處理所有標準和 hub class 請求。

USB 3.x Control Transfer 特性：
- EP0 最大封包：**512 bytes**（vs USB 2.0 HS: 64 bytes）
- `bMaxPacketSize0`：編碼為 `9`（指數值，2^9 = 512 bytes）
- 結構與 USB 2.0 相同：SETUP + DATA（選用）+ STATUS 三階段

## Interrupt Transfer

**SS Hub 使用**：是 — 唯一的 interrupt IN endpoint 是 status change endpoint。

USB 3.x Interrupt Transfer 特性：
- 週期性輪詢：host 以 `bInterval` 指定的間隔（微幀 125 μs 為單位）輪詢。
- 有界延遲：transfer 在有界時間內完成。
- Flow control：使用 NRDY（endpoint 尚未就緒）和 ERDY（endpoint 主動通知就緒）。
- 無 split transaction：SS hub 不需要 TT，不進行速度域轉換。

SS hub 的 status change endpoint 特性：
- 方向：IN（hub → host）
- 封包大小：1 byte per 8 ports（與 USB 2.0 相同計算）
- `bInterval`：2^(bInterval-1) × 125 μs；範圍 1–16（與 USB 2.0 HS 相同編碼）

## Bulk Transfer

**SS Hub 使用**：否。Hub 沒有 Bulk endpoint。

USB 3.x Bulk Transfer 特性（供 reference）：
- 最大封包：**1024 bytes**（vs USB 2.0 HS: 512 bytes）
- 錯誤恢復：有（ACK/NACK retry）
- Flow control：NRDY/ERDY（主動通知取代輪詢）

## Isochronous Transfer

**SS Hub 使用**：否。Hub 沒有 Isochronous endpoint。

USB 3.x Isochronous Transfer 特性（供 reference）：
- 使用 **ITP（Isochronous Timestamp Packet）** 提供時序基準（取代 USB 2.0 SOF）
- 最大封包：1024 bytes
- 無錯誤重傳（與 USB 2.0 相同）

## NRDY / ERDY Flow Control

USB 3.x 引入 NRDY/ERDY 機制，取代 USB 2.0 的輪詢重試模型：

| 封包 | 方向 | 說明 |
|---|---|---|
| **NRDY** | Device → Host | Endpoint 尚未就緒，host 應暫停輪詢此 endpoint |
| **ERDY** | Device → Host | Endpoint 主動通知 host 已就緒（減少不必要的輪詢）|

ERDY 讓設備在資料就緒時主動通知 host，大幅減少輪詢開銷。NRDY/ERDY 的 runtime 行為細節超出本頁驗證範圍。

## 無 Split Transaction

**SS hub 無需 split transaction（Transaction Translator）**：
- USB 2.0 HS hub 需要 TT 橋接 HS bus 與下行 FS/LS 設備的速度差異。
- USB 3.x SS hub 的下行連接均為 SS（或向下相容的設備）；SuperSpeed 協定層本身處理流量控制，不需要速度域轉換。

詳見 `specs/usb3/ss_transactions.md`。

## 與 USB 2.0 的差異

| 面向 | USB 2.0 Hub | USB 3.x SS Hub |
|---|---|---|
| Control EP0 最大封包 | 64 bytes（HS）| **512 bytes**（2^9）|
| Bulk 最大封包 | 512 bytes（HS）| **1024 bytes** |
| Interrupt flow control | Host 輪詢，無額外信號 | NRDY/ERDY 主動通知 |
| Isochronous 時序基準 | SOF（Start of Frame）| **ITP**（Isochronous Timestamp Packet）|
| Split transaction | HS hub 必要（TT）| **不需要**（SS hub 無 TT）|

## Governed Linkage

- `specs/usb3/ss_transactions.md`：SS transaction model 與 NRDY/ERDY 說明
- `specs/usb3/ss_hub_interrupt_endpoint.md`：hub status change interrupt endpoint descriptor
- `specs/usb3/ss_packet_types.md`：SS 封包類型（TP/DP/LMP/ITP）

## Non-claims

- 本頁不宣告傳輸類型實作已針對實體 SS hub 驗證。
- 本頁不宣告 NRDY/ERDY runtime flow control 行為已驗證。
- 本頁不定義完整的 xHCI 排程器或頻寬分配演算法。
- 本頁不覆蓋 consuming repo 已確認的 project facts。

→ [SS Transactions](ss_transactions.md) | [SS Packet Types](ss_packet_types.md) | [Verification Status](../verification_status.md)
