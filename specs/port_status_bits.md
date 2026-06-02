---
title: 連接埠狀態位元
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# 連接埠狀態位元

> 來源範圍：USB 2.0 Specification Rev 2.0，第 11.24.2.7 節。
> 本頁目前是 reference summary，不代表所有 bit 都已完成逐位驗證。

## 狀態欄位概念

- `GET_STATUS` 可回傳 hub 層級的 `wHubStatus` / `wHubChange`，或 port 層級的 `wPortStatus` / `wPortChange`。
- `Status` bits 表示目前狀態；`Change` bits 表示「自上次被清除以來是否發生過變化」。
- 對 change bits 而言，`CLEAR_FEATURE` 的角色不是一般設定命令，而是「清除這個變更紀錄」。

## Hub 層級位元

| 欄位 | Bit | 名稱 | 語意 |
|---|---|---|---|
| `wHubStatus` | 0 | `HUB_LOCAL_POWER` | Hub local power status |
| `wHubStatus` | 1 | `HUB_OVER_CURRENT` | Hub over-current status |
| `wHubChange` | 0 | `C_HUB_LOCAL_POWER` | 記錄 local power 狀態自上次清除後是否發生過變化 |
| `wHubChange` | 1 | `C_HUB_OVER_CURRENT` | 記錄 over-current 狀態自上次清除後是否發生過變化 |

## Port 層級最低必要邊界

| 欄位 | Bit | 名稱 | 狀態 | 說明 |
|---|---|---|---|---|
| `wPortStatus` | 0 | `PORT_CONNECTION` | defined | Port connection status |
| `wPortStatus` | 1 | `PORT_ENABLE` | defined | Port enabled status |
| `wPortStatus` | 15 | `PORT_STATUS_HIGH_BIT_BOUNDARY` | reserved | 16-bit status field boundary placeholder |
| `wPortChange` | 0 | `C_PORT_CONNECTION` | defined | 記錄連接狀態自上次清除後是否發生過變化 |
| `wPortChange` | 1 | `C_PORT_ENABLE` | defined | 記錄 enable 狀態自上次清除後是否發生過變化 |
| `wPortChange` | 15 | `PORT_CHANGE_HIGH_BIT_BOUNDARY` | reserved | 16-bit change field boundary placeholder |

## Change bits 與 `CLEAR_FEATURE`

可以把 `wPortChange` / `wHubChange` 想成「變更事件旗標」：

- bit 被設為 `1`：代表自上次清除以來，該狀態至少變動過一次
- bit 維持 `0`：代表自上次清除以來，沒有觀測到該類變化
- 使用對應的 `CLEAR_FEATURE`：清掉這個 change bit，表示 host 已讀取並處理過這個事件

常見理解方式：

- `C_PORT_CONNECTION = 1`：代表連接狀態自上次清除後發生過變化
- host 讀完 `GET_STATUS` 後，可對該 port 發 `CLEAR_FEATURE(C_PORT_CONNECTION)` 清除此事件紀錄
- 清除後若再次發生變化，bit 會再被設為 `1`

## 速度位元需要組合判讀

`PORT_LOW_SPEED` 與 `PORT_HIGH_SPEED` 不能各自獨立解讀，必須一起看：

| `PORT_LOW_SPEED` | `PORT_HIGH_SPEED` | 解讀 |
|---|---|---|
| 0 | 0 | Full-speed |
| 1 | 0 | Low-speed |
| 0 | 1 | High-speed |
| 1 | 1 | 保留 / 非預期組合 |

因此像「`PORT_LOW_SPEED = 0` 表示全速」這種寫法本身不完整；只有在 `PORT_HIGH_SPEED` 也為 `0` 時，才能解讀成 full-speed。

## 使用注意

- 這份頁面不是完整 bit encyclopedia，而是目前已進入 machine-readable layer 的必要子集。
- `PORT_OVER_CURRENT`、`PORT_RESET`、`PORT_POWER`、速度指示 bit 等語意若要作為強依據，仍應回到後續 PDF 驗證計畫。
- `Reserved` bit 不應被 firmware 任意拿來承載專案私有語意；若已使用，屬於 escalation trigger。
