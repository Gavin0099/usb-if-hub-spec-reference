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

> 資料來源：USB 2.0 Specification Rev 2.0，11.24.2 章節。  
> 本頁是請求族群參考摘要，不是完整 setup packet 真值表，也不是 section-level 的 PDF 驗證紀錄。

## 頁面目的

本頁回答：

- USB 2.0 hub class request family 有哪些。
- 各 family 的方向、recipient、target 與 setup 欄位義意。
- 需要回鏈到 `class_request_matrix`、`feature_selector_matrix`、`port_status_bit_matrix` 的欄位。

本頁不回答：

- 每個 request 的每個欄位是否已完成 PDF section-level 驗證。
- TT request 欄位 encoding 是否已完成 correctness 驗證。
- 本 repo 是否已有 `SET_FEATURE` / `CLEAR_FEATURE` 完整 state-transition 模型。

## Request Family Overview

| bRequest | Value | Direction | Target | High-Level Role |
|---|---|---|---|---|
| `GET_STATUS` | `0x00` | Device-to-Host | Hub / Port | 讀取 hub 或 port 的 status / change 欄位 |
| `CLEAR_FEATURE` | `0x01` | Host-to-Device | Hub / Port | 清除 feature，或清除 change bit 所代表的事件紀錄 |
| `SET_FEATURE` | `0x03` | Host-to-Device | Hub / Port | 設定 hub 或 port feature |
| `GET_DESCRIPTOR` | `0x06` | Device-to-Host | Hub | 讀取 hub class 特定 descriptor |
| `SET_DESCRIPTOR` | `0x07` | Host-to-Device | Hub | 寫入 hub class 特定 descriptor（是否支援由實作決定） |
| `CLEAR_TT_BUFFER` | `0x08` | Host-to-Device | TT-capable Hub | 清除 TT buffer 相關 state |
| `RESET_TT` | `0x09` | Host-to-Device | TT-capable Hub | 重設 Transaction Translator |
| `GET_TT_STATE` | `0x0A` | Device-to-Host | TT-capable Hub | 讀取 TT 診斷狀態 |
| `STOP_TT` | `0x0B` | Host-to-Device | TT-capable Hub | 停止 TT split-transaction 處理 |

## 閱讀本頁的邊界條件

- `bmRequestType` 僅以 direction / type / recipient 層級做摘要。
- 當 `wValue`、`wIndex`、`wLength` 僅呈現為欄位角色名稱而非固定常數時，本 repo 的邊界是縮到「欄位角色」而非完整 encoding 真值。
- hub-recipient 與 port-recipient 請勿合併；TT request 僅適用於含 TT 的 HS hub。

## `GET_STATUS`

**Purpose**

- 讀取 hub 或 port 的 status / change 欄位。

**Direction / recipient**

- Hub: Device-to-Host, class, device recipient.
- Port: Device-to-Host, class, other recipient.

**Target**

- hub 本身，或指定 port。

**Setup-field summary**

- `bRequest`: `GET_STATUS`
- `wValue`: `0x0000`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `4`

**Governed linkage**

- Hub request 映射到 `wHubStatus` + `wHubChange`。
- Port request 映射到 `wPortStatus` + `wPortChange`。
- 本 repo 目前已 review 的 scope 僅覆蓋 request 到 status-field 的對應關係。
- `GET_STATUS` 的 context-only selector 表面包含 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED` 作為比較錨點。

**Reviewed surface**

- 目前將 `GET_STATUS` 目前限縮為 hub/port status-field 對應層。
- 仍不主張已覆蓋 bit-level 行為、host polling 策略、debounce 或 speed 組合解碼正確性。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 本頁不主張所有回傳 bit 已完成 bit-level 驗證。
- 本頁不定義 host-side polling 或 debounce 行為。

## `CLEAR_FEATURE`

**Purpose**

- 清除 hub 或 port feature。
- 對 change bit 而言，代表 host 已觀察到事件並進行 ack，接著清除該事件紀錄。

**Direction / recipient**

- Hub: Host-to-Device, class, device recipient.
- Port: Host-to-Device, class, other recipient.

**Target**

- hub 本身，或指定 port。

**Setup-field summary**

- `bRequest`: `CLEAR_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `0`

