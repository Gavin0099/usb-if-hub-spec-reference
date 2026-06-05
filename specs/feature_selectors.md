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

# 功能選擇子

> 來源範圍：USB 2.0 規範 Rev 2.0，第 11.24.2 章節。  
> 本頁為 `SET_FEATURE` / `CLEAR_FEATURE` selector 命名空間的參考摘要，不是完整控制行為真值表，也不是 section-level PDF 驗證記錄。

## 頁面目的

本頁回答：

- USB 2.0 hub request 空間中有哪些 feature selectors。
- 哪些 selector 屬於 hub recipient，哪些屬於 port recipient。
- 為何 `0-22` 屬於 E-05 standard port selector 邊界。
- 哪些 selector 主要出現在 `SET_FEATURE`、`CLEAR_FEATURE` 或 `GET_STATUS` 的 context。

本頁不回答：

- 是否每個 selector 已完成 PDF section-level 驗證。
- 是否每個 selector 的 side effect 都完成 correctness 驗證。
- `SET_FEATURE` / `CLEAR_FEATURE` 的完整 state-transition 行為模型。

## 閱讀本頁的邊界條件

- Hub selector 與 port selector 可能共用數值，但 recipient 不同，不能混用。
- E-05 的邊界意義是：**標準 port selector 範圍 `0-22` 不能與 vendor-defined selector 重疊**。
- 某些 entries 僅作為 `GET_STATUS` context，不能視為可直接設定的 feature target。

## 命名空間總覽

| Namespace | Range | Recipient | Meaning |
|---|---:|---|---|
| Hub change selectors | `0-1` | device | `CLEAR_FEATURE` 的 hub-recipient 清除 selector |
| Port standard selectors | `0-22` | other | E-05 standard boundary；不與 vendor-defined selector 重疊 |

## Hub Selectors

目前 matrix 中包含這些 hub selectors：

| Value | Name | 主語義 |
|---:|---|---|
| `0` | `C_HUB_LOCAL_POWER` | 清除 hub local power change condition |
| `1` | `C_HUB_OVER_CURRENT` | 清除 hub over-current change condition |

這些 selector：

- 僅以 hub recipient 解讀
- 主要屬於 `CLEAR_FEATURE` family
- 不得合併到 port selector 命名空間

目前本 repo 的 reviewed linkage surface 包含：

- `PORT_CONNECTION` <-> `wPortStatus bit 0`（僅 `GET_STATUS` context）
- `PORT_OVER_CURRENT` <-> `wPortStatus bit 3`（僅 `GET_STATUS` context）
- `PORT_LOW_SPEED` <-> `wPortStatus` 中 speed indication（僅 `GET_STATUS` context）
- `PORT_HIGH_SPEED` <-> `wPortStatus` 中 speed indication（僅 `GET_STATUS` context）
- `5-7`、`11-15` 為 reserved slot，僅保留 reserved-boundary surface
- `C_HUB_LOCAL_POWER` <-> `wHubChange bit 0`
- `C_HUB_OVER_CURRENT` <-> `wHubChange bit 1`
- `C_PORT_CONNECTION` <-> `wPortChange bit 0`
- `C_PORT_ENABLE` <-> `wPortChange bit 1`
- `C_PORT_SUSPEND` <-> standard suspend-change selector 邊界
- `C_PORT_OVER_CURRENT` <-> standard over-current change selector 邊界
- `C_PORT_RESET` <-> standard reset-change selector 邊界
- `PORT_ENABLE` <-> standard port enable selector 邊界
- `PORT_SUSPEND` <-> standard port suspend selector 邊界
- `PORT_RESET` <-> standard port reset selector 邊界
- `PORT_POWER` <-> standard port power selector 邊界
- `PORT_TEST` <-> standard port test selector 邊界
- `PORT_INDICATOR` <-> standard port indicator selector 邊界

因此，selector 命名空間目前被視為「reviewed boundary-only」參考面。
本頁不把這視為 host-side sequencing、selector side-effect 或更完整 request behavior 的 correctness 驗證。
`PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED` 為 context-only `GET_STATUS` linkage，不能直接視為 `SET_FEATURE` / `CLEAR_FEATURE` 目標。
reserved rows 只表示那些數值維持在標準 port selector 範圍，不表示可用 selector 或可自訂 vendor slot。
`PORT_TEST` 與 `PORT_INDICATOR` 目前僅保留在 selector-boundary surface；尚未驗證 test mode、indicator policy 或硬體支援。

## `PORT_*` / `C_PORT_*` 行為邊界（selector 層）

- `PORT_CONNECTION`
  - selector 值對應連接語義，但本頁不主張完整主機 connect/disconnect 行為模型。
