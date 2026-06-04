---
title: Hub Class Requests
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Class Requests

> Source scope: USB 2.0 規格 Rev 2.0, Section 11.24.2。  
> 本頁是請求族的參考摘要，不是完整 setup packet 真值表，也不是逐段 PDF 驗證紀錄。

## 頁面用途

本頁回答：

- USB 2.0 hub class 目前有哪些 request family。
- 每個 family 的方向、recipient、target 與 setup 欄位的高階含義。
- 哪些欄位應對應到 `class_request_matrix`、`feature_selector_matrix`、`port_status_bit_matrix`。

本頁不回答：

- 每個 request 的每個欄位是否已在 USB 2.0 PDF 段落層面完成驗證。
- TT 請求欄位編碼是否已完成 correctness 驗證。
- `SET_FEATURE` / `CLEAR_FEATURE` 是否在本 repo 已有完整 state-transition 行為模型。

## Request Family Overview

| bRequest | Value | Direction | Target | High-Level Role |
|---|---|---|---|---|
| `GET_STATUS` | `0x00` | Device-to-Host | Hub / Port | 讀取 hub 或 port 的 status / change 欄位 |
| `CLEAR_FEATURE` | `0x01` | Host-to-Device | Hub / Port | 清除某個 feature，或清除 change bit 所代表的事件紀錄 |
| `SET_FEATURE` | `0x03` | Host-to-Device | Hub / Port | 設定 hub 或 port 的 feature |
| `GET_DESCRIPTOR` | `0x06` | Device-to-Host | Hub | 讀取 hub class-specific descriptor |
| `SET_DESCRIPTOR` | `0x07` | Host-to-Device | Hub | 寫入 hub class-specific descriptor，是否支援由實作決定 |
| `CLEAR_TT_BUFFER` | `0x08` | Host-to-Device | TT-capable Hub | 清除 TT buffer 相關狀態 |
| `RESET_TT` | `0x09` | Host-to-Device | TT-capable Hub | 重置 Transaction Translator |
| `GET_TT_STATE` | `0x0A` | Device-to-Host | TT-capable Hub | 讀取 TT 診斷狀態 |
| `STOP_TT` | `0x0B` | Host-to-Device | TT-capable Hub | 停止 TT 的 split transaction 處理 |

## 本頁閱讀邊界

- 這裡只在方向 / 類型 / recipient 層級整理 `bmRequestType`。
- 若 `wValue`、`wIndex`、`wLength` 仍只以抽象欄位角色呈現而非固定常數，代表本 repo 僅縮小欄位角色邊界，未將完整編碼升為 verified 真值。
- Port-recipient 與 hub-recipient 的請求不能互相混淆；TT 請求僅適用於有 embedded TT 的 HS hub。

## `GET_STATUS`

**用途**

- 讀取 hub 或 port 的 status / change 欄位。

**Direction / recipient**

- Hub: Device-to-Host，class / device recipient。
- Port: Device-to-Host，class / other recipient。

**Target**

- hub 本體或特定 port。

**Setup field summary**

- `bRequest`: `GET_STATUS`
- `wValue`: `0x0000`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `4`

**Governed linkage**

- Hub 請求對應 `wHubStatus` + `wHubChange`。
- Port 請求對應 `wPortStatus` + `wPortChange`。
- 目前 reviewed surface 僅覆蓋 request 到 status-field 的 linkage。
- context-only selector 的對照包含 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED`，作為 `GET_STATUS` 比對 anchor。

**Reviewed surface**

- 本 repo 現在將 `GET_STATUS` 收斂到 hub/port status-field linkage surface。
- 仍不宣告回傳位元逐值行為、host polling 策略、debounce 行為、或速度組合解碼的完整 correctness。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 本頁不宣告所有回傳位元皆有 bit-level 驗證。
- 本頁不定義 host-side polling 或 debounce 行為。

## `CLEAR_FEATURE`

**用途**

- 清除 hub 或 port 的 feature。
- 對 change bits 來說，表示 host 已觀察到事件，並將該事件紀錄清除。

**Direction / recipient**

- Hub: Host-to-Device，class / device recipient。
- Port: Host-to-Device，class / other recipient。

**Target**

- hub 本體或特定 port。

**Setup field summary**

- `bRequest`: `CLEAR_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `0`

