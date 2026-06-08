---
title: SS Hub Compound Device
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

# SS Hub Compound Device

> 資料範圍：USB 3.2 Specification Rev 1.0，Section 10.14.2（wHubCharacteristics bit[2]）。
> 本頁是消費端參考摘要，不是 compound device behavior 驗證紀錄。

## 頁面目的

本頁回答：

- 什麼是 USB 3.x compound device hub。
- `wHubCharacteristics bit[2]`（Compound Device flag）的語意。
- Compound device 在 USB 3.x 拓撲中的意義。

本頁不回答：

- Compound device topology 的 firmware 行為是否正確。
- DeviceRemovable bitmap 的解讀語意。
- USB-IF compound device 認證要求。

## Compound Device 定義

**Compound device**：一個 USB compound device 是指 hub 與一個或多個 function（downstream device）在同一個物理外殼中整合，且直接連接到 hub 的某些 downstream ports 上，這些連接是固定的（non-removable）。

USB 3.x SS hub 的 `wHubCharacteristics bit[2]` 反映此狀態：

| bit[2] | 語意 |
|---|---|
| 0 | Hub 不是 compound device 的一部分 |
| 1 | Hub 是 compound device 的一部分（部分下游 functions 固定連接） |

此 bit identity 已在 `ss_hub_characteristics_bit_matrix` 完成 verified promotion（bit name 和 value encoding identity only）。

## Compound Device 在 USB 3.x 拓撲中的意義

- 當 compound device bit = 1 時，host 應將某些 downstream ports 視為 non-removable。
- `DeviceRemovable` bitmap（Hub Descriptor 中）標示哪些 ports 是固定連接（compound ports）。
- DeviceRemovable 的解讀語意超出本頁 verified scope。

## 與 USB 2.0 的差異

USB 3.x `wHubCharacteristics bit[2]` 的 compound device flag 與 USB 2.0 bit[2] 語意相同（identical encoding）。

主要差異在拓撲限制：
- USB 2.0 compound device 的固定 functions 通常是 Full-Speed 或 High-Speed。
- USB 3.x compound device 的固定 functions 可以是 SuperSpeed。
- 兩者的 `wHubCharacteristics bit[2]` encoding 相同（0=not compound, 1=compound）。

## 本頁不宣告

- Compound device topology behavior 或 link routing。
- DeviceRemovable bitmap 解讀語意。
- Firmware compound device 實作正確性。
- USB-IF compound device 認證要求或測試標準。

→ [SS Hub Characteristics](ss_hub_characteristics.md) | [SS Hub Descriptor](ss_hub_descriptor.md) | [Verification Status](../verification_status.md)
