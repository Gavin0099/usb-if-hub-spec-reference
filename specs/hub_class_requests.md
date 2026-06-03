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
> 本頁是 request-family reference summary，不是完整的 SETUP packet truth table，也不是 section-level PDF verification record。

## Page Purpose

本頁回答：

- USB 2.0 hub class request families 有哪些
- 每個 family 的高層 direction、recipient、target 與 setup-field meaning
- 哪些欄位應回連到 `class_request_matrix`、`feature_selector_matrix`、`port_status_bit_matrix`

本頁不回答：

- 每個 request 的每個欄位是否都已完成 PDF section-level verification
- TT request field encodings 是否已完成 correctness verification
- `SET_FEATURE` / `CLEAR_FEATURE` 是否已在本 repo 建立完整 state-transition model

## Request Family Overview

| bRequest | Value | Direction | Target | High-Level Role |
|---|---|---|---|---|
| `GET_STATUS` | `0x00` | Device-to-Host | Hub / Port | 讀取 hub 或 port 的 status/change fields |
| `CLEAR_FEATURE` | `0x01` | Host-to-Device | Hub / Port | 清除 feature，或清除由 change bit 代表的事件記錄 |
| `SET_FEATURE` | `0x03` | Host-to-Device | Hub / Port | 設定 hub 或 port features |
| `GET_DESCRIPTOR` | `0x06` | Device-to-Host | Hub | 讀取 hub class-specific descriptor |
| `SET_DESCRIPTOR` | `0x07` | Host-to-Device | Hub | 寫入 hub class-specific descriptor；是否支援取決於實作 |
| `CLEAR_TT_BUFFER` | `0x08` | Host-to-Device | TT-capable Hub | 清除 TT buffer 相關狀態 |
| `RESET_TT` | `0x09` | Host-to-Device | TT-capable Hub | 重置 Transaction Translator |
| `GET_TT_STATE` | `0x0A` | Device-to-Host | TT-capable Hub | 讀取 TT diagnostic state |
| `STOP_TT` | `0x0B` | Host-to-Device | TT-capable Hub | 停止 TT split-transaction processing |

## Boundary Conditions for Reading This Page

- `bmRequestType` 在本頁只摘要到 direction / type / recipient 層級
- 若 `wValue`、`wIndex`、`wLength` 仍標記為 `spec_defined`，表示本 repo 尚未完成這些欄位的 section-level verification
- port-recipient、hub-recipient 與 TT requests 不能混讀；TT requests 只適用於內嵌 TT 的 HS hubs

## `GET_STATUS`

**Purpose**

- 讀取 hub 或 port 的 status 與 change fields

**Direction / recipient**

- Hub: Device-to-Host, class, device recipient.
- Port: Device-to-Host, class, other recipient.

**Target**

- Hub 本體或特定 port

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

- 本頁不宣告所有 returned bits 都已完成 bit-level verification
- 本頁不定義 host-side polling 或 debounce behavior

## `CLEAR_FEATURE`

**Purpose**

- 清除 hub 或 port feature
- 對 change bits 而言，表示 host 已觀察並 acknowledge 該事件，現在要清除事件記錄

**Direction / recipient**

- Hub: Host-to-Device, class, device recipient.
- Port: Host-to-Device, class, other recipient.

**Target**

- Hub 本體或特定 port

**Setup-field summary**

- `bRequest`: `CLEAR_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `0`

**Governed linkage**

- Hub 與 port selector spaces 必須分開解讀
- 常見 change-bit semantics 應和 `GET_STATUS` 一起閱讀

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 本頁不建立完整的 `CLEAR_FEATURE` state-transition model
- 本頁不宣告所有 selectors 都已完成 section-level packet verification

## `SET_FEATURE`

**Purpose**

- 設定 hub 或 port feature

**Direction / recipient**

- Hub: Host-to-Device, class, device recipient.
- Port: Host-to-Device, class, other recipient.

**Target**

- Hub 本體或特定 port

**Setup-field summary**

- `bRequest`: `SET_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `0`

**Governed linkage**

