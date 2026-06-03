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

本頁回答：

- USB 2.0 hub class request families 有哪些。
- 每個 family 的高層 direction、recipient、target 與 setup-field meaning。
- 哪些欄位應連回 `class_request_matrix`、`feature_selector_matrix` 與 `port_status_bit_matrix`。

本頁不回答：

- 每個 request 的每個欄位是否都已完成 PDF section-level verification。
- TT request field encodings 是否已完成 correctness verification。
- `SET_FEATURE` / `CLEAR_FEATURE` 是否已在本 repo 建立完整 state-transition model。

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

## Boundary Conditions for Reading This Page

- `bmRequestType` 在本頁只整理到 direction / type / recipient 層級。
- 如果 `wValue`、`wIndex` 或 `wLength` 仍以 abstract field-role name 呈現，代表本 repo 只收斂欄位角色，尚未把完整 encoding 升級成 verified truth。
- Port-recipient 與 hub-recipient requests 不得合併解讀；TT requests 只適用於具 embedded TT 的 HS hubs。

## `GET_STATUS`

**Purpose**

- Reads hub or port status and change fields.

**Direction / recipient**

- Hub: Device-to-Host, class, device recipient.
- Port: Device-to-Host, class, other recipient.

**Target**

- Hub 本身或特定 port。

**Setup-field summary**

- `bRequest`: `GET_STATUS`
- `wValue`: `0x0000`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `4`

**Governed linkage**

- Hub request maps to `wHubStatus` + `wHubChange`。
- Port request maps to `wPortStatus` + `wPortChange`。
- 目前 reviewed request surface 只涵蓋這個 request-to-status-field linkage。
- 相關 context-only selector surface 包含 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED`，作為 `GET_STATUS` comparison anchors。

**Reviewed surface**

- 本 repo 現在把 `GET_STATUS` 收斂到 hub/port status-field linkage surface。
- 這仍不宣告 returned-bit behavior、host polling strategy、debounce behavior 或 combined speed decoding correctness。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 本頁不宣告所有 returned bits 都有 bit-level verification。
- 本頁不定義 host-side polling 或 debounce behavior。

## `CLEAR_FEATURE`

**Purpose**

- Clears a hub or port feature。
- 對 change bits 來說，這代表 host 已觀察並 acknowledge 該 event，接著清除 event record。

**Direction / recipient**

- Hub: Host-to-Device, class, device recipient.
- Port: Host-to-Device, class, other recipient.

**Target**

- Hub 本身或特定 port。

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
- Port-recipient reviewed linkage 目前包含 `C_PORT_CONNECTION`、`C_PORT_ENABLE`、`C_PORT_SUSPEND`、`C_PORT_OVER_CURRENT`、`C_PORT_RESET` 這組 standard port change-selector boundary。
- Common change-bit semantics 應與 `GET_STATUS` 一起閱讀。

**Reviewed surface**

- 本 repo 現在把 `CLEAR_FEATURE` 收斂到已 reviewed 的 `C_HUB_*` / `C_PORT_*` selector-linkage surface。
- 這仍不宣告 host-side event-acknowledgement sequencing、完整 change-bit lifecycle correctness 或完整 `CLEAR_FEATURE` behavior model。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 本頁不建立完整 `CLEAR_FEATURE` state-transition model。
- 本頁不宣告所有 selectors 都已有 section-level packet verification。

## `SET_FEATURE`

**Purpose**

- Sets a hub or port feature。

**Direction / recipient**

- Hub: Host-to-Device, class, device recipient.
- Port: Host-to-Device, class, other recipient.

**Target**

- Hub 本身或特定 port。

**Setup-field summary**

- `bRequest`: `SET_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `0`

**Governed linkage**

- Hub 與 port selector namespaces 必須保持分離。
- 有些 selectors 影響 port power、reset 或 suspend behavior，但本頁仍只是 request summary。
- 這裡目前的 reviewed request surface 只到 namespace 層級：hub-recipient selectors 不得與 standard port selector range 混在一起。
- Port-recipient reviewed anchors 目前包含 `PORT_ENABLE`、`PORT_SUSPEND`、`PORT_RESET`、`PORT_POWER`。

**Reviewed surface**

