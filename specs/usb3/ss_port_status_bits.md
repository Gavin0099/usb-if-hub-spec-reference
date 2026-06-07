---
title: SS Port Status Bits
claim_level: inferred
spec_family: usb3
status: review_required
last_reviewed: "2026-06-07"
usb_versions:
  - usb_3_2
source_refs:
  - usb32_spec
semantic_verification_claimed: false
---

# SS Port Status Bits

> 資料範圍：USB 3.2 Specification Rev 1.0，Section 10.14.2.6（GET_STATUS for SS hub port）。  
> 本頁是消費端參考摘要，不是逐位元 PDF 驗證紀錄。

## 頁面目的

本頁回答：

- `wPortStatus` / `wPortChange` 在 USB 3.x SS hub 下的完整位元定義。
- `PORT_LINK_STATE`（bits[8:5]）的 link state 編碼表。
- `PORT_SPEED`（bits[12:10]）的速度編碼表。
- 與 USB 2.0 port status bits 的關鍵差異。

本頁不回答：

- LTSSM（Link Training and Status State Machine）完整轉換行為。
- 各 link state 的 timing 或電氣特性。

## GET_STATUS 回應格式

GET_STATUS（wValue=0x0000，wIndex=port number）回傳 4 bytes：

```
Bytes 0-1: wPortStatus  (16-bit)
Bytes 2-3: wPortChange  (16-bit)
```

## wPortStatus 位元定義

| 位元 | 欄位 | 說明 |
|---|---|---|
| bit[0] | PORT_CONNECTION | 目前是否有裝置連接 |
| bit[1] | PORT_ENABLE | 端口是否啟用；SS 裝置連接時恆為 1 |
| bit[2] | PORT_OVER_CURRENT | 端口過電流狀態 |
| bit[3] | PORT_RESET | 端口正在進行 reset signaling |
| bits[8:5] | PORT_LINK_STATE | Link 目前狀態（見 Link State 編碼表） |
| bit[9] | PORT_POWER | 端口電源狀態（0=off, 1=on） |
| bits[12:10] | PORT_SPEED | 目前連接速度（見 Speed 編碼表） |
| bit[13] | PORT_U1_ENABLE | U1 entry 是否啟用 |
| bit[14] | PORT_U2_ENABLE | U2 entry 是否啟用 |
| bit[15] | Reserved | 必須為 0 |

### PORT_LINK_STATE 編碼（bits[8:5]）

| 值 | Link State | 說明 |
|---|---|---|
| 0 | U0 | 正常工作狀態（active） |
| 1 | U1 | 低功耗待機，host 觸發，exit latency < 10μs |
| 2 | U2 | 更低功耗，host 或 device 觸發，exit latency < 2ms |
| 3 | U3 | Suspended（類似 USB 2.0 SUSPEND） |
| 4 | SS.Disabled | 端口已禁用 |
| 5 | Rx.Detect | 偵測接收器存在（連接偵測階段） |
| 6 | SS.Inactive | 鏈路錯誤後非活躍狀態 |
| 7 | Polling | 正在進行 link training |
| 8 | Recovery | 從低功耗或錯誤狀態恢復 |
| 9 | Hot Reset | 正在進行 hot reset（Warm Reset） |
| 10 | Compliance Mode | 電氣一致性測試模式 |
| 11 | Loopback | Loopback 測試模式 |
| 12–15 | Reserved | — |

### PORT_SPEED 編碼（bits[12:10]）

| 值 | 速度 | 說明 |
|---|---|---|
| 0 | — | 未定義 |
| 1 | Full-speed | 12 Mbps |
| 2 | Low-speed | 1.5 Mbps |
| 3 | High-speed | 480 Mbps |
| 4 | SuperSpeed | 5 Gbps（USB 3.2 Gen 1） |
| 5 | SuperSpeed+ | 10 Gbps（USB 3.2 Gen 2） |
| 6–7 | Reserved | — |

## wPortChange 位元定義

| 位元 | 欄位 | 說明 |
|---|---|---|
| bit[0] | C_PORT_CONNECTION | 連接狀態改變 |
| bit[1] | Reserved | 恆為 0（SS 中 PORT_ENABLE 不產生 change event） |
| bit[2] | C_PORT_OVER_CURRENT | 過電流狀態改變 |
| bit[3] | C_PORT_RESET | 標準 reset 完成 |
| bit[4] | C_BH_PORT_RESET | Warm Reset（BH Port Reset）完成 |
| bit[5] | C_PORT_LINK_STATE | Link state 改變 |
| bit[6] | C_PORT_CONFIG_ERROR | 配置錯誤發生（SS 裝置配置失敗） |
| bits[15:7] | Reserved | 必須為 0 |

## 與 USB 2.0 port status bits 的差異

| 差異點 | USB 2.0 | USB 3.x / SuperSpeed |
|---|---|---|
| PORT_SUSPEND（bit[2]） | 有 | **無**（suspend 由 U1/U2/U3 link states 取代） |
| PORT_LOW_SPEED / PORT_HIGH_SPEED | 有（bit[9]/bit[10]） | **無**（合併為 PORT_SPEED 3-bit field） |
| PORT_TEST / PORT_INDICATOR | 有（bit[11]/bit[12]） | **無**（SS 測試模式另有機制） |
| PORT_LINK_STATE | 無 | **新增**：bits[8:5]，4-bit link state |
| PORT_SPEED | 無 | **新增**：bits[12:10]，3-bit 速度場 |
| PORT_U1_ENABLE / PORT_U2_ENABLE | 無 | **新增**：bit[13]/bit[14] |
| C_BH_PORT_RESET | 無 | **新增**：bit[4]，warm reset 完成 |
| C_PORT_LINK_STATE | 無 | **新增**：bit[5] |
| C_PORT_CONFIG_ERROR | 無 | **新增**：bit[6] |

## Non-claims

- 不宣告此頁的位元定義已逐位元對照 USB 3.2 PDF 驗證。
- 不宣告 LTSSM 完整狀態轉換行為（U1→U0 exit sequence 等）。
- 不宣告各 link state 的電氣或 timing 合規。
