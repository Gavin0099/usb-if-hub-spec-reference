---
title: SS Port 指示燈
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

# SS Port 指示燈

> 來源範圍：USB 3.2 Specification Rev 1.0，§10.14.2（wHubCharacteristics bit[5]）。
> 本頁涵蓋 USB 3.x SS hub 選用的 port 指示燈（LED）控制功能。

## 頁面目的

本頁回答：

- USB 3.x SS hub 的 `wHubCharacteristics bit[5]` 如何指示 port 指示燈支援。
- `SET_FEATURE(PORT_INDICATOR)` 在 USB 3.x 中的編碼與 USB 2.0 是否相同。
- USB 3.x 與 USB 2.0 port 指示燈功能的主要差異。

本頁不回答：

- 特定 hub 實作的 LED 硬體行為。
- USB-IF 指示燈合規測試要求。
- Hub 在 automatic 模式下的 LED 顏色邏輯（firmware 定義）。

## Port 指示燈支援旗標

USB 3.x SS hub 的 `wHubCharacteristics bit[5]` 指示 port 指示燈支援：

| `wHubCharacteristics bit[5]` | 含義 |
|---|---|
| `0` | Port 指示燈**不支援** |
| `1` | Port 指示燈支援；host 可使用 `SET_FEATURE(PORT_INDICATOR)` |

> **與 USB 2.0 的差異**：USB 2.0 hub 的 port 指示燈旗標在 `wHubCharacteristics bit[7]`；USB 3.x 移至 **bit[5]**（因 TT Think Time bits 不再存在，位元佈局改變）。

`wHubCharacteristics bit[5]` 的編碼 identity 已透過 `usb3_ss_whc_port_indicators` evidence packet 驗證（位元名稱和值 identity only）。

## SET_FEATURE(PORT_INDICATOR) 請求編碼

若 `wHubCharacteristics bit[5] = 1`，host 可使用以下請求控制 port LED：

```
bmRequestType: 0x23  (Host→Device, Class, Other recipient)
bRequest:      0x03  (SET_FEATURE)
wValue:        PORT_INDICATOR selector 值（0–3，見下表）
wIndex:        port_number（1-based）
wLength:       0
```

LED 狀態編碼（與 USB 2.0 相同）：

| Selector 值 | LED 狀態 | 含義 |
|---|---|---|
| `0` | Automatic | Hub 控制 LED（預設行為）|
| `1` | Amber | Host 強制顯示琥珀色 |
| `2` | Green | Host 強制顯示綠色 |
| `3` | Off | Host 關閉 LED |

## wHubCharacteristics 位元佈局差異

| 位元 | USB 2.0 wHubCharacteristics | USB 3.x wHubCharacteristics |
|---|---|---|
| bit[1:0] | Logical Power Switching Mode | Logical Power Switching Mode（相同）|
| bit[2] | Compound Device | Compound Device（相同）|
| bit[4:3] | Over-Current Protection Mode | Over-Current Protection Mode（相同）|
| bit[6:5] | **TT Think Time**（USB 2.0 only）| **保留**（USB 3.x 無 TT）|
| bit[7] | **Port Indicators**（USB 2.0）| **保留** |
| bit[5] | （TT Think Time 的一部分）| **Port Indicators**（USB 3.x）|
| bit[15:8] | 保留 | —— |
| bit[15:6] | —— | 保留（USB 3.x）|

Port Indicators 在 USB 3.x 中從 bit[7] 移至 bit[5]，是因為 bit[6:5] 的 TT Think Time 欄位在 USB 3.x 中不再存在。

## Governed Linkage

- `tables/ss_hub_characteristics_bit_matrix.yaml`：`usb3_ss_whc_port_indicators`（bit[5]）—— verified
- `specs/usb3/ss_hub_characteristics.md`：wHubCharacteristics 完整位元說明
- `specs/usb3/ss_feature_selectors.md`：SS hub feature selector 完整列表
- `specs/usb3/ss_hub_class_requests.md`：SET_FEATURE 請求結構

## Non-claims

- 本頁不宣告任何特定 SS hub 實作的 port 指示燈 LED 顏色行為已驗證。
- 本頁不宣告 automatic 模式下 LED 顏色邏輯的 firmware 正確性。
- 本頁不宣告 PORT_INDICATOR feature selector 的 runtime request 行為已驗證。
- 本頁不覆蓋 consuming repo 已確認的 project facts。

→ [SS Hub Characteristics](ss_hub_characteristics.md) | [SS Feature Selectors](ss_feature_selectors.md) | [Verification Status](../verification_status.md)
