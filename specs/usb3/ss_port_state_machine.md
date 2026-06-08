---
title: SS Port State Machine
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

# SS Port State Machine

> 資料範圍：USB 3.2 Specification Rev 1.0，Section 10.14.2（SuperSpeed Hub Port Management）。
> 本頁是消費端參考摘要，不是 LTSSM runtime state transition 驗證紀錄。
> **重要**：本頁不宣告任何 LTSSM runtime behavior。

## 頁面目的

本頁回答：

- USB 3.x SS hub port 有哪些主要 port states（以 `wPortStatus` bits 為依據）。
- 哪些 port status bits 與 port state 相關。
- SS hub port reset 的種類。

本頁不回答：

- LTSSM 的 state machine 轉換時序與行為。
- xHCI 如何驅動 port state 轉換。
- firmware 是否正確實作 port state machine。

## SS Hub Port 主要狀態

以下狀態來自 `wPortStatus` bits（`tables/ss_port_status_bit_matrix.yaml` 中的 verified entries）：

| 狀態 | 相關 wPortStatus bits | 說明 |
|---|---|---|
| Disconnected | PORT_CONNECTION=0 | 無裝置連接 |
| Connected (not enabled) | PORT_CONNECTION=1, PORT_ENABLE=0 | 裝置已連接但 port 未啟用 |
| Enabled | PORT_CONNECTION=1, PORT_ENABLE=1 | Port 啟用，link 在 U0 |
| U1/U2 (LPM) | PORT_LINK_STATE=U1/U2 | Link 在低功耗待機狀態 |
| U3 (Suspended) | PORT_LINK_STATE=U3, PORT_SUSPEND=1 | Port 已暫停 |
| In Reset | PORT_RESET=1 | Port 正在執行 Warm Reset 或 Hot Reset |
| Over-current | PORT_OVER_CURRENT=1 | Port 偵測到 over-current |

> `PORT_LINK_STATE` verified scope：bit range [8:5] 與 12-value encoding table identity only；LTSSM 狀態轉換 behavior 超出 verified scope。

## SS Hub Port Reset 類型

USB 3.x SS hub 支援兩種 port reset：

### Warm Reset（BH_PORT_RESET / 0x1C）

- 透過 SET_FEATURE(BH_PORT_RESET) 觸發。
- 執行 BH（Buffered Host）reset 序列，用於修復 link layer 問題。
- 對應 `C_BH_PORT_RESET` change bit（wPortChange 中的 SS-only change bits）。
- BH reset 時序、LFPS signaling、xHCI warm reset behavior 超出本頁 verified scope。

### Hot Reset（PORT_RESET / 0x04）

- 透過 SET_FEATURE(PORT_RESET) 觸發，與 USB 2.0 bus reset 語意不同。
- SS context 中的 Hot Reset 觸發完整的 SS link re-initialization。

## PORT_LINK_STATE Encoding（wPortStatus bits[8:5]）

`PORT_LINK_STATE` 欄位提供 12 個 SS link state 值的 encoding identity（verified）：

| Value | Link state | 說明 |
|---|---|---|
| 0x0 | U0 | Active |
| 0x1 | U1 | U1 LPM |
| 0x2 | U2 | U2 LPM |
| 0x3 | U3 | Suspended |
| 0x4 | Disabled | Port disabled |
| 0x5 | RxDetect | Receiver detection phase |
| 0x6 | Inactive | Inactive |
| 0x7 | Polling | Link polling |
| 0x8 | Recovery | Link recovery |
| 0x9 | Hot Reset | Port hot reset |
| 0xA | Compliance Mode | Compliance test mode |
| 0xB | Loopback | Loopback test |

Source: USB 3.2 Specification §10.14.2 Table 10-9。

**Verified scope**：encoding table identity only（bit range [8:5] 與 12 values）。LTSSM runtime state transition behavior 超出 verified scope。

## PORT_SPEED Encoding（wPortStatus bits[12:10]）

| Value | Speed |
|---|---|
| 0x0 | High-speed |
| 0x1 | Full-speed |
| 0x2 | Low-speed |
| 0x3 | SuperSpeed |
| 0x4 | SuperSpeedPlus (Gen 2×1) |
| 0x5 | SuperSpeedPlus (Gen 1×2) |

**Verified scope**：encoding table identity only。Speed detection hardware 或 link training outcome 超出 verified scope。

## 本頁不宣告

- LTSSM runtime state transition timing 或 behavior。
- xHCI port management 行為。
- firmware port state machine 實作正確性。
- Link training 或 speed negotiation outcome。
- USB-IF compliance 或測試認證。

→ [SS Port Status Bits](ss_port_status_bits.md) | [SS Hub Class Requests](ss_hub_class_requests.md) | [Verification Status](../verification_status.md)