- Hub 與 port selector namespaces 必須維持區分
- 某些 selectors 會影響 port power、reset 或 suspend behavior，但本頁仍只是 request summary

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`

**Non-claims**

- 本頁不宣告 `SET_FEATURE` side effects 已完成 correctness verification
- 本頁不把 selector summaries 升級成 firmware control truth table

## `GET_DESCRIPTOR`

**Purpose**

- 讀取 hub class-specific descriptor

**Direction / recipient**

- Device-to-Host, class, device recipient.

**Target**

- Hub 本體

**Setup-field summary**

- `bRequest`: `GET_DESCRIPTOR`
- `wValue`: 編碼 hub descriptor type `0x29` 與 descriptor index
- `wIndex`: `0x0000`
- `wLength`: 依 hub descriptor length 而定；本 repo 不把它硬寫成單一固定常數

**Governed linkage**

- 這個 request family 會暴露 `specs/hub_descriptor.md` 摘要的那些欄位

**Reviewed surface**

- 本 repo 已收斂到：hub class-specific `GET_DESCRIPTOR` 的 descriptor type 是 `0x29`
- 仍未在本 repo 內宣告每一種 host request length 策略都已完成 correctness verification

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁不把 `wValue` / `wLength` encoding details 升成 section-level verified truth
- 本頁不宣告所有 hubs 都必須支援某種 consumer-side descriptor workflow

## `SET_DESCRIPTOR`

**Purpose**

- 寫入 hub class-specific descriptor

**Direction / recipient**

- Host-to-Device, class, device recipient.

**Target**

- Hub 本體

**Setup-field summary**

- `bRequest`: `SET_DESCRIPTOR`
- `wValue`: 編碼 hub descriptor type `0x29` 與 descriptor index
- `wIndex`: `0x0000`
- `wLength`: 依 descriptor payload size 而定

**Governed linkage**

- 與 `GET_DESCRIPTOR` 同屬 descriptor family，但不能預設一定支援

**Reviewed surface**

- 本 repo 已收斂到：若討論 hub class-specific `SET_DESCRIPTOR`，descriptor type surface 仍是 `0x29`
- 這不等於宣告所有 hubs 都支援 `SET_DESCRIPTOR`

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁不宣告所有 hubs 都實作 `SET_DESCRIPTOR`
- 本頁不把 descriptor-write support 升級成 normative compatibility claim

## `CLEAR_TT_BUFFER`

**Purpose**

- 清除 TT buffer 相關狀態

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 內嵌 TT 的 HS hub

**Setup-field summary**

- `bRequest`: `CLEAR_TT_BUFFER`
- `wValue`: 帶有 TT-related encoded fields；仍為 `spec_defined`
- `wIndex`: 帶有 TT port / context；仍為 `spec_defined`
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，只對 TT-capable hubs 有意義

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不驗證 TT buffer field encoding correctness
- 本頁不建立 TT state machine

## `RESET_TT`

**Purpose**

- 重置 Transaction Translator

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 內嵌 TT 的 HS hub

**Setup-field summary**

- `bRequest`: `RESET_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port / context；仍為 `spec_defined`
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，並與 TT recovery / restart concerns 有關

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 reset 前後的 TT behavior 已驗證
- 本頁不建立 split-transaction completion rules 的 correctness claim

## `GET_TT_STATE`

**Purpose**

- 讀取 TT diagnostic state data

**Direction / recipient**

- Device-to-Host, class, other recipient.

**Target**

- 內嵌 TT 的 HS hub

**Setup-field summary**

- `bRequest`: `GET_TT_STATE`
- `wValue`: `0x0000`
- `wIndex`: TT port / context；仍為 `spec_defined`
- `wLength`: TT state data length；仍為 `spec_defined`

**Governed linkage**

- 回傳內容屬於 TT diagnostic surface，不應與一般 port status semantics 混讀

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 TT state payload bit meanings 已完成 section-level verification
- 本頁不規定 host stack 應如何消費 TT state data

## `STOP_TT`

**Purpose**

- 停止 TT split-transaction processing

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 內嵌 TT 的 HS hub

**Setup-field summary**

- `bRequest`: `STOP_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port / context；仍為 `spec_defined`
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，通常和 TT diagnostics 或 recovery scenarios 相關

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 TT stop 之後的 downstream timing behavior
- 本頁不建立 TT traffic control 的 correctness model

## Governed Table Linkage Summary

- `tables/class_request_matrix.yaml`: 9 個 hub class request families 的主要結構來源
- `tables/feature_selector_matrix.yaml`: `SET_FEATURE` / `CLEAR_FEATURE` 的 selector boundary reference
- `tables/port_status_bit_matrix.yaml`: `GET_STATUS` 與 change-bit interpretation 的 comparison source
- `specs/hub_descriptor.md`: `GET_DESCRIPTOR` / `SET_DESCRIPTOR` 的 descriptor-side reference page
- `specs/transaction_translator.md`: TT request family 的高層 semantic summary

## Non-claims

- 本頁不是完整的 setup-packet truth table
- 本頁不是逐 request 的 section-level USB 2.0 PDF verification record
- 本頁不宣告 TT request field encodings 已完成 correctness verification
- 本頁不覆蓋 consuming repos 中已確認的 project facts
