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
> 本頁是 request-family reference summary，不是完整 SETUP packet truth table，也不是 section-level 的 PDF verification record。

## Page Purpose

本頁回答：

- USB 2.0 hub class 的 request family 有哪些。
- 每個 family 的 direction、recipient、target 與 setup field 代表什麼。
- 哪些欄位應回指 `class_request_matrix`、`feature_selector_matrix`、`port_status_bit_matrix`。

本頁不回答：

- 每一個請求欄位是否都已完成 PDF section-level verification。
- TT request 的欄位編碼是否已完整 correctness-verified。
- `SET_FEATURE` / `CLEAR_FEATURE` 是否已有完整 state-transition model。

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

- `bmRequestType` 在本頁僅整理到 direction / type / recipient 層級。
- 如果 `wValue`、`wIndex` 或 `wLength` 仍用抽象 field-role 名稱表示，代表本 repo 只完成欄位角色收斂，尚未將完整 encoding 升級為 verified truth。
- Port-recipient 與 hub-recipient requests 不可混合；TT requests 僅適用於具備 embedded TT 的 HS hubs。

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

- Hub request 對應 `wHubStatus` + `wHubChange`。
- Port request 對應 `wPortStatus` + `wPortChange`。
- 目前 reviewed request surface 只聚焦 request-to-status-field linkage。
- context-only selector surface 僅涵蓋 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED` 作為 `GET_STATUS` 比較錨點。

**Reviewed surface**

- 本 repo 已把 `GET_STATUS` 收斂到 hub / port status-field linkage。
- 仍不宣告 returned bits behavior、host polling strategy、debounce 或 speed decode correctness。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 本頁不宣告所有 returned bits 都有 bit-level verification。
- 本頁不定義 host-side polling 或 debounce behavior。

## `CLEAR_FEATURE`

**Purpose**

- Clears a hub or port feature.
- 對 change bit 而言，代表 host 已觀察並 acknowledge 該 event，接著清除 event record。

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
- Hub-recipient reviewed linkage 目前包括 `C_HUB_LOCAL_POWER` <-> `wHubChange bit 0`、`C_HUB_OVER_CURRENT` <-> `wHubChange bit 1`。
- Port-recipient reviewed linkage 目前納入 `C_PORT_CONNECTION`、`C_PORT_ENABLE`、`C_PORT_SUSPEND`、`C_PORT_OVER_CURRENT`、`C_PORT_RESET`（皆屬標準 port change-selector boundary）。
- 共同的 change-bit 解讀需與 `GET_STATUS` 一併參照。

**Reviewed surface**

- 本 repo 將 `CLEAR_FEATURE` 收斂為 reviewed selector-linkage surface，涵蓋 `C_HUB_*`、`C_PORT_*` change selectors。
- 仍不宣告 host-side event acknowledgement sequencing、完整 change-bit lifecycle correctness、或完整 `CLEAR_FEATURE` 行為模型。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 本頁不建立完整 `CLEAR_FEATURE` state-transition model。
- 本頁不宣告所有 selectors 已完成 section-level packet verification。

## `SET_FEATURE`

**Purpose**

- Sets a hub or port feature.

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

- Hub 與 port selector namespaces 保持獨立，不可混淆。
- 部分 selector 會影響 port power/reset/suspend 行為，但本頁只作 request summary。
- reviewed surface 仍為 namespace boundary：hub-recipient 與 port-recipient selector spaces 嚴格分離。
- Port-recipient reviewed anchors 目前包括 `PORT_ENABLE`、`PORT_SUSPEND`、`PORT_RESET`、`PORT_POWER`。

**Reviewed surface**

- 本 repo 將 `SET_FEATURE` 收斂為 reviewed selector namespace boundary。
- 仍不宣告 power、reset、suspend 等 selector side-effect 的 correctness 驗證。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`

**Non-claims**

- 本頁不宣告 `SET_FEATURE` side effects 已完成 correctness 驗證。
- 本頁不將 selector summaries 當作 firmware control truth table。

## `GET_DESCRIPTOR`

**Purpose**

- Reads the hub class-specific descriptor.

**Direction / recipient**

- Device-to-Host, class, device recipient.

**Target**

- Hub 本體。

**Setup-field summary**

- `bRequest`: `GET_DESCRIPTOR`
- `wValue`: combines hub descriptor type `0x29` with descriptor index
- `wIndex`: `0x0000`
- `wLength`: depends on hub descriptor length; 本 repo 不以單一固定常數硬編碼

**Governed linkage**

- 對應到 `specs/hub_descriptor.md` 的字段族群摘要。

**Reviewed surface**

