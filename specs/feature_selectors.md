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
> This page is a reference summary for the `SET_FEATURE` / `CLEAR_FEATURE` selector namespace, not a complete control truth table and not a section-level PDF verification record.

## 頁面目的

本頁回答：

- USB 2.0 hub 請求空間中有哪些 selector。
- 哪些 selector 屬於 hub recipient，哪些屬於 port recipient。
- 為何 `0-22` 是 E-05 的標準 port selector 邊界。
- 哪些 selector 主要出現在 `SET_FEATURE`、`CLEAR_FEATURE`、或 `GET_STATUS` 的解讀脈絡中。

本頁不回答：

- selector `0-22` 是否已完成每一列逐值 PDF section-level 驗證。
- selector side-effect 是否已完成 correctness 驗證。
- `SET_FEATURE` / `CLEAR_FEATURE` 的完整 state-transition model。

## Boundary Before Reading

- Hub selectors 與 port selectors 可能共享數值，但它們使用不同 recipient，不能混用。
- E-05 關係到 **vendor command selectors 不得覆蓋標準 port selector `0-22` 的範圍**。
- 某些列為 `GET_STATUS` 上下文條目，僅代表查核語意，不代表一定為 `SET_FEATURE`/`CLEAR_FEATURE` 的可直接設定目標。
- 在標準範圍內的預留列只作為界線資訊，不轉為 vendor-extension 可用 selector。

## Namespace Summary

| Namespace | Range | Recipient | Meaning |
|---|---:|---|---|
| Hub change selectors | `0-1` | device | Used by hub-recipient `CLEAR_FEATURE` |
| Port standard selectors | `0-22` | other | E-05 boundary; vendor-defined selectors must not overlap |

## Hub Selectors

目前 matrix 列出的 hub selectors 有：

| Value | Name | Main Use |
|---:|---|---|
| `0` | `C_HUB_LOCAL_POWER` | Clears the hub local power change condition |
| `1` | `C_HUB_OVER_CURRENT` | Clears the hub over-current change condition |

這些 selector：

- 僅能以 hub recipient 解讀。
- 主要屬於 `CLEAR_FEATURE` 家族。
- 不得與 port selector namespace 合併。

本頁目前紀錄的 repo-local reviewed linkage 包含：

- `PORT_CONNECTION` <-> `wPortStatus bit 0`（僅 `GET_STATUS` 脈絡）
- `PORT_OVER_CURRENT` <-> `wPortStatus bit 3`（僅 `GET_STATUS` 脈絡）
- `PORT_LOW_SPEED` <-> `wPortStatus` speed 指示（僅 `GET_STATUS` 脈絡）
- `PORT_HIGH_SPEED` <-> `wPortStatus` speed 指示（僅 `GET_STATUS` 脈絡）
- reserved rows `5-7` 與 `11-15`（僅保留為 boundary surface）
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

這表示 selector namespace boundary 已作為 reference surface reviewed；  
但不代表有 host-side 行為順序、`SET_FEATURE`/`CLEAR_FEATURE` side-effect 或較完整 request 行為驗證。  
對 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED`，本頁目前僅保留 `GET_STATUS` context-only linkage，不代表它們可直接被視作 `SET_FEATURE` 或 `CLEAR_FEATURE` 的直接目標。  
reserved 列同理，僅表示屬於標準 port selector 邊界區間，不表示 vendor extension 可用位址。  
`PORT_TEST`、`PORT_INDICATOR` 也僅保留 selector boundary reviewed，尚未驗證 test mode / indicator 策略 / 硬體支援。

## Port Standard Selector Boundary (`0-22`)

`tables/feature_selector_matrix.yaml` 目前保存 port 標準 selector `0-22` 的 boundary。  
E-05 的核心邏輯是：**vendor-defined selector 不得進入此範圍**。

Representative selectors:

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

本頁目前在閱讀上區分三類：

- **defined selector**：matrix 中已具名與角色明確的 selector。
- **reserved selector**：屬於標準範圍內的預留欄位，不作為標準行為 selector 重用。
- **context-only selector**：僅為完成 namespace 或 `GET_STATUS` 比對面，未宣告為可直接行為目標。

## Relationship to Request Families

- `SET_FEATURE` / `CLEAR_FEATURE` 的 `wValue` 應回推至 `tables/feature_selector_matrix.yaml`。
- `GET_STATUS` 並非直接「設定 selector」；`PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED` 僅有 context-only linkage，用於 status-field 對照。
- reserved selector rows 是 boundary-only，不做 selector 行為宣告。
- `C_PORT_*` 與 `specs/port_status_bits.md` 的 `change bits` 維持對齊。
- Reviewed 的 `PORT_*`、`C_HUB_*`、`C_PORT_*` 關聯僅到 selector-boundary，未延伸到 `SET_FEATURE` / `CLEAR_FEATURE` 行為正確性。
- `PORT_TEST`、`PORT_INDICATOR` 僅維持 selector slot boundary reviewed。

## Governed Linkage

- `tables/feature_selector_matrix.yaml`: selector namespaces 的主要機器可讀來源。
- `specs/hub_class_requests.md`: `SET_FEATURE` / `CLEAR_FEATURE` request-family summary。
- `specs/port_status_bits.md`: `GET_STATUS`、`change bits` 與 `CLEAR_FEATURE` 關係參照。
- `specs/escalation_table.md`: E-05 escalation trigger。

## Non-claims

- 本頁不宣告 selector `0-22` 的逐值 PDF section-level 驗證。
- 本頁不宣告所有 selector side-effects 的 correctness 驗證。
- 本頁不把預留 selector slot 升為 firmware 實作權威。
- 本頁不把 selector summary 升格為 consuming repo 的 implementation authority。
- 本頁不替代 consuming repo 已確認的 project facts。
