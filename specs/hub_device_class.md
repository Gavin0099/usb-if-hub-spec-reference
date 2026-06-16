---
title: Hub Device Class Codes
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Device Class Codes

> 來源範圍：USB 2.0 Specification Rev 2.0，§11.3 / §11.23.1。  
> 本頁記錄 hub 在標準 USB device descriptor 中應呈現的 class code 欄位值，屬 reviewed boundary；不是 descriptor dump 驗證或 firmware 行為驗證。

## 頁面目的

本頁回答：

- 為什麼 `bDeviceClass = 0x09` 表示 hub class。
- `bDeviceSubClass` 和 `bDeviceProtocol` 在 hub 語境中代表什麼。
- Single-TT hub 與 Multi-TT hub 如何透過 `bDeviceProtocol` 區分。

本頁不回答：

- Hub 的 USB 2.0 device descriptor 其他欄位（VID、PID、bcdUSB 等）是否已驗證。
- 特定 hub 韌體的 device descriptor 是否正確。
- 是否所有 HS hub 都必須聲明 TT 能力。

## Device Descriptor Class Code 欄位

USB device descriptor 在 offset 4–6 包含三個 class code 欄位，對 hub 有特定意義：

| Offset | 欄位 | 大小 | Hub 規範值 |
|---|---|---|---|
| 4 | `bDeviceClass` | 1 byte | `0x09`（Hub 類別） |
| 5 | `bDeviceSubClass` | 1 byte | `0x00` |
| 6 | `bDeviceProtocol` | 1 byte | `0x00` / `0x01` / `0x02`（見下） |

### `bDeviceClass = 0x09`

- Hub 類別碼為 `0x09`，由 USB-IF 保留給 hub class。
- Host stack / 驅動程式以此識別 hub class device，並套用 hub class request 集合。
- 若 `bDeviceClass = 0x00`（表示 interface-level class），hub 仍需在 interface descriptor 的 `bInterfaceClass` 中設為 `0x09`。

### `bDeviceSubClass = 0x00`

- hub class 的 SubClass 固定為 `0x00`，USB 2.0 spec 未定義 hub subclass。

### `bDeviceProtocol`：TT 能力識別碼

| `bDeviceProtocol` | Hub 類型 | 說明 |
|---:|---|---|
| `0x00` | Full-speed hub 或不聲明 TT 的 hub | FS hub；或 HS hub 但不透過 device descriptor 廣播 TT 能力 |
| `0x01` | HS hub，single Transaction Translator | 整個 hub 只有一個 TT（所有 port 共用） |
| `0x02` | HS hub，multiple Transaction Translators | 每個 port 有獨立的 TT（multi-TT hub） |

TT 能力僅在 HS hub 有意義。FS hub 使用 `0x00`，因為 FS hub 不需要 TT（FS hub 自身不支援 HS downstream）。

## 與 TT Matrix 的關聯

- `tables/transaction_translator_matrix.yaml` 中的 `usb20_tt_type_single` 與 `usb20_tt_type_multiple` 對應此處的 `0x01` 和 `0x02` protocol code。
- `bDeviceProtocol` 是 host 在枚舉期間識別 single-TT vs multi-TT 的入口點。
- `SET_FEATURE(PORT_*)` 的 TT 行為細節見 `specs/transaction_translator.md`。

## 安全解讀邊界

- 本頁記錄 class code 欄位的 identity 邊界，不聲明特定 hub 的實際 TT 實作是否正確。
- `bDeviceProtocol = 0x01` 只表示 hub 聲明 single-TT；不代表 TT think-time 或 buffer 行為已驗證。
- 若 consuming repo 的 hub 硬體 `bDeviceProtocol` 與預期不符，應進入 Standard Escalation Mode。

## Governed Linkage

- `tables/transaction_translator_matrix.yaml`：TT type 與 TT think-time 的 governed surface
- `specs/transaction_translator.md`：TT type 與 multi-TT behavior 的 reference summary
- `specs/hub_descriptor.md`：hub class descriptor 欄位（bDescLength 到 PortPwrCtrlMask）

## Non-claims

- 本頁不是 USB device descriptor 的完整欄位驗證。
- 本頁不宣告任何 hub 的 `bDeviceClass`、`bDeviceSubClass`、`bDeviceProtocol` 值已被驗證為正確。
- 本頁不覆蓋 consuming repo 已確認的 project facts。

## Reference Navigation

- specs/usb2.md: USB 2.0 topic index (zh).
- specs/en/hub_device_class.md: English counterpart topic (en).
