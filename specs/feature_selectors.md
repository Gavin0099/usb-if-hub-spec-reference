---
title: Feature Selectors
claim_level: inferred
status: review_required
last_reviewed: "2026-06-05"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Feature Selectors

> 來源範圍：USB 2.0 Specification Rev 2.0，Section 11.24.2。  
> 本頁是 `SET_FEATURE` / `CLEAR_FEATURE` selector namespace 的參考摘要，不是完整 control truth table，也不是 section-level PDF 驗證紀錄。

## 頁面用途

本頁回答：

- USB 2.0 hub request space 中有哪些 feature selector；
- 哪些 selector 屬於 hub recipient、哪些屬於 port recipient；
- 為什麼 `0-22` 是 E-05 的標準 port selector 邊界；
- 哪些 selector 主要出現在 `SET_FEATURE`、`CLEAR_FEATURE` 或 `GET_STATUS` 的上下文。

本頁不回答：

- selector 是否都已完成 PDF section-level verification；
- selector side effect 是否完整 correctness 驗證；
- `SET_FEATURE` / `CLEAR_FEATURE` 的完整 state-transition model。

## 閱讀前邊界

- Hub selector 與 port selector 可能重複編碼值，但使用不同 recipient，不可合併。
- E-05 僅限定 vendor command selectors 不重疊標準 port selector `0-22` 範圍。
- 某些 matrix entry 僅作為 `GET_STATUS` context，不應被誤讀為直接可設置目標。

## Namespace Summary

| Namespace | Range | Recipient | Meaning |
|---|---:|---|---|
| Hub change selectors | `0-1` | device | hub-recipient `CLEAR_FEATURE` 所用 |
| Port standard selectors | `0-22` | other | E-05 標準範圍；vendor selector 不得重疊 |

## Hub Selectors

目前 matrix 目前收錄：

| Value | Name | Main Use |
|---:|---|---|
| `0` | `C_HUB_LOCAL_POWER` | 清除 hub local power change condition |
| `1` | `C_HUB_OVER_CURRENT` | 清除 hub over-current change condition |

這些 selector：

- 僅以 hub recipient 解讀
- 主要屬於 `CLEAR_FEATURE` family
- 不要合併進 port selector namespace

## reviewed linkage surface（本 repo）

- `PORT_CONNECTION` <-> `wPortStatus bit 0`（僅作 `GET_STATUS` context）
- `PORT_OVER_CURRENT` <-> `wPortStatus bit 3`（僅作 `GET_STATUS` context）
- `PORT_LOW_SPEED` <-> `wPortStatus` speed 指示（僅作 `GET_STATUS` context）
- `PORT_HIGH_SPEED` <-> `wPortStatus` speed 指示（僅作 `GET_STATUS` context）
- `reserved` slot `5-7`、`11-15` 僅為 reserved-boundary
- `C_HUB_LOCAL_POWER` <-> `wHubChange bit 0`
- `C_HUB_OVER_CURRENT` <-> `wHubChange bit 1`
- `C_PORT_CONNECTION` <-> `wPortChange bit 0`（事件變更位元）
- `C_PORT_ENABLE` <-> `wPortChange bit 1`（事件變更位元）
- `C_PORT_SUSPEND` <-> `wPortChange bit 2`（事件變更位元）
- `C_PORT_OVER_CURRENT` <-> `wPortChange bit 3`（事件變更位元）
- `C_PORT_RESET` <-> `wPortChange bit 4`（事件變更位元）
- `PORT_ENABLE` <-> `PORT_ENABLE` selector boundary
- `PORT_SUSPEND` <-> `PORT_SUSPEND` selector boundary
- `PORT_RESET` <-> `PORT_RESET` selector boundary
- `PORT_POWER` <-> `PORT_POWER` selector boundary
- `PORT_TEST` <-> `PORT_TEST` selector boundary
- `PORT_INDICATOR` <-> `PORT_INDICATOR` selector boundary

`PORT_*` 與 `C_PORT_*` 的 selector boundary 僅是邊界層描述，不代表完整 host 行為或 selector side-effect。

- `PORT_CONNECTION`
  - selector 值表示 port connection 概念；不主張完整 connect/disconnect 行為
- `PORT_OVER_CURRENT`
  - 在 status context 表示過流；`C_PORT_OVER_CURRENT` 為 change-selector acknowledge 路徑
  - 不延伸至 recovery policy / timing
- `PORT_TEST` / `PORT_INDICATOR`
  - 目前仍為 selector boundary-only；不作為 test-mode 或 indicator 行為驗證
- `C_PORT_CONNECTION`、`C_PORT_ENABLE`、`C_PORT_SUSPEND`、`C_PORT_OVER_CURRENT`、`C_PORT_RESET`
  - 僅作 change selector（事件 ack/clear 對應），不宣告時序真值

## In-Practice Alignment

`PORT_*` 與 `C_PORT_*` 在本 repo 與 `specs/port_status_bits.md` 的 request-linkage 對應：

- `PORT_*`：`wPortStatus` 狀態欄位的 role mapping
- `C_PORT_*`：`wPortChange` 變更/事件欄位的 role mapping

## Port Standard Selector Boundary (`0-22`)

