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

> 資料範圍：USB 2.0 Specification Rev 2.0，第 11.24.2 章節。  
> 本頁是 request family 參考摘要，不是完整 setup packet 真值表，也不是完整 section-level PDF 驗證紀錄。

## 頁面目的

本頁回答：

- USB 2.0 hub class request family 有哪些。
- 每個 family 的高階方向、recipient、目標與 setup field 角色。
- 哪些欄位應關聯到 `class_request_matrix`、`feature_selector_matrix`、`port_status_bit_matrix`。

本頁不回答：

- 每一個欄位都已在 PDF section-level 完成驗證。
- TT request 的欄位編碼已完成 correctness-verified。
- 本 repo 還沒有 `SET_FEATURE` / `CLEAR_FEATURE` 的完整 state-transition 模型。

## Request Family Overview

| bRequest | Value | Direction | Target | 高階用途 |
|---|---|---|---|---|
| `GET_STATUS` | `0x00` | Device-to-Host | Hub / Port | 讀取 hub 或 port 的 status / change 欄位 |
| `CLEAR_FEATURE` | `0x01` | Host-to-Device | Hub / Port | 清除 feature，或清除由 change bit 記錄的事件 |
| `SET_FEATURE` | `0x03` | Host-to-Device | Hub / Port | 設定 hub 或 port feature |
| `GET_DESCRIPTOR` | `0x06` | Device-to-Host | Hub | 讀取 hub class-specific descriptor |
| `SET_DESCRIPTOR` | `0x07` | Host-to-Device | Hub | 寫入 hub class-specific descriptor；是否支援依實作而定 |
| `CLEAR_TT_BUFFER` | `0x08` | Host-to-Device | TT-capable Hub | 清除 TT buffer 相關狀態 |
| `RESET_TT` | `0x09` | Host-to-Device | TT-capable Hub | 重置 Transaction Translator |
| `GET_TT_STATE` | `0x0A` | Device-to-Host | TT-capable Hub | 讀取 TT 診斷狀態 |
| `STOP_TT` | `0x0B` | Host-to-Device | TT-capable Hub | 停止 TT split-transaction 處理 |

## 閱讀本頁的邊界條件

- `bmRequestType` 只在方向 / type / recipient 層級做摘要。
- 當 `wValue`、`wIndex`、`wLength` 仍是抽象欄位角色時，本 repo 只縮窄欄位角色，尚未升級為完整編碼真值。
- hub-recipient 與 port-recipient 必須分開判讀，TT request 僅適用於具 TT 的 HS hub。

## `GET_STATUS`

**Purpose**

- 讀取 hub 或 port 的 status 及 change 欄位。

**Direction / recipient**

- Hub：Device-to-Host, class, device recipient.
- Port：Device-to-Host, class, other recipient.

**Target**

- Hub 本身或指定 port。

**Setup-field summary**

- `bRequest`: `GET_STATUS`
- `wValue`: `0x0000`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `4`

**Response format**

`GET_STATUS` 一律回傳 4 個 bytes（`wLength=4`）：

| Bytes | 欄位 | Hub recipient | Port recipient |
|---|---|---|---|
| `[1:0]` | `wStatus` | `wHubStatus` | `wPortStatus` |
| `[3:2]` | `wChange` | `wHubChange` | `wPortChange` |

`wChange` bits 會持續累積直到 host 對各 bit 發出 `CLEAR_FEATURE`。Bit 定義請見 `specs/port_status_bits.md`。

**Governed linkage**

- Hub request 對應 `wHubStatus` + `wHubChange`。
- Port request 對應 `wPortStatus` + `wPortChange`。
- 本 repo 已聚焦於 request 與 status-field 的關聯面。
- `GET_STATUS` 的 context-only selector 參照錨點包含 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED`。

**Reviewed surface**

- 已將 `GET_STATUS` 的關聯面收斂到 hub/port status-field 連結。
- 尚未聲明回傳 bit 行為、host polling 策略、debounce 行為或 speed 合併解碼的 correctness。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 不聲明所有回傳 bit 都有 bit-level 驗證。
- 不定義 host-side polling 或 debounce 行為。

## `CLEAR_FEATURE`

**Purpose**

- 清除 hub 或 port feature。
- 對 change bit 而言，表示 host 已觀察到事件並清除事件紀錄。

**Direction / recipient**

- Hub：Host-to-Device, class, device recipient.
- Port：Host-to-Device, class, other recipient.

**Target**

- Hub 本身或指定 port。

**Setup-field summary**

- `bRequest`: `CLEAR_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `0`

