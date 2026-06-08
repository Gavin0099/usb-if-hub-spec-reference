---
title: SS USB 裝置狀態
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

# SS USB 裝置狀態

> 來源範圍：USB 3.2 Specification Rev 1.0，§9.1 / Chapter 10。
> 本頁說明 USB 3.x SuperSpeed hub 的設備層級狀態（§9.1）與 USB 3.x 新增的 link power 狀態（U0–U3）。Hub port 狀態請見 `specs/usb3/ss_port_state_machine.md`。

## 頁面目的

本頁回答：

- USB 3.x SS hub 的設備狀態與 USB 2.0 有何異同。
- U0–U3 link power 狀態如何疊加在設備狀態上。
- SS hub 什麼時候才能接受 hub class 請求。

本頁不回答：

- Hub port 狀態（Disconnected、Enabled、Resetting 等）—— 請見 `specs/usb3/ss_port_state_machine.md`。
- U1/U2 timeout selector 的詳細規則 —— 請見 `specs/usb3/ss_lpm.md`。
- LTSSM 訓練細節或 xHCI 設備狀態管理。

## USB 設備狀態（§9.1，USB 2.0 與 USB 3.x 共用）

USB 3.x 保留與 USB 2.0 相同的設備狀態框架：

| 狀態 | 說明 |
|---|---|
| **Attached** | 設備已實體連接；VBUS 可能尚未施加 |
| **Powered** | VBUS 存在；設備尚未被 reset |
| **Default** | 設備已接收 USB reset；以位址 0 回應；尚未指定位址 |
| **Address** | Host 已發出 `SET_ADDRESS`；設備取得唯一 bus 位址 |
| **Configured** | Host 已發出 `SET_CONFIGURATION`；設備功能完整啟動 |
| **Suspended** | 超過 3ms（SS：超過 2ms）無 bus activity；設備進入低功耗 |

## State Transition

```
Attached ──VBUS 施加──> Powered
Powered ──USB reset 接收──> Default
Default ──SET_ADDRESS(n)──> Address
Address ──SET_CONFIGURATION(1)──> Configured
Configured ──無 SS bus activity >2ms──> Suspended
Suspended ──resume / LFPS 接收──> Configured
任意狀態 ──USB reset 接收──> Default
```

## USB 3.x 新增：U0–U3 Link Power 狀態

USB 3.x 在 Configured 狀態疊加了 **link power 狀態（U0–U3）**：

| 狀態 | 說明 | 對應 USB 2.0 |
|---|---|---|
| **U0** | 鏈路完全活躍（active）| 類似 Active（Resume 後）|
| **U1** | 短暫低功耗鏈路狀態（幾百 μs 退出延遲）| 無直接對應 |
| **U2** | 較深低功耗鏈路狀態（幾 ms 退出延遲）| 無直接對應 |
| **U3** | 鏈路 Suspend（類似 USB 2.0 Suspend）| 類似 Suspended |

U1/U2 是 USB 3.x 特有的鏈路層省電機制；U3 對應設備層的 Suspended 狀態。詳見 `specs/usb3/ss_lpm.md`。

## 各狀態下可用的請求

| 請求 | Default | Address | Configured |
|---|---|---|---|
| `SET_ADDRESS` | ✓ | ✓ | — |
| `GET_DESCRIPTOR` | ✓ | ✓ | ✓ |
| `SET_CONFIGURATION` | — | ✓ | ✓ |
| `GET_CONFIGURATION` | — | ✓ | ✓ |
| `SET_HUB_DEPTH` | — | — | ✓（SS hub 必須在配置後設定）|
| Hub class 請求（GET_STATUS port、SET_FEATURE port）| — | — | ✓ |

**`SET_HUB_DEPTH` 是 USB 3.x SS hub 的必要請求**，在 `SET_CONFIGURATION` 後且在 port 啟用前必須發出。詳見 `specs/usb3/ss_hub_class_requests.md`。

## 設備狀態 vs. Port 狀態 vs. Link 狀態的比較

| 層次 | 概念 | 主要狀態 |
|---|---|---|
| USB 設備層（§9.1）| Hub 設備本身 | Default → Address → Configured → Suspended |
| Hub port 狀態（§10.14.2）| Hub 的下行 port | Disconnected → Enabled → Resetting …等 |
| Link power 狀態（§10.14.2）| SS 鏈路層省電 | U0（active）→ U1 → U2 → U3（suspend）|

這三個層次是獨立但相關的。SS hub 同時管理自己的設備狀態、每個 port 的 port 狀態、以及每個 port 連接設備的 link power 狀態。

## 與 USB 2.0 的差異

| 面向 | USB 2.0 Hub | USB 3.x SS Hub |
|---|---|---|
| 設備狀態框架 | 相同（§9.1）| 相同（§9.1）|
| Suspend 門檻 | 無 bus activity >3ms | 無 SS bus activity >2ms |
| Link power 狀態 | 無 U1/U2 概念 | U0/U1/U2/U3（SET_FEATURE PORT_U1/U2_TIMEOUT）|
| 設備重置觸發者 | SE0 ≥10ms（Warm Reset）| SS reset（Warm Reset 或 Hot Reset）|
| SET_HUB_DEPTH | 不適用 | **必要**（SS hub 唯一新增的必要枚舉步驟）|

## Governed Linkage

- `specs/usb3/ss_port_state_machine.md`：Hub port 狀態機（PORT_LINK_STATE 12 個值）
- `specs/usb3/ss_lpm.md`：U0–U3 link power 狀態與 timeout selector
- `specs/usb3/ss_hub_enumeration.md`：SS hub 枚舉 sequence（含 SET_HUB_DEPTH 步驟）
- `specs/usb3/ss_hub_class_requests.md`：SS hub class 請求（SET_HUB_DEPTH 必要性）

## Non-claims

- 本頁不宣告設備 state transition 已針對實體 SS hub 驗證。
- 本頁不宣告 U1/U2/U3 link power 狀態行為或 exit latency 已驗證。
- 本頁不宣告 LTSSM 訓練行為或 xHCI 設備狀態管理已驗證。
- 本頁不覆蓋 consuming repo 已確認的 project facts。

→ [SS Port State Machine](ss_port_state_machine.md) | [SS LPM](ss_lpm.md) | [Verification Status](../verification_status.md)