**Governed linkage**

- hub 與 port selector namespace 必須分開解讀。
- Hub-recipient 已 review 的 linkage 包含：
  - `C_HUB_LOCAL_POWER` <-> `wHubChange bit 0`
  - `C_HUB_OVER_CURRENT` <-> `wHubChange bit 1`
- Port-recipient 已 review 的 linkage 包含標準 port change-selector:
  - `C_PORT_CONNECTION`
  - `C_PORT_ENABLE`
  - `C_PORT_SUSPEND`
  - `C_PORT_OVER_CURRENT`
  - `C_PORT_RESET`
- change-bit 行為語意需與 `GET_STATUS` 併讀。
- reviewed change selector 為 boundary-level 證據：
  - `C_PORT_CONNECTION`、`C_PORT_ENABLE`、`C_PORT_SUSPEND`、`C_PORT_OVER_CURRENT`、`C_PORT_RESET` 僅代表 host 可 ack/clear 的事件紀錄 selector。
  - 本頁不主張完整控制 state-machine、時序或錯誤恢復行為。

**Reviewed surface**

- 本 repo 將 `CLEAR_FEATURE` 縮為已 review 的 `C_HUB_*` 與 `C_PORT_*` change selector 對應層。
- 仍不主張 host 事件 ack 序列、完整 change-bit lifecycle 正確性、或完整 `CLEAR_FEATURE` 行為模型。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 本頁不建立完整 `CLEAR_FEATURE` state-transition 模型。
- 本頁不主張所有 selector 已完成 section-level packet 驗證。

## `SET_FEATURE`

**Purpose**

- 設定 hub 或 port feature。

**Direction / recipient**

- Hub: Host-to-Device, class, device recipient.
- Port: Host-to-Device, class, other recipient.

**Target**

- hub 本身，或指定 port。

**Setup-field summary**

- `bRequest`: `SET_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `0`

**Governed linkage**

- hub 與 port selector namespace 必須保持獨立。
- 部分 selector 會影響 port power / reset / suspend 行為，但本頁僅作 request summary。
- 目前 reviewed 的 request surface 僅到 namespace 級別：hub-recipient selector 不可與標準 port selector 範圍混用。
- Port-recipient 已 review anchors 包含：
  - `PORT_ENABLE`
  - `PORT_SUSPEND`
  - `PORT_RESET`
  - `PORT_POWER`
- `PORT_TEST`、`PORT_INDICATOR` 僅保留在 selector coverage 的 namespace 表面上。
  - 本頁不主張這些條目已包含完整 test-mode 或 indicator 行為 semantics。

**Reviewed surface**

- 本 repo 將 `SET_FEATURE` 縮為 reviewed 的 selector namespace 邊界：hub-recipient / port-recipient selector 空間刻意區分。
- 仍不主張已驗證 power、reset、suspend 或其他 port-feature 的 side-effect。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`

**Non-claims**

- 本頁不主張 `SET_FEATURE` side effect 已完成 correctness 驗證。
- 本頁不將 selector 清單直接等同為 firmware control 真值。

## `GET_DESCRIPTOR`

**Purpose**

- 讀取 hub class 專屬 descriptor。

**Direction / recipient**

- Device-to-Host, class, device recipient.

**Target**

- hub 本身。

**Setup-field summary**

- `bRequest`: `GET_DESCRIPTOR`
- `wValue`: 編碼 hub descriptor type `0x29` 及 descriptor index
- `wIndex`: `0x0000`
- `wLength`: 依 descriptor 長度而定；本 repo 不把它固定為單一常數

**Governed linkage**

- 本 request family 對應 `specs/hub_descriptor.md` 的欄位摘要。

**Reviewed surface**

- 本 repo 將 class-specific `GET_DESCRIPTOR` descriptor type 表面收斂到 `0x29`。
- 仍不主張 host request-length 策略已全部完成 correctness 驗證。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁不將 `wValue` / `wLength` encoding 提升為 section-level verified truth。
- 本頁不主張所有 hub 都必須支援某一條 descriptor workflow。

## `SET_DESCRIPTOR`

**Purpose**

- 寫入 hub class 專屬 descriptor。

**Direction / recipient**

- Host-to-Device, class, device recipient.