**Governed linkage**

- hub/port selector 空間必須分開解讀。
- Hub-recipient reviewed linkage 目前包含：
  - `C_HUB_LOCAL_POWER` <-> `wHubChange bit 0`
  - `C_HUB_OVER_CURRENT` <-> `wHubChange bit 1`
- Port-recipient reviewed linkage 目前包含：
  - `C_PORT_CONNECTION` <-> `wPortChange bit 0`
  - `C_PORT_ENABLE` <-> `wPortChange bit 1`
  - `C_PORT_SUSPEND` <-> `wPortChange bit 2`
  - `C_PORT_OVER_CURRENT` <-> `wPortChange bit 3`
  - `C_PORT_RESET` <-> `wPortChange bit 4`
- change-bit 行為需與 `GET_STATUS` 一起判讀。

**Reviewed surface**

- 已將 `CLEAR_FEATURE` 收斂為 `C_HUB_*` 與 `C_PORT_*` 變更 selector 的 boundary 參考面。
- 不聲明 host-side event acknowledge/clear 的完整序列、完整 change-bit lifecycle，或完整 `CLEAR_FEATURE` 行為模型的 correctness。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- 不建立完整 `CLEAR_FEATURE` 的 state-transition 模型。
- 不聲明所有 selector 已有 section-level packet 驗證。

## `SET_FEATURE`

**Purpose**

- 設定 hub 或 port feature。

**Direction / recipient**

- Hub：Host-to-Device, class, device recipient.
- Port：Host-to-Device, class, other recipient.

**Target**

- Hub 本身或指定 port。

**Setup-field summary**

- `bRequest`: `SET_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `0`

**Governed linkage**

- hub/port selector 空間需保持獨立。
- 部分 selector 會影響 port power、reset、suspend 行為；本頁仍保留 request 摘要層級。
- reviewed scope 僅在 namespace 層級：hub-recipient 與 port-recipient selector 空間不混用。
- Port-recipient reviewed anchors 目前包含 `PORT_ENABLE`、`PORT_SUSPEND`、`PORT_RESET`、`PORT_POWER`。
- `PORT_TEST`、`PORT_INDICATOR` 僅維持 namespace 對應 coverage，尚未聲明 test-mode 或指示燈控制 semantics。

**Reviewed surface**

- 已將 `SET_FEATURE` 收斂為 reviewed selector namespace 邊界，hub-recipient 與 port-recipient 明確分離。
- 不聲明 port power、reset、suspend 等 feature 的 side-effect 已完整 correctness-verified。

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`

**Non-claims**

- 不聲明 `SET_FEATURE` 的 side-effect 已完成 correctness 驗證。
- 不把 selector 摘要上升為 firmware control 真值表。

## `GET_DESCRIPTOR`

**Purpose**

- 讀取 hub class-specific descriptor。

**Direction / recipient**

- Device-to-Host, class, device recipient.

**Target**

- Hub 本身。

**Setup-field summary**

- `bRequest`: `GET_DESCRIPTOR`
- `wValue`: 編碼 hub descriptor type `0x29` 與 descriptor index
- `wIndex`: `0x0000`
- `wLength`: 依 hub descriptor 長度決定；本 repo 不硬編為單一固定值

**Governed linkage**

- 該 family 對應 `specs/hub_descriptor.md` 的欄位摘要。

**Reviewed surface**

- 已將 class-specific `GET_DESCRIPTOR` 的 descriptor type 範圍收斂為 `0x29`。
- 不聲明 host request-length 策略已完成 correctness 驗證。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 不將 `wValue` / `wLength` 編碼提升為 section-level verified truth。
- 不聲明所有 hub 都具備特定 descriptor workflow。

## `SET_DESCRIPTOR`

**Purpose**

- 寫入 hub class-specific descriptor。

**Direction / recipient**

- Host-to-Device, class, device recipient.

**Target**

- Hub 本身。

**Setup-field summary**

- `bRequest`: `SET_DESCRIPTOR`
- `wValue`: 編碼 hub descriptor type `0x29` 與 descriptor index
- `wIndex`: `0x0000`
- `wLength`: 依 descriptor payload 大小決定

**Governed linkage**

- 與 `GET_DESCRIPTOR` 屬於同一 descriptor family，支援與否視實作而定。

**Reviewed surface**

