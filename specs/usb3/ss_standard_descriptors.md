---
title: SS 標準描述符
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

# SS 標準描述符

> 來源範圍：USB 3.2 Specification Rev 1.0，§9.5–9.6 / §10.14.2。
> 本頁是 USB 3.x SuperSpeed hub 相關標準描述符類型的 reviewed reference summary。SS hub class-specific descriptor 欄位請見 `specs/usb3/ss_hub_descriptor.md`。

## 頁面目的

本頁回答：

- USB 3.x 新增了哪些描述符類型（BOS、SuperSpeed Endpoint Companion）。
- SS hub 的 device descriptor hub-specific 欄位值。
- 與 USB 2.0 標準描述符的主要差異。

本頁不回答：

- SS Hub class-specific descriptor 欄位（type 0x2A）—— 請見 `specs/usb3/ss_hub_descriptor.md`。
- Vendor-specific 或其他 class-specific 描述符擴展。

## 描述符類型一覽

| `bDescriptorType` | 名稱 | 適用範圍 |
|---|---|---|
| `0x01` | Device Descriptor | 標準（USB 2.0 + USB 3.x）|
| `0x02` | Configuration Descriptor | 標準（USB 2.0 + USB 3.x）|
| `0x04` | Interface Descriptor | 標準（USB 2.0 + USB 3.x）|
| `0x05` | Endpoint Descriptor | 標準（USB 2.0 + USB 3.x）|
| `0x06` | Device Qualifier | USB 2.0（HS/FS dual-mode）|
| `0x0F` | BOS Descriptor | **USB 3.x 新增（必要）**|
| `0x10` | Device Capability Descriptor | **USB 3.x 新增**（BOS 內部）|
| `0x2A` | SS Hub Descriptor | **USB 3.x SS hub class-specific**|
| `0x30` | SuperSpeed Endpoint Companion | **USB 3.x 新增（每個 SS endpoint 必要）**|

## Device Descriptor（USB 3.x Hub）

大小：**18 bytes**。Descriptor type：`0x01`。

| Offset | 欄位 | 大小 | SS Hub 值 |
|---|---|---|---|
| 0 | `bLength` | 1 | `18` |
| 1 | `bDescriptorType` | 1 | `0x01` |
| 2–3 | `bcdUSB` | 2 | `0x0300` 或更高（USB 3.0/3.1/3.2）|
| 4 | `bDeviceClass` | 1 | `0x09`（Hub class）|
| 5 | `bDeviceSubClass` | 1 | `0x00` |
| 6 | `bDeviceProtocol` | 1 | `0x03`（SuperSpeed hub）|
| 7 | `bMaxPacketSize0` | 1 | `9`（SS EP0 使用 512-byte packets，以指數 2^9=512 編碼）|
| 8–9 | `idVendor` | 2 | Vendor ID（廠商相關）|
| 10–11 | `idProduct` | 2 | Product ID（廠商相關）|
| 12–13 | `bcdDevice` | 2 | 設備版本號（廠商相關）|
| 14 | `iManufacturer` | 1 | 字串描述符索引 |
| 15 | `iProduct` | 1 | 字串描述符索引 |
| 16 | `iSerialNumber` | 1 | 字串描述符索引 |
| 17 | `bNumConfigurations` | 1 | `1`（通常）|

> SS hub 的 `bMaxPacketSize0 = 9`：EP0 的最大封包大小以指數表示，2^9 = 512 bytes。這是 USB 3.x 的新編碼方式，與 USB 2.0（直接字節值）不同。

## BOS Descriptor（type 0x0F）

USB 3.x **要求**所有設備提供 BOS descriptor；USB 2.0 設備不需要（可選）。

```
BOS Descriptor（5 bytes）
  └── SuperSpeed USB Device Capability（10 bytes）[bDevCapabilityType=0x03]
  └── SuperSpeed Plus USB Device Capability（可選，Gen 2 設備）[bDevCapabilityType=0x0A]
  └── 其他 capability descriptors（LTM、Container ID 等，依設備而定）
```

BOS 讓 host 在枚舉時發現設備的 SuperSpeed 能力（U1/U2 exit latency、LTM support 等）。

## SuperSpeed USB Device Capability（BOS 內，bDevCapabilityType=0x03）

| 欄位 | 大小 | 說明 |
|---|---|---|
| `bLength` | 1 | 10 bytes |
| `bDescriptorType` | 1 | `0x10`（Device Capability）|
| `bDevCapabilityType` | 1 | `0x03`（SuperSpeed USB）|
| `bmAttributes` | 1 | bit 1 = LTM support |
| `wSpeedsSupported` | 2 | 支援速度位元集（bit 3 = SS）|
| `bFunctionalitySupport` | 1 | 最低完全功能速度（通常 0x03 = SS）|
| `bU1DevExitLat` | 1 | U1 exit latency（μs，0–10）|
| `wU2DevExitLat` | 2 | U2 exit latency（μs，0–2047）|

## SuperSpeed Endpoint Companion Descriptor（type 0x30）

USB 3.x 每個非 EP0 endpoint 之後**必須**緊接 SuperSpeed Endpoint Companion Descriptor：

| 欄位 | 大小 | SS Hub Interrupt IN 典型值 | 說明 |
|---|---|---|---|
| `bLength` | 1 | `6` | |
| `bDescriptorType` | 1 | `0x30` | |
| `bMaxBurst` | 1 | `0` | interrupt 不支援 burst（0 = 1 packet/transfer）|
| `bmAttributes` | 1 | `0x00` | interrupt 保留，必須為 0 |
| `wBytesPerInterval` | 2 | ≥ 1 byte | 每輪詢間隔最大 bytes（hub status bitmap）|

## 與 USB 2.0 標準描述符的主要差異

| 面向 | USB 2.0 | USB 3.x SuperSpeed |
|---|---|---|
| `bDeviceProtocol` | 0x00/0x01/0x02 | 0x03 |
| `bMaxPacketSize0` | 直接字節值（8/64）| 指數值（9 = 2^9 = 512 bytes）|
| BOS descriptor | 可選 | **必要** |
| Endpoint Companion | 不存在 | **必要**（每個 SS endpoint）|
| Device Qualifier | FS/HS dual-mode 設備使用 | SS 設備不使用 |
| Hub class descriptor type | `0x29`（USB 2.0 Hub Descriptor）| `0x2A`（SuperSpeed Hub Descriptor）|

## Governed Linkage

- `specs/usb3/ss_hub_descriptor.md`：SS Hub Descriptor（type 0x2A）欄位
- `specs/usb3/ss_hub_configuration.md`：SS hub configuration/BOS/Companion descriptor 結構
- `specs/usb3/ss_hub_device_class.md`：`bDeviceProtocol = 0x03` 說明

## Non-claims

- 本頁不是任何特定 SS hub 的 descriptor dump 驗證。
- 本頁不宣告 BOS/SuperSpeed Capability 的 U1/U2 latency 值已驗證。
- 本頁不宣告 `bMaxPacketSize0 = 9` 已針對特定 hub 驗證。
- 本頁不覆蓋 consuming repo 已確認的 project facts。

→ [SS Hub Configuration](ss_hub_configuration.md) | [SS Hub Descriptor](ss_hub_descriptor.md) | [Verification Status](../verification_status.md)