- 本 repo 現在把 `SET_FEATURE` 收斂到 reviewed selector-namespace boundary：hub-recipient 與 port-recipient selector spaces 是刻意分開的。
- 這仍不宣告 power、reset、suspend 或其他 port-feature behaviors 的 selector side-effect verification。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`

**Non-claims**

- 本頁不宣告 `SET_FEATURE` side effects 已完成 correctness verification。
- 本頁不把 selector summaries 轉成 firmware control truth table。

## `GET_DESCRIPTOR`

**Purpose**

- Reads the hub class-specific descriptor。

**Direction / recipient**

- Device-to-Host, class, device recipient.

**Target**

- Hub 本身。

**Setup-field summary**

- `bRequest`: `GET_DESCRIPTOR`
- `wValue`: encodes hub descriptor type `0x29` together with the descriptor index
- `wIndex`: `0x0000`
- `wLength`: depends on hub descriptor length；本 repo 不把它硬編成單一固定常數

**Governed linkage**

- 這是 exposes `specs/hub_descriptor.md` 所整理 descriptor fields 的 request family。

**Reviewed surface**

- 本 repo 已將 class-specific `GET_DESCRIPTOR` descriptor type surface 收斂到 `0x29`。
- 這仍不宣告所有 host request-length strategy 已完成 correctness verification。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁不把 `wValue` / `wLength` encoding details 升級成 section-level verified truth。
- 本頁不宣告所有 hubs 都必須支援某種 consumer-side descriptor workflow。

## `SET_DESCRIPTOR`

**Purpose**

- Writes the hub class-specific descriptor。

**Direction / recipient**

- Host-to-Device, class, device recipient.

**Target**

- Hub 本身。

**Setup-field summary**

- `bRequest`: `SET_DESCRIPTOR`
- `wValue`: encodes hub descriptor type `0x29` together with the descriptor index
- `wIndex`: `0x0000`
- `wLength`: depends on descriptor payload size

**Governed linkage**

- 與 `GET_DESCRIPTOR` 屬於同一個 descriptor family，但不應假設所有實作都支援。

**Reviewed surface**

- 本 repo 已將 class-specific `SET_DESCRIPTOR` descriptor type surface 收斂到 `0x29`。
- 這不代表所有 hubs 都 implement `SET_DESCRIPTOR`。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁不宣告所有 hubs 都 implement `SET_DESCRIPTOR`。
- 本頁不把 descriptor-write support 升級成 normative compatibility claim。

## `CLEAR_TT_BUFFER`

**Purpose**

- Clears TT buffer-related state。

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 具 embedded TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `CLEAR_TT_BUFFER`
- `wValue`: carries TT buffer selector fields
- `wIndex`: carries TT port or related context
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，且只有在 TT-capable hubs 上才有意義。

**Reviewed surface**

- 本 repo 現在把 `wValue` 收斂到 TT buffer selector fields，而不是 arbitrary opaque value。
- `wIndex` 用來選擇 TT port 或相關 TT context。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不驗證 TT buffer field encoding correctness。
- 本頁不建立 TT state machine。

## `RESET_TT`

**Purpose**

- Resets the Transaction Translator。

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 具 embedded TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `RESET_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，並與 TT recovery / restart concerns 相關。

**Reviewed surface**

- 本 repo 現在把 `RESET_TT` 收斂到 `wValue = 0x0000`。
- `wIndex` selects the TT port or TT target instance to reset。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 reset 前後的 TT behavior 已驗證。
- 本頁不建立 split-transaction completion rules 的 correctness claims。

## `GET_TT_STATE`

**Purpose**

- Reads TT diagnostic state data。

**Direction / recipient**

- Device-to-Host, class, other recipient.

**Target**

- 具 embedded TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `GET_TT_STATE`
- `wValue`: `0x0000`
- `wIndex`: TT port or related diagnostic context
- `wLength`: TT state data length

**Governed linkage**

- Returned content 屬於 TT diagnostic surface，不應與 general port status semantics 合併。

**Reviewed surface**

- 本 repo 現在把 `wValue` 收斂到 `0x0000`。
- `wIndex` points to the TT port / diagnostic context。
- `wLength` 命名 TT state data length，但本 repo 仍不把它硬編成單一常數。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 TT state payload bit meanings 已完成 section-level verification。
- 本頁不規定 host stack 應如何 consume TT state data。

## `STOP_TT`

**Purpose**

- Stops TT split-transaction processing。

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 具 embedded TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `STOP_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，通常與 TT diagnostics 或 recovery scenarios 有關。

**Reviewed surface**

- 本 repo 現在把 `STOP_TT` 收斂到 `wValue = 0x0000`。
- `wIndex` selects the TT port or TT target instance whose split-transaction processing is being stopped。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 TT stop 之後的 downstream timing behavior。
- 本頁不建立 TT traffic control 的 correctness model。

## Governed Table Linkage Summary

- `tables/class_request_matrix.yaml`: 9 個 hub class request families 的 primary structural source。
- `tables/feature_selector_matrix.yaml`: `SET_FEATURE` / `CLEAR_FEATURE` 的 selector boundary reference。
- `tables/port_status_bit_matrix.yaml`: `GET_STATUS` 與 change-bit interpretation 的 comparison source。
- `specs/hub_descriptor.md`: `GET_DESCRIPTOR` / `SET_DESCRIPTOR` 的 descriptor-side reference page。
- `specs/transaction_translator.md`: TT request family 的 high-level semantic summary。

## Non-claims

- 本頁不是完整 setup-packet truth table。
- 本頁不是 per-request section-level USB 2.0 PDF verification record。
- 本頁不宣告 TT request field encodings 已完成 correctness verification。
- 本頁不覆蓋 consuming repos 中已確認的 project facts。
