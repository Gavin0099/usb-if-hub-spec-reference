---
title: SS Link Power Management (U1/U2/U3)
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

# SS Link Power Management (U1/U2/U3)

> 資料範圍：USB 3.2 Specification Rev 1.0，Section 7.2（Link Power Management）及 Section 10.14。
> 本頁是消費端參考摘要，不是 LPM runtime behavior 驗證紀錄。
> **重要**：本頁不宣告任何 LTSSM state transition behavior。

## 頁面目的

本頁回答：

- USB 3.x 的四個 link power states（U0–U3）的定義摘要。
- U1/U2 進入的前提條件概述。
- Hub port 透過哪些 feature selectors 控制 U1/U2。

本頁不回答：

- U1/U2/U3 進入或離場的 LTSSM state transition behavior。
- xHCI U1/U2 policy enforcement 實作。
- U1/U2 timeout 的實際語意與 wValue 編碼細節。

## USB 3.x Link Power States（U0–U3）

| State | 說明 | 典型 wake latency |
|---|---|---|
| U0 | Active（正常工作） | N/A |
| U1 | 待機（短 wake latency） | < 10 μs（參考值，依硬體而異） |
| U2 | 待機（較長 wake latency） | < 2 ms（參考值，依硬體而異） |
| U3 | Suspend（深度省電） | Suspend/Resume 序列 |

> Wake latency 為 spec 參考值；實際硬體行為超出本頁 verified scope。

## U1/U2 進入概述

USB 3.x 中，U1/U2 進入可由 device 或 host 發起（須符合各方 policy 條件）。Hub port 需透過 feature selectors 允許：

- **SET_FEATURE(PORT_U1_ENABLE)**：允許 hub port 接受 device 發起的 U1 進入。
- **SET_FEATURE(PORT_U2_ENABLE)**：允許 hub port 接受 device 發起的 U2 進入。

LTSSM 中的 U1/U2 進入或退出序列超出本頁 verified scope。

## U1/U2 Timeout Selectors

- **PORT_U1_TIMEOUT (0x17)**：設定 SS hub port 的 U1 inactivity timeout。
- **PORT_U2_TIMEOUT (0x18)**：設定 SS hub port 的 U2 inactivity timeout。

wValue high byte 的 timeout 編碼語意超出本頁 verified scope；timeout 值的實際語意屬於 firmware 行為。

## U3（Suspend）

- U3 是最深的省電狀態；對應 USB 2.0 的 Suspend。
- Host 透過 SET_FEATURE(PORT_SUSPEND) 觸發 U3。
- `PORT_SUSPEND` bit（wPortStatus bit 2）反映 U3 狀態（verified）。
- U3 進入和離場的完整序列（包含 resume signaling）超出本頁 verified scope。

## wPortStatus 中的 LPM 相關 bits

以下 bits 在 `ss_port_status_bit_matrix` 中已完成 verified promotion（bit identity only）：

| Bit | 名稱 | 說明 |
|---|---|---|
| wPortStatus bit 2 | PORT_SUSPEND | Port 處於 U3 suspend 狀態 |
| wPortStatus bits[8:5] | PORT_LINK_STATE | 目前 link state（12 個值） |

## 本頁不宣告

- U1/U2/U3 進入或離場的 LTSSM state transition behavior。
- xHCI U1/U2 policy enforcement 或 power management 實作。
- U1/U2 timeout 編碼語意或 inactivity timeout 行為。
- Resume signaling 或 wakeup 行為。
- 實際 wake latency 保證。

→ [SS Feature Selectors](ss_feature_selectors.md) | [SS Port State Machine](ss_port_state_machine.md) | [Verification Status](../verification_status.md)
