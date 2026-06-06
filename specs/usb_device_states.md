---
title: USB Device States
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# USB Device States

> 來源範圍：USB 2.0 Specification Rev 2.0，§9.1。  
> 本頁說明 USB 設備層級狀態（Chapter 9）。這些狀態與 hub port 狀態（Chapter 11，見 `specs/port_state_machine.md`）是不同的概念。

## 頁面目的

本頁回答：

- USB device framework 層級（§9.1）定義哪些 USB 設備狀態。
- USB 2.0 hub 在枚舉過程中如何轉換這些狀態。

本頁不回答：

- Hub port 狀態 —— 請見 `specs/port_state_machine.md`。
- State transition 時序或錯誤恢復。

## USB 設備狀態

USB 2.0 §9.1 定義以下設備狀態：

| 狀態 | 說明 |
|---|---|
| **Attached** | 設備已實體連接；VBUS 可能尚未施加 |
| **Powered** | VBUS 存在；設備尚未被 reset |
| **Default** | 設備已接收 USB reset；以位址 0 回應；尚未指定位址 |
| **Address** | Host 已發出 `SET_ADDRESS`；設備取得唯一 bus 位址 |
| **Configured** | Host 已發出 `SET_CONFIGURATION`；所有 interface endpoints 已啟動 |
| **Suspended** | 超過 3ms 無 bus activity；設備進入低功耗狀態 |

## State Transition

```
Attached ──VBUS 施加──> Powered
Powered ──USB reset 接收──> Default
Default ──SET_ADDRESS(n)──> Address
Address ──SET_CONFIGURATION(1)──> Configured
Configured ──無 bus activity >3ms──> Suspended
Suspended ──resume 信號 / SOF 接收──> Configured（或 Address，若未 configured）
任意狀態 ──USB reset 接收──> Default
```

## State Transition 表

| 起始狀態 | 觸發條件 | 目標狀態 |
|---|---|---|
| Attached | VBUS 施加（hub/root port 上電）| Powered |
| Powered | USB reset 接收（SE0 ≥10ms）| Default |
| Default | `SET_ADDRESS(n)` | Address |
| Address | `SET_CONFIGURATION(bConfigurationValue)` | Configured |
| Configured | 無 bus activity >3ms | Suspended |
| Suspended | Resume 信號接收 | Configured |
| 任意（非 Attached）| USB reset 接收 | Default |
| 任意（非 Attached）| VBUS 移除 | Attached |

## 各狀態下可用的請求

不是所有請求在所有狀態下都有效：

| 請求 | Default | Address | Configured |
|---|---|---|---|
| `SET_ADDRESS` | ✓ | ✓ | — |
| `GET_DESCRIPTOR` | ✓ | ✓ | ✓ |
| `SET_CONFIGURATION` | — | ✓ | ✓ |
| `GET_CONFIGURATION` | — | ✓ | ✓ |
| Hub class requests | — | — | ✓（僅在 configured 後）|

> Hub class requests（GET_STATUS port、SET_FEATURE port、TT requests）只有在 `SET_CONFIGURATION` 之後才有效。

## 設備狀態 vs. Port 狀態的比較

| 面向 | USB 設備狀態（§9.1）| Hub Port 狀態（§11.5）|
|---|---|---|
| 主體 | Hub 設備本身 | Hub 上的下行 port |
| 狀態 | Attached、Powered、Default、Address、Configured、Suspended | Powered-off、Disconnected、Disabled、Enabled、Suspended、Resetting、Port Error |
| 觸發者 | 標準請求（`SET_ADDRESS`、`SET_CONFIGURATION`）| Hub class 請求（`SET_FEATURE PORT_RESET`、`SET_FEATURE PORT_POWER`）|
| 狀態讀取 | 標準 `GET_STATUS`（device，2 bytes）| Hub class `GET_STATUS`（port，4 bytes）|

Hub 同時是一個 **USB device**（擁有 §9.1 設備狀態）和一個 **hub**（擁有 §11.5 的下行 port 狀態）。

## Governed Linkage

- `specs/port_state_machine.md`：Hub port 狀態（§11.5）—— 與設備狀態不同
- `specs/hub_enumeration.md`：顯示 Default → Address → Configured 轉換的枚舉 sequence
- `specs/standard_device_requests.md`：`SET_ADDRESS`、`SET_CONFIGURATION` 請求
- `specs/hub_power_management.md`：Suspended 狀態與 remote wakeup

## Non-claims

- 本頁不宣告設備 state transition 已針對實體 hub 驗證。
- 本頁不建立 reset 後的完整恢復行為。
- 本頁不覆蓋 consuming repo 已確認的 project facts。