`tables/feature_selector_matrix.yaml` 目前收錄標準 port selector 範圍 `0-22`。  
此為 E-05 核心邊界：vendor-defined selector 不可重疊此範圍。

示例欄位：

| Value | Name | Common Context |
|---:|---|---|
| `0` | `PORT_CONNECTION` | `GET_STATUS` context |
| `1` | `PORT_ENABLE` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `2` | `PORT_SUSPEND` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `3` | `PORT_OVER_CURRENT` | `GET_STATUS` context |
| `4` | `PORT_RESET` | `SET_FEATURE` |
| `5-7` | reserved | reserved standard-range slots |
| `8` | `PORT_POWER` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `9` | `PORT_LOW_SPEED` | `GET_STATUS` context |
| `10` | `PORT_HIGH_SPEED` | `GET_STATUS` context |
| `11-15` | reserved | reserved standard-range slots |
| `16` | `C_PORT_CONNECTION` | `CLEAR_FEATURE` change selector |
| `17` | `C_PORT_ENABLE` | `CLEAR_FEATURE` change selector |
| `18` | `C_PORT_SUSPEND` | `CLEAR_FEATURE` change selector |
| `19` | `C_PORT_OVER_CURRENT` | `CLEAR_FEATURE` change selector |
| `20` | `C_PORT_RESET` | `CLEAR_FEATURE` change selector |
| `21` | `PORT_TEST` | `SET_FEATURE` |
| `22` | `PORT_INDICATOR` | `SET_FEATURE` |

## Defined / Reserved / Context-Only

本 repo 目前將 selector 分為三種閱讀層級：

- **defined selector**：矩陣中明確列出名稱與 role 的 selector
- **reserved selector**：保留但仍在標準範圍，不能被視為一般使用 selector
- **context-only selector**：為了完成 namespace 或 `GET_STATUS` 對照加入，不代表可直接做 feature set/clear 操作

## Relationship to Request Families

- `SET_FEATURE` / `CLEAR_FEATURE` 的 `wValue` 應對應 `tables/feature_selector_matrix.yaml`
- `GET_STATUS` 本身不直接設定 selector，但 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED` 目前有 reviewed context-only 的 `status-field` 對照
- `C_PORT_*` 應搭配 `specs/port_status_bits.md` 的 change bits 一起解讀
- `PORT_*`、`C_HUB_*`、`C_PORT_*` 的 reviewed linkage 僅為 boundary，不構成 `SET_FEATURE` 或 `CLEAR_FEATURE` 行為證據
- `PORT_TEST` 與 `PORT_INDICATOR` 雖有 selector slot reviewed，但仍不作為 test-mode / indicator 行為驗證

## `PORT_TEST` 測試模式編碼（`wIndex` 高位元組）

> 來源：§11.24.2.13 / Table 11-20。Reviewed boundary only；非測試模式電氣或合規驗證。

發送 `SET_FEATURE(PORT_TEST)` 時，測試模式由 `wIndex[15:8]` 指定：

| `wIndex[15:8]` | 名稱 | 說明 |
|---:|---|---|
| `0x00` | Reserved | |
| `0x01` | Test_J | J-state 靜態測試 |
| `0x02` | Test_K | K-state 靜態測試 |
| `0x03` | Test_SE0_NAK | SE0 NAK 測試 |
| `0x04` | Test_Packet | 測試封包傳送 |
| `0x05` | Test_Force_Enable | 強制 port enable |
| `0x06–0xFF` | Reserved | |

本表僅記錄 selector 編碼 identity，不驗證測試模式電氣行為、合規測試程序或設備回應。

## `PORT_INDICATOR` 指示燈顏色編碼（`wIndex` 高位元組）

> 來源：§11.24.2.7.1.1 / Table 11-20。Reviewed boundary only；非指示燈硬體或政策驗證。

發送 `SET_FEATURE(PORT_INDICATOR)` 時，指示燈顏色由 `wIndex[15:8]` 指定：

| `wIndex[15:8]` | 顏色 | 說明 |
|---:|---|---|
| `0x00` | Off | 指示燈關閉 |
| `0x01` | Amber | 琥珀色 |
| `0x02` | Green | 綠色 |
| `0x03` | Undefined | 軟體自定義；USB 2.0 spec 未定義含義 |

本表僅記錄編碼 identity，不驗證指示燈硬體支援、政策或 hub 是否實際實作指示燈控制。

## Governed Linkage

- `tables/feature_selector_matrix.yaml`：selector namespace 的主要 machine-readable source
- `specs/hub_class_requests.md`：`SET_FEATURE` / `CLEAR_FEATURE` request-family 摘要
- `specs/port_status_bits.md`：`GET_STATUS` 與 change bits、`CLEAR_FEATURE` 的關聯
- `specs/port_feature_change_vocabulary.md`：`PORT_*` / `C_PORT_*` 詞彙對齊頁
- `specs/escalation_table.md`：E-05 相關 escalation trigger 參考

## Non-claims

- 本頁不宣告 `0-22` selector 值逐一完成 PDF section-level verification
- 本頁不宣告 selector side effect correctness
- 本頁不宣告 `SET_FEATURE` / `CLEAR_FEATURE` 的 request 成功/失敗、時序與復原行為
- 本頁不將 selector 摘要提升為 firmware 實作權威
- 本頁不覆寫 consuming repo 的確認專案事實
