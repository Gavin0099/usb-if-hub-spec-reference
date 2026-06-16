---
title: USB 2.0 Hub 參考
layout: doc
claim_level: inferred
spec_family: usb2
status: review_required
last_reviewed: "2026-06-16"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# USB 2.0 Hub 參考

> 範圍：USB 2.0 規格第 11 章（Hub Class）。
> 這是 USB 2.0 主題索引頁，USB 3.2 SuperSpeed hub 請參考 [USB 3.2 / SuperSpeed Hub Reference](/en/usb3/)。

## Hub Class Topics

這些頁面涵蓋 USB 2.0 第 11 章定義的 Hub 相關欄位、請求與行為邊界。

| Topic | Description |
|---|---|
| [Hub Descriptor](/hub_descriptor) | Descriptor 欄位、`bDescriptorType=0x29`、`wHubCharacteristics`、`bPwrOn2PwrGood` |
| [Hub Class Requests](/hub_class_requests) | `GET_STATUS`、`SET_FEATURE`、`CLEAR_FEATURE`、`GET_DESCRIPTOR`、`CLEAR_TT_BUFFER`、`RESET_TT` 等 |
| [Feature Selectors](/feature_selectors) | Hub 與 Port selector 命名空間、selector 值 `0-22` |
| [Port Status Bits](/port_status_bits) | `wPortStatus`、`wPortChange`、`wHubStatus`、`wHubChange` bit 定義 |
| [Port Feature / Change Vocabulary](/port_feature_change_vocabulary) | `PORT_*` 與 `C_PORT_*` 的詞彙對齊 |
| [Port State Machine](/port_state_machine) | 7 個 Hub port state 與狀態轉移觸發條件 |
| [Port Indicators](/port_indicators) | LED 控制、`wHubCharacteristics` bit 7、`PORT_INDICATOR` selector |
| [Hub Device Class Codes](/hub_device_class) | `bDeviceClass=0x09`、`bDeviceSubClass`、`bDeviceProtocol` 與 TT type 編碼 |
| [Hub Interrupt Endpoint](/hub_interrupt_endpoint) | status change endpoint descriptor、`wMaxPacketSize` 計算、`bInterval` 編碼 |
| [Hub Power Management](/hub_power_management) | 電源切換模式、`bPwrOn2PwrGood` 時序、過流保護、suspend/resume |
| [Hub Configuration Descriptors](/hub_configuration) | Configuration/Interface Descriptor 欄位、TT 多重 alternate settings |
| [Hub Enumeration Sequence](/hub_enumeration) | 列舉流程、`GET_STATUS` 4-byte 格式、Port 上電時序 |
| [Hub Compound Device](/hub_compound_device) | `wHubCharacteristics` bit 2、`DeviceRemovable`、`PortPwrCtrlMask` |
| [Hub Power Budget](/hub_power_budget) | 自供電與匯流電源限制、每 Port 電流（500mA 與 100mA） |
| [Transaction Translator](/transaction_translator) | TT 規則、`CLEAR_TT_BUFFER`、`RESET_TT`、TT think time、HS hub TT type |
| [High-Speed Detection](/hs_detection) | Chirp K 握手、hub KJ 回應特徵、HS speed negotiation 結果 |

## USB 2.0 Protocol Foundation

這些頁面涵蓋 Hub 運作所需的 USB 2.0 基礎協定內容。

| Topic | Description |
|---|---|
| [Standard Device Requests](/standard_device_requests) | 9.4 章節中 `GET_DESCRIPTOR`、`SET_ADDRESS`、`SET_CONFIGURATION`、標準 feature selectors |
| [Standard USB Descriptors](/standard_descriptors) | Device、configuration、interface、endpoint、string descriptor 欄位 |
| [USB Device States](/usb_device_states) | 9.1 狀態：Attached、Powered、Default、Address、Configured、Suspended |
| [USB Transfer Types](/usb_transfer_types) | Control、Interrupt、Bulk、Isochronous 與 Hub 實作關聯 |
| [USB Signaling](/usb_signaling) | J/K/SE0 狀態、NRZI 編碼、reset/suspend/resume 信號 |
| [USB Packet Types](/usb_packet_types) | PID 編碼、控制/資料/握手/特殊封包 |
| [USB Transactions](/usb_transactions) | SETUP/IN/OUT 流程、control transfer 3 階段、data toggle |
| [Split Transaction Packets](/split_transaction_packets) | SSPLIT/CSPLIT 結構、TT hub split transactions、NYET 重試 |
| [USB Test Modes](/usb_test_modes) | TEST_J/K/SE0_NAK/PACKET/FORCE_ENABLE、`SET_FEATURE(TEST_MODE)` 編碼 |

## Reference & Governance

| Topic | Description |
|---|---|
| [Escalation Table](/escalation_table) | 發生規格與既有實作衝突時，需進一步 review 的條件 |
| [Version Source Map](/version_source_map) | USB 2.0～3.2 source authority 對照 |
| [Verification Status](/verification_status) | Evidence 成熟度：151 tracked / 105 verified / 46 reviewed |
| [Glossary](/glossary) | USB 術語與縮寫 |
