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

> Source scope: USB 2.0 Specification Rev 2.0, Section 11.24.2.  
> This page is a request-family reference summary, not a complete setup packet truth table and not a section-level PDF verification record.

## 頁面目的

本頁回答：

- 哪些 USB 2.0 hub class 的 request family 存在
- 每個 family 在 direction、recipient、target、setup-field 的高階含義
- 哪些欄位應回連到 `class_request_matrix`、`feature_selector_matrix`、`port_status_bit_matrix`

本頁不回答：

- 每一個 request 的每一欄位是否都已經完成 PDF section-level 驗證
- TT request 的欄位編碼是否都已 correctness 驗證
- `SET_FEATURE` / `CLEAR_FEATURE` 是否已在本 repo 建立完整 state-transition model

## Request Family Overview

| bRequest | Value | Direction | Target | High-Level Role |
|---|---|---|---|---|
| `GET_STATUS` | `0x00` | Device-to-Host | Hub / Port | Reads hub or port status/change fields |
| `CLEAR_FEATURE` | `0x01` | Host-to-Device | Hub / Port | Clears a feature, or clears the event record represented by a change bit |
| `SET_FEATURE` | `0x03` | Host-to-Device | Hub / Port | Sets hub or port features |
| `GET_DESCRIPTOR` | `0x06` | Device-to-Host | Hub | Reads the hub class-specific descriptor |
| `SET_DESCRIPTOR` | `0x07` | Host-to-Device | Hub | Writes the hub class-specific descriptor; support is implementation-dependent |
| `CLEAR_TT_BUFFER` | `0x08` | Host-to-Device | TT-capable Hub | Clears TT buffer-related state |
| `RESET_TT` | `0x09` | Host-to-Device | TT-capable Hub | Resets the Transaction Translator |
| `GET_TT_STATE` | `0x0A` | Device-to-Host | TT-capable Hub | Reads TT diagnostic state |
| `STOP_TT` | `0x0B` | Host-to-Device | TT-capable Hub | Stops TT split-transaction processing |

## 讀取本頁的前置條件

- `bmRequestType` 僅在 direction / type / recipient 層級摘要。
- 若 `wValue`、`wIndex`、`wLength` 仍是抽象欄位角色名稱而非固定常數，本 repo 僅縮窄了 field role，尚未升為完整 verified encoding。
- Port-recipient 與 hub-recipient 請求不能合併，TT requests 僅適用於有 embedded TT 的 HS hub。

## `GET_STATUS`

**目的**

- 讀取 hub 或 port 的 status/change fields。

**Direction / recipient**

- Hub：Device-to-Host，class，device recipient
- Port：Device-to-Host，class，other recipient

**Target**

- hub 本身或特定 port

**Setup field 摘要**

- `bRequest`: `GET_STATUS`
- `wValue`: `0x0000`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `4`

**Governed linkage**

- Hub request 對應 `wHubStatus` + `wHubChange`
- Port request 對應 `wPortStatus` + `wPortChange`
- 本 repo 目前的 reviewed surface 僅涵蓋 request 到 status-field 的連結
- 相關 context-only selector surface 包含 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED` 作為 `GET_STATUS` 比較錨點

**Reviewed surface**

- 本 repo 目前將 `GET_STATUS` 限定為 hub/port status-field linkage surface
- 仍未宣告回傳 bit 行為、host polling 策略、debounce 行為、或 speed decode 完整正確性

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 本頁不宣告所有回傳 bits 都有 bit-level 驗證
- 本頁不定義 host-side polling 或 debounce 行為

## `CLEAR_FEATURE`

**目的**

- 清除 hub 或 port feature
- 對 change bits 來說，表示 host 已觀察並 acknowledge，並清除對應 event record

**Direction / recipient**

- Hub：Host-to-Device，class，device recipient
- Port：Host-to-Device，class，other recipient

**Target**

- hub 本身或特定 port

**Setup field 摘要**

- `bRequest`: `CLEAR_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `0`

**Governed linkage**

