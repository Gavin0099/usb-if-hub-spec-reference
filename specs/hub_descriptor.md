---
title: Hub 描述符
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub 描述符

> 來源範圍：USB 2.0 Specification Rev 2.0，第 11.23.2.1 節。
> 本頁目前是人工整理摘要，尚未完成逐欄位 PDF 驗證，因此仍維持 `inferred`。

## Descriptor 主要欄位

Hub descriptor 由 class-specific `GET_DESCRIPTOR` 取得，descriptor type 為 `0x29`。

| Offset | 欄位 | 大小 | 說明 |
|---|---|---|---|
| 0 | `bDescLength` | 1 | Descriptor 總長度 |
| 1 | `bDescriptorType` | 1 | Hub descriptor type，預期為 `0x29` |
| 2 | `bNbrPorts` | 1 | Hub 報告的 downstream port 數量 |
| 3 | `wHubCharacteristics` | 2 | Hub 特性位元欄位 |
| 5 | `bPwrOn2PwrGood` | 1 | Power-on 到 power-good 的延遲，單位為 2 ms |
| 6 | `bHubContrCurrent` | 1 | Hub controller 所需電流，單位為 mA |
| 7 | `DeviceRemovable` | variable | 各 port 是否 removable 的 bitmap |
| 7+x | `PortPwrCtrlMask` | variable | 保留遮罩，常見為 `0xFF` 模式 |

## `wHubCharacteristics` 摘要

| Bits | 欄位 | 說明 |
|---|---|---|
| 1:0 | Logical Power Switching Mode | Power switching 模式 |
| 2 | Compound Device | 是否為 compound device |
| 4:3 | Over-current Protection Mode | Over-current 保護模式 |
| 6:5 | TT Think Time | Transaction Translator think time |
| 7 | Port Indicators Supported | 是否支援 port indicator |
| 15:8 | Reserved | 保留位元 |

## 升級相關重點

- `bNbrPorts` 若與 firmware 實際暴露的 port 數量不一致，屬於 escalation trigger。
- `wHubCharacteristics[1:0]` 與 `wHubCharacteristics[6:5]` 牽涉 power switching 與 TT 行為，不應在沒有 section-level 驗證下直接當成專案事實覆寫來源。
- consuming repo 若依本頁內容打算更動 descriptor 值，應先確認那是標準語意比較，不是直接替換已確認的專案約束。
