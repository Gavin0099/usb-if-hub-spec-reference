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

> 來源範圍：USB 2.0 規範 Rev 2.0，11.24.2 章節。  
> 本頁為 `SET_FEATURE` / `CLEAR_FEATURE` selector 命名空間的參考摘要，不是完整控制真值表，也不是 section-level PDF 驗證記錄。

## 頁面目的

本頁回答：

- USB 2.0 hub request 空間中有哪些 feature selector。
- 哪些 selector 屬於 hub recipient，哪些屬於 port recipient。
- 為什麼 `0-22` 是 E-05 的標準 port selector 邊界。
- 哪些 selector 主要出現在 `SET_FEATURE`、`CLEAR_FEATURE` 或 `GET_STATUS` 的上下文解讀中。

本頁不回答：

- 每個 selector 是否都已完成 PDF 章節級驗證。
- 每個 selector 的 side effect 是否都完成 correctness 驗證。
- `SET_FEATURE` / `CLEAR_FEATURE` 的完整 state-transition 模型。

## 先決邊界

- Hub selector 與 port selector 可能有相同數值，但 recipient 不同，不能混用。
- E-05 僅規範**廠商命令 selector 不得落在標準 port selector 範圍 `0-22`**。
- 有些 matrix entry 僅作為 `GET_STATUS` context，不能直接解讀為可設定（set）目標。

## 命名空間摘要

| Namespace | Range | Recipient | 意義 |
|---|---:|---|---|
| Hub change selectors | `0-1` | device | 供 `CLEAR_FEATURE` 的 hub-recipient 請求使用 |
| Port standard selectors | `0-22` | other | E-05 標準範圍；廠商 selector 不可與此重疊 |

## Hub Selectors

目前 matrix 包含下列 hub selector：

| Value | Name | 主要用途 |
|---:|---|---|
| `0` | `C_HUB_LOCAL_POWER` | 清除 hub local power change condition |
| `1` | `C_HUB_OVER_CURRENT` | 清除 hub 過電流 change condition |

這些 selector 的使用原則：

- 僅能以 hub recipient 解讀。
- 主要屬於 `CLEAR_FEATURE` 家族。
- 不可與 port selector 命名空間合併。

本 repo 的 reviewed linkage 目前覆蓋：

- `PORT_CONNECTION` <-> `wPortStatus bit 0`（僅作 `GET_STATUS` context）
- `PORT_OVER_CURRENT` <-> `wPortStatus bit 3`（僅作 `GET_STATUS` context）
- `PORT_LOW_SPEED` <-> `wPortStatus` 的速度指示（`GET_STATUS` context）
- `PORT_HIGH_SPEED` <-> `wPortStatus` 的速度指示（`GET_STATUS` context）
- reserved slot `5-7`、`11-15` 作為 reserved-boundary surface
- `C_HUB_LOCAL_POWER` <-> `wHubChange bit 0`
- `C_HUB_OVER_CURRENT` <-> `wHubChange bit 1`
- `C_PORT_CONNECTION` <-> `wPortChange bit 0`
- `C_PORT_ENABLE` <-> `wPortChange bit 1`
- `C_PORT_SUSPEND` <-> 標準 suspend-change selector 邊界
- `C_PORT_OVER_CURRENT` <-> 標準 over-current-change selector 邊界
- `C_PORT_RESET` <-> 標準 reset-change selector 邊界
- `PORT_ENABLE` <-> 標準 port enable selector 邊界
- `PORT_SUSPEND` <-> 標準 port suspend selector 邊界
- `PORT_RESET` <-> 標準 port reset selector 邊界
- `PORT_POWER` <-> 標準 port power selector 邊界
- `PORT_TEST` <-> 標準 port test selector 邊界
- `PORT_INDICATOR` <-> 標準 port indicator selector 邊界