- 本 repo 已將 class-specific `GET_DESCRIPTOR` 的 descriptor type surface 收斂為 `0x29`。
- 仍不宣告 host request-length strategy 的 correctness 已完成驗證。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁不將 `wValue` / `wLength` 編碼細節升級為 section-level verified truth。
- 本頁不宣告所有 hub 都支援某種 consumer-side descriptor 流程。

## `SET_DESCRIPTOR`

**Purpose**

- Writes the hub class-specific descriptor.

**Direction / recipient**

- Host-to-Device, class, device recipient.

**Target**

- Hub 本體。

**Setup-field summary**

- `bRequest`: `SET_DESCRIPTOR`
- `wValue`: combines hub descriptor type `0x29` with descriptor index
- `wIndex`: `0x0000`
- `wLength`: depends on descriptor payload size

**Governed linkage**

- 與 `GET_DESCRIPTOR` 屬於同一 descriptor family，但不應假設一定支援。

**Reviewed surface**

- 本 repo 已將 class-specific `SET_DESCRIPTOR` descriptor type surface 收斂為 `0x29`。
- 這不代表所有 hub 都實作 `SET_DESCRIPTOR`。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁不宣告所有 hub 實作 `SET_DESCRIPTOR`。
- 本頁不把 descriptor write support 提升為 normative compatibility claim。

## `CLEAR_TT_BUFFER`

**Purpose**

- Clears TT buffer-related state.

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 具備 embedded TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `CLEAR_TT_BUFFER`
- `wValue`: carries TT buffer selector fields
- `wIndex`: carries TT port or related TT context
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，僅在 TT-capable hubs 有意義。

**Reviewed surface**

- 本 repo 已將 `wValue` 收斂為 TT buffer selector fields，而非任意 opaque value。
- `wIndex` 用於選取 TT port 或 TT context。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不驗證 TT buffer 欄位編碼 correctness。
- 本頁不建立 TT state machine。

## `RESET_TT`

**Purpose**

- Resets the Transaction Translator.

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 具備 embedded TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `RESET_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，關聯 TT recovery / restart 需求。

**Reviewed surface**

- 本 repo 已將 `RESET_TT` 收斂為 `wValue = 0x0000`。
- `wIndex` 選擇 TT port 或 TT 目標實例以 reset。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 reset 前後 TT 行為已驗證。
- 本頁不建立 split-transaction completion rules 的 correctness claim。

## `GET_TT_STATE`

**Purpose**

- Reads TT diagnostic state data.

**Direction / recipient**

- Device-to-Host, class, other recipient.

**Target**

- 具備 embedded TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `GET_TT_STATE`
- `wValue`: `0x0000`
- `wIndex`: TT port 或相關 diagnostic context
- `wLength`: TT state data length

**Governed linkage**

- 回傳內容屬於 TT diagnostic surface，不應與一般 port status semantics 混用。

**Reviewed surface**

- 本 repo 已將 `wValue` 收斂為 `0x0000`。
- `wIndex` 指向 TT port / diagnostic context。
- `wLength` 為 TT state data 長度，本 repo 仍不以單一常數替代。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 TT state payload bit 意義已完成 section-level 驗證。
- 本頁不規範 host stack 如何 consume TT state data。

## `STOP_TT`

**Purpose**

- Stops TT split-transaction processing.

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 具備 embedded TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `STOP_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，通常與 TT diagnosis / recovery 場景相關。

**Reviewed surface**

- 本 repo 已將 `STOP_TT` 收斂為 `wValue = 0x0000`。
- `wIndex` 指定欲停止 split-transaction processing 的 TT port 或對象。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 TT stop 後下游 timing behavior。
- 本頁不建立 TT traffic-control 的 correctness model。

## Governed Table Linkage Summary

- `tables/class_request_matrix.yaml`: primary structural source for hub class request families。
- `tables/feature_selector_matrix.yaml`: selector boundary reference for `SET_FEATURE` / `CLEAR_FEATURE`。
- `tables/port_status_bit_matrix.yaml`: comparison source for `GET_STATUS` and change-bit interpretation。
- `specs/hub_descriptor.md`: descriptor-side reference page for `GET_DESCRIPTOR` / `SET_DESCRIPTOR`。
- `specs/transaction_translator.md`: high-level semantic summary for TT request family。

## Non-claims

- 本頁不是完整 setup-packet truth table。
- 本頁不是逐一 request 的 section-level USB 2.0 PDF verification record。
- 本頁不宣告 TT request field encodings 已完成 correctness verification。
- 本頁不覆蓋 consuming repos 的已確認 project facts。