- Hub 與 port selector spaces 必須分開解讀
- Hub-recipient reviewed linkage 目前包含 `C_HUB_LOCAL_POWER` <-> `wHubChange bit 0`、`C_HUB_OVER_CURRENT` <-> `wHubChange bit 1`
- Port-recipient reviewed linkage 目前包含 `C_PORT_CONNECTION`、`C_PORT_ENABLE`、`C_PORT_SUSPEND`、`C_PORT_OVER_CURRENT`、`C_PORT_RESET`，皆為標準 port change-selector boundary 內
- change-bit 的常見語意需與 `GET_STATUS` 一併閱讀

**Reviewed surface**

- 本 repo 將 `CLEAR_FEATURE` 縮窄為已 reviewed 的 `C_HUB_*` 與 `C_PORT_*` change selector linkage surface
- 仍不宣告 host-side event acknowledge sequencing、完整 change-bit lifecycle 正確性，或完整 `CLEAR_FEATURE` 行為模型

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 本頁不建立完整 `CLEAR_FEATURE` state-transition model
- 本頁不宣告所有 selector 都已有 section-level packet 驗證

## `SET_FEATURE`

**目的**

- 設定 hub 或 port feature

**Direction / recipient**

- Hub：Host-to-Device，class，device recipient
- Port：Host-to-Device，class，other recipient

**Target**

- hub 本身或特定 port

**Setup field 摘要**

- `bRequest`: `SET_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `0`

**Governed linkage**

- Hub、port selector namespace 需維持分離
- 部分 selectors 可能影響 port power、reset、suspend，但本頁仍是 request summary
- 目前 reviewed surface 只到 namespace level：hub-recipient selectors 不能與 standard port selector range 混用
- Port-recipient reviewed anchors 目前包括 `PORT_ENABLE`、`PORT_SUSPEND`、`PORT_RESET`、`PORT_POWER`

**Reviewed surface**

- 本 repo 將 `SET_FEATURE` 縮窄為 reviewed selector namespace boundary：hub-recipient 與 port-recipient namespace 有意分離
- 仍不宣告 power、reset、suspend 或其他 port feature 的 side-effect 驗證

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`

**Non-claims**

- 本頁不宣告 `SET_FEATURE` side effects 已完成 correctness 驗證
- 本頁不把 selector summary 升格為 firmware control truth table

## `GET_DESCRIPTOR`

**目的**

- 讀取 hub class-specific descriptor

**Direction / recipient**

- Device-to-Host，class，device recipient

**Target**

- hub 本身

**Setup field 摘要**

- `bRequest`: `GET_DESCRIPTOR`
- `wValue`: 組合 hub descriptor type `0x29` 與 descriptor index
- `wIndex`: `0x0000`
- `wLength`: 依 hub descriptor 長度而定，本頁未硬編成單一固定值

**Governed linkage**

- 這是將 `specs/hub_descriptor.md` 欄位語意暴露給請求層的 request family

**Reviewed surface**

- 本 repo 將 class-specific `GET_DESCRIPTOR` descriptor-type surface 縮到 `0x29`
- 仍不宣告每個 host request-length 策略皆完成 correctness 驗證

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁不把 `wValue` / `wLength` 的 encoding 推升為 section-level verified truth
- 本頁不宣告所有 hub 都必須支援某種 consumer-side descriptor workflow

## `SET_DESCRIPTOR`

**目的**

- 寫入 hub class-specific descriptor

**Direction / recipient**

- Host-to-Device，class，device recipient

**Target**

- hub 本身

**Setup field 摘要**

- `bRequest`: `SET_DESCRIPTOR`
- `wValue`: 組合 hub descriptor type `0x29` 與 descriptor index
- `wIndex`: `0x0000`
- `wLength`: 依 descriptor payload 大小而定

**Governed linkage**

- 與 `GET_DESCRIPTOR` 屬於同一 descriptor family，但不能假設支援

**Reviewed surface**

