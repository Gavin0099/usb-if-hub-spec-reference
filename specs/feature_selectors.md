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

# 功能選擇值（Feature Selectors）

> Source scope: USB 2.0 規格 Rev 2.0，11.24.2。  
> 本頁是 `SET_FEATURE` / `CLEAR_FEATURE` 選擇值命名空間的參考摘要，不是完整控制行為真值表，也不是逐段 PDF 驗證紀錄。

## 頁面用途

本頁回答：

- USB 2.0 中 Hub 請求空間到底有哪些 feature selector。
- 哪些 selector 屬於 hub recipient，哪些屬於 port recipient。
- 為何 `0-22` 代表 E-05 的標準 port selector 邊界。
- `SET_FEATURE`、`CLEAR_FEATURE`、`GET_STATUS` 主要在何種 context 下使用這些 selector。

本頁不回答：

- 是否每個 selector 都有 PDF 逐段驗證。
- 是否所有 selector 的 side effect 已完成正確性驗證。
- `SET_FEATURE` / `CLEAR_FEATURE` 的完整 state transition 行為模型。

## 閱讀邊界

- Hub selector 與 port selector 可能共用數值，但屬於不同 recipient，不得互相混用。
- E-05 只界定：**vendor command selector 不可與標準 port selector 範圍 `0-22` 重疊**。
- 某些表格列項目只作為 `GET_STATUS` context 標註，不能直接視為可直接設定的功能目標。

## 命名空間摘要

| Namespace | Range | Recipient | 含義 |
|---|---:|---|---|
| Hub change selectors | `0-1` | hub recipient | 用於 hub-recipient 的 `CLEAR_FEATURE` |
| Port standard selectors | `0-22` | port recipient | E-05 邊界；vendor-defined selector 不得與此範圍重疊 |

## Hub Selectors

目前 matrix 與對照表中列出的 hub selectors 為：

| Value | Name | 主要用途 |
|---:|---|---|
| `0` | `C_HUB_LOCAL_POWER` | 清除此 hub local power change condition |
| `1` | `C_HUB_OVER_CURRENT` | 清除此 hub over-current change condition |

這些 selector 應以 hub recipient 為主，主要對應 `CLEAR_FEATURE`；不得與 port 選擇值命名空間混淆。

本 repo-local 已有的 reviewed linkage 包含：

- `PORT_CONNECTION` <-> `wPortStatus bit 0`（僅供 `GET_STATUS` context）
- `PORT_OVER_CURRENT` <-> `wPortStatus bit 3`（僅供 `GET_STATUS` context）
- `PORT_LOW_SPEED` <-> `wPortStatus` 的速度註解欄位（僅供 `GET_STATUS` context）
- `PORT_HIGH_SPEED` <-> `wPortStatus` 的速度註解欄位（僅供 `GET_STATUS` context）
- reserved slot `5-7`、`11-15` 僅作 boundary surface 界定
- `C_HUB_LOCAL_POWER` <-> `wHubChange bit 0`
- `C_HUB_OVER_CURRENT` <-> `wHubChange bit 1`
- `C_PORT_CONNECTION` <-> `wPortChange bit 0`
- `C_PORT_ENABLE` <-> `wPortChange bit 1`
- `C_PORT_SUSPEND` <-> suspend-change boundary
- `C_PORT_OVER_CURRENT` <-> over-current-change boundary
- `C_PORT_RESET` <-> reset-change boundary
- `PORT_ENABLE` <-> port enable boundary
- `PORT_SUSPEND` <-> port suspend boundary
- `PORT_RESET` <-> port reset boundary
- `PORT_POWER` <-> port power boundary
- `PORT_TEST` <-> port test boundary
- `PORT_INDICATOR` <-> port indicator boundary

這段邊界層僅標示選擇值命名空間已被整理為可閱讀 reference；不表示 host-side 實作、state transition 行為或 side-effect 正確性已完成驗證。  
對 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED`，reviewed surface 僅為 `GET_STATUS` 的 context-only 鏈接；不代表其可直接作為 `SET_FEATURE` / `CLEAR_FEATURE` 的直接目標。  
reserved rows (`5-7`、`11-15`) 只表示數值仍屬於標準範圍，並不宣告可使用方式或 vendor-extend 行為。  
對 `PORT_TEST` 與 `PORT_INDICATOR`，目前 reviewed 僅到 selector boundary，未聲明測試模式、指示燈策略或硬體支援行為。

## Port Standard Selector Boundary (`0-22`)

`tables/feature_selector_matrix.yaml` 目前對應了標準 port selector 邊界 `0-22`。  
這是 E-05 的核心邊界：**vendor-defined selector 不可重疊到標準範圍 `0-22`**。  

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

本 repo 目前把 selector 分為：

- **defined selector**：在 matrix 中明確列出名稱與角色。
- **reserved selector**：仍屬於標準範圍，不得作為標準 selector 的其他用途。
- **context-only selector**：用來補齊命名空間閱讀或 `GET_STATUS` 對照，不代表其在所有情境都可直接作為設定目標。

## Relationship to Request Families

- `SET_FEATURE` / `CLEAR_FEATURE` 的 `wValue` 應回到 `tables/feature_selector_matrix.yaml` 來對照。
- `GET_STATUS` 並不直接「設定 selector」，但 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED` 的 context-only 對照可保留為 `status-field` 閱讀邊界。
- `C_PORT_*` 仍需搭配 `specs/port_status_bits.md` 的 change bit surface 閱讀。
- 已 reviewed 的 `PORT_*`、`C_HUB_*`、`C_PORT_*` 對照僅可視為 selector boundary；不構成 `SET_FEATURE`、`CLEAR_FEATURE` 的行為正確性證明。
- `PORT_TEST` 與 `PORT_INDICATOR` 雖在命名空間中有 reviewed slot，但仍不在此頁內作為行為驗證範圍。

## Governed Linkage

- `tables/feature_selector_matrix.yaml`：selector 命名空間的主要機器可讀來源。
- `specs/hub_class_requests.md`：`SET_FEATURE` / `CLEAR_FEATURE` 請求族摘要。
- `specs/port_status_bits.md`：`GET_STATUS` 與 change bit 的關聯對照。
- `specs/escalation_table.md`：E-05 escalation trigger。

## Non-claims

- 本頁不聲明 `0-22` 每一個 selector 的 PDF 逐段驗證。
- 本頁不聲明所有 selector side-effect 的 correctness 已驗證。
- 本頁不聲明任何 selector slot 已可直接作為 firmware 實作規格。
- 本頁不聲明 selector 摘要可作為 consuming repo 的 implementation authority。
- 本頁不覆蓋 consuming repo 已確認的 project fact。