本頁的 selector 命名空間邊界已完成 reviewed，作為 reference surface，  
但不代表主機端 sequencing、selector side effect 或更廣泛 request 行為已驗證。  
對 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED`，目前只屬於 `GET_STATUS` 的 context-only linkage，不是直接宣告可供 `SET_FEATURE` / `CLEAR_FEATURE` 使用。  
對 reserved rows，reviewed 僅表示這些數值屬於標準 port selector 邊界，並不代表可當作可用 selector。  
`PORT_TEST` / `PORT_INDICATOR` 目前也僅有 selector-boundary reviewed，未驗證 test mode 或 indicator 行為。

## Port Standard Selector Boundary（`0-22`）

`tables/feature_selector_matrix.yaml` 目前記錄標準 port selector 範圍 `0-22`。  
這就是 E-05 的核心邊界：**vendor-defined selector 不可重疊到此範圍**。

主要 selector 列如下：

| Value | Name | 常見 context |
|---:|---|---|
| `0` | `PORT_CONNECTION` | `GET_STATUS` |
| `1` | `PORT_ENABLE` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `2` | `PORT_SUSPEND` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `3` | `PORT_OVER_CURRENT` | `GET_STATUS` |
| `4` | `PORT_RESET` | `SET_FEATURE` |
| `5-7` | reserved | reserved 標準槽位 |
| `8` | `PORT_POWER` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `9` | `PORT_LOW_SPEED` | `GET_STATUS` |
| `10` | `PORT_HIGH_SPEED` | `GET_STATUS` |
| `11-15` | reserved | reserved 標準槽位 |
| `16` | `C_PORT_CONNECTION` | `CLEAR_FEATURE` change selector |
| `17` | `C_PORT_ENABLE` | `CLEAR_FEATURE` change selector |
| `18` | `C_PORT_SUSPEND` | `CLEAR_FEATURE` change selector |
| `19` | `C_PORT_OVER_CURRENT` | `CLEAR_FEATURE` change selector |
| `20` | `C_PORT_RESET` | `CLEAR_FEATURE` change selector |
| `21` | `PORT_TEST` | `SET_FEATURE` |
| `22` | `PORT_INDICATOR` | `SET_FEATURE` |

## `PORT_*` / `C_PORT_*` 行為邊界（selector 層）

以下是 selector page 的行為邊界提醒，不等於 full state-machine verified：

- `PORT_CONNECTION`
  - selector 值對應 port 連線語義，但本頁不將其提升為 host-side 連線/斷線流程真值。
- `PORT_ENABLE`、`PORT_SUSPEND`、`PORT_RESET`、`PORT_POWER`
  - 這些 selector 在標準 selector 命名空間中出現，但對應 `SET_FEATURE` / `CLEAR_FEATURE` 的完整啟停副作用未在本 repo 完成驗證。
- `PORT_OVER_CURRENT`
  - `C_PORT_OVER_CURRENT` 屬於 change selector 族群；本頁保留 `change` 識別語義，不直接定義 recovery policy。
- `C_PORT_CONNECTION`、`C_PORT_ENABLE`、`C_PORT_SUSPEND`、`C_PORT_OVER_CURRENT`、`C_PORT_RESET`
  - 一般作為 change selector，表示「事件可被清除/追蹤」的 `CHANGE` 類型語義，而不是直接的電氣時序定義。
- `PORT_TEST`、`PORT_INDICATOR`
  - 本頁目前僅保留 selector boundary；不推進至 test-mode、indicator mode 之 correctness 結論。

實務上，這裡的 `PORT_*` / `C_PORT_*` 與 `specs/port_status_bits.md` 的 status / change bit 分別對齊：

- `PORT_*`：對應 `wPortStatus` 狀態欄位的名義識別
- `C_PORT_*`：對應 `wPortChange` 變更位元的事件識別

## Defined / Reserved / Context-only

本 repo 目前用三種閱讀分類：

- **defined selector**：matrix 上明確列出名稱與作用
- **reserved selector**：屬於標準範圍內的保留值，不可被當作標準 selector 重用
- **context-only selector**：為 namespace 或 `GET_STATUS` 對照 completeness 而列入，不代表直接可當做實作 target

## 與請求族群的關係

- `SET_FEATURE` / `CLEAR_FEATURE` 的 `wValue` 應對應 `tables/feature_selector_matrix.yaml`。
- `GET_STATUS` 本身不直接設定 selector，但 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED` 已有 context-only 的狀態欄位比對 linkage。
- `C_PORT_*` selector 請與 `specs/port_status_bits.md` 的 `change bits` 一併閱讀。
- 已 review 的 `PORT_*`、`C_HUB_*`、`C_PORT_*` linkage 仍只可視為 selector boundary，不能推到 `SET_FEATURE` 或 `CLEAR_FEATURE` 的行為驗證結論。
- `PORT_TEST` 與 `PORT_INDICATOR` 僅保持 selector-slot reviewed，未宣告 test-mode 或指示燈行為驗證。

## Governed Linkage

- `tables/feature_selector_matrix.yaml`：selector 命名空間主要 machine-readable source
- `specs/hub_class_requests.md`：`SET_FEATURE` / `CLEAR_FEATURE` 請求族群摘要
- `specs/port_status_bits.md`：`GET_STATUS`、change bits 與 `CLEAR_FEATURE` 的關聯
- `specs/escalation_table.md`：E-05 escalation trigger context

## Non-claims

- 本頁不宣告 `0-22` selector 全部完成 PDF section-level 驗證。
- 本頁不宣告所有 selector side effect 均有 correctness 驗證。
- 本頁不將 selector 清單直接提升為 firmware 實作真值。
- 本頁不覆蓋 consuming repo 已確認的實作事實。