**Governed linkage**

- hub-selector 空間與 port-selector 空間需分開理解。
- Hub-recipient 的 reviewed linkage 目前包含 `C_HUB_LOCAL_POWER` <-> `wHubChange bit 0`、`C_HUB_OVER_CURRENT` <-> `wHubChange bit 1`。
- Port-recipient 的 reviewed linkage 目前包含 `C_PORT_CONNECTION`、`C_PORT_ENABLE`、`C_PORT_SUSPEND`、`C_PORT_OVER_CURRENT`、`C_PORT_RESET`，皆在標準 port change selector range。
- 一般的 change-bit 行為語義需搭配 `GET_STATUS` 一起閱讀。

**Reviewed surface**

- 本 repo 將 `CLEAR_FEATURE` 收斂為已 review 的 `C_HUB_*` 與 `C_PORT_*` change selector 對應面。
- 仍不宣告 host-side 的事件 ack/清除順序、完整 change-bit 生命周期正確性，或完整 `CLEAR_FEATURE` 行為模型。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 本頁不建立 `CLEAR_FEATURE` 完整 state-transition 模型。
- 本頁不宣告所有 selector 已有 section-level packet 驗證。

## `SET_FEATURE`

**用途**

- 設定 hub 或 port 的 feature。

**Direction / recipient**

- Hub: Host-to-Device，class / device recipient。
- Port: Host-to-Device，class / other recipient。

**Target**

- hub 本體或特定 port。

**Setup field summary**

- `bRequest`: `SET_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `0`

**Governed linkage**

- Hub 與 port selector 命名空間保持獨立。
- 某些 selector 會影響 port power / reset / suspend 行為，但本頁仍為 request-level summary。
- 本頁的 reviewed surface 僅到 namespace 層級：hub-recipient selector 不可與標準 port selector range 混用。
- Port-recipient reviewed anchors 目前包含 `PORT_ENABLE`、`PORT_SUSPEND`、`PORT_RESET`、`PORT_POWER`。

**Reviewed surface**

- 本 repo 已將 `SET_FEATURE` 收斂到 reviewed selector 命名空間邊界：hub-recipient 與 port-recipient selector 空間刻意分離。
- 仍不宣告 `power`、`reset`、`suspend` 等 selector side-effect 的 correctness 驗證。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`

**Non-claims**

- 本頁不宣告 `SET_FEATURE` side effects 已經 correctness 驗證。
- 本頁不把 selector 摘要直接轉為 firmware control 真值表。

## `GET_DESCRIPTOR`

**用途**

- 讀取 hub class-specific descriptor。

**Direction / recipient**

- Device-to-Host，class / device recipient。

**Target**

- hub 本體。

**Setup field summary**

- `bRequest`: `GET_DESCRIPTOR`
- `wValue`: 編碼 hub descriptor type `0x29` 與 descriptor index
- `wIndex`: `0x0000`
- `wLength`: 取決於 hub descriptor 長度；本 repo 不會硬編碼為固定常數

**Governed linkage**

- 這是暴露 `specs/hub_descriptor.md` 欄位的 request family。

**Reviewed surface**

- 本 repo 已將 class-specific `GET_DESCRIPTOR` descriptor type surface 收斂到 `0x29`。
- 仍不宣告所有 host request-length 策略已完成 correctness 驗證。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁不將 `wValue` / `wLength` 的編碼細節升為 section-level verified truth。
- 本頁不宣告所有 hub 都必須支援某種 descriptor consumer-workflow。

## `SET_DESCRIPTOR`

**用途**

- 寫入 hub class-specific descriptor。

**Direction / recipient**

- Host-to-Device，class / device recipient。

**Target**

- hub 本體。

**Setup field summary**

- `bRequest`: `SET_DESCRIPTOR`
- `wValue`: 編碼 hub descriptor type `0x29` 與 descriptor index
- `wIndex`: `0x0000`
- `wLength`: descriptor payload 大小相關

**Governed linkage**

- 與 `GET_DESCRIPTOR` 屬於同一 descriptor family，但不可假設都支援。

**Reviewed surface**

