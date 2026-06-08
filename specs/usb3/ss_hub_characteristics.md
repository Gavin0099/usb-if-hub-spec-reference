---
title: SS Hub Characteristics
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

# SS Hub Characteristics

> 資料範圍：USB 3.2 Specification Rev 1.0，Section 10.14.2 Table 10-10（wHubCharacteristics for SuperSpeed Hub）。
> 本頁是消費端參考摘要，不是逐 bit group PDF 驗證紀錄。
> 治理矩陣：`tables/ss_hub_characteristics_bit_matrix.yaml`（4 verified + 1 reviewed reserved）。

## 頁面目的

本頁回答：

- USB 3.x SS hub 的 `wHubCharacteristics` 欄位有哪些 bit groups 及其語意。
- USB 3.x 與 USB 2.0 的 `wHubCharacteristics` 有何關鍵差異。
- Port Indicators bit 在 USB 3.x 中的位置。

本頁不回答：

- 各 power switching mode 的 firmware 行為如何實作。
- Over-current 偵測的硬體閾值。
- Port indicator LED 的顏色編碼或控制協定。

## USB 3.x wHubCharacteristics 位元配置

| Bit range | 語意群組 | Claim level | 說明 |
|---|---|---|---|
| bits[1:0] | Power Switching Mode | **verified** | 00=ganged, 01=per-port, 1x=no switching |
| bit[2] | Compound Device | **verified** | 0=not compound, 1=compound |
| bits[4:3] | Over-current Protection Mode | **verified** | 00=global, 01=per-port, 1x=no OC |
| bit[5] | Port Indicators Supported | **verified** | 0=不支援, 1=支援 |
| bits[15:6] | Reserved | reviewed | Reserved, shall be zero（永久邊界） |

Source: USB 3.2 Specification §10.14.2 Table 10-10。

## USB 3.x 與 USB 2.0 的關鍵差異

USB 3.x `wHubCharacteristics` 與 USB 2.0 的主要差異：

| 差異 | USB 2.0 | USB 3.x |
|---|---|---|
| TT Think Time bits | bits[6:5]（4 個 TT timing values） | **不存在**（USB 3.x 無 Transaction Translator） |
| Port Indicators bit | bit[7] | **bit[5]**（因 TT bits 移除而前移） |
| Reserved bits | bits[15:8] | **bits[15:6]**（範圍擴大） |

> **重要**：USB 3.x hubs 沒有 Transaction Translator（TT），因此沒有 TT Think Time bits。USB 2.0 cross-link 的 TT-related wHubCharacteristics bits 在 USB 3.x hub 中不存在。

## Power Switching Mode（bits[1:0]）

| 值 | 語意 |
|---|---|
| 00 | Ganged power switching（所有 ports 一起 power on/off） |
| 01 | Individual port power switching（每個 port 獨立控制） |
| 1x | No power switching（hub 不支援 power switching） |

## Compound Device（bit[2]）

- `0`：hub 不是 compound device 的一部分。
- `1`：hub 是 compound device 的一部分。

Compound device 相關語意（topology behavior、DeviceRemovable bitmap interpretation）超出本頁 verified scope。

## Over-current Protection Mode（bits[4:3]）

| 值 | 語意 |
|---|---|
| 00 | Global（hub-level）over-current protection |
| 01 | Individual port over-current protection |
| 1x | No over-current protection |

Over-current detection hardware behavior、threshold、C_PORT_OVER_CURRENT notification 超出本頁 verified scope。

## Port Indicators Supported（bit[5]）

- `0`：hub 不支援 port indicators。
- `1`：hub 支援 LED port indicators，可透過 SET_FEATURE(PORT_INDICATOR) 控制。

LED 硬體行為、顏色編碼、firmware indicator state management 超出本頁 verified scope。

## Verified Gate 說明

本治理矩陣（`tables/ss_hub_characteristics_bit_matrix.yaml`）的 verified gate 狀態：**PARTIAL（allowlist，4 個 defined bit groups 已完成 verified promotion）**。

Verified scope：bit group name、bit range、value encoding identity only。

Evidence packets: `evidence/entry_verification_packets/usb3/ss_whc_*.yaml`（4 筆）。

## 本頁不宣告

- SET_FEATURE(PORT_POWER) firmware behavior。
- Per-port power sequencing 或 timing。
- Over-current detection hardware behavior 或 threshold。
- LED indicator 硬體行為或顏色編碼。
- Compound device topology behavior。
- firmware compliance。

→ [Verification Status](../verification_status.md)
