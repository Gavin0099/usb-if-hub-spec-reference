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

> Source scope: USB 2.0 Specification Rev 2.0, Section 11.24.2.
> 本頁是 `SET_FEATURE` / `CLEAR_FEATURE` selector namespace 的 reference summary，不是完整 control truth table，也不是 section-level PDF verification record。

## Page Purpose

本頁回答：

- USB 2.0 hub request space 中有哪些 hub / port feature selectors。
- 哪些 selectors 屬於 hub recipient，哪些屬於 port recipient。
- 為什麼 `0-22` 是 E-05 standard port selector boundary。
- 哪些 selectors 主要出現在 `SET_FEATURE`、`CLEAR_FEATURE` 或 `GET_STATUS` interpretation context。

本頁不回答：

- 每個 selector 是否都已完成 PDF section-level verification。
- 每個 selector side effect 是否已完成 correctness verification。
- `SET_FEATURE` / `CLEAR_FEATURE` 的完整 state-transition model。

## Boundary Before Reading

- Hub selectors 與 port selectors 可能共用數值，但 recipient 不同，不能合併解讀。
- E-05 特別針對 **vendor command selectors 不得 overlap standard port selector range `0-22`**。
- 有些 matrix entries 是為了 `GET_STATUS` context 而存在，不應解讀成可直接 set/clear 的 feature target。
- Reserved selector rows 只代表 standard range 內的保留槽位，不代表可用 selector 或 vendor-extension 授權。

## Namespace Summary

| Namespace | Range | Recipient | Meaning |
|---|---:|---|---|
| Hub change selectors | `0-1` | device | 用於 hub-recipient `CLEAR_FEATURE` |
| Port standard selectors | `0-22` | other | E-05 standard boundary；vendor selectors 不得 overlap |

## Hub Selectors

目前 matrix 包含這些 hub selectors：

| Value | Name | Main Use |
|---:|---|---|
| `0` | `C_HUB_LOCAL_POWER` | Clears the hub local power change condition |
| `1` | `C_HUB_OVER_CURRENT` | Clears the hub over-current change condition |

這些 selectors：

- 必須以 hub recipient 解讀
- 主要屬於 `CLEAR_FEATURE` family
- 不得合併到 port selector namespace

目前 repo-local reviewed linkage surface 包含：

- `PORT_CONNECTION` <-> `wPortStatus bit 0`，僅限 `GET_STATUS` context
- `PORT_OVER_CURRENT` <-> `wPortStatus bit 3`，僅限 `GET_STATUS` context
- `PORT_LOW_SPEED` <-> `wPortStatus` speed indication，僅限 `GET_STATUS` context
- `PORT_HIGH_SPEED` <-> `wPortStatus` speed indication，僅限 `GET_STATUS` context
- reserved port selector slots `5-7` 與 `11-15`，僅限 reserved-boundary surface
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

這表示 selector namespace boundary 已作為 reference surface 完成 reviewed 收斂。
這不代表 host-side sequencing、selector side effects 或更廣泛 request behavior 已 verified。
對 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED` 來說，reviewed surface 只限 context-only `GET_STATUS` linkage；它們不是直接的 `SET_FEATURE` / `CLEAR_FEATURE` target。
對 reserved rows 來說，reviewed surface 只代表那些數值仍位於 standard port selector boundary 內；它們不是可用 selector，也不是 vendor-extension slots。

## Port Standard Selector Boundary (`0-22`)

`tables/feature_selector_matrix.yaml` 目前記錄 standard port selector boundary `0-22`。
這是 E-05 的核心 boundary：**vendor-defined selectors 不得 overlap 這個 range**。

Representative selectors：

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

本 repo 目前把 selectors 分成三種閱讀類別：

- **defined selector**：matrix 明確列出名稱與角色
- **reserved selector**：仍屬於 standard range，不得被改作其他 standard selector，也不得視為 vendor-extension 空間
- **context-only selector**：用來補齊 namespace 或 `GET_STATUS` comparison surface，不代表它一定是直接 feature target

## Relationship to Request Families

- `SET_FEATURE` / `CLEAR_FEATURE` 的 `wValue` 應連回 `tables/feature_selector_matrix.yaml`。
- `GET_STATUS` 不會直接「set a selector」，但 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED` 現在有 reviewed context-only linkage，可對應到 status-field comparison surface。
- Reserved selector rows 只支援 standard boundary 判斷，不支援 behavior claim 或 implementation guidance。
- `C_PORT_*` selectors 應與 `specs/port_status_bits.md` 的 `change bits` 一起閱讀。
- Reviewed `PORT_*`、`C_HUB_*`、reserved 與 `C_PORT_*` linkage 仍只代表 selector boundary，不代表 `SET_FEATURE` 或 `CLEAR_FEATURE` 行為證明。

## Governed Linkage

- `tables/feature_selector_matrix.yaml`: selector namespaces 的 primary machine-readable source。
- `specs/hub_class_requests.md`: `SET_FEATURE` / `CLEAR_FEATURE` 的 request-family summary。
- `specs/port_status_bits.md`: `GET_STATUS`、change bits 與 `CLEAR_FEATURE` 的關係。
- `specs/escalation_table.md`: E-05 escalation trigger。

## Non-claims

- 本頁不宣告 selector `0-22` 已完成 value-by-value PDF section-level verification。
- 本頁不宣告所有 selector side effects 已完成 correctness verification。
- 本頁不把 reserved selector slots 視為可用 feature selectors。
- 本頁不把 selector summaries 升級成 firmware implementation authority。
- 本頁不覆蓋 consuming repos 中已確認的 project facts。
