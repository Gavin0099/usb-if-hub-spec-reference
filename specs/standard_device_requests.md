---
title: Standard USB Device Requests
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Standard USB Device Requests

> 來源範圍：USB 2.0 Specification Rev 2.0，§9.3 和 §9.4。  
> 本頁涵蓋所有 USB 設備（包含 hub）必須實作或確認的標準 USB 設備請求。這是 reviewed reference summary，不是 section-level 合規驗證紀錄。

## 頁面目的

本頁回答：

- USB 8-byte setup packet 的結構是什麼。
- `bmRequestType` 如何編碼方向、類型與 recipient。
- 哪些標準 USB 設備請求適用於 USB 2.0 hub。

本頁不回答：

- Hub class 專用請求（GET_STATUS hub/port、SET_FEATURE port、TT requests）—— 請見 `specs/hub_class_requests.md`。
- 任何請求是否已針對實體 hub 完成 correctness-verified。

## Setup Packet 格式

每個 USB control transfer 都以一個 8-byte setup packet 開始：

| Byte(s) | 欄位 | 說明 |
|---|---|---|
| 0 | `bmRequestType` | 編碼方向、類型與 recipient |
| 1 | `bRequest` | 請求代碼 |
| 2–3 | `wValue` | 請求相關值（little-endian）|
| 4–5 | `wIndex` | 請求相關索引（little-endian）|
| 6–7 | `wLength` | 資料階段長度（無資料時為 0）|

### `bmRequestType` 欄位分解

| Bits | 欄位 | 數值 |
|---|---|---|
| `[7]` | 資料方向 | `0` = Host→Device；`1` = Device→Host |
| `[6:5]` | 請求類型 | `00` = Standard；`01` = Class；`10` = Vendor；`11` = Reserved |
| `[4:0]` | Recipient | `00000` = Device；`00001` = Interface；`00010` = Endpoint；`00011` = Other |

標準請求常用 `bmRequestType` 值：

| 值 | 方向 | 類型 | Recipient |
|---|---|---|---|
| `0x00` | Host→Device | Standard | Device |
| `0x01` | Host→Device | Standard | Interface |
| `0x02` | Host→Device | Standard | Endpoint |
| `0x80` | Device→Host | Standard | Device |
| `0x81` | Device→Host | Standard | Interface |
| `0x82` | Device→Host | Standard | Endpoint |

> **Hub class requests** 使用 type=`01`（Class）：`0x20` / `0x23` / `0xA0` / `0xA3`。標準請求使用 type=`00`。

## 標準設備請求（§9.4）

所有 USB 設備都必須回應標準請求。下表列出所有標準 `bRequest` 代碼及其對 USB 2.0 hub 的適用性：

| `bRequest` | 值 | 方向 | Hub 適用性 |
|---|---|---|---|
| `GET_STATUS` | `0x00` | Device→Host | 必要（device、interface、endpoint）|
| `CLEAR_FEATURE` | `0x01` | Host→Device | 必要（DEVICE_REMOTE_WAKEUP、ENDPOINT_HALT）|
| `SET_FEATURE` | `0x03` | Host→Device | 必要（DEVICE_REMOTE_WAKEUP、TEST_MODE）|
| `SET_ADDRESS` | `0x05` | Host→Device | 枚舉時必要 |
| `GET_DESCRIPTOR` | `0x06` | Device→Host | 必要（device、config、string、hub class）|
| `SET_DESCRIPTOR` | `0x07` | Host→Device | 選用 |
| `GET_CONFIGURATION` | `0x08` | Device→Host | 必要 |
| `SET_CONFIGURATION` | `0x09` | Host→Device | 必要 |
| `GET_INTERFACE` | `0x0A` | Device→Host | multi-TT hub 必要（alternate settings）|
| `SET_INTERFACE` | `0x0B` | Host→Device | multi-TT hub 必要 |
| `SYNCH_FRAME` | `0x0C` | Device→Host | Hub 不適用（僅 isochronous）|

### `GET_STATUS`（標準，§9.4.5）

