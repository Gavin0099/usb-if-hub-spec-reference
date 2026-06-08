---
title: SS Hub Enumeration
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

# SS Hub Enumeration

> 資料範圍：USB 3.2 Specification Rev 1.0，Section 10.14 / 10.14.2。
> 本頁是消費端參考摘要，不是 enumeration runtime behavior 驗證紀錄。

## 頁面目的

本頁回答：

- USB 3.x SS hub 枚舉（enumeration）序列中的關鍵步驟。
- `SET_HUB_DEPTH` 請求的用途與必要性。
- SS hub 枚舉與 USB 2.0 hub 枚舉的主要差異。

本頁不回答：

- xHCI host controller 如何實作 SS hub enumeration 的內部機制。
- firmware enumeration 邏輯是否符合規格。
- USB-IF 認證程序或測試規範。

## SS Hub Enumeration 序列（簡述）

1. **Reset + Speed Detection**：Host 對 port 發出 bus reset；link training 決定 SuperSpeed 或 fallback。
2. **GET_DESCRIPTOR(DeviceDescriptor)**：取得裝置描述符，確認 bDeviceClass=0x09（Hub）。
3. **SET_ADDRESS**：指定 USB address。
4. **GET_DESCRIPTOR(HubDescriptor)**：取得 SS Hub Descriptor（USB 3.x 專用 type bDescriptorType=0x2A）。
5. **SET_HUB_DEPTH**（SS hub 必要步驟）：通知 hub 其在 bus topology 中的層次深度。
6. **SET_CONFIGURATION**：啟用 configuration。
7. **Port power on**：依 wHubCharacteristics 選擇 ganged 或 per-port power on。
8. **Wait bPwrOn2PwrGood × 2 ms**：等待 port 電源穩定。

> **Step 5 (SET_HUB_DEPTH) 是 USB 3.x SS hub 特有的必要步驟**；USB 2.0 hub 不需要此請求。

## SET_HUB_DEPTH 請求

| 欄位 | 值 |
|---|---|
| bmRequestType | 0x20（Class, Device, host-to-device） |
| bRequest | 0x0C |
| wValue | Hub depth（0=root hub 或直接連接 root hub；最大值 5） |
| wIndex | 0 |
| wLength | 0 |

- Root hub 或直接連接 root hub 的 SS hub：depth = 0。
- 每多一層 hub：depth +1，最大 depth = 5。
- xHCI 必須在完成 hub 配置前發送此請求。

## USB 3.x 枚舉與 USB 2.0 枚舉的主要差異

| 特性 | USB 2.0 Hub | USB 3.x SS Hub |
|---|---|---|
| Hub Descriptor type | 0x29 | **0x2A**（SS-specific） |
| SET_HUB_DEPTH | 不需要 | **必要（mandatory）** |
| Transaction Translator (TT) | 有（HS hub） | **無** |
| TT-related requests（CLEAR_TT_BUFFER 等）| 有 | **不支援** |
| U1/U2 feature selectors | 無 | **有（6 個）** |
| bInterval 編碼 | 依速度不同（FS ms, HS microframe） | **microframe（同 HS USB 2.0）** |

## SS Hub Descriptor Type

USB 3.x SS hub 使用 **SuperSpeed Hub Descriptor**（bDescriptorType=0x2A），欄位與 USB 2.0 Hub Descriptor（0x29）不同。詳見 [SS Hub Descriptor](ss_hub_descriptor.md)。

## 本頁不宣告

- xHCI host controller 內部 SS hub enumeration 實作。
- firmware enumeration 行為的正確性。
- Link training 或 LTSSM negotiation behavior。
- USB-IF 認證程序或測試合規性。

→ [SS Hub Descriptor](ss_hub_descriptor.md) | [SS Hub Class Requests](ss_hub_class_requests.md) | [Verification Status](../verification_status.md)