- 本 repo 將 class-specific `SET_DESCRIPTOR` descriptor type surface 縮到 `0x29`
- 這不表示所有 hub 都有 `SET_DESCRIPTOR` 實作

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁不宣告所有 hub 實作 `SET_DESCRIPTOR`
- 本頁不把 descriptor-write 支援升級為規範性相容性主張

## `CLEAR_TT_BUFFER`

**目的**

- 清除 TT buffer 相關狀態

**Direction / recipient**

- Host-to-Device，class，other recipient

**Target**

- 具備 embedded TT 的 HS hub

**Setup field 摘要**

- `bRequest`: `CLEAR_TT_BUFFER`
- `wValue`: 帶 TT buffer selector fields
- `wIndex`: 帶 TT port 或相關 context
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，僅適用於 TT-capable hub

**Reviewed surface**

- 本 repo 將 `wValue` 限定為 TT buffer selector fields，而非任意 opaque value
- `wIndex` 用於選擇 TT port 或相關 TT context

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不驗證 TT buffer 欄位 encoding
- 本頁不建立 TT 狀態機

## `RESET_TT`

**目的**

- 重設 Transaction Translator

**Direction / recipient**

- Host-to-Device，class，other recipient

**Target**

- 具備 embedded TT 的 HS hub

**Setup field 摘要**

- `bRequest`: `RESET_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，關聯 TT recovery / restart

**Reviewed surface**

- 本 repo 將 `RESET_TT` 縮到 `wValue = 0x0000`
- `wIndex` 用於選擇 TT port 或 TT target instance 進行重設

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 TT reset 前後行為已驗證
- 本頁不建立 split-transaction completion 的 correctness model

## `GET_TT_STATE`

**目的**

- 讀取 TT 診斷狀態資料

**Direction / recipient**

- Device-to-Host，class，other recipient

**Target**

- 具備 embedded TT 的 HS hub

**Setup field 摘要**

- `bRequest`: `GET_TT_STATE`
- `wValue`: `0x0000`
- `wIndex`: TT port 或相關診斷 context
- `wLength`: TT state data length

**Governed linkage**

- 回傳內容屬於 TT diagnostic surface，不應與一般 port status 語意合併

**Reviewed surface**

- 本 repo 將 `wValue` 縮到 `0x0000`
- `wIndex` 指向 TT port / 診斷 context
- `wLength` 為 TT state data 長度，但本 repo 未將其硬編為單一值

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 TT state payload bit 意涵已完成 section-level 驗證
- 本頁不規定 host stack 應如何消化 TT state data

## `STOP_TT`

**目的**

- 停止 TT split-transaction processing

**Direction / recipient**

- Host-to-Device，class，other recipient

**Target**

- 具備 embedded TT 的 HS hub

**Setup field 摘要**

- `bRequest`: `STOP_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，通常與 TT diagnostics 或 recovery 場景相關

**Reviewed surface**

- 本 repo 將 `STOP_TT` 縮到 `wValue = 0x0000`
- `wIndex` 選擇 TT port 或 TT target instance 以停止其 split-transaction processing

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 TT stop 後的 downstream timing 行為
- 本頁不建立 TT traffic control 的 correctness model

## Governed Table Linkage Summary

- `tables/class_request_matrix.yaml`: 9 種 hub class request families 的主要結構來源
- `tables/feature_selector_matrix.yaml`: `SET_FEATURE` / `CLEAR_FEATURE` 的 selector boundary reference
- `tables/port_status_bit_matrix.yaml`: `GET_STATUS` 與 change-bit 解讀的比對來源
- `specs/hub_descriptor.md`: `GET_DESCRIPTOR` / `SET_DESCRIPTOR` 的 descriptor-side 參考頁
- `specs/transaction_translator.md`: TT request family 的高階語意摘要

## Non-claims

- 本頁不是完整 setup-packet truth table
- 本頁不是每個 request 的 section-level USB 2.0 PDF 驗證紀錄
- 本頁不宣告 TT request 欄位 encoding 已 correctness-verified
- 本頁不覆蓋 consuming repo 已確認 project facts
