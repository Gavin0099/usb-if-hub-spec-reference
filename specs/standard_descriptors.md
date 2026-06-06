---
title: Standard USB Descriptors
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Standard USB Descriptors

> 來源範圍：USB 2.0 Specification Rev 2.0，§9.5 和 §9.6。  
> 本頁是 USB 2.0 標準描述符類型的 reviewed reference summary。Hub class descriptor 欄位請見 `specs/hub_descriptor.md`。

## 頁面目的

本頁回答：

- USB 2.0 標準描述符有哪些類型，各包含哪些欄位。
- 每個描述符中哪些欄位與 USB hub 識別相關。

本頁不回答：

- Hub class descriptor 欄位 —— 請見 `specs/hub_descriptor.md`。
- Hub class 以外的 vendor-specific 或 class-specific 描述符擴展。

## 描述符層次

Host 讀取 `GET_DESCRIPTOR (configuration)` 時，設備依序回傳完整 configuration descriptor set：

```
Configuration Descriptor（9 bytes）
  └── Interface Descriptor（9 bytes）  [每個 interface 一個]
        └── Endpoint Descriptor（7 bytes）  [每個 endpoint 一個]
  └── Hub Class Descriptor（可變長度）  [hub class interface 專用]
```

Hub class descriptor 須另以 `GET_DESCRIPTOR`（`bmRequestType=0xA0`）單獨請求。

## Device Descriptor（§9.6.1）

大小：**18 bytes**。Descriptor type：`0x01`。

| Offset | 欄位 | 大小 | Hub 值 |
|---|---|---|---|
| 0 | `bLength` | 1 | `18` |
| 1 | `bDescriptorType` | 1 | `0x01` |
| 2–3 | `bcdUSB` | 2 | `0x0200`（USB 2.0）|
| 4 | `bDeviceClass` | 1 | `0x09`（Hub class）|
| 5 | `bDeviceSubClass` | 1 | `0x00` |
| 6 | `bDeviceProtocol` | 1 | `0x00` FS/無TT，`0x01` HS/single-TT，`0x02` HS/multi-TT |
| 7 | `bMaxPacketSize0` | 1 | EP0 最大封包大小（FS: 8，HS: 64）|
| 8–9 | `idVendor` | 2 | Vendor ID（USB-IF 指派）|
| 10–11 | `idProduct` | 2 | Product ID（廠商自訂）|
| 12–13 | `bcdDevice` | 2 | 設備版本號（BCD）|
| 14 | `iManufacturer` | 1 | 字串描述符索引（0 = 無字串）|
| 15 | `iProduct` | 1 | 字串描述符索引（0 = 無字串）|
| 16 | `iSerialNumber` | 1 | 字串描述符索引（0 = 無字串）|
| 17 | `bNumConfigurations` | 1 | Configuration 數量（通常為 `1`）|

> Hub class codes（`bDeviceClass`、`bDeviceSubClass`、`bDeviceProtocol`）請見 `specs/hub_device_class.md`。

## Device_Qualifier Descriptor（§9.6.2）

大小：**10 bytes**。Descriptor type：`0x06`。**僅限 HS-capable 設備。**

描述設備在另一速度下（例如 HS hub 的 FS 行為）的運作方式：

| Offset | 欄位 | 說明 |
|---|---|---|
| 0 | `bLength` | `10` |
| 1 | `bDescriptorType` | `0x06` |
| 2–3 | `bcdUSB` | USB 版本 |
| 4 | `bDeviceClass` | 相同 class code |
| 5 | `bDeviceSubClass` | 相同 |
| 6 | `bDeviceProtocol` | 另一速度下的 protocol |
| 7 | `bMaxPacketSize0` | 另一速度下的 EP0 最大封包 |
| 8 | `bNumConfigurations` | 另一速度下的 config 數量 |
| 9 | `bReserved` | 必須為零 |

FS hub 沒有 Device_Qualifier descriptor；向 FS hub 請求此描述符會收到 STALL。

## Configuration Descriptor（§9.6.3）

大小：**9 bytes**。Descriptor type：`0x02`。作為完整 configuration set 的一部分回傳。

