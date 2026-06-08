---
title: SS Hub 配置描述符
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

# SS Hub 配置描述符

> 來源範圍：USB 3.2 Specification Rev 1.0，§10.14.2 / §10.15.1。
> 本頁是 SS hub 在枚舉過程中呈現的 configuration、interface、BOS 及 SuperSpeed Endpoint Companion descriptor 欄位的 reviewed reference summary；不是 descriptor dump 驗證。

## 頁面目的

本頁回答：

- SS hub 的 configuration descriptor 集合包含哪些描述符類型。
- BOS（Binary Device Object Store）descriptor 在 USB 3.x 中扮演什麼角色。
- SS hub interface descriptor 的 class code 欄位值。
- SuperSpeed Endpoint Companion Descriptor（type 0x30）的作用。

本頁不回答：

- 特定 hub 的 VID、PID、`bcdUSB`、`iProduct` 等廠商相關欄位。
- SS Hub class-specific descriptor 欄位細節（見 `specs/usb3/ss_hub_descriptor.md`）。
- 任何特定 hub 的 descriptor dump 是否已驗證。

## SS Hub 枚舉中的 Descriptor 層次

USB 3.x SS hub 枚舉時 host 讀取的描述符流程：

```
GET_DESCRIPTOR(DEVICE)          → device descriptor（bDeviceProtocol=0x03）
GET_DESCRIPTOR(CONFIGURATION)   → configuration descriptor set：
    configuration descriptor（9 bytes）
    interface descriptor（9 bytes）
    endpoint descriptor（7 bytes，interrupt IN）
    SuperSpeed Endpoint Companion Descriptor（6 bytes）
GET_DESCRIPTOR(BOS)             → BOS descriptor + capability descriptors
GET_DESCRIPTOR(HUB_CLASS=0x2A)  → SS Hub class-specific descriptor
```

SS hub 比 USB 2.0 hub 多了 **BOS descriptor** 和 **SuperSpeed Endpoint Companion Descriptor**。

## Configuration Descriptor

SS hub 通常呈現 1 個 configuration：

| 欄位 | 典型值 | 說明 |
|---|---|---|
| `bNumConfigurations` | `1` | SS hub 通常只有一個 configuration |
| `bConfigurationValue` | `1` | host 以 `SET_CONFIGURATION(1)` 選取 |
| `bNumInterfaces` | `1` | SS hub class 只需一個 interface |
| `bmAttributes` | 依設計而定 | bit 6 = 自供電（1）/ 匯流排供電（0）；bit 5 = remote wakeup 支援 |
| `bMaxPower` | 依設計而定 | hub 從 VBUS 汲取的最大電流（以 2 mA 為單位）|

> USB 3.x 自供電 hub 可提供每 port 最高 900 mA；匯流排供電 hub 限制較低。詳見 `specs/usb3/ss_hub_power_budget.md`。

## Interface Descriptor

SS hub 使用單一 interface；與 USB 2.0 的 TT 模式差異如下：

| 欄位 | 值 | 說明 |
|---|---|---|
| `bInterfaceClass` | `0x09` | Hub class（與 device descriptor 相同）|
| `bInterfaceSubClass` | `0x00` | USB 3.x 未定義 hub interface subclass |
| `bInterfaceProtocol` | `0x00` | SS hub 無 TT；不需要 alternate setting |
| `bNumEndpoints` | `1` | 僅一個 interrupt IN endpoint |

**無 alternate setting**：USB 2.0 multi-TT hub 透過 `SET_INTERFACE` 切換 single/multi-TT 模式；SS hub 沒有 TT，不需要 alternate setting。

## BOS Descriptor（Binary Device Object Store）

USB 3.x 設備必須提供 BOS descriptor（descriptor type `0x0F`）：

| 欄位 | 大小 | 說明 |
|---|---|---|
| `bLength` | 1 | 5 bytes（BOS descriptor header）|
| `bDescriptorType` | 1 | `0x0F`（BOS）|
| `wTotalLength` | 2 | BOS header + 所有 capability descriptors 的總長度 |
| `bNumDeviceCaps` | 1 | 內含的 Device Capability Descriptor 數量 |

BOS 包含一個或多個 Device Capability Descriptor，SS hub 至少包含：
- **SuperSpeed USB Device Capability**（`bDevCapabilityType = 0x03`）

## SuperSpeed USB Device Capability Descriptor

BOS 內的 SuperSpeed USB Device Capability（`bDevCapabilityType = 0x03`）：

| 欄位 | 說明 |
|---|---|
| `bmAttributes` | bit 1 = LTM（Latency Tolerance Messaging）支援 |
| `wSpeedsSupported` | 設備支援的速度位元集（Full-Speed=bit 1, High-Speed=bit 2, SS=bit 3）|
| `bFunctionalitySupport` | 最低完全功能速度（通常 SS=0x03）|
| `bU1DevExitLat` | U1 exit latency（μs；0–10μs）|
| `wU2DevExitLat` | U2 exit latency（μs；0–2047μs）|

SuperSpeed USB Device Capability 描述 U1/U2 延遲的具體值是設備相關的，本頁不宣告特定值已驗證。

## SuperSpeed Endpoint Companion Descriptor

SS hub 的 interrupt IN endpoint 後面緊跟著 SuperSpeed Endpoint Companion Descriptor（type `0x30`）：

| 欄位 | 大小 | SS Hub 典型值 | 說明 |
|---|---|---|---|
| `bLength` | 1 | `6` | descriptor 大小 |
| `bDescriptorType` | 1 | `0x30` | SuperSpeed Endpoint Companion |
| `bMaxBurst` | 1 | `0` | interrupt endpoint 不支援 burst（0 = 1 packet）|
| `bmAttributes` | 1 | `0x00` | interrupt endpoint 保留（必須為 0）|
| `wBytesPerInterval` | 2 | 依 port 數而定 | 每輪詢間隔的最大 bytes（hub status bitmap）|

## 與 USB 2.0 的差異

| 面向 | USB 2.0 Hub | USB 3.x SS Hub |
|---|---|---|
| BOS descriptor | 非必要 | **必要**（USB 3.x 設備必須提供）|
| Endpoint Companion | 無 | **必要**（每個 SS endpoint 需要）|
| Interface alternate setting | multi-TT hub 可能有 2 個 | 無（SS hub 無 TT）|
| `bInterfaceProtocol` | 0x00（FS/不廣告 TT）| 0x00（無 TT，SS hub 永遠無 TT）|

## Governed Linkage

- `specs/usb3/ss_hub_descriptor.md`：SS hub class-specific descriptor（type 0x2A）欄位
- `specs/usb3/ss_hub_device_class.md`：bDeviceClass/SubClass/Protocol 的詳細說明
- `specs/usb3/ss_hub_interrupt_endpoint.md`：interrupt IN endpoint descriptor 欄位
- `specs/usb3/ss_hub_power_budget.md`：SS hub 電源預算規則（900 mA per port）

## Non-claims

- 本頁不是任何特定 SS hub 的 descriptor dump 驗證。
- 本頁不宣告 `bMaxPower`、`bmAttributes`、U1/U2 latency 等廠商相關欄位的正確值。
- 本頁不宣告 BOS/SuperSpeed Capability 的語義行為已驗證。
- 本頁不覆蓋 consuming repo 已確認的 project facts。

→ [SS Hub Descriptor](ss_hub_descriptor.md) | [SS Standard Descriptors](ss_standard_descriptors.md) | [Verification Status](../verification_status.md)