- 已將 class-specific `SET_DESCRIPTOR` 的 descriptor type 範圍收斂為 `0x29`。
- 不代表所有 hub 都有 `SET_DESCRIPTOR` 實作。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- 不聲明所有 hub 都支援 `SET_DESCRIPTOR`。
- 不將 descriptor 寫入能力宣告為規範相容性結論。

## `CLEAR_TT_BUFFER`

**Purpose**

- 清除 TT buffer 相關狀態。

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 具 TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `CLEAR_TT_BUFFER`
- `wValue`: TT buffer selector 欄位
- `wIndex`: TT port 或相關 context
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，僅對 TT-capable hub 有意義。

**`wValue` sub-field encoding（§11.24.2.3 Table 11-17）**

`wValue` 攜帶待清除的 TT buffer 對應 endpoint 資訊：

| bits | 欄位 | 說明 |
|---|---|---|
| `[3:0]` | Endpoint number | 待清除的 endpoint number（4 bits） |
| `[10:4]` | Device address | 目標設備的 USB address（7 bits） |
| `[12:11]` | Endpoint type | `00`=Control, `01`=Isochronous, `10`=Bulk, `11`=Interrupt |
| `[14:13]` | Reserved | 保留，應為 0 |
| `[15]` | Direction | `0`=OUT, `1`=IN |

`wIndex`：TT port 號碼（1-based；對應具體 TT 的 port number）。

**Reviewed surface**

- 已將 `wValue` 收斂為 TT buffer selector 欄位，不視為任意 opaque。
- `wIndex` 用於選擇 TT port 或 TT context。
- `wValue` sub-field encoding 為 reviewed boundary；不是 TT buffer 清除行為驗證。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 不驗證 TT buffer 欄位編碼的 correctness。
- 不建立 TT state machine。

## `RESET_TT`

**Purpose**

- 重置 Transaction Translator。

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 具 TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `RESET_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，關係到 TT 恢復 / 重啟。

**Reviewed surface**

- 已將 `RESET_TT` 收斂為 `wValue = 0x0000`。
- `wIndex` 選擇要重置的 TT port 或 TT target 實例。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 不聲明 TT reset 前後行為已全部驗證。
- 不建立 split-transaction completion 的 correctness 模型。

## `GET_TT_STATE`

**Purpose**

- 讀取 TT 診斷狀態資料。

**Direction / recipient**

- Device-to-Host, class, other recipient.

**Target**

- 具 TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `GET_TT_STATE`
- `wValue`: `0x0000`
- `wIndex`: TT port 或相關 diagnostic context
- `wLength`: TT state data length

**Governed linkage**

- 回傳內容屬於 TT diagnostic surface，不得與一般 port status semantics 混用。

**Reviewed surface**

- 已將 `wValue` 收斂為 `0x0000`。
- `wIndex` 指向 TT port 或 diagnostic context。
- `wLength` 代表 TT state data 長度，但本 repo 不將其硬編為單一常數。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 不聲明 TT state payload bit 意義已有 section-level 驗證。
- 不規定 host stack 應如何消費 TT state 資料。

## `STOP_TT`

**Purpose**

- 停止 TT split-transaction 處理。

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- 具 TT 的 HS hub。

**Setup-field summary**

- `bRequest`: `STOP_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- 屬於 TT request family，通常關聯 TT 診斷或 recovery 場景。

**Reviewed surface**

- 已將 `STOP_TT` 收斂為 `wValue = 0x0000`。
- `wIndex` 選擇 TT port / TT target 實例以停止 split-transaction。

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- 不聲明 TT 停止後的 downstream timing 行為。
- 不建立 TT 流量控制 correctness 模型。

## Governed Table Linkage Summary

- `tables/class_request_matrix.yaml`：hub class request family 的主要結構來源。
- `tables/feature_selector_matrix.yaml`：`SET_FEATURE` / `CLEAR_FEATURE` selector 邊界參考。
- `tables/port_status_bit_matrix.yaml`：`GET_STATUS` 與 change-bit 解讀對照來源。
- `specs/hub_descriptor.md`：`GET_DESCRIPTOR` / `SET_DESCRIPTOR` 的 descriptor-side 參考頁。
- `specs/transaction_translator.md`：TT request family 的高階語義參考。

## Non-claims

- 本頁不是完整 setup-packet 真值表。
- 本頁不是每個 request 的 section-level USB 2.0 PDF 驗證紀錄。
- 本頁不聲明 TT request 欄位編碼已完成 correctness 驗證。
- 本頁不將 request 摘要提升為韌體控制真值。
- 本頁不會覆蓋 consuming repo 已確認 project fact。

