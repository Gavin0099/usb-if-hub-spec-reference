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
> 本頁是 request-family reference summary，不是完整 SETUP packet truth table，也不是 section-level PDF verification record。

## Page Purpose

本頁要回答的是：

- USB 2.0 hub class request families 有哪些
- 每個 family 的高層 direction、recipient、target 與 setup-field meaning
- 哪些欄位應回連到 `class_request_matrix`、`feature_selector_matrix`、`port_status_bit_matrix`

本頁不打算回答：

- 每個 request 的每個欄位是否都已完成 PDF section-level verification
- TT request field encodings 是否已完成 correctness verification
- `SET_FEATURE` / `CLEAR_FEATURE` 是否已在本 repo 形成完整 state-transition model

## Request Family Overview

| bRequest | Value | Direction | Target | High-Level Role |
|---|---|---|---|---|
| `GET_STATUS` | `0x00` | Device-to-Host | Hub / Port | 讀取 hub 或 port 的 status/change fields |
| `CLEAR_FEATURE` | `0x01` | Host-to-Device | Hub / Port | 清除 feature，或清除 change bit 所代表的事件紀錄 |
| `SET_FEATURE` | `0x03` | Host-to-Device | Hub / Port | 設定 hub 或 port features |
| `GET_DESCRIPTOR` | `0x06` | Device-to-Host | Hub | 讀取 hub class-specific descriptor |
| `SET_DESCRIPTOR` | `0x07` | Host-to-Device | Hub | 寫入 hub class-specific descriptor；是否支援視實作而定 |
| `CLEAR_TT_BUFFER` | `0x08` | Host-to-Device | TT-capable Hub | 清除 TT buffer 相關狀態 |
| `RESET_TT` | `0x09` | Host-to-Device | TT-capable Hub | 重置 Transaction Translator |
| `GET_TT_STATE` | `0x0A` | Device-to-Host | TT-capable Hub | 讀取 TT diagnostic state |
| `STOP_TT` | `0x0B` | Host-to-Device | TT-capable Hub | 停止 TT split-transaction processing |

## Boundary Conditions for Reading This Page

- 本頁對 `bmRequestType` 只收斂到 direction / type / recipient 層級。
- 如果 `wValue`、`wIndex`、`wLength` 仍以抽象 field-role name 表示，而不是固定常數，代表本 repo 只收斂了欄位角色，尚未把完整 encoding 升級成 verified truth。
- Port-recipient、hub-recipient 與 TT requests 不得混讀；TT requests 只適用於內嵌 TT 的 HS hubs。

## `GET_STATUS`

**Purpose**

- 讀取 hub 或 port 的 status / change fields。

**Direction / recipient**

- Hub: Device-to-Host, class, device recipient.
- Port: Device-to-Host, class, other recipient.

**Target**

- Hub 本身或某一個 port。

**Setup-field summary**

- `bRequest`: `GET_STATUS`
- `wValue`: `0x0000`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `4`

**Governed linkage**

- Hub request 對應 `wHubStatus` + `wHubChange`
- Port request 對應 `wPortStatus` + `wPortChange`

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 本頁不宣告所有 returned bits 都已完成 bit-level verification。
- 本頁不定義 host-side polling 或 debounce behavior。

## `CLEAR_FEATURE`

**Purpose**

- 清除 hub 或 port feature。
- 對 change bits 而言，表示 host 已觀察並 acknowledge 事件，現在要清除該事件紀錄。

**Direction / recipient**

- Hub: Host-to-Device, class, device recipient.
- Port: Host-to-Device, class, other recipient.

**Target**

- Hub 本身或某一個 port。

**Setup-field summary**

- `bRequest`: `CLEAR_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `0`

**Governed linkage**

- Hub 與 port selector spaces 必須分開解讀。
- Hub-recipient reviewed linkage 目前包含 `C_HUB_LOCAL_POWER` <-> `wHubChange bit 0` 與 `C_HUB_OVER_CURRENT` <-> `wHubChange bit 1`。
- Port-recipient reviewed linkage 目前包含 `C_PORT_CONNECTION`、`C_PORT_ENABLE`、`C_PORT_SUSPEND`、`C_PORT_OVER_CURRENT`、`C_PORT_RESET` 這組標準 port change-selector boundary。
- 共通的 change-bit semantics 應和 `GET_STATUS` 一起解讀。

**Reviewed surface**

- 本 repo 現在把 `CLEAR_FEATURE` 收斂到已 reviewed 的 `C_HUB_*` / `C_PORT_*` selector-linkage surface。
- 這仍不宣告 host-side event-acknowledgement sequencing、完整 change-bit lifecycle correctness，或完整 `CLEAR_FEATURE` behavior model。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 本頁不建立完整的 `CLEAR_FEATURE` state-transition model。
- 本頁不宣告所有 selectors 都已完成 section-level packet verification。

## `SET_FEATURE`

**Purpose**

- 設定 hub 或 port feature。

**Direction / recipient**

- Hub: Host-to-Device, class, device recipient.
- Port: Host-to-Device, class, other recipient.

**Target**

- Hub 本身或某一個 port。

**Setup-field summary**

- `bRequest`: `SET_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `0`

**Governed linkage**

- Hub 與 port selector namespaces 必須保持分離。
- 某些 selectors 會影響 port power、reset、suspend behavior，但本頁仍只是 request summary。
- 這裡目前的 reviewed request surface 只到 namespace 層級：hub-recipient selectors 不得和標準 port selector range 混在一起。

**Reviewed surface**

