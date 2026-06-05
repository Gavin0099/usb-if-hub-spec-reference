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

> 資料範圍：USB 2.0 Specification Rev 2.0，第 11.24.2 章節。  
> 本頁是 `SET_FEATURE` / `CLEAR_FEATURE` selector namespace 的參考摘要，不是完整控制真值表，也不是 section-level PDF 驗證紀錄。

## 頁面目的

本頁回答：

- USB 2.0 hub request 空間中有哪些 feature selector。
- 哪些 selector 屬於 hub recipient、哪些屬於 port recipient。
- 為何 `0-22` 是 E-05 的標準 port selector 邊界。
- 哪些 selector 主要出現在 `SET_FEATURE`、`CLEAR_FEATURE` 或 `GET_STATUS` 的解讀脈絡。

本頁不回答：

- 每個 selector 是否都已完成 PDF section-level 驗證。
- 每個 selector side effect 是否都有 correctness 驗證。
- `SET_FEATURE` / `CLEAR_FEATURE` 的完整 state-transition 模型。

## 閱讀前置邊界

- Hub selector 和 port selector 可能有相同數值，但 recipient 不同，不能混用。
- E-05 強調的是：**vendor command selector 不可與標準 port selector 範圍 `0-22` 重疊**。
- 有些 matrix 列位僅作為 `GET_STATUS` context，不能直接解讀為可直接 set 的 feature target。

## Namespace 摘要

| Namespace | Range | Recipient | 意義 |
|---|---:|---|---|
| Hub change selectors | `0-1` | device | 供 hub-recipient `CLEAR_FEATURE` 使用 |
| Port standard selectors | `0-22` | other | E-05 標準邊界；vendor selector 不得重疊 |

## Hub Selectors

目前 matrix 含有以下 hub selector：

| Value | Name | 主要用途 |
|---:|---|---|
| `0` | `C_HUB_LOCAL_POWER` | 清除 hub local power 變化條件 |
| `1` | `C_HUB_OVER_CURRENT` | 清除 hub over-current 變化條件 |

這些 selector：

- 僅以 hub recipient 解讀
- 主要隸屬 `CLEAR_FEATURE` family
- 不應併入 port selector namespace

目前 repo reviewed 的 linkage surface 包含：

- `PORT_CONNECTION` <-> `wPortStatus bit 0`（僅 `GET_STATUS` context）
- `PORT_OVER_CURRENT` <-> `wPortStatus bit 3`（僅 `GET_STATUS` context）
- `PORT_LOW_SPEED` <-> `wPortStatus` 中 speed indication（僅 `GET_STATUS` context）
- `PORT_HIGH_SPEED` <-> `wPortStatus` 中 speed indication（僅 `GET_STATUS` context）
- reserved port selector 槽位 `5-7`、`11-15` 僅作標準邊界保留面
- `C_HUB_LOCAL_POWER` <-> `wHubChange bit 0`
- `C_HUB_OVER_CURRENT` <-> `wHubChange bit 1`
- `C_PORT_CONNECTION` <-> `wPortChange bit 0`
- `C_PORT_ENABLE` <-> `wPortChange bit 1`
- `C_PORT_SUSPEND` <-> 標準 suspend-change selector 邊界
- `C_PORT_OVER_CURRENT` <-> 標準 over-current-change selector 邊界
- `C_PORT_RESET` <-> 標準 reset-change selector 邊界
- `PORT_ENABLE` <-> 標準 port enable feature selector 邊界
- `PORT_SUSPEND` <-> 標準 port suspend feature selector 邊界
- `PORT_RESET` <-> 標準 port reset feature selector 邊界
- `PORT_POWER` <-> 標準 port power feature selector 邊界
- `PORT_TEST` <-> 標準 port test feature selector 邊界
- `PORT_INDICATOR` <-> 標準 port indicator feature selector 邊界

