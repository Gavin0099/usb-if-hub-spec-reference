---
title: Hub Class Requests
claim_level: inferred
status: review_required
last_reviewed: "2026-06-05"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Class Requests

> 來源範圍：USB 2.0 規範 Rev 2.0，Section 11.24.2。  
> 本頁為 hub class request 請求族群參考摘要，不是完整 setup packet 真值表，也不是 section-level PDF 驗證記錄。

## 頁面目的

本頁回答：

- USB 2.0 hub class request family 有哪些。
- 每一族的方向、recipient、目標與 setup 欄位意義。
- 哪些欄位要回鏈到 `class_request_matrix`、`feature_selector_matrix`、`port_status_bit_matrix`。

本頁不回答：

- 是否每個 request 的每個欄位已完成 PDF section-level 驗證。
- TT request 的欄位編碼是否已完成 correctness 驗證。
- 本 repo 是否已有 `SET_FEATURE` / `CLEAR_FEATURE` 完整的 state-transition 模型。

## Request Family Overview

| bRequest | Value | Direction | Target | High-Level Role |
|---|---|---|---|---|
| `GET_STATUS` | `0x00` | Device-to-Host | Hub / Port | 讀取 hub 或 port 的 status / change 欄位 |
| `CLEAR_FEATURE` | `0x01` | Host-to-Device | Hub / Port | 清除 feature，或清除以 change bit 表示的事件紀錄 |
| `SET_FEATURE` | `0x03` | Host-to-Device | Hub / Port | 設定 hub 或 port feature |
| `GET_DESCRIPTOR` | `0x06` | Device-to-Host | Hub | 讀取 hub class descriptor |
| `SET_DESCRIPTOR` | `0x07` | Host-to-Device | Hub | 寫入 hub class descriptor；是否支援視實作而定 |
| `CLEAR_TT_BUFFER` | `0x08` | Host-to-Device | TT-capable Hub | 清除 TT buffer 相關狀態 |
| `RESET_TT` | `0x09` | Host-to-Device | TT-capable Hub | 重置 Transaction Translator |
| `GET_TT_STATE` | `0x0A` | Device-to-Host | TT-capable Hub | 讀取 TT diagnostic 狀態 |
| `STOP_TT` | `0x0B` | Host-to-Device | TT-capable Hub | 停止 TT split-transaction 處理 |

## 閱讀本頁的邊界條件

- `bmRequestType` 僅在 direction / type / recipient 層級摘要，未展開完整 encoding 的全部細節。
- 如果 `wValue`、`wIndex`、`wLength` 僅用抽象欄位角色描述而非固定常數，本 repo 僅縮小為欄位角色邊界，尚未升級為完整 encoding 真值。
- 不能混淆 port-recipient 與 hub-recipient；TT request 僅適用於具嵌入 TT 的 HS hub。

## `GET_STATUS`

**用途**

- 讀取 hub 或 port 的 status / change 欄位。

**Direction / recipient**

- Hub：Device-to-Host、class、device recipient。
- Port：Device-to-Host、class、other recipient。

**Target**

- hub 本體或指定 port。

**Setup 欄位摘要**

- `bRequest`: `GET_STATUS`
- `wValue`: `0x0000`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `4`

**Governed linkage**

- Hub request 對應 `wHubStatus` + `wHubChange`。
- Port request 對應 `wPortStatus` + `wPortChange`。
- 本 repo 當前 reviewed 邊界面僅涵蓋 request-to-status-field 的對應關係。
- `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED` 僅作為 `GET_STATUS` 比對 anchor 的 context-only surface。

**Review 範圍**

- 本 repo 已將 `GET_STATUS` 讀取邊界限定為 hub / port status-field 對應面。
- 這不代表回傳 bit 的完整位元行為、主機輪詢策略、debounce 行為或 speed 合併解碼都已完成 correctness 驗證。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 本頁不宣稱已完成所有回傳 bit 的 bit-level 驗證。
- 本頁不定義主機輪詢或 debounce 行為。

## `CLEAR_FEATURE`

**用途**

- 清除 hub 或 port feature。
- 對 change bit 而言，表示主機已觀察並 acknowledge 該事件，並清除此事件紀錄。

**Direction / recipient**

- Hub：Host-to-Device、class、device recipient。
- Port：Host-to-Device、class、other recipient。

**Target**

- hub 本體或指定 port。

**Setup 欄位摘要**