- 本 repo 已將 class-specific `SET_DESCRIPTOR` descriptor type surface 收斂到 `0x29`。
- 這不表示所有 hub 實作都支援 `SET_DESCRIPTOR`。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁不宣告 `SET_DESCRIPTOR` 在所有 hub 上皆有實作。
- 本頁不將 descriptor 寫入能力提升為規範兼容性要求。

## `CLEAR_TT_BUFFER`

**用途**

- 清除 TT buffer 相關狀態。

**Direction / recipient**

- Host-to-Device，class / other recipient。

**Target**

- 具備 embedded TT 的 HS hub。

**Setup field summary**

- `bRequest`: `CLEAR_TT_BUFFER`
- `wValue`: carrying TT buffer selector fields（TT buffer selector 欄位）
- `wIndex`: carrying TT port 或相關 context
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，僅對 TT-capable hub 有意義。

**Reviewed surface**

- 本 repo 將 `wValue` 收斂為 TT buffer selector 欄位而非純粹當作任意 opaque 值。
- `wIndex` 用來選擇 TT port 或相關 TT context。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不驗證 TT buffer 欄位編碼 correctness。
- 本頁不建立 TT state machine。

## `RESET_TT`

**用途**

- 重置 Transaction Translator。

**Direction / recipient**

- Host-to-Device，class / other recipient。

**Target**

- 具備 embedded TT 的 HS hub。

**Setup field summary**

- `bRequest`: `RESET_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，關聯 TT 恢復/重啟情境。

**Reviewed surface**

- 本 repo 將 `RESET_TT` 收斂到 `wValue = 0x0000`。
- `wIndex` 選擇欲 reset 的 TT port 或 TT 目標實例。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 reset 前後 TT 行為已驗證。
- 本頁不建立 split transaction 完成規則的 correctness。

## `GET_TT_STATE`

**用途**

- 讀取 TT 診斷狀態資料。

**Direction / recipient**

- Device-to-Host，class / other recipient。

**Target**

- 具備 embedded TT 的 HS hub。

**Setup field summary**

- `bRequest`: `GET_TT_STATE`
- `wValue`: `0x0000`
- `wIndex`: TT port 或相關 diagnostic context
- `wLength`: TT state data length

**Governed linkage**

- 回傳內容屬於 TT 診斷面，不應與一般 port status 語義混用。

**Reviewed surface**

- 本 repo 將 `GET_TT_STATE` 收斂為 `wValue = 0x0000`。
- `wIndex` 指向 TT port / 診斷 context。
- `wLength` 表示 TT state data 長度，但本 repo 仍不會硬編為固定常數。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 TT 狀態 payload 位元意涵已完成 section-level 驗證。
- 本頁不規定 host stack 應如何消費 TT state data。

## `STOP_TT`

**用途**

- 停止 TT split-transaction 處理。

**Direction / recipient**

- Host-to-Device，class / other recipient。

**Target**

- 具備 embedded TT 的 HS hub。

**Setup field summary**

- `bRequest`: `STOP_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，通常與 TT 診斷或恢復場景相關。

**Reviewed surface**

- 本 repo 將 `STOP_TT` 收斂為 `wValue = 0x0000`。
- `wIndex` 選擇欲停止 split-transaction processing 的 TT port 或 TT 目標實例。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 TT 停止後的下游時序行為。
- 本頁不建立 TT traffic control 的 correctness 模型。

## Governed Table Linkage Summary

- `tables/class_request_matrix.yaml`: 9 個 hub class request family 的主要結構來源。
- `tables/feature_selector_matrix.yaml`: `SET_FEATURE` / `CLEAR_FEATURE` 的 selector boundary 參考。
- `tables/port_status_bit_matrix.yaml`: `GET_STATUS` 及 change-bit 解讀比對來源。
- `specs/hub_descriptor.md`: `GET_DESCRIPTOR` / `SET_DESCRIPTOR` 對應的 descriptor 參考頁。
- `specs/transaction_translator.md`: TT request family 的高階語義摘要。

## Non-claims

- 本頁不是完整 setup-packet 真值表。
- 本頁不是每個 request 的 section-level USB 2.0 PDF 驗證記錄。
- 本頁不宣告 TT request 欄位編碼已完成 correctness 驗證。
- 本頁不覆蓋 consuming repo 的確認 project fact。
