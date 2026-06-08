---
title: SS Hub 設備類別碼
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

# SS Hub 設備類別碼

> 來源範圍：USB 3.2 Specification Rev 1.0，§10.14.2 / §10.15.1。
> 本頁記錄 SuperSpeed hub 在標準 USB device descriptor 中呈現的 class code 欄位值，屬 reviewed reference；不是 descriptor dump 驗證或 firmware 行為驗證。

## 頁面目的

本頁回答：

- USB 3.x SS hub 的 `bDeviceClass`、`bDeviceSubClass`、`bDeviceProtocol` 規範值。
- `bDeviceProtocol = 0x03` 在 USB 3.x 語境中代表什麼。
- SS hub 與 USB 2.0 hub 在 device class code 上的差異。

本頁不回答：

- Hub 的 VID、PID、`bcdUSB` 等廠商相關欄位是否已驗證。
- 特定 hub 韌體的 device descriptor 是否正確。
- LTSSM 訓練後的 speed 識別機制。

## Device Descriptor Class Code 欄位

USB device descriptor 在 offset 4–6 包含三個 class code 欄位，對 SS hub 有特定意義：

| Offset | 欄位 | 大小 | SS Hub 規範值 |
|---|---|---|---|
| 4 | `bDeviceClass` | 1 byte | `0x09`（Hub 類別） |
| 5 | `bDeviceSubClass` | 1 byte | `0x00` |
| 6 | `bDeviceProtocol` | 1 byte | `0x03`（SuperSpeed hub）|

### `bDeviceClass = 0x09`

- Hub 類別碼為 `0x09`，USB 2.0 與 USB 3.x 相同，由 USB-IF 保留給 hub class。
- Host stack 以此識別 hub class device 並套用 hub class request 集合。

### `bDeviceSubClass = 0x00`

- hub class 的 SubClass 固定為 `0x00`，USB 3.x 未定義 hub subclass。

### `bDeviceProtocol = 0x03`：SuperSpeed Hub

USB 3.x SuperSpeed hub 使用 `bDeviceProtocol = 0x03`，與 USB 2.0 協議碼不同：

| `bDeviceProtocol` | Hub 類型 | 說明 |
|---:|---|---|
| `0x00` | USB 2.0 FS hub 或不聲明 TT 的 hub | USB 2.0 only |
| `0x01` | USB 2.0 HS hub，single TT | USB 2.0 only |
| `0x02` | USB 2.0 HS hub，multi-TT | USB 2.0 only |
| `0x03` | **SuperSpeed hub** | USB 3.x SS hub（無 TT；SS hub 不需要 TT）|

`bDeviceProtocol = 0x03` 是 USB 3.x SuperSpeed hub 的識別碼。SS hub 沒有 Transaction Translator，因此無需 0x01/0x02 的 TT 類型區分。

## bcdUSB 版本欄位

SS hub 的 `bcdUSB`（device descriptor offset 2–3）反映最低支援的 USB 規格版本：

| `bcdUSB` | USB 版本 |
|---|---|
| `0x0300` | USB 3.0 |
| `0x0310` | USB 3.1（Gen 2 / 10 Gbps 時） |
| `0x0320` | USB 3.2（多通道 Gen 2×2 時） |

`bcdUSB` 的實際值由設備功能決定，本頁不宣告特定值已驗證。

## 與 USB 2.0 的差異

| 面向 | USB 2.0 Hub | USB 3.x SS Hub |
|---|---|---|
| `bDeviceProtocol` | 0x00/0x01/0x02（TT 類型） | 0x03（SuperSpeed，無 TT）|
| TT 能力廣告 | 透過 protocol code 區分 single/multi-TT | 不適用（SS hub 無 TT）|
| `bcdUSB` | 0x0200 | 0x0300 或更高 |

## Governed Linkage

- `specs/usb3/ss_hub_descriptor.md`：SS hub class-specific descriptor 欄位
- `specs/usb3/ss_hub_configuration.md`：SS hub configuration/interface descriptor 結構
- `specs/usb3/ss_hub_class_requests.md`：SS hub class 請求集合（無 TT 請求）

## Non-claims

- 本頁不是 USB device descriptor 的完整欄位驗證。
- 本頁不宣告任何 SS hub 的 `bDeviceClass`、`bDeviceSubClass`、`bDeviceProtocol` 值已被驗證為正確。
- 本頁不宣告 LTSSM 訓練行為或 speed 識別機制已驗證。
- 本頁不覆蓋 consuming repo 已確認的 project facts。

→ [SS Hub Descriptor](ss_hub_descriptor.md) | [SS Hub Configuration](ss_hub_configuration.md) | [Verification Status](../verification_status.md)