- `bRequest`: `CLEAR_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `0`

**Governed linkage**

- Hub 與 port selector namespace 必須分開解讀。
- Hub-recipient 已 reviewed 的 linkage：`C_HUB_LOCAL_POWER` <-> `wHubChange bit 0`，`C_HUB_OVER_CURRENT` <-> `wHubChange bit 1`。
- Port-recipient 已 reviewed 的 linkage：`C_PORT_CONNECTION`、`C_PORT_ENABLE`、`C_PORT_SUSPEND`、`C_PORT_OVER_CURRENT`、`C_PORT_RESET` 皆在標準 port change-selector 邊界內。
- change-bit 的一般語意需與 `GET_STATUS` 一起閱讀。
- 已 review 的 change selectors 僅是邊界證據，**不是**完整行為模型：
  - `C_PORT_CONNECTION`、`C_PORT_ENABLE`、`C_PORT_SUSPEND`、`C_PORT_OVER_CURRENT`、`C_PORT_RESET` 只表達「主機可 ack/清除的事件紀錄 selector」。
  - 不主張完整控制狀態轉移、時序、錯誤恢復行為。

**Review 範圍**

- 本 repo 已將 `CLEAR_FEATURE` 限於 `C_HUB_*`、`C_PORT_*` change selector linkage。
- 仍不宣告主機事件 ack 的完整順序模型、change-bit lifecycle 完整 correctness，或 `CLEAR_FEATURE` 完整行為模型。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 本頁未建立完整 `CLEAR_FEATURE` state-transition 模型。
- 本頁未宣稱所有 selector 已有 section-level packet 驗證。

## `SET_FEATURE`

**用途**

- 設定 hub 或 port feature。

**Direction / recipient**

- Hub：Host-to-Device、class、device recipient。
- Port：Host-to-Device、class、other recipient。

**Target**

- hub 本體或指定 port。

**Setup 欄位摘要**

- `bRequest`: `SET_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `0`

**Governed linkage**

- Hub 與 port selector namespace 必須保持 distinct。
- 部分 selector 會影響 port power / reset / suspend，但本頁仍只提供 request summary。
- 本 repo 的 reviewed 邊界面僅為 namespace-level：hub-recipient selector 不可與標準 port selector range 合併。
- Port-recipient reviewed anchors 目前包含 `PORT_ENABLE`、`PORT_SUSPEND`、`PORT_RESET`、`PORT_POWER`。
- `PORT_TEST` 與 `PORT_INDICATOR` 目前只保留 selector coverage 層級；本 repo 尚不主張這兩個 request entry 有完整 test-mode 或 indicator 行為語意驗證。

**Review 範圍**

- 本 repo 已將 `SET_FEATURE` 限縮為 selector-namespace boundary 已 review：hub-recipient 與 port-recipient selector 空間明確隔離。
- 仍未宣告 port power / reset / suspend 等 selector side-effect 的 correctness 驗證。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`

**Non-claims**

- 本頁不宣稱 `SET_FEATURE` side effect 已完成 correctness 驗證。
- 本頁不將 selector 摘要提升為 firmware control 真值。

## `GET_DESCRIPTOR`

**用途**

- 讀取 hub class-specific descriptor。

**Direction / recipient**

- Device-to-Host、class、device recipient。

**Target**

- hub 本體。

**Setup 欄位摘要**

- `bRequest`: `GET_DESCRIPTOR`
- `wValue`: 與 descriptor type `0x29` 及 descriptor index 編碼
- `wIndex`: `0x0000`
- `wLength`: 依 hub descriptor 長度而定，本 repo 不將其硬編為單一定值

**Governed linkage**

- 這個 request family 對應 `specs/hub_descriptor.md` 的欄位摘要。

**Review 範圍**

- 本 repo 僅將 class-specific `GET_DESCRIPTOR` 型別面限定為 `0x29`。
- 仍未宣稱所有 host request-length 策略都完成 correctness 驗證。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁未把 `wValue` / `wLength` encoding 升級為 section-level verified truth。
- 本頁不宣稱所有 hub 都必須具備特定 consumer-side descriptor workflow。

## `SET_DESCRIPTOR`

**用途**

- 寫入 hub class-specific descriptor。

**Direction / recipient**

- Host-to-Device、class、device recipient。

**Target**

- hub 本體。

**Setup 欄位摘要**

- `bRequest`: `SET_DESCRIPTOR`
- `wValue`: 與 descriptor type `0x29` 及 descriptor index 編碼
- `wIndex`: `0x0000`
- `wLength`: descriptor payload 大小（視實作而定）

**Governed linkage**

- 與 `GET_DESCRIPTOR` 屬同一 descriptor family。

**Review 範圍**

- 本 repo 僅將 class-specific `SET_DESCRIPTOR` 的 descriptor type 限在 `0x29`。
- 不代表所有 hub 都實作 `SET_DESCRIPTOR`。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁不宣稱 `SET_DESCRIPTOR` 在所有 hub 上實作。
- 本頁不將 descriptor 寫入支援行為提升為規格要求。

## `CLEAR_TT_BUFFER`

**用途**

- 清除 TT buffer 相關狀態。

**Direction / recipient**

- Host-to-Device、class、other recipient。

**Target**

- 具 TT 的 HS hub。

**Setup 欄位摘要**

- `bRequest`: `CLEAR_TT_BUFFER`
- `wValue`: TT buffer selector 欄位
- `wIndex`: TT port 或相關 context
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，僅對 TT-capable hub 有意義。

**Review 範圍**

- 本 repo 將 `wValue` 聚焦為 TT buffer selector 欄位，而非任意不透明值。
- `wIndex` 用來選擇 TT port 或 TT context。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不驗證 TT buffer 欄位 encoding 的 correctness。
- 本頁不建立 TT state machine。

## `RESET_TT`

**用途**

- 重置 Transaction Translator。

**Direction / recipient**

- Host-to-Device、class、other recipient。

**Target**

- 具 TT 的 HS hub。

**Setup 欄位摘要**

- `bRequest`: `RESET_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，和 TT recovery / restart 關聯。