- `PORT_ENABLE`、`PORT_SUSPEND`、`PORT_RESET`、`PORT_POWER`
  - 這些位於 standard namespace；`SET_FEATURE` / `CLEAR_FEATURE` 的完整 transition impact 尚未在本頁完成驗證。
- `PORT_OVER_CURRENT`
  - `C_PORT_OVER_CURRENT` 屬於 change-selector family；本頁僅保留 `CHANGE` 語義，不定義 recovery policy。
- `C_PORT_CONNECTION`、`C_PORT_ENABLE`、`C_PORT_SUSPEND`、`C_PORT_OVER_CURRENT`、`C_PORT_RESET`
  - 這些都以 change selector 對待：保留 host ack/clear 的事件語義，不宣告時序或 state-machine 真值。
- `PORT_TEST`、`PORT_INDICATOR`
  - 僅保留 selector-boundary，目前不推進 test-mode 或 indicator 行為驗證。

實務上，`PORT_*` / `C_PORT_*` 對齊 `specs/port_status_bits.md` 中的狀態分類：

- `PORT_*`：對應 `wPortStatus` 狀態欄位語義
- `C_PORT_*`：對應 `wPortChange` 事件欄位語義

## Port Standard Selector Boundary (`0-22`)

`tables/feature_selector_matrix.yaml` 目前收錄標準 port selector 範圍 `0-22`，即 E-05 核心邊界：
**vendor-defined selectors 不得與這段範圍重疊**。

代表 selector：

| Value | Name | Common Context |
|---:|---|---|
| `0` | `PORT_CONNECTION` | `GET_STATUS` |
| `1` | `PORT_ENABLE` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `2` | `PORT_SUSPEND` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `3` | `PORT_OVER_CURRENT` | `GET_STATUS` |
| `4` | `PORT_RESET` | `SET_FEATURE` |
| `5-7` | reserved | reserved standard-range slots |
| `8` | `PORT_POWER` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `9` | `PORT_LOW_SPEED` | `GET_STATUS` |
| `10` | `PORT_HIGH_SPEED` | `GET_STATUS` |
| `11-15` | reserved | reserved standard-range slots |
| `16` | `C_PORT_CONNECTION` | `CLEAR_FEATURE` change selector |
| `17` | `C_PORT_ENABLE` | `CLEAR_FEATURE` change selector |
| `18` | `C_PORT_SUSPEND` | `CLEAR_FEATURE` change selector |
| `19` | `C_PORT_OVER_CURRENT` | `CLEAR_FEATURE` change selector |
| `20` | `C_PORT_RESET` | `CLEAR_FEATURE` change selector |
| `21` | `PORT_TEST` | `SET_FEATURE` |
| `22` | `PORT_INDICATOR` | `SET_FEATURE` |

## Defined / Reserved / Context-Only

本 repo 將 selector 分為三類：

- **defined selector**：名稱與角色明確出現在 matrix 中
- **reserved selector**：仍在標準範圍，不能被視為一般 selector 使用
- **context-only selector**：只為補全 namespace / `GET_STATUS` 比對面，不代表一定可直接作為 feature target

## 與 request families 的關聯

- `SET_FEATURE` / `CLEAR_FEATURE` 的 `wValue` 應回鏈到 `tables/feature_selector_matrix.yaml`。
- `GET_STATUS` 不直接「設定 selector」，但 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED` 有 context-only linkage 到 status-field 比對面。
- `C_PORT_*` selector 請與 `specs/port_status_bits.md` 的 `change bits` 一併閱讀。
- reviewed 的 `PORT_*`、`C_HUB_*`、`C_PORT_*` linkage 僅作 selector boundary 參考，不可上升為 `SET_FEATURE` / `CLEAR_FEATURE` 實作證據。
- `PORT_TEST` 與 `PORT_INDICATOR` 目前仍停留在 selector-slot reviewed，未包含行為面。

## Governed Linkage

- `tables/feature_selector_matrix.yaml`：selector namespace 的機器可讀主要來源。
- `specs/hub_class_requests.md`：`SET_FEATURE` / `CLEAR_FEATURE` family 的請求摘要。
- `specs/port_status_bits.md`：`GET_STATUS` 與 change bits、`CLEAR_FEATURE` 的關聯。
- `specs/escalation_table.md`：E-05 escalation trigger 對齊參考。

## Non-claims

- 本頁不宣告 selector `0-22` 的 value-by-value section-level PDF verification。
- 本頁不宣告所有 selector side effect 的 correctness 驗證。
- 本頁不把 selector 清單轉為 firmware 控制真值。
- 本頁不覆蓋 consuming repo 已確認的 project fact。
