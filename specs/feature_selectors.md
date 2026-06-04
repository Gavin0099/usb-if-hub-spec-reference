---
title: Feature Selectors
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Feature Selectors

> Source scope: USB 2.0 Specification Rev 2.0, Section 11.24.2。  
> 本頁是 `SET_FEATURE` / `CLEAR_FEATURE` selector namespace 的參考摘要，不是完整 control truth table，也不是 section-level PDF verification record。

## Page Purpose

本頁主要回答：

- USB 2.0 hub request space 中有哪些 feature selectors。
- 哪些 selectors 屬於 hub recipient，哪些屬於 port recipient。
- 為什麼 `0-22` 是 E-05 的標準 port selector 邊界。
- 哪些 selectors 主要出現在 `SET_FEATURE`、`CLEAR_FEATURE` 或 `GET_STATUS` 解讀情境中。

本頁不回答：

- 是否每個 selector 都已完成 PDF section-level verification。
- 是否每個 selector side effect 都已完成 correctness verification。
- `SET_FEATURE` / `CLEAR_FEATURE` 的完整 state-transition model。

## Boundary Before Reading

- Hub selectors 與 port selectors 可能共用數值，但 recipient 不同，不能合併解讀。
- E-05 專門處理 **vendor command selectors 不得與標準 port selector 範圍 `0-22` 重疊**。
- 某些 matrix entries 是作為 `GET_STATUS` context 出現，不應被解讀成可直接 settable 的 feature targets。

## Namespace Summary

| Namespace | Range | Recipient | Meaning |
|---|---:|---|---|
| Hub change selectors | `0-1` | hub recipient | 用於 hub-recipient `CLEAR_FEATURE` |
| Port standard selectors | `0-22` | port recipient | E-05 標準邊界；vendor selectors 不得重疊 |

## Hub Selectors

目前 matrix 收錄的 hub selectors 如下：

| Value | Name | Main Use |
|---:|---|---|
| `0` | `C_HUB_LOCAL_POWER` | 清除 hub local power change condition |
| `1` | `C_HUB_OVER_CURRENT` | 清除 hub over-current change condition |

這些 selectors：

- 只應搭配 hub recipient 解讀
- 主要屬於 `CLEAR_FEATURE` family
- 不可與 port selector namespace 合併

目前 repo-local reviewed linkage surface 包含：

- `PORT_CONNECTION` <-> `wPortStatus bit 0`，僅作為 `GET_STATUS` context
- `PORT_OVER_CURRENT` <-> `wPortStatus bit 3`，僅作為 `GET_STATUS` context
- `PORT_LOW_SPEED` <-> `wPortStatus` 中的 speed indication，僅作為 `GET_STATUS` context
- `PORT_HIGH_SPEED` <-> `wPortStatus` 中的 speed indication，僅作為 `GET_STATUS` context
- reserved port selector slots `5-7`，僅作為 reserved-boundary surface
- reserved port selector slots `11-15`，僅作為 reserved-boundary surface
- `C_HUB_LOCAL_POWER` <-> `wHubChange bit 0`
- `C_HUB_OVER_CURRENT` <-> `wHubChange bit 1`
- `C_PORT_CONNECTION` <-> `wPortChange bit 0`
- `C_PORT_ENABLE` <-> `wPortChange bit 1`
- `C_PORT_SUSPEND` <-> standard suspend-change selector boundary
- `C_PORT_OVER_CURRENT` <-> standard over-current-change selector boundary
- `C_PORT_RESET` <-> standard reset-change selector boundary
- `PORT_ENABLE` <-> standard port enable feature selector boundary
- `PORT_SUSPEND` <-> standard port suspend feature selector boundary
- `PORT_RESET` <-> standard port reset feature selector boundary
- `PORT_POWER` <-> standard port power feature selector boundary
- `PORT_TEST` <-> standard port test feature selector boundary
- `PORT_INDICATOR` <-> standard port indicator feature selector boundary

這代表 selector namespace boundary 已被整理成較清楚的 reference surface。  
這不代表 host-side sequencing、selector side effects 或更廣泛的 request behavior 已完成 verified。

對於 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED` 與 `PORT_HIGH_SPEED`，目前的 reviewed surface 只是 context-only `GET_STATUS` linkage，不表示它們是直接的 `SET_FEATURE` / `CLEAR_FEATURE` targets。  
對於 reserved rows，reviewed surface 只表示這些數值仍位於標準 port selector boundary 內，不表示它們是可用 selectors 或 vendor-extension slots。  
對於 `PORT_TEST` 與 `PORT_INDICATOR`，目前 reviewed surface 只到 selector boundary，不驗證 test-mode behavior、indicator policy 或 hardware support。

## Port Standard Selector Boundary (`0-22`)

`tables/feature_selector_matrix.yaml` 目前明確收錄了標準 port selector boundary `0-22`。  
這是 E-05 的核心邊界：**vendor-defined selectors 不得與此範圍重疊**。

代表性 selectors：

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

本 repo 目前將 selectors 分成三種讀法：

- **defined selector**：matrix 中明確列出名稱與角色
- **reserved selector**：仍在標準範圍內，但不應被重用為標準 selector
- **context-only selector**：為了補齊 namespace 或 `GET_STATUS` 比對 surface 而納入，不代表它一定是直接 feature target

## Relationship to Request Families

- `SET_FEATURE` / `CLEAR_FEATURE` 的 `wValue` 應回連到 `tables/feature_selector_matrix.yaml`
- `GET_STATUS` 不會直接「設定 selector」，但 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED` 目前都有 reviewed 的 context-only linkage，可作為 status-field 對照 surface
- `C_PORT_*` selectors 應與 `specs/port_status_bits.md` 中的 change bits 一起閱讀
- 目前 reviewed 的 `PORT_*`、`C_HUB_*`、`C_PORT_*` linkage 仍應視為 selector boundary，不是 `SET_FEATURE` / `CLEAR_FEATURE` behavior proof
- `PORT_TEST` 與 `PORT_INDICATOR` 雖然 selector slots 已 reviewed，但仍未進入 behavior verification

## Governed Linkage

- `tables/feature_selector_matrix.yaml`：selector namespace 的主要 machine-readable source
- `specs/hub_class_requests.md`：`SET_FEATURE` / `CLEAR_FEATURE` 的 request-family 摘要
- `specs/port_status_bits.md`：`GET_STATUS`、change bits 與 `CLEAR_FEATURE` 的關聯
- `specs/escalation_table.md`：E-05 escalation trigger

## Non-claims

- 本頁不宣告 selector `0-22` 已完成逐值 PDF section-level verification
- 本頁不宣告所有 selector side effects 都已完成 correctness verification
- 本頁不把 selector summaries 升級為 firmware implementation authority
- 本頁不覆蓋 consuming repos 中已確認的 project facts
