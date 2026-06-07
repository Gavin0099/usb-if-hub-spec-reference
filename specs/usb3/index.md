---
title: USB 3.x / SuperSpeed Hub 參考
claim_level: inferred
spec_family: usb3
status: review_required
last_reviewed: "2026-06-07"
usb_versions:
  - usb_3_2
source_refs:
  - usb32_spec
semantic_verification_claimed: false
---

# USB 3.x / SuperSpeed Hub 參考

> 資料範圍：USB 3.2 Specification Rev 1.0，第 10 章 Hub Class。  
> 本節是 SuperSpeed hub 規格澄清層；不宣告 LTSSM 完整行為模型、xHCI 互動語意或電氣合規。

## 本節覆蓋範圍

| 頁面 | 主題 |
|---|---|
| [SuperSpeed Hub Descriptor](./ss_hub_descriptor) | bDescriptorType=0x2A、wHubCharacteristics、bHubDecLat、wHubDelay |
| [SS Port Status Bits](./ss_port_status_bits) | wPortStatus / wPortChange 位元定義、PORT_LINK_STATE、PORT_SPEED |
| [SS Hub Class Requests](./ss_hub_class_requests) | SET_HUB_DEPTH、GET_PORT_ERR_COUNT、與 USB 2.0 的差異 |

## USB 2.0 vs USB 3.x hub：關鍵差異

| 面向 | USB 2.0 | USB 3.x / SuperSpeed |
|---|---|---|
| Hub descriptor type | 0x29 | 0x2A |
| TT（Transaction Translator） | 有（HS hub） | 無 |
| Suspend 機制 | PORT_SUSPEND bit | U1/U2/U3 link states |
| Port speed 表達 | PORT_LOW_SPEED + PORT_HIGH_SPEED | PORT_SPEED 3-bit field |
| Hub routing depth | 無限制 | 最多 5 層（SET_HUB_DEPTH） |
| Warm reset | 無 | BH Port Reset |

## Non-claims

- 不宣告 LTSSM 完整狀態機行為
- 不宣告 xHCI host controller 互動語意
- 不宣告 USB 3.x 電氣、timing 或互通性合規
- 不宣告 USB4 / Thunderbolt hub 語意
- 不覆寫 consuming repo 的 confirmed project facts
