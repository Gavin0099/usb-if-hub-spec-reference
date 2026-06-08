---
title: SS Transactions
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

# SS Transactions

> 資料範圍：USB 3.2 Specification Rev 1.0，Section 8（Transaction Layer）。
> 本頁是消費端參考摘要，不是 transaction behavior 驗證紀錄。

## 頁面目的

本頁回答：

- USB 3.x SuperSpeed 的 transaction 模型概述。
- SS transaction 與 USB 2.0 transaction 的主要差異。
- Hub 在 SS transaction routing 中的角色。

本頁不回答：

- Transaction layer 的 runtime behavior 或 retry 機制。
- xHCI 如何實作 SS transaction scheduling。
- USB-IF transaction 合規性或互操作性測試。

## USB 3.x SuperSpeed Transaction 模型

USB 3.x SuperSpeed 採用**點對點（point-to-point）**全雙工 link，transaction 模型與 USB 2.0 有根本差異：

### USB 2.0 vs USB 3.x Transaction 比較

| 特性 | USB 2.0 | USB 3.x SuperSpeed |
|---|---|---|
| 拓撲 | 共享匯流排（half-duplex） | 點對點（full-duplex） |
| 事務發起 | Host 發出 Token packet | Host 發出 Transaction Packet (TP) |
| 流量控制 | 無（polling-based） | Link layer flow control（NRDY/ERDY） |
| 重傳機制 | Host polling retry | Link layer ACK/NACK |
| Split Transaction | 需要（HS hub 的 TT） | **不需要**（無 TT） |

### SS Transaction 步驟（Bulk IN 範例）

1. **Host → Device**: DP（Data Packet request）+ TP
2. **Device → Host**: DP（Data Packet）
3. **Host → Device**: TP（ACK）

Flow control 透過 NRDY（not ready）/ ERDY（endpoint ready）TP 實現，device 可主動通知 host 端點就緒。

## NRDY / ERDY 流量控制

- **NRDY（Not Ready）**：裝置通知 host 端點目前無法接受或提供資料。
- **ERDY（Endpoint Ready）**：裝置主動通知 host 端點已就緒（可替代 host polling）。

NRDY/ERDY 機制減少了 host 輪詢開銷，提高了 SuperSpeed 的效率。

ERDY 的 runtime behavior 超出本頁 verified scope。

## Hub 在 SS Transaction 中的角色

SS hub 作為封包路由器：

- **Downstream routing**：Hub 將 host 發出的 TP/DP 路由到對應的 downstream port。
- **Upstream routing**：Hub 將 downstream device 發出的 TP/DP 路由回 upstream。
- **No TT buffering**：SS hub 不需要 TT（所有連接為 SuperSpeed；無速度域轉換）。

Hub 封包路由的 runtime behavior 超出本頁 verified scope。

## Isochronous Transactions

USB 3.x isochronous transactions 使用 ITP（Isochronous Timestamp Packet）提供同步時間戳記，取代 USB 2.0 的 SOF（Start of Frame）。

等時傳輸的 runtime scheduling 行為超出本頁 verified scope。

## 本頁不宣告

- Transaction layer runtime behavior 或 retry 機制。
- xHCI SS transaction scheduling 實作。
- NRDY/ERDY runtime flow control behavior。
- Link layer ACK/NACK 機制的時序。
- USB-IF transaction 合規性或互操作性測試。

→ [SS Packet Types](ss_packet_types.md) | [SS Hub Class Requests](ss_hub_class_requests.md) | [Verification Status](../verification_status.md)
