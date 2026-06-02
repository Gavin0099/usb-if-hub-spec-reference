---
title: 功能選擇器
claim_level: inferred
status: review_required
last_reviewed: "2026-06-02"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# 功能選擇器

> 來源範圍：USB 2.0 Specification Rev 2.0，Section 11.24.2。  
> 本頁是 `SET_FEATURE` / `CLEAR_FEATURE` selector namespace 的 reference summary，不是完整 control truth table，也不是 section-level PDF 驗證紀錄。

## 頁面用途

本頁回答的問題是：

- USB 2.0 hub class request 中有哪些 hub / port feature selectors。
- 哪些 selector 屬於 hub recipient，哪些屬於 port recipient。
- 為什麼 `0-22` 是 E-05 的標準 port selector 邊界。
- 哪些 selector 主要出現在 `SET_FEATURE`、`CLEAR_FEATURE` 或 `GET_STATUS` 的解讀情境中。

本頁不回答的問題是：

- 每個 selector 是否都已完成 PDF section-level verification。
- 每個 selector 的硬體副作用是否已完成 correctness verification。
- `SET_FEATURE` / `CLEAR_FEATURE` 的完整狀態轉移模型。

## 先掌握的邊界

- hub selectors 與 port selectors 可以有相同數值，但 recipient 不同，不能混讀。
- E-05 關心的是 **vendor command selector 不得與標準 port selector 範圍 `0-22` 重疊**。
- 某些項目雖列在 matrix 中，但實際角色是 `GET_STATUS` 的 context，而不是可直接 `SET_FEATURE` 的 target。

## Namespace Summary

| Namespace | 範圍 | Recipient | 說明 |
|---|---:|---|---|
| Hub change selectors | `0-1` | device | 用於 hub recipient 的 `CLEAR_FEATURE` |
| Port standard selectors | `0-22` | other | E-05 的標準邊界，vendor selector 不可重疊 |

## Hub Selectors

目前 matrix 中的 hub selectors 為：

| 值 | 名稱 | 主要用途 |
|---:|---|---|
| `0` | `C_HUB_LOCAL_POWER` | 清除 hub local power change condition |
| `1` | `C_HUB_OVER_CURRENT` | 清除 hub over-current change condition |

這些 selector：

- 只應與 hub recipient 一起解讀。
- 主要屬於 `CLEAR_FEATURE` family。
- 不應拿來當 port selector namespace 的一部分。

## Port Standard Selector Boundary (`0-22`)

`tables/feature_selector_matrix.yaml` 目前已整理出標準 port selector 邊界 `0-22`。  
這個邊界是 E-05 的核心：**vendor-defined selector 不應與這個範圍重疊**。

代表性 selector 如下：

| 值 | 名稱 | 常見語境 |
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

本 repo 目前把 selector 分成三種閱讀方式：

- **defined selector**：名稱與用途已在 matrix 中列出。
- **reserved selector**：仍屬標準範圍的一部分，但不應被 vendor 重新定義成標準 selector。
- **context-only selector**：出現在 matrix 中是為了補齊 namespace 或 `GET_STATUS` 對照，不代表它一定是可直接設定的 feature target。

## 與 Request Family 的關係

- `SET_FEATURE` / `CLEAR_FEATURE` 的 `wValue` 應連回 `tables/feature_selector_matrix.yaml`。
- `GET_STATUS` 雖不直接「設定 selector」，但某些 matrix entries 仍用來說明 status / change field 的對照語境。
- `C_PORT_*` selector 與 `change bits` 的語意應與 `specs/port_status_bits.md` 一起閱讀。

## Governed Linkage

- `tables/feature_selector_matrix.yaml`：selector namespace 的主要 machine-readable source。
- `specs/hub_class_requests.md`：`SET_FEATURE` / `CLEAR_FEATURE` 的 request-family summary。
- `specs/port_status_bits.md`：`GET_STATUS`、change bits、`CLEAR_FEATURE` 的關聯說明。
- `specs/escalation_table.md`：E-05 escalation trigger。

## Non-claims

- 本頁不宣告 selector `0-22` 已完成逐值 PDF section-level verification。
- 本頁不宣告所有 selector 的副作用都已完成硬體或韌體 correctness 驗證。
- 本頁不把 selector summary 升級成 firmware implementation authority。
- 本頁不覆寫 consuming repo 的 confirmed project facts。
