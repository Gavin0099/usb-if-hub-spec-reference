---
title: Hub Compound Device
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Compound Device

> 來源範圍：USB 2.0 Specification Rev 2.0，§11.12 和 §11.23.2。  
> 本頁是 USB 2.0 hub compound device 識別、`DeviceRemovable` 處理與 `PortPwrCtrlMask` 語意的 reviewed reference summary；不是 compound device 合規驗證紀錄。

## 頁面目的

本頁回答：

- USB 2.0 hub 語境下 compound device 的定義。
- `wHubCharacteristics bit 2` 與 `DeviceRemovable` 欄位的含義。
- USB 2.0 中 `PortPwrCtrlMask` 應如何解讀。

本頁不回答：

- Compound device hub firmware 的完整實作規則。
- 特定設備組合是否符合 compound device 要求。

## Compound Device 定義

**Compound device**（複合設備）是一種包含內嵌 hub 及一個或多個永久連接下行設備的 USB 設備。Hub 與這些連接設備共用同一個外殼，使用者無法個別拆除。

Hub class descriptor 中的 `wHubCharacteristics bit 2` 指示 compound device 狀態：

| Bit 2 | 含義 |
|---|---|
| `0` | Hub **不是** compound device；所有下行 port 皆可獨立插拔 |
| `1` | Hub **是** compound device 的一部分；部分 port 可能連接不可移除設備 |

## `DeviceRemovable` Bitmap

Hub class descriptor 包含一個可變長度的 `DeviceRemovable` bitmap，每個 port 佔一個 bit：

| Bit 索引 | 指派 |
|---|---|
| Bit 0 | 保留；必須為 0 |
| Bit N（N = 1 到 bNbrPorts）| Port N 可移除性指示 |

Bit 編碼：

| Bit N 值 | 含義 |
|---|---|
| `0` | Port N 連接的設備可由使用者移除（標準行為） |
| `1` | Port N 連接的設備**不可**由使用者移除；是 compound unit 的固定組成部分 |

`DeviceRemovable` 欄位在 hub class descriptor 中緊接著 `PortPwrCtrlMask`。兩個欄位長度可變，皆向上取整為完整 byte。

## `PortPwrCtrlMask`

`PortPwrCtrlMask` 是從 USB 1.x 繼承下來的遺留 bitmap。在 USB 1.x 中，它指示哪些 port 可以獨立控制電源。在 **USB 2.0 中所有 bit 必須設為 `0xFF`**（全 1）。此欄位在 USB 2.0 中不攜帶任何可操作的 port 電源控制資訊，不應用於電源切換決策。

## Host 對不可移除 Port 的處理

當 `DeviceRemovable bit N = 1`（port N 不可移除）：

- Host 不應將連接設備呈現為可使用者移除（例如不出現「安全移除硬體」選項）。
- 不可移除 port 在正常操作下若出現 `C_PORT_CONNECTION` 變化事件，可能代表硬體故障而非使用者主動拔除。
- Host 通常跳過不可移除設備的使用者通知流程。

當 `wHubCharacteristics bit 2 = 1`（compound device）：

- Hub 與其不可移除的下行設備作為單一邏輯單元運作。
- Hub 的電源狀態轉換會影響整個 compound unit。

## `wHubCharacteristics` Bit 配置關係

`wHubCharacteristics` 包含多個 hub 層級的配置欄位，bit 2 是 compound device 指示：

| Bits | 欄位 | 參考 |
|---|---|---|
| `[1:0]` | 邏輯電源切換模式 | `specs/hub_power_management.md` |
| `[2]` | Compound Device 指示 | 本頁 |
| `[4:3]` | 過電流保護模式 | `specs/hub_power_management.md` |
| `[6:5]` | TT Think Time | `specs/transaction_translator.md` |
| `[7]` | Port 指示燈支援 | `specs/hub_descriptor.md` |
| `[15:8]` | 保留 | 必須為零 |

## Governed Linkage

- `specs/hub_descriptor.md`：完整 hub class descriptor 配置，包含 `DeviceRemovable`、`PortPwrCtrlMask`、`wHubCharacteristics`
- `specs/hub_power_management.md`：`wHubCharacteristics` 中的電源切換與過電流欄位
- `specs/hub_enumeration.md`：hub 枚舉 sequence 及初始化時如何讀取 `DeviceRemovable`
- `specs/port_state_machine.md`：port 連接與斷開的 state transition

## Non-claims

- 本頁不宣告任何特定 hub 的 compound device 行為已驗證。
- 本頁不覆蓋 `specs/hub_descriptor.md` 中的 hub descriptor 欄位定義。
- 本頁不宣告 `PortPwrCtrlMask` 在 USB 2.0 中攜帶可操作資訊。
- 本頁不覆蓋 consuming repo 已確認的 project facts。

## Reference Navigation

- specs/usb2.md: USB 2.0 topic index (zh).
- specs/en/hub_compound_device.md: English counterpart topic (en).
