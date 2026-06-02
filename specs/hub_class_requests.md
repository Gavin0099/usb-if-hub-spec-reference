---
title: Hub 類別請求
claim_level: inferred
status: review_required
last_reviewed: "2026-06-02"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub 類別請求

> 來源範圍：USB 2.0 Specification Rev 2.0，Section 11.24.2。
> 本頁是 request-family reference summary，不是完整 SETUP packet truth table，也不是 section-level PDF 驗證紀錄。

## 頁面用途

本頁回答的問題是：

- USB 2.0 hub class request 有哪些 request family。
- 每個 family 的方向、recipient、target 與高層 setup-field 意義。
- 哪些欄位應該連回 `class_request_matrix`、`feature_selector_matrix`、`port_status_bit_matrix`。

本頁不回答的問題是：

- 每個 request 的所有欄位是否已完成 PDF section-level 驗證。
- TT request 的欄位編碼是否已完成 correctness verification。
- `SET_FEATURE` / `CLEAR_FEATURE` 是否已建立完整狀態轉移模型。

## Request Families 總覽

| bRequest | 值 | 方向 | Target | 高層角色 |
|---|---|---|---|---|
| `GET_STATUS` | `0x00` | Device-to-Host | Hub / Port | 讀取 hub 或 port 的 status/change 欄位 |
| `CLEAR_FEATURE` | `0x01` | Host-to-Device | Hub / Port | 清除 feature，或清除由 change bit 表示的事件紀錄 |
| `SET_FEATURE` | `0x03` | Host-to-Device | Hub / Port | 設定 hub 或 port feature |
| `GET_DESCRIPTOR` | `0x06` | Device-to-Host | Hub | 讀取 hub class-specific descriptor |
| `SET_DESCRIPTOR` | `0x07` | Host-to-Device | Hub | 寫入 hub class-specific descriptor；是否支援依實作而定 |
| `CLEAR_TT_BUFFER` | `0x08` | Host-to-Device | TT-capable Hub | 清除 TT buffer 相關狀態 |
| `RESET_TT` | `0x09` | Host-to-Device | TT-capable Hub | 重設 Transaction Translator |
| `GET_TT_STATE` | `0x0A` | Device-to-Host | TT-capable Hub | 讀取 TT 診斷狀態 |
| `STOP_TT` | `0x0B` | Host-to-Device | TT-capable Hub | 停止 TT split transaction 處理 |

## 讀這頁前先掌握的邊界

- `bmRequestType` 在本頁只做 direction / type / recipient 的高層摘要。
- `wValue`、`wIndex`、`wLength` 若仍標記為 `spec_defined`，代表本 repo 尚未做 section-level field verification。
- Port recipient 與 hub recipient 不能混用；TT requests 只適用於含 TT 的 HS hub。

## `GET_STATUS`

**Purpose**

- 讀取 hub 或 port 的 status 與 change 欄位。

**Direction / recipient**

- Hub：Device-to-Host，class，device recipient。
- Port：Device-to-Host，class，other recipient。

**Target**

- Hub 本體或指定 port。

**Setup-field summary**

- `bRequest`: `GET_STATUS`
- `wValue`: `0x0000`
- `wIndex`:
  - Hub request：`0x0000`
  - Port request：`port_number`
- `wLength`: `4`

**Governed linkage**

- Hub request 對應 `wHubStatus` + `wHubChange`。
- Port request 對應 `wPortStatus` + `wPortChange`。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 本頁不宣告所有 returned bits 都已完成 bit-level verification。
- 本頁不建立 host 端 polling 或 debounce 行為模型。

## `CLEAR_FEATURE`

**Purpose**

- 清除 hub 或 port feature。
- 對 change bits 來說，表示 host 已讀取並確認該事件，現在清除事件紀錄。

**Direction / recipient**

- Hub：Host-to-Device，class，device recipient。
- Port：Host-to-Device，class，other recipient。

**Target**

- Hub 本體或指定 port。

**Setup-field summary**

- `bRequest`: `CLEAR_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request：`0x0000`
  - Port request：`port_number`
- `wLength`: `0`

**Governed linkage**

- Hub/Port selector 要分開解讀。
- 對 change bits 的常見語意，需與 `GET_STATUS` 一起閱讀。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 本頁不建立完整 `CLEAR_FEATURE` 狀態轉移模型。
- 本頁不宣告所有 selector 都已做 section-level packet verification。

## `SET_FEATURE`

**Purpose**

- 設定 hub 或 port feature。

**Direction / recipient**

- Hub：Host-to-Device，class，device recipient。
- Port：Host-to-Device，class，other recipient。

**Target**

- Hub 本體或指定 port。

**Setup-field summary**

- `bRequest`: `SET_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request：`0x0000`
  - Port request：`port_number`
- `wLength`: `0`

**Governed linkage**

