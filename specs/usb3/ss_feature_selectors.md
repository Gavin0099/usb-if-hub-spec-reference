---
title: SS Feature Selectors
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

# SS Feature Selectors

> 資料範圍：USB 3.2 Specification Rev 1.0，Section 10.14 Table 10-8（SuperSpeed Hub Feature Selectors）。
> 本頁是消費端參考摘要，不是逐 selector PDF 驗證紀錄。
> 治理矩陣：`tables/ss_feature_selector_matrix.yaml`（6 個 SS-only port feature selectors，全部 verified）。

## 頁面目的

本頁回答：

- USB 3.x SS hub 中有哪些 SS-only port feature selectors（USB 2.0 不存在）。
- 每個 selector 的數值（value）、recipient（port），以及適用的請求（SetFeature / ClearFeature）。
- 什麼是 U1/U2 Link Power Management（LPM）selector。

本頁不回答：

- U1/U2 enable 後的 LTSSM 狀態轉換行為。
- xHCI port power policy 或 U1/U2 policy enforcement 實作。
- firmware compliance 是否已驗證。

## SS-Only Port Feature Selectors

以下 6 個 feature selectors 僅存在於 USB 3.x SuperSpeed hub；不存在於 USB 2.0 hub feature selector namespace。

| Selector name | Value | Hex | Recipient | SetFeature | ClearFeature |
|---|---:|---|---|---|---|
| PORT_U1_ENABLE | 17 | 0x11 | port | ✓ | ✓ |
| PORT_U2_ENABLE | 18 | 0x12 | port | ✓ | ✓ |
| PORT_U1_TIMEOUT | 23 | 0x17 | port | ✓ | — |
| PORT_U2_TIMEOUT | 24 | 0x18 | port | ✓ | — |
| PORT_REMOTE_WAKE_MASK | 27 | 0x1B | port | ✓ | — |
| BH_PORT_RESET | 28 | 0x1C | port | ✓ | — |

Source: USB 3.2 Specification §10.14 Table 10-8。

## U1/U2 Link Power Management (LPM) Selectors

**PORT_U1_ENABLE (0x11)** 和 **PORT_U2_ENABLE (0x12)**：
- 允許 hub port 進入 U1 / U2 link power state。
- SET_FEATURE: 允許 SS hub port 接受來自 downstream device 的 U1/U2 進入請求。
- CLEAR_FEATURE: 停止接受 U1/U2 進入請求。

**PORT_U1_TIMEOUT (0x17)** 和 **PORT_U2_TIMEOUT (0x18)**：
- 設定 SS hub port 的 U1/U2 超時閾值。
- SET_FEATURE(wValue): wValue 的 high byte 為 timeout 編碼，低 byte 為 port 號。
- 詳細 timeout 編碼語意超出本頁 verified scope。

## PORT_REMOTE_WAKE_MASK (0x1B)

- 設定 SS hub port 的 remote wake 事件 mask。
- wValue high byte 為 wake mask 編碼：各 bit 對應不同 wake 事件類型。
- Wake mask encoding 語意超出本頁 verified scope。

## BH_PORT_RESET (0x1C)

- 又稱 Warm Reset。觸發 SS hub port 執行 BH（Buffered Host）reset 序列。
- SET_FEATURE: 發起 Warm Reset，用於修復 link layer 問題。
- BH reset 時序、LFPS signaling、xHCI warm reset behavior 超出本頁 verified scope。

## Verified Gate 說明

本治理矩陣（`tables/ss_feature_selector_matrix.yaml`）的 verified gate 狀態：**PARTIAL（allowlist，全 6 筆已完成 verified promotion）**。

Verified scope 限制在：selector name、value、applicability（SetFeature/ClearFeature）、recipient（port）identity only。

Evidence packets: `evidence/entry_verification_packets/usb3/ss_feature_selector_*.yaml`（6 筆）。

## 本頁不宣告

- U1/U2 enable 後的 LTSSM 狀態轉換。
- U1/U2 timeout 編碼語意或 wValue 行為。
- xHCI port power policy 或 U1/U2 policy enforcement。
- Remote wake event routing 或 OS 電源管理。
- BH reset 時序、LFPS signaling、link recovery outcome。
- firmware compliance。

→ [Verification Status](../verification_status.md)
