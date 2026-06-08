---
title: SS Test Modes
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

# SS Test Modes

> 資料範圍：USB 3.2 Specification Rev 1.0，Section 10.14（Hub Class Requests）及 Section 6–7（Physical Layer）。
> 本頁是消費端參考摘要，不是 test mode behavior 驗證紀錄。
> **重要**：本頁不宣告任何電氣合規性或 USB-IF 認證。

## 頁面目的

本頁回答：

- USB 3.x SS hub 支援哪些 test modes（測試模式）概述。
- Compliance Mode 與 Loopback 的用途摘要。
- Test mode 對應的 `PORT_LINK_STATE` 值。

本頁不回答：

- Test mode 的電氣規格或合規測試步驟。
- USB-IF 認證測試程序。
- firmware 如何實作 test mode 進入/離場。

## USB 3.x SuperSpeed Test Modes 概述

USB 3.x SS hub 支援多種 test mode，主要透過 SET_FEATURE(PORT_LINK_STATE) 或 hub class request 機制觸發（依實作而異）。

### Compliance Mode（0xA）

- **用途**：讓 SS port 進入固定的 Compliance 訊號模式，用於電氣互操作性測試（眼圖、信號品質）。
- **對應 PORT_LINK_STATE**：0xA（Compliance Mode）。
- 觸發後 port 持續輸出 Compliance pattern，通常需要重置離場。
- 電氣規格與測試標準超出本頁 verified scope。

### Loopback（0xB）

- **用途**：讓 SS port 進入 loopback 模式，將接收到的資料原樣發回（用於 PHY 測試）。
- **對應 PORT_LINK_STATE**：0xB（Loopback）。
- Loopback 測試的行為與觸發機制超出本頁 verified scope。

## PORT_LINK_STATE 與 Test Mode 的對應

以下 PORT_LINK_STATE 值與 test/diagnostic 相關（encoding identity 已 verified）：

| PORT_LINK_STATE 值 | Link state | 說明 |
|---|---|---|
| 0xA | Compliance Mode | 電氣合規測試模式 |
| 0xB | Loopback | PHY loopback 測試模式 |
| 0x7 | Polling | Link training/polling（非測試模式，但可作為 test 觀察點） |

**Verified scope**：encoding identity only（bit range [8:5] 與 12-value table）。Test mode behavior 超出 verified scope。

## 與 USB 2.0 Test Mode 的差異

| 特性 | USB 2.0 | USB 3.x SuperSpeed |
|---|---|---|
| Test 觸發 | SET_FEATURE(PORT_TEST, wValue=test_mode) | 透過 PORT_LINK_STATE 等機制 |
| Test modes | Test_J, Test_K, Test_SE0_NAK, Test_Packet, Test_Force_Enable | Compliance Mode, Loopback |
| 訊號 | D+/D- 差分 | SS TX+/TX-（差分串行） |

## 本頁不宣告

- Test mode 電氣規格或眼圖標準。
- USB-IF Compliance 測試程序或認證要求。
- firmware test mode 進入/離場實作正確性。
- Compliance pattern 或 loopback 測試的行為細節。

→ [SS Signaling](ss_signaling.md) | [SS Port State Machine](ss_port_state_machine.md) | [Verification Status](../verification_status.md)