- Hub/Port selector namespace 必須分開。
- 某些 selector 會直接影響 port power、reset 或 suspend 相關行為，但本頁只做 request summary。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`

**Non-claims**

- 本頁不宣告 `SET_FEATURE` 的行為副作用已完成 correctness verification。
- 本頁不把 selector summary 升級為 firmware control truth table。

## `GET_DESCRIPTOR`

**Purpose**

- 讀取 hub class-specific descriptor。

**Direction / recipient**

- Device-to-Host，class，device recipient。

**Target**

- Hub 本體。

**Setup-field summary**

- `bRequest`: `GET_DESCRIPTOR`
- `wValue`: encodes descriptor type 與 descriptor index；在本 repo 中仍屬 `spec_defined`
- `wIndex`: `0x0000`
- `wLength`: 依 descriptor size 而定；目前仍屬 `spec_defined`

**Governed linkage**

- 這是讀取 `specs/hub_descriptor.md` 所描述欄位的入口 request family。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁不把 `wValue` / `wLength` 的實際編碼升級為 section-level verified truth。
- 本頁不宣告所有 hub 都必須支援某種 consumer-side descriptor workflow。

## `SET_DESCRIPTOR`

**Purpose**

- 寫入 hub class-specific descriptor。

**Direction / recipient**

- Host-to-Device，class，device recipient。

**Target**

- Hub 本體。

**Setup-field summary**

- `bRequest`: `SET_DESCRIPTOR`
- `wValue`: encodes descriptor type 與 descriptor index；目前仍屬 `spec_defined`
- `wIndex`: `0x0000`
- `wLength`: 依 payload size 而定；目前仍屬 `spec_defined`

**Governed linkage**

- 與 `GET_DESCRIPTOR` 同屬 hub descriptor family，但支援性不應預設。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁不宣告 `SET_DESCRIPTOR` 在所有 hub 上都被實作。
- 本頁不把 descriptor write support 升級成 normative compatibility claim。

## `CLEAR_TT_BUFFER`

**Purpose**

- 清除 TT buffer 相關狀態。

**Direction / recipient**

- Host-to-Device，class，other recipient。

**Target**

- 含內建 TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `CLEAR_TT_BUFFER`
- `wValue`: carries TT-related encoded fields；目前仍屬 `spec_defined`
- `wIndex`: carries TT port / context；目前仍屬 `spec_defined`
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，僅對 TT-capable hub 有意義。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不驗證 TT buffer 欄位編碼 correctness。
- 本頁不建立 TT state machine。

## `RESET_TT`

**Purpose**

- 重設 Transaction Translator。

**Direction / recipient**

- Host-to-Device，class，other recipient。

**Target**

- 含內建 TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `RESET_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port / context；目前仍屬 `spec_defined`
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，與 TT recovery / restart 類問題相關。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 reset 前後的 TT 行為已完成驗證。
- 本頁不建立 split transaction completion 規則的 correctness claim。

## `GET_TT_STATE`

**Purpose**

- 讀取 TT 診斷狀態資料。

**Direction / recipient**

- Device-to-Host，class，other recipient。

**Target**

- 含內建 TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `GET_TT_STATE`
- `wValue`: `0x0000`
- `wIndex`: TT port / context；目前仍屬 `spec_defined`
- `wLength`: TT state data length；目前仍屬 `spec_defined`

**Governed linkage**

- 回傳內容屬於 TT diagnostic surface，不應和一般 port status 混讀。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 TT state payload 的位元語意已完成 section-level verification。
- 本頁不提供 host stack 應如何消費 TT state 的行為建議。

## `STOP_TT`

**Purpose**

- 停止 TT split transaction 處理。

**Direction / recipient**

- Host-to-Device，class，other recipient。

**Target**

- 含內建 TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `STOP_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port / context；目前仍屬 `spec_defined`
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，與 TT 診斷或 recovery 情境相關。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不宣告 TT 停止後的 downstream timing 行為。
- 本頁不建立 TT traffic control 的 correctness model。

## Governed Table Linkage 摘要

- `tables/class_request_matrix.yaml`：9 個 hub class request family 的主要結構來源。
- `tables/feature_selector_matrix.yaml`：`SET_FEATURE` / `CLEAR_FEATURE` 的 selector 邊界。
- `tables/port_status_bit_matrix.yaml`：`GET_STATUS` 與 change-bit 解讀的對照來源。
- `specs/hub_descriptor.md`：`GET_DESCRIPTOR` / `SET_DESCRIPTOR` 的 descriptor-side 參照頁。
- `specs/transaction_translator.md`：TT request family 的高層語意摘要。

## Non-claims

- 本頁不是完整 setup packet truth table。
- 本頁不是 USB 2.0 PDF 的逐 request section-level 驗證紀錄。
- 本頁不宣告 TT requests 的欄位編碼 correctness 已完成。
- 本頁不覆寫 consuming repo 的 confirmed project facts。