這表示 selector namespace boundary 目前僅作 boundary-only 參考面，不代表 host-side sequencing、selector side-effect，或整體 request behavior 已驗證。
對 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED`，現有 reviewed surface 僅是 `GET_STATUS` 的 context-only linkage，並不轉為直接 `SET_FEATURE` / `CLEAR_FEATURE` target。
對 reserved 欄位， reviewed surface 僅代表該數值仍屬標準 port selector 範圍，不代表該值可直接用作 vendor selector 或既有實作支援。
對 `PORT_TEST`、`PORT_INDICATOR`，reviewed surface 僅在 selector-boundary 層，未驗證 test-mode / indicator 行為與韌體政策。

## `PORT_*` / `C_PORT_*` 行為邊界（selector 層）

- `PORT_CONNECTION`
  - selector 對應「該 port 的連接狀態」，本頁不主張全域 connect/disconnect 行為完整正確性。
- `PORT_ENABLE`、`PORT_SUSPEND`、`PORT_RESET`、`PORT_POWER`
  - 這些 selector 在標準命名空間中；`SET_FEATURE` / `CLEAR_FEATURE` 的完整 transition 影響不在本頁完成驗證。
- `PORT_OVER_CURRENT`
  - `PORT_OVER_CURRENT` 在 status context 報告過電流狀態；`C_PORT_OVER_CURRENT` 則是對應的 change-selector 事件與 ack/clear 流程，皆不延伸到 recovery policy 或時序真假值。
- `C_PORT_CONNECTION`、`C_PORT_ENABLE`、`C_PORT_SUSPEND`、`C_PORT_OVER_CURRENT`、`C_PORT_RESET`
  - 這些是 change selector：本頁只記錄事件 ack/clear 的 selector 角色，不以 timing 或 control-state machine 當真值。
- `PORT_TEST`、`PORT_INDICATOR`
  - 本刀僅保留 selector-boundary；尚未推進 test-mode / indicator 行為驗證。

實務上，`PORT_*` / `C_PORT_*` 對齊 `specs/port_status_bits.md` 的 status/change 分類：

- `PORT_*`：對應 `wPortStatus` 狀態欄位
- `C_PORT_*`：對應 `wPortChange` change/event 欄位

## Port Standard Selector Boundary (`0-22`)

`tables/feature_selector_matrix.yaml` 目前收錄標準 port selector 邊界 `0-22`。  
這是 E-05 核心邊界：**vendor-defined selectors 不得與此範圍重疊**。

代表性 selector：

| Value | Name | 常見 Context |
|---:|---|---|
| `0` | `PORT_CONNECTION` | `GET_STATUS` context |
| `1` | `PORT_ENABLE` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `2` | `PORT_SUSPEND` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `3` | `PORT_OVER_CURRENT` | `GET_STATUS` context |
| `4` | `PORT_RESET` | `SET_FEATURE` |
| `5-7` | reserved | standard-range 保留插槽 |
| `8` | `PORT_POWER` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `9` | `PORT_LOW_SPEED` | `GET_STATUS` context |
| `10` | `PORT_HIGH_SPEED` | `GET_STATUS` context |
| `11-15` | reserved | standard-range 保留插槽 |
| `16` | `C_PORT_CONNECTION` | `CLEAR_FEATURE` change selector |
| `17` | `C_PORT_ENABLE` | `CLEAR_FEATURE` change selector |
| `18` | `C_PORT_SUSPEND` | `CLEAR_FEATURE` change selector |
| `19` | `C_PORT_OVER_CURRENT` | `CLEAR_FEATURE` change selector |
| `20` | `C_PORT_RESET` | `CLEAR_FEATURE` change selector |
| `21` | `PORT_TEST` | `SET_FEATURE` |
| `22` | `PORT_INDICATOR` | `SET_FEATURE` |

## Defined / Reserved / Context-Only

本 repo 目前將 selector 分三類閱讀：

- **defined selector**：名稱與角色在 matrix 中明列
- **reserved selector**：保留插槽，屬於標準範圍且不應被重定義為標準 selector
- **context-only selector**：作為 namespace 或 `GET_STATUS` 比較上下文而列入，並不代表可直接當作 set 目標

## 與 request families 的關係

- `SET_FEATURE` / `CLEAR_FEATURE` 的 `wValue` 應回鏈到 `tables/feature_selector_matrix.yaml`。
- `GET_STATUS` 不直接設定 selector，但 `PORT_CONNECTION`、`PORT_OVER_CURRENT`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED` 已有 reviewed 的 context-only linkage 到 status-field 比較面。
- `C_PORT_*` selector 應與 `specs/port_status_bits.md` 的 `change bits` 一併閱讀。
- 已 reviewed 的 `PORT_*`、`C_HUB_*`、`C_PORT_*` 連結仍屬 selector boundary，不應當作 `SET_FEATURE` / `CLEAR_FEATURE` 行為驗證。
- `PORT_TEST`、`PORT_INDICATOR` 即使已有 selector 欄位，仍未進入行為驗證。

## Governed Linkage

- `tables/feature_selector_matrix.yaml`：selector namespace 的主要機器可讀來源。
- `specs/hub_class_requests.md`：`SET_FEATURE` / `CLEAR_FEATURE` 的 request-family 摘要。
- `specs/port_status_bits.md`：`GET_STATUS`、change bits 與 `CLEAR_FEATURE` 的關係。
- `specs/escalation_table.md`：E-05 escalation trigger。

## Non-claims

- 本頁不聲明 selector `0-22` 的 value-by-value PDF section-level 驗證。
- 本頁不聲明所有 selector side effect 的 correctness 驗證。
- 本頁不將 selector 摘要升為 firmware 實作權威。
- 本頁不覆蓋 consuming repo 的 confirmed project fact。