**Review 範圍**

- 本 repo 將 `RESET_TT` `wValue` 限為 `0x0000`。
- `wIndex` 選定被重置的 TT port / TT target 實例。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不主張 TT reset 前後行為已完成驗證。
- 本頁不建立 split-transaction completion 的 correctness 模型。

## `GET_TT_STATE`

**用途**

- 讀取 TT diagnostic state 資料。

**Direction / recipient**

- Device-to-Host、class、other recipient。

**Target**

- 具 TT 的 HS hub。

**Setup 欄位摘要**

- `bRequest`: `GET_TT_STATE`
- `wValue`: `0x0000`
- `wIndex`: TT port 或 diagnostic context
- `wLength`: TT state data length

**Governed linkage**

- 回傳內容屬於 TT diagnostic surface，不可與一般 port status semantics 混用。

**Review 範圍**

- 本 repo 將 `GET_TT_STATE` `wValue` 限為 `0x0000`。
- `wIndex` 指向 TT port / diagnostic context。
- `wLength` 是 TT state data 長度名稱，本 repo 仍不硬編為單一固定值。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不主張 TT state payload bit 意義有 section-level 驗證。
- 本頁不規定 host stack 應如何消費 TT state data。

## `STOP_TT`

**用途**

- 停止 TT split-transaction 處理。

**Direction / recipient**

- Host-to-Device、class、other recipient。

**Target**

- 具 TT 的 HS hub。

**Setup 欄位摘要**

- `bRequest`: `STOP_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，通常與 TT diagnostics / recovery 情境有關。

**Review 範圍**

- 本 repo 將 `STOP_TT` 限為 `wValue = 0x0000`。
- `wIndex` 指定要停止 split-transaction 的 TT port / TT target instance。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不主張 TT stop 後下游時序行為已驗證。
- 本頁不建立 TT 交通控制的 correctness 模型。

## Governed Table Linkage Summary

- `tables/class_request_matrix.yaml`：hub class request family 的主要結構來源。
- `tables/feature_selector_matrix.yaml`：`SET_FEATURE` / `CLEAR_FEATURE` 的 selector 邊界。
- `tables/port_status_bit_matrix.yaml`：`GET_STATUS` 與 change-bit 解讀比對來源。
- `specs/hub_descriptor.md`：`GET_DESCRIPTOR` / `SET_DESCRIPTOR` 的 descriptor 參考頁。
- `specs/transaction_translator.md`：TT request family 的高階語意摘要。

## Non-claims

- 本頁不是完整 setup-packet 真值表。
- 本頁不是 USB 2.0 PDF section-level 驗證紀錄。
- 本頁不宣稱 TT request 欄位 encoding 正確性已驗證。
- 本頁不取代 consuming repo 中已確認的 project facts。
