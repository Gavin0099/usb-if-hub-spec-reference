---
title: PORT_* / C_PORT_* 詞彙對齊
claim_level: inferred
status: review_required
last_reviewed: "2026-06-16"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# PORT_* / C_PORT_* 詞彙對齊

> 本頁僅對齊 `PORT_*` 與 `C_PORT_*` 的術語關係，用於減少 AI/LLM 對現有欄位與事件詞彙的誤判。
> 它不擴大可宣告的行為正確性。

## 範圍

- 將 `wPortStatus` 的 `PORT_*` 狀態詞與 `wPortChange` 的 `C_PORT_*` 變更詞做對齊。
- 對應 `feature_selector_matrix` 與 `port_status_bit_matrix` 的命名關係。
- 明確列出 boundary / reserved 項目為「命名邊界」而非行為契約。

## 不處理目標

- 不主張 `PORT_*` 的完整狀態機行為。
- 不將 `C_PORT_*` 視為完整狀態模型。
- 不宣告 `SET_FEATURE` / `CLEAR_FEATURE` 的時序或轉換正確性。

## 詞彙對照

### `PORT_*` 狀態詞（對應 `wPortStatus`）

| 詞彙 | 欄位/位元 | 對齊語義 |
|---|---|---|
| `PORT_CONNECTION` | `wPortStatus.bit0` | 連線存在狀態 |
| `PORT_ENABLE` | `wPortStatus.bit1` | 連接/使能狀態標記 |
| `PORT_SUSPEND` | `wPortStatus.bit2` | 暫停相關狀態標記 |
| `PORT_OVER_CURRENT` | `wPortStatus.bit3` | 過流條件標記 |
| `PORT_RESET` | `wPortStatus.bit4` | 重設條件標記 |
| `PORT_POWER` | `wPortStatus.bit8` | 供電狀態標記 |
| `PORT_LOW_SPEED` | `wPortStatus.bit9` | 速度解讀位元之一，需與 `PORT_HIGH_SPEED` 一起看 |
| `PORT_HIGH_SPEED` | `wPortStatus.bit10` | 速度解讀位元之一，需與 `PORT_LOW_SPEED` 一起看 |
| `PORT_TEST` | `wPortStatus.bit11` | 測試模式相關狀態標記 |
| `PORT_INDICATOR` | `wPortStatus.bit12` | 指示燈模式相關狀態標記 |

#### `PORT_*` boundary 標記

| 詞彙 | 欄位/位元 | 對齊語義 |
|---|---|---|
| `PORT_STATUS_HIGH_BIT_BOUNDARY` | `wPortStatus.bit15` | 16-bit status 欄位邊界標記 |
| `PORT_STATUS_RESERVED_BIT5` | `wPortStatus.bit5` | 保留位元（命名邊界） |
| `PORT_STATUS_RESERVED_BIT6` | `wPortStatus.bit6` | 保留位元（命名邊界） |
| `PORT_STATUS_RESERVED_BIT7` | `wPortStatus.bit7` | 保留位元（命名邊界） |
| `PORT_STATUS_RESERVED_BIT13` | `wPortStatus.bit13` | 保留位元（命名邊界） |
| `PORT_STATUS_RESERVED_BIT14` | `wPortStatus.bit14` | 保留位元（命名邊界） |

### `C_PORT_*` 變更詞（對應 `wPortChange`）

| 詞彙 | 欄位/位元 | 對齊語義 |
|---|---|---|
| `C_PORT_CONNECTION` | `wPortChange.bit0` | 連線變更事件記錄 |
| `C_PORT_ENABLE` | `wPortChange.bit1` | 使能變更事件記錄 |
| `C_PORT_SUSPEND` | `wPortChange.bit2` | 暫停變更事件記錄 |
| `C_PORT_OVER_CURRENT` | `wPortChange.bit3` | 過流變更事件記錄 |
| `C_PORT_RESET` | `wPortChange.bit4` | 重設條件變更事件記錄 |

#### `C_PORT_*` boundary 標記

| 詞彙 | 欄位/位元 | 對齊語義 |
|---|---|---|
| `PORT_CHANGE_HIGH_BIT_BOUNDARY` | `wPortChange.bit15` | 16-bit change 欄位邊界標記 |
| `PORT_CHANGE_RESERVED_BIT5` | `wPortChange.bit5` | 保留位元（命名邊界） |
| `PORT_CHANGE_RESERVED_BIT6` | `wPortChange.bit6` | 保留位元（命名邊界） |
| `PORT_CHANGE_RESERVED_BIT7` | `wPortChange.bit7` | 保留位元（命名邊界） |
| `PORT_CHANGE_RESERVED_BIT8` | `wPortChange.bit8` | 保留位元（命名邊界） |
| `PORT_CHANGE_RESERVED_BIT9` | `wPortChange.bit9` | 保留位元（命名邊界） |
| `PORT_CHANGE_RESERVED_BIT10` | `wPortChange.bit10` | 保留位元（命名邊界） |
| `PORT_CHANGE_RESERVED_BIT11` | `wPortChange.bit11` | 保留位元（命名邊界） |
| `PORT_CHANGE_RESERVED_BIT12` | `wPortChange.bit12` | 保留位元（命名邊界） |
| `PORT_CHANGE_RESERVED_BIT13` | `wPortChange.bit13` | 保留位元（命名邊界） |
| `PORT_CHANGE_RESERVED_BIT14` | `wPortChange.bit14` | 保留位元（命名邊界） |

## 使用規則

- `PORT_*` 對應到「當前狀態欄位」；`C_PORT_*` 對應到「變更事件欄位」。
- `PORT_*` 通常是 status 現狀語義，`C_PORT_*` 通常是 change 事件紀錄語義。
- `C_PORT_*` 常見在 `GET_STATUS` + `wPortChange` 的取值/清除流程上下文中使用；請透過對應頁面確認請求邊界。

## 交叉參照

- `specs/port_status_bits.md`：Status/Change 位元主頁
- `specs/feature_selectors.md`：PORT/C_PORT selector 對應頁
- `specs/hub_class_requests.md`：`GET_STATUS` / `SET_FEATURE` / `CLEAR_FEATURE` 請求族上下文
- `tables/port_status_bit_matrix.yaml`：狀態與變更位元來源表
- `tables/feature_selector_matrix.yaml`：selector 來源表

