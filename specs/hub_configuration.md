---
title: Hub Configuration Descriptors
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Configuration Descriptors

> 來源範圍：USB 2.0 Specification Rev 2.0，§11.23 / §11.21。  
> 本頁是 hub 在 USB 枚舉過程中呈現的 configuration 與 interface descriptor 欄位的 reviewed reference summary；不是 descriptor dump 驗證。

## 頁面目的

本頁回答：

- Hub 的 configuration descriptor 通常有哪些特性。
- Hub class 的 interface descriptor 中 `bInterfaceClass`、`bInterfaceSubClass`、`bInterfaceProtocol` 的值。
- Hub 具體有哪些 endpoints（interrupt IN）。

本頁不回答：

- 特定 hub 的 VID、PID、`bcdUSB`、`iProduct` 等廠商相關欄位。
- Hub descriptor（class-specific descriptor）的欄位細節（見 `specs/hub_descriptor.md`）。
- 任何特定 hub 的 descriptor dump 是否已驗證。

## USB Hub 枚舉中的 Descriptor 層次

USB hub 枚舉的 descriptor 流程：

```
GET_DESCRIPTOR(DEVICE) → device descriptor（含 bDeviceClass=0x09）
GET_DESCRIPTOR(CONFIGURATION) → configuration descriptor + interface + endpoint + hub class descriptor
GET_DESCRIPTOR(HUB_CLASS, type=0x29) → hub class-specific descriptor（bDescLength, bNbrPorts, wHubCharacteristics…）
```

## Device Descriptor Hub-Specific 欄位

（詳見 `specs/hub_device_class.md`）

| 欄位 | Hub 規範值 |
|---|---|
| `bDeviceClass` | `0x09` |
| `bDeviceSubClass` | `0x00` |
| `bDeviceProtocol` | `0x00`/`0x01`/`0x02` |

## Configuration Descriptor 典型欄位

USB 2.0 hub 通常呈現 1 個 configuration：

| 欄位 | 典型值 | 說明 |
|---|---|---|
| `bNumConfigurations` | `1` | hub 通常只有一個 configuration |
| `bConfigurationValue` | `1` | host 以 `SET_CONFIGURATION(1)` 選取 |
| `bNumInterfaces` | `1` | hub class 只需一個 interface |
| `bmAttributes` | 依設計而定 | 是否支援 remote wakeup（bit 5）、是否 bus-powered（bit 6） |
| `bMaxPower` | 依設計而定 | hub 從 VBUS 取用的最大電流（以 2 mA 為單位） |

> 以上為典型值，不是 spec 強制值。消費 hub 的 firmware 應通過實際 GET_DESCRIPTOR 讀取確認。

## Interface Descriptor Hub Class 欄位

Hub 使用單一 interface，interface descriptor 的 class code 欄位：

| 欄位 | 值 | 說明 |
|---|---|---|
| `bInterfaceClass` | `0x09` | Hub class（與 device descriptor bDeviceClass 相同） |
| `bInterfaceSubClass` | `0x00` | USB 2.0 未定義 hub interface subclass |
| `bInterfaceProtocol` | `0x00` | Interface level 的 protocol（通常為 0；TT 能力由 device descriptor 的 bDeviceProtocol 表達） |
| `bNumEndpoints` | `1` | Hub class interface 通常只有 1 個 endpoint（interrupt IN） |

## Hub Endpoints 概述

Hub class interface 包含：

1. **Endpoint 0（Control）**：隱式存在，用於所有 hub class requests（GET_STATUS、SET_FEATURE 等）。
2. **Interrupt IN endpoint**：status change endpoint，用於通知 host port/hub 狀態變化。詳見 `specs/hub_interrupt_endpoint.md`。

Hub 不需要 Bulk 或 Isochronous endpoints。

## GET_DESCRIPTOR 請求與 Hub Class Descriptor

Host 以 `GET_DESCRIPTOR` 請求取得 hub class-specific descriptor：

| 欄位 | 值 |
|---|---|
| `bmRequestType` | `0xA0`（device→host, class, device recipient） |
| `bRequest` | `GET_DESCRIPTOR`（class-specific，bRequest=6） |
| `wValue` | `0x2900`（descriptor type=0x29, index=0） |
| `wLength` | hub descriptor 長度（至少 7 bytes，依 port 數而定） |

詳細欄位見 `specs/hub_descriptor.md`。

## Multi-TT Hub 的 Alternate Setting

HS multi-TT hub（`bDeviceProtocol = 0x02`）可能透過 alternate interface setting 支援 single-TT 與 multi-TT 兩種模式：

- `SET_INTERFACE(alternateSetting=0)` → single-TT 模式（所有 port 共用一個 TT）
- `SET_INTERFACE(alternateSetting=1)` → multi-TT 模式（每個 port 有獨立 TT）

Host 在枚舉後依需要選擇 alternate setting。

## Governed Linkage

- `specs/hub_device_class.md`：bDeviceClass/SubClass/Protocol 的詳細說明
- `specs/hub_descriptor.md`：hub class-specific descriptor 欄位（§11.23.2.1）
- `specs/hub_interrupt_endpoint.md`：interrupt IN endpoint descriptor 欄位
- `specs/transaction_translator.md`：multi-TT 與 single-TT hub 行為

## Non-claims

- 本頁不是任何特定 hub 的 descriptor dump 驗證。
- 本頁不宣告 `bMaxPower`、`bmAttributes` 等廠商相關欄位的正確值。
- 本頁不覆蓋 consuming repo 已確認的 project facts。
