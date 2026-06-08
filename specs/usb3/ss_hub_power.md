---
title: SS Hub Power Management
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

# SS Hub Power Management

> 資料範圍：USB 3.2 Specification Rev 1.0，Section 10.14 / 10.14.2。
> 本頁是消費端參考摘要，不是 power management runtime behavior 驗證紀錄。

## 頁面目的

本頁回答：

- USB 3.x SS hub 的 port power 控制方式（ganged vs. per-port）。
- U1/U2 link power state 對 SS hub port 的影響。
- `bPwrOn2PwrGood` 的語意。

本頁不回答：

- 各 power state 的 firmware 實作是否正確。
- U1/U2 入/離場的 LTSSM runtime behavior。
- 電氣/功率合規性（electrical/power compliance）。

## SS Hub Port Power Control

USB 3.x SS hub 的 power switching mode 由 `wHubCharacteristics bits[1:0]` 定義：

| Mode | 說明 |
|---|---|
| Ganged (00) | 所有 ports 統一 power on/off |
| Per-port (01) | 每個 port 獨立透過 SET_FEATURE(PORT_POWER) 控制 |
| No switching (1x) | Hub 不支援 power switching |

Power switching mode 的 bit identity 已完成 verified promotion（`ss_hub_characteristics_bit_matrix`）。

> **無 Transaction Translator**：USB 3.x SS hub 無 TT，因此無 TT Think Time bits 及 TT-related power management。

## U1/U2 Link Power States

SuperSpeed hub port 支援 U1/U2 link power states（低功耗待機）：

- **U0**：Active（正常工作狀態）
- **U1**：Standby（short wake latency, < 10 μs）
- **U2**：Standby（longer wake latency, < 2 ms）
- **U3**：Suspend（deepest power saving）

**PORT_U1_ENABLE / PORT_U2_ENABLE feature selectors** 控制是否允許 port 接受 device 發起的 U1/U2 進入請求。

U1/U2 進入或離場後的 LTSSM state transition behavior 超出本頁 verified scope。

## bPwrOn2PwrGood

`wHubDescriptor.bPwrOn2PwrGood`（2 ms 單位）：

- 定義 hub 在 power-on 或 resume 後需要多少時間讓 port 穩定供電。
- Host 在此時間內不應對 port 發出請求。
- 實際 power stabilization 行為超出本頁 verified scope；此欄位的 identity 已在 ss_hub_descriptor_matrix 完成 verified promotion。

## Over-current Protection

SS hub 的 over-current protection mode 由 `wHubCharacteristics bits[4:3]` 定義：

- `00`：Global（hub-level）OC reporting。
- `01`：Individual port OC reporting。
- `1x`：No OC protection。

Over-current 偵測硬體行為、閾值、C_PORT_OVER_CURRENT notification behavior 超出本頁 verified scope。

## 本頁不宣告

- U1/U2 power state 進入或離場的 LTSSM behavior。
- Port power sequencing 或 timing 的正確性。
- Over-current 偵測硬體行為或閾值。
- firmware power management 實作的正確性。
- 電氣或功率合規性（electrical/power compliance）。

→ [SS Hub Characteristics](ss_hub_characteristics.md) | [SS Feature Selectors](ss_feature_selectors.md) | [Verification Status](../verification_status.md)