| Offset | 欄位 | 大小 | Hub 值 |
|---|---|---|---|
| 0 | `bLength` | 1 | `9` |
| 1 | `bDescriptorType` | 1 | `0x02` |
| 2–3 | `wTotalLength` | 2 | Configuration descriptor set 的總長度 |
| 4 | `bNumInterfaces` | 1 | `1`（hub 只有一個 interface）|
| 5 | `bConfigurationValue` | 1 | Configuration 編號（通常為 `1`）|
| 6 | `iConfiguration` | 1 | 字串描述符索引 |
| 7 | `bmAttributes` | 1 | bit 7=1（必要），bit 6=Self-Powered，bit 5=Remote-Wakeup |
| 8 | `bMaxPower` | 1 | 最大匯流排電流，單位 2mA |

`bmAttributes` bit 7 必須永遠為 1（USB 2.0 規格要求）；bits 4:0 保留必須為零。

## Interface Descriptor（§9.6.5）

大小：**9 bytes**。Descriptor type：`0x04`。

| Offset | 欄位 | 大小 | Hub 值 |
|---|---|---|---|
| 0 | `bLength` | 1 | `9` |
| 1 | `bDescriptorType` | 1 | `0x04` |
| 2 | `bInterfaceNumber` | 1 | `0` |
| 3 | `bAlternateSetting` | 1 | `0`=single-TT，`1`=multi-TT（僅限 HS）|
| 4 | `bNumEndpoints` | 1 | `1`（status change endpoint）|
| 5 | `bInterfaceClass` | 1 | `0x09`（Hub class）|
| 6 | `bInterfaceSubClass` | 1 | `0x00` |
| 7 | `bInterfaceProtocol` | 1 | `0x00` |
| 8 | `iInterface` | 1 | 字串描述符索引 |

> Multi-TT hub 在同一 interface number 下提供兩個 alternate settings（0 和 1）。請見 `specs/hub_configuration.md`。

## Endpoint Descriptor（§9.6.6）

大小：**7 bytes**。Descriptor type：`0x05`。Hub 只有一個 endpoint：status change interrupt IN endpoint。

| Offset | 欄位 | 大小 | Hub 值 |
|---|---|---|---|
| 0 | `bLength` | 1 | `7` |
| 1 | `bDescriptorType` | 1 | `0x05` |
| 2 | `bEndpointAddress` | 1 | bit 7=1（IN 方向），bits 3:0=endpoint 編號 |
| 3 | `bmAttributes` | 1 | `0x03`（bits[1:0]=11：Interrupt transfer type）|
| 4–5 | `wMaxPacketSize` | 2 | `ceil((bNbrPorts + 1) / 8)` bytes |
| 6 | `bInterval` | 1 | Polling interval（FS: 1–255 ms；HS: 2^(n-1) × 125µs）|

`wMaxPacketSize` 與 `bInterval` 編碼細節請見 `specs/hub_interrupt_endpoint.md`。

## String Descriptor（§9.6.7）

大小：**可變**。Descriptor type：`0x03`。

- String 0（language ID 清單）：最少 4 bytes；包含支援的 `LANGID` 代碼。
- String N（語言相關文字）：2 + 2×字串長度 bytes；UTF-16LE 編碼。

Hub 不強制要求 String 0 以外的字串描述符，但 iManufacturer、iProduct、iSerialNumber 可選擇性指向字串。

## Governed Linkage

- `specs/hub_descriptor.md`：Hub class descriptor 欄位（type `0x29`），由 class GET_DESCRIPTOR 取得
- `specs/hub_device_class.md`：用於 hub 識別的 `bDeviceClass`、`bDeviceSubClass`、`bDeviceProtocol` 值
- `specs/hub_configuration.md`：hub configuration 與 interface descriptor 的使用情境
- `specs/hub_interrupt_endpoint.md`：hub status change endpoint 的 endpoint descriptor 欄位
- `specs/standard_device_requests.md`：`GET_DESCRIPTOR` 請求編碼與 descriptor type codes

## Non-claims

- 本頁不宣告任何描述符欄位已針對實體 hub 完成 correctness-verified。
- 本頁不宣告 `bMaxPower` 或 `bmAttributes` 的 self-powered vs. bus-powered 語意已驗證。
- 本頁不覆蓋 consuming repo 已確認的 project facts。
