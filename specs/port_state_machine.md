---
title: Port State Machine
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Port State Machine

> 來源範圍：USB 2.0 Specification Rev 2.0，§11.5。  
> 本頁是 USB 2.0 hub port state machine 的 reviewed reference summary；不是完整 state-transition 行為驗證或 firmware 實作真值。

## 頁面目的

本頁回答：

- USB 2.0 hub port 的 7 個標準狀態是什麼。
- 哪些事件或請求會觸發 state transition。
- `wPortStatus` bits 的狀態值與 port state 的對應關係。

本頁不回答：

- 每個 state transition 的完整時序保證。
- Firmware 實作錯誤的恢復流程。
- `PORT_RESET` 完成後的設備枚舉流程。

## Port 的 7 個標準狀態

USB 2.0 hub port 有以下 7 個規範狀態（§11.5）：

| 狀態 | 說明 |
|---|---|
| **Powered-off** | Port 未上電；`wPortStatus.PORT_POWER = 0` |
| **Disconnected** | Port 已上電，但無設備連接；`PORT_CONNECTION = 0` |
| **Disabled** | 設備已連接但 port 未 enabled；`PORT_ENABLE = 0` |
| **Enabled** | Port 已 enabled，設備可以通訊；`PORT_ENABLE = 1` |
| **Suspended** | Port 處於 suspend 狀態；`PORT_SUSPEND = 1` |
| **Resetting** | Port 正在 reset；`PORT_RESET = 1` |
| **Port Error** | Hub 偵測到 port 錯誤，port 已被 disabled |

## State Transition 概覽

```
Powered-off ──SET_FEATURE(PORT_POWER)──> Disconnected
Disconnected ──設備連接（硬體事件）──> Disabled
Disabled ──SET_FEATURE(PORT_RESET) + reset 完成──> Enabled
Enabled ──SET_FEATURE(PORT_SUSPEND)──> Suspended
Suspended ──CLEAR_FEATURE(PORT_SUSPEND) 或設備 wakeup──> Enabled
Enabled ──設備斷開 或 port 錯誤──> Disabled
Enabled ──CLEAR_FEATURE(PORT_ENABLE)──> Disabled
Disconnected ──CLEAR_FEATURE(PORT_POWER)──> Powered-off
任意狀態 ──硬體過電流或錯誤──> Disabled / Port Error
```

## 主要 State Transition 表

| 起始狀態 | 觸發條件 | 目標狀態 |
|---|---|---|
| Powered-off | `SET_FEATURE(PORT_POWER)` | Disconnected |
| Disconnected | 設備連接（硬體事件） | Disabled |
| Disabled | `SET_FEATURE(PORT_RESET)` | Resetting |
| Resetting | Reset 完成（硬體） | Enabled（若設備成功 reset） |
| Enabled | `SET_FEATURE(PORT_SUSPEND)` | Suspended |
| Suspended | `CLEAR_FEATURE(PORT_SUSPEND)` 或設備 wakeup | Enabled |
| Enabled | `CLEAR_FEATURE(PORT_ENABLE)` | Disabled |
| Enabled | 設備斷開（硬體事件） | Disconnected |
| 任意（上電）| 過電流偵測 | Disabled / Port Error |
| 任意（上電） | `CLEAR_FEATURE(PORT_POWER)` | Powered-off |

## `wPortStatus` Bits 與 Port State 的對應

| `wPortStatus` bit | 名稱 | State 中為 `1` 的狀態 |
|---:|---|---|
| 0 | `PORT_CONNECTION` | Disabled、Enabled、Suspended、Resetting |
| 1 | `PORT_ENABLE` | Enabled、Suspended |
| 2 | `PORT_SUSPEND` | Suspended |
| 3 | `PORT_OVER_CURRENT` | 過電流偵測時 |
| 4 | `PORT_RESET` | Resetting |
| 8 | `PORT_POWER` | Disconnected 及以上（已上電） |

> 注意：上表是狀態對應的概述，不是逐 bit 的語意真值表。完整的 bit 定義見 `specs/port_status_bits.md`。

## 解讀邊界

- 本頁呈現的 state machine 是規範摘要，不是用於 firmware 正確性驗證的完整 state chart。
- State transition 可能受 hub 實作細節影響（例如：Resetting → Enabled 的時序）。
- `PORT_RESET` 完成到 `Enabled` 的路徑取決於設備是否正確回應 reset；設備不回應時 port 應維持在 Disabled。

## Governed Linkage

- `specs/port_status_bits.md`：wPortStatus / wPortChange bits 的詳細定義
- `specs/feature_selectors.md`：`PORT_RESET`、`PORT_ENABLE`、`PORT_SUSPEND`、`PORT_POWER` 等 selector 值
- `specs/hub_class_requests.md`：`SET_FEATURE` 與 `CLEAR_FEATURE` request family
- `specs/escalation_table.md`：port state 相關的 escalation triggers

## Non-claims

- 本頁不宣告任何 hub 的 port state machine 實作已驗證。
- 本頁不宣告 state transition 時序或設備回應的完整規格。
- 本頁不覆蓋 consuming repo 已確認的 project facts。