- 本 repo 現在把 `SET_FEATURE` 收斂到 reviewed selector-namespace boundary：hub-recipient 與 port-recipient selector spaces 是刻意分開的。
- 這仍不宣告 power、reset、suspend 或其他 port-feature behaviors 的 selector side effects 已驗證。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`

**Non-claims**

- 本頁不宣告 `SET_FEATURE` side effects 已完成 correctness verification。
- 本頁不把 selector summary 升格成 firmware control truth table。

## `GET_DESCRIPTOR`

**Purpose**

- 讀取 hub class-specific descriptor。

**Direction / recipient**

- Device-to-Host, class, device recipient.

**Target**

- Hub 本身。

**Setup-field summary**

- `bRequest`: `GET_DESCRIPTOR`
- `wValue`: 同時編碼 hub descriptor type `0x29` 與 descriptor index
- `wIndex`: `0x0000`
- `wLength`: 取決於 hub descriptor length；本 repo 不把它硬編碼成單一固定常數

**Governed linkage**

- 這個 request family 對應到 `specs/hub_descriptor.md` 所整理的 descriptor fields。

**Reviewed surface**

- 本 repo 已把 class-specific `GET_DESCRIPTOR` 的 descriptor type surface 收斂到 `0x29`
- 這仍不宣告所有 host request-length strategy 都已完成 correctness verification

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁不把 `wValue` / `wLength` encoding details 升格成 section-level verified truth。
- 本頁不宣告所有 hubs 都必須支援某種 consumer-side descriptor workflow。

## `SET_DESCRIPTOR`

**Purpose**

- 寫入 hub class-specific descriptor。

**Direction / recipient**

- Host-to-Device, class, device recipient.

**Target**

- Hub 本身。

**Setup-field summary**

- `bRequest`: `SET_DESCRIPTOR`
- `wValue`: 同時編碼 hub descriptor type `0x29` 與 descriptor index
- `wIndex`: `0x0000`
- `wLength`: 取決於 descriptor payload size

**Governed linkage**

- 與 `GET_DESCRIPTOR` 同屬 descriptor family，但不應假設所有裝置都支援。

**Reviewed surface**

- 本 repo 已把 class-specific `SET_DESCRIPTOR` 的 descriptor type surface 收斂到 `0x29`
- 這不代表所有 hubs 都實作 `SET_DESCRIPTOR`

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁不宣告所有 hubs 都實作 `SET_DESCRIPTOR`。
- 本頁不把 descriptor-write support 升格成 normative compatibility claim。

## `CLEAR_TT_BUFFER`

**Purpose**

- 清除 TT buffer 相關狀態。

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 內嵌 TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `CLEAR_TT_BUFFER`
- `wValue`: 攜帶 TT buffer selector fields
- `wIndex`: 攜帶 TT port 或相關 context
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，只對 TT-capable hubs 有意義。

**Reviewed surface**

- 本 repo 已把 `wValue` 收斂成 TT buffer selector fields，而不是任意 opaque 值
- `wIndex` 用來選擇 TT port 或相關 TT context

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不驗證 TT buffer field encoding correctness。
- 本頁不建立 TT state machine。

## `RESET_TT`

**Purpose**

- 重置 Transaction Translator。

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 內嵌 TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `RESET_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，並和 TT recovery / restart concerns 有關。

**Reviewed surface**

- 本 repo 已把 `RESET_TT` 收斂到 `wValue = 0x0000`
- `wIndex` 用來選擇要 reset 的 TT port 或 TT target instance

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 reset 前後的 TT behavior 已驗證。
- 本頁不建立 split-transaction completion rules 的 correctness claim。

## `GET_TT_STATE`

**Purpose**

- 讀取 TT diagnostic state data。

**Direction / recipient**

- Device-to-Host, class, other recipient.

**Target**

- 內嵌 TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `GET_TT_STATE`
- `wValue`: `0x0000`
- `wIndex`: TT port 或相關 diagnostic context
- `wLength`: TT state data length

**Governed linkage**

- 回傳內容屬於 TT diagnostic surface，不應和一般 port status semantics 混在一起。

**Reviewed surface**

- 本 repo 已把 `wValue` 收斂到 `0x0000`
- `wIndex` 指向 TT port / diagnostic context
- `wLength` 只命名為 TT state data length，不把它硬編碼成單一常數

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 TT state payload bit meanings 已完成 section-level verification。
- 本頁不規定 host stack 應如何消費 TT state data。

## `STOP_TT`

**Purpose**

- 停止 TT split-transaction processing。

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 內嵌 TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `STOP_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，通常和 TT diagnostics 或 recovery scenarios 有關。

**Reviewed surface**

- 本 repo 已把 `STOP_TT` 收斂到 `wValue = 0x0000`
- `wIndex` 用來選擇要停止 split-transaction processing 的 TT port 或 TT target instance

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 TT stop 之後的 downstream timing behavior。
- 本頁不建立 TT traffic control 的 correctness model。

## Governed Table Linkage Summary

- `tables/class_request_matrix.yaml`: 9 個 hub class request families 的主要結構來源
- `tables/feature_selector_matrix.yaml`: `SET_FEATURE` / `CLEAR_FEATURE` 的 selector boundary reference
- `tables/port_status_bit_matrix.yaml`: `GET_STATUS` 與 change-bit interpretation 的 comparison source
- `specs/hub_descriptor.md`: `GET_DESCRIPTOR` / `SET_DESCRIPTOR` 的 descriptor-side reference page
- `specs/transaction_translator.md`: TT request family 的高層 semantic summary

## Non-claims

- 本頁不是完整 setup-packet truth table。
- 本頁不是逐 request 的 section-level USB 2.0 PDF verification record。
- 本頁不宣告 TT request field encodings 已完成 correctness verification。
- 本頁不會覆蓋 consuming repos 的 confirmed project facts。
