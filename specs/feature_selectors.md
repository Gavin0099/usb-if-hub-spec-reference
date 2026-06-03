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
> 本頁是 `SET_FEATURE` / `CLEAR_FEATURE` selector namespace 的 reference summary，不是完整的 control truth table，也不是 section-level PDF 驗證紀錄。

## Page Purpose

本頁回答：

- USB 2.0 hub request space 中有哪些 hub / port feature selectors。
- 哪些 selectors 屬於 hub recipient，哪些屬於 port recipient。
- 為什麼 `0-22` 是 E-05 的標準 port selector boundary。
- 哪些 selectors 主要出現在 `SET_FEATURE`、`CLEAR_FEATURE` 或 `GET_STATUS` 的語意上下文中。

本頁不回答：

- 每個 selector 是否都已完成 PDF section-level verification。
- 每個 selector side effect 是否都已完成 correctness verification。
- `SET_FEATURE` / `CLEAR_FEATURE` 的完整 state-transition model。

## Boundary Before Reading

- Hub selectors 與 port selectors 可能共用相同數值，但 recipient 不同，不能混讀。
- E-05 的核心是：**vendor command selectors 不得與標準 port selector 範圍 `0-22` 重疊**。
- 有些 matrix entries 是為了補齊 `GET_STATUS` context，不應被誤讀成一定可直接 set/clear 的 feature target。

## Namespace Summary

| Namespace | Range | Recipient | Meaning |
|---|---:|---|---|
| Hub change selectors | `0-1` | device | 用於 hub-recipient `CLEAR_FEATURE` |
| Port standard selectors | `0-22` | other | E-05 標準邊界；vendor selectors 不得重疊 |

## Hub Selectors

目前 matrix 中的 hub selectors 如下：

| Value | Name | Main Use |
|---:|---|---|
| `0` | `C_HUB_LOCAL_POWER` | 清除 hub local power change condition |
| `1` | `C_HUB_OVER_CURRENT` | 清除 hub over-current change condition |

這些 selectors：

- 只能搭配 hub recipient 解讀
- 主要屬於 `CLEAR_FEATURE` family
- 不應被混入 port selector namespace

## Port Standard Selector Boundary (`0-22`)

`tables/feature_selector_matrix.yaml` 目前追蹤的標準 port selector boundary 為 `0-22`。  
這就是 E-05 的核心邊界：**vendor-defined selectors 不得與這個範圍重疊**。

Representative selectors：

| Value | Name | Common Context |
|---:|---|---|
| `0` | `PORT_CONNECTION` | `GET_STATUS` context |
| `1` | `PORT_ENABLE` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `2` | `PORT_SUSPEND` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `3` | `PORT_OVER_CURRENT` | `GET_STATUS` context |
| `4` | `PORT_RESET` | `SET_FEATURE` |
| `8` | `PORT_POWER` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `9` | `PORT_LOW_SPEED` | `GET_STATUS` context |
| `10` | `PORT_HIGH_SPEED` | `GET_STATUS` context |
| `16` | `C_PORT_CONNECTION` | `CLEAR_FEATURE` change selector |
| `17` | `C_PORT_ENABLE` | `CLEAR_FEATURE` change selector |
| `18` | `C_PORT_SUSPEND` | `CLEAR_FEATURE` change selector |
| `19` | `C_PORT_OVER_CURRENT` | `CLEAR_FEATURE` change selector |
| `20` | `C_PORT_RESET` | `CLEAR_FEATURE` change selector |
| `21` | `PORT_TEST` | `SET_FEATURE` |
| `22` | `PORT_INDICATOR` | `SET_FEATURE` |

## Defined / Reserved / Context-Only

本 repo 目前把 selectors 分成三種閱讀類型：

- **defined selector**：名稱與角色已明確列在 matrix 中
- **reserved selector**：仍位於標準範圍內，不應被挪作其他標準 selector
- **context-only selector**：為了補齊 namespace 或 `GET_STATUS` 比較面而保留，不代表它一定是直接 feature target

## Relationship to Request Families

- `SET_FEATURE` / `CLEAR_FEATURE` 的 `wValue` 應回連到 `tables/feature_selector_matrix.yaml`
- `GET_STATUS` 不會直接「設定 selector」，但某些 matrix entries 仍存在，用來解釋 status / change-field comparison context
- `C_PORT_*` selectors 應與 `specs/port_status_bits.md` 中的 `change bits` 一起閱讀

## Governed Linkage

- `tables/feature_selector_matrix.yaml`: selector namespace 的主要 machine-readable source
- `specs/hub_class_requests.md`: `SET_FEATURE` / `CLEAR_FEATURE` 的 request-family summary
- `specs/port_status_bits.md`: `GET_STATUS`、change bits 與 `CLEAR_FEATURE` 的關係
- `specs/escalation_table.md`: E-05 escalation trigger

## Non-claims

- 本頁不宣告 selector `0-22` 已逐值完成 PDF section-level verification
- 本頁不宣告所有 selector side effects 已完成 correctness verification
- 本頁不把 selector summary 升級成 firmware implementation authority
- 本頁不覆蓋 consuming repo 中已確認的 project facts
