---
title: SS Standard Device Requests
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

# SS Standard Device Requests

> 資料範圍：USB 3.2 Specification Rev 1.0，Section 9.4（Standard Device Requests）。
> 本頁是消費端參考摘要，不是請求行為驗證紀錄。

## 頁面目的

本頁回答：

- USB 3.x SS hub 適用的 standard device requests 有哪些。
- 哪些請求與 USB 2.0 相同，哪些是 USB 3.x 新增或修改。
- LPM（U1/U2）相關的 standard request feature selectors。

本頁不回答：

- 每個請求的 firmware 實作是否正確。
- xHCI 如何驅動這些請求。

## USB 3.x SS Hub 適用的 Standard Device Requests

大部分 USB 2.0 standard device requests 在 USB 3.x 中保持相同（USB 3.2 Section 9.4）：

| 請求 | bmRequestType | bRequest | 適用說明 |
|---|---|---|---|
| GET_STATUS | 0x80/0x81/0x82 | 0x00 | 裝置/介面/端點狀態 |
| CLEAR_FEATURE | 0x00/0x01/0x02 | 0x01 | 清除 feature selector |
| SET_FEATURE | 0x00/0x01/0x02 | 0x03 | 設定 feature selector |
| SET_ADDRESS | 0x00 | 0x05 | 指定 USB address |
| GET_DESCRIPTOR | 0x80 | 0x06 | 讀取描述符 |
| SET_DESCRIPTOR | 0x00 | 0x07 | 寫入描述符（optional） |
| GET_CONFIGURATION | 0x80 | 0x08 | 讀取目前 configuration |
| SET_CONFIGURATION | 0x00 | 0x09 | 設定 configuration |
| GET_INTERFACE | 0x81 | 0x0A | 讀取 interface alternate setting |
| SET_INTERFACE | 0x01 | 0x0B | 設定 interface alternate setting |

## USB 3.x 新增的 Standard Feature Selectors

USB 3.x 在 SET_FEATURE / CLEAR_FEATURE 中新增 LPM 相關的 standard device feature selectors：

| Feature selector | 值 | Recipient | 說明 |
|---|---|---|---|
| U1_ENABLE | 48 (0x30) | Device | 允許裝置主動發起 U1 進入請求 |
| U2_ENABLE | 49 (0x31) | Device | 允許裝置主動發起 U2 進入請求 |
| LTM_ENABLE | 50 (0x32) | Device | 啟用 Latency Tolerance Messaging (LTM) |

> 注意：以上是 **standard device feature selectors**，與 SS hub port feature selectors（PORT_U1_ENABLE 等）不同。Hub port feature selectors 作用於 hub class request，standard device feature selectors 作用於 device 本身。

## GET_DESCRIPTOR（USB 3.x 新增的描述符類型）

USB 3.x 新增以下描述符類型：

| bDescriptorType | 名稱 | 說明 |
|---|---|---|
| 0x0F | BOS (Binary Device Object Store) | 裝置能力的容器描述符 |
| 0x10 | Device Capability | BOS 內的裝置能力描述符 |
| 0x2A | SuperSpeed Hub Descriptor | SS hub 專用描述符（見 ss_hub_descriptor.md） |

## 本頁不宣告

- 每個請求的 firmware 實作正確性。
- xHCI 驅動 standard requests 的內部機制。
- LTM、U1/U2 device feature selector 的語意或行為。
- USB-IF 認證合規性。

→ [SS Hub Class Requests](ss_hub_class_requests.md) | [SS Hub Descriptor](ss_hub_descriptor.md) | [Verification Status](../verification_status.md)