回傳 2 bytes 狀態（對應指定 recipient）：

- **Device recipient**（`wIndex=0x0000`）：bit 0=Self-Powered，bit 1=Remote-Wakeup-Enabled。
- **Interface recipient**（`wIndex=interface_number`）：回傳 `0x0000`（保留）。
- **Endpoint recipient**（`wIndex=endpoint_address`）：bit 0=Halt。

> 這與 hub class `GET_STATUS`（回傳 4 bytes wPortStatus/wPortChange）**不同**，兩者不可混用。

### `GET_DESCRIPTOR`（標準，§9.4.3）

`wValue` 的高 byte 是 descriptor type，低 byte 是 descriptor index：

| Descriptor Type | `wValue` 高 byte | 說明 |
|---|---|---|
| Device | `0x01` | 標準設備描述符 |
| Configuration | `0x02` | Configuration + interface + endpoint |
| String | `0x03` | 字串描述符（依 index）|
| Interface | `0x04` | 不直接請求；包含在 config set 中回傳 |
| Endpoint | `0x05` | 不直接請求 |
| Device_Qualifier | `0x06` | 僅限 HS（描述 HS 設備的 FS 行為）|
| Other_Speed_Configuration | `0x07` | 僅限 HS |
| Hub（class-specific）| `0x29` | Hub class descriptor；需使用 class-type bmRequestType |

### `SET_ADDRESS`（標準，§9.4.6）

為設備指定 USB bus 位址：

- `wValue`：新位址（1–127）。
- `wIndex`：`0x0000`。
- `wLength`：`0`。
- 此請求完成後，設備必須在下一個 transaction 開始使用新位址回應。

### `SET_CONFIGURATION` / `GET_CONFIGURATION`（§9.4.7、§9.4.2）

`SET_CONFIGURATION(bConfigurationValue)` 啟用設備的一個 configuration：
- Hub 通常使用 `bConfigurationValue=1`（單一 configuration）。
- `SET_CONFIGURATION` 後，status change interrupt endpoint 開始運作。

### `SET_INTERFACE` / `GET_INTERFACE`（§9.4.9、§9.4.4）

Multi-TT hub 用於切換 single-TT（`bAlternateSetting=0`）和 multi-TT（`bAlternateSetting=1`）模式。請見 `specs/hub_configuration.md`。

### 標準 Feature Selector（§9.4.1、§9.4.9）

標準 `SET_FEATURE` / `CLEAR_FEATURE` 使用的 feature selectors：

| Selector | 值 | Recipient | 說明 |
|---|---|---|---|
| `ENDPOINT_HALT` | `0x00` | Endpoint | 停用（stall）一個 endpoint |
| `DEVICE_REMOTE_WAKEUP` | `0x01` | Device | 啟用 remote wakeup |
| `TEST_MODE` | `0x02` | Device | 進入 USB 2.0 電氣測試模式 |

> 這些是**標準** feature selectors，不可與 hub **class** feature selectors（`PORT_POWER`、`PORT_RESET` 等）混淆。

## Governed Linkage

- `specs/hub_class_requests.md`：Hub class 專用請求（type=Class，`bmRequestType[6:5]=01`）
- `specs/standard_descriptors.md`：所有標準 USB descriptor 欄位定義
- `specs/hub_configuration.md`：multi-TT 的 hub interface alternate settings
- `specs/hub_enumeration.md`：枚舉 sequence，顯示 GET_DESCRIPTOR、SET_ADDRESS、SET_CONFIGURATION 的順序
- `tables/standard_device_request_matrix.yaml`：機器可讀的標準請求 entries

## Non-claims

- 本頁不宣告任何標準請求實作已針對實體 hub 驗證。
- 本頁不宣告 GET_STATUS（標準，2 bytes）與 GET_STATUS（hub class，4 bytes）可互換。
- 本頁不宣告 TEST_MODE 或 ENDPOINT_HALT 語意已針對 hub 完成 correctness-verified。
- 本頁不覆蓋 consuming repo 已確認的 project facts。