**Target**

- hub 本身。

**Setup-field summary**

- `bRequest`: `SET_DESCRIPTOR`
- `wValue`: 編碼 hub descriptor type `0x29` 及 descriptor index
- `wIndex`: `0x0000`
- `wLength`: 依 descriptor payload 大小而定

**Governed linkage**

- 與 `GET_DESCRIPTOR` 屬於同一 descriptor family；是否支援需以實作確認。

**Reviewed surface**

- 本 repo 將 class-specific `SET_DESCRIPTOR` descriptor type 表面收斂到 `0x29`。
- 不代表所有 hub 都支援 `SET_DESCRIPTOR`。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 本頁不主張所有 hub 都有 `SET_DESCRIPTOR` 實作。
- 本頁不把 descriptor 寫入支援提升為規範上可互換的兼容性宣告。

## `CLEAR_TT_BUFFER`

**Purpose**

- 清除 TT buffer 相關 state。

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 含 TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `CLEAR_TT_BUFFER`
- `wValue`: TT buffer selector 欄位
- `wIndex`: TT port 或 TT context
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，且只在具 TT 能力的 hub 有意義。

**Reviewed surface**

- 本 repo 將 `wValue` 限縮為 TT buffer selector 欄位，不再將其視為任意不透明值。
- `wIndex` 用於選擇 TT port 或相關 TT context。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不驗證 TT buffer 欄位 encoding 的 correctness。
- 本頁不建立 TT state-machine。

## `RESET_TT`

**Purpose**

- 重設 Transaction Translator。

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 含 TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `RESET_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，與 TT recovery / restart 相關。

**Reviewed surface**

- 本 repo 將 `RESET_TT` 收斂為 `wValue = 0x0000`。
- `wIndex` 選擇要 reset 的 TT port 或 TT target 實例。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不主張 TT 重設前後行為已完成驗證。
- 本頁不建立 split-transaction completion 規則的 correctness 結論。

## `GET_TT_STATE`

**Purpose**

- 讀取 TT 診斷狀態。

**Direction / recipient**

- Device-to-Host, class, other recipient.

**Target**

- 含 TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `GET_TT_STATE`
- `wValue`: `0x0000`
- `wIndex`: TT port 或診斷 context
- `wLength`: TT state data length

**Governed linkage**

- 回傳內容屬於 TT 診斷 surface，不與一般 port status semantics 混用。

**Reviewed surface**

- 本 repo 將 `wValue` 收斂為 `0x0000`。
- `wIndex` 指向 TT port / diagnostic context。
- `wLength` 表示 TT state 資料長度，本 repo 仍不將其硬編為單一常數。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不主張 TT state payload bit 意涵已有 section-level 驗證。
- 本頁不規定 host stack 應如何消費 TT state 資料。

## `STOP_TT`

**Purpose**

- 停止 TT split-transaction 處理。

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 含 TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `STOP_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，通常與 TT 診斷或 recovery 情境相關。

**Reviewed surface**

- 本 repo 將 `STOP_TT` 收斂為 `wValue = 0x0000`。
- `wIndex` 選擇要停止 split-transaction 處理的 TT port 或 TT target 實例。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 本頁不主張 TT stop 後的下游時序行為。
- 本頁不建立 TT 流量控制 correctness 模型。

## Governed Table Linkage Summary

- `tables/class_request_matrix.yaml`：9 個 hub class request family 的主要結構來源。
- `tables/feature_selector_matrix.yaml`：`SET_FEATURE` / `CLEAR_FEATURE` selector boundary 參考。
- `tables/port_status_bit_matrix.yaml`：`GET_STATUS` 對應與 change-bit 解讀來源。
- `specs/hub_descriptor.md`：`GET_DESCRIPTOR` / `SET_DESCRIPTOR` 的 descriptor-side 參考頁。
- `specs/transaction_translator.md`：TT request family 的高階語意摘要。

## Non-claims

- 本頁不是完整 setup-packet 真值表。
- 本頁不是每個 request 的 section-level USB 2.0 PDF 驗證紀錄。
- 本頁不主張 TT request 欄位 encoding 已 correctness 驗證。
- 本頁不覆蓋 consuming repo 已確認的 project facts。
