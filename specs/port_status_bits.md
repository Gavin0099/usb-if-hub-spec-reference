---
title: Port Status Bits
claim_level: inferred
status: review_required
last_reviewed: "2026-06-05"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Port Status Bits

> 資料範圍：USB 2.0 Specification Rev 2.0，第 11.24.2.7 章節。  
> 本頁是參考摘要，不是完整逐 bit 重建的規格真值表。

## 頁面目的

本頁回答：

- `GET_STATUS` 可回傳哪些 hub-level / port-level 欄位
- `Status` bit 與 `Change` bit 的差異
- 哪些 hub/port 狀態/變更 bit 已透過機器可讀層曝光
- 哪些 entries 目前有 `verified`，以及 verified 範圍有多窄

本頁不回答：

- 是否所有 port bit 都已完成 PDF section-level 驗證
- timing、debounce、reset、error-recovery 是否已完成 correctness 驗證
- `SET_FEATURE` / `CLEAR_FEATURE` 的完整 host behavior 模型

## Status Field Model

- `GET_STATUS` 可回傳 hub-level 的 `wHubStatus` / `wHubChange`
- 也可回傳 port-level 的 `wPortStatus` / `wPortChange`
- `Status` bits：描述目前狀態
- `Change` bits：描述自上次 clear 之後是否有變更
- 對於 change bits，`CLEAR_FEATURE(...)` 最好先解作「acknowledge 並清除已記錄事件」

## Hub-Level Bits

| Field | Bit | Name | 意義 |
|---|---|---|---|
| `wHubStatus` | 0 | `HUB_LOCAL_POWER` | Hub local power 狀態 |
| `wHubStatus` | 1 | `HUB_OVER_CURRENT` | Hub 過電流狀態 |
| `wHubChange` | 0 | `C_HUB_LOCAL_POWER` | 表示自上次 clear 後 local power 有變更 |
| `wHubChange` | 1 | `C_HUB_OVER_CURRENT` | 表示自上次 clear 後 over-current 有變更 |

## Port-Level Bits

| Field | Bit | Name | State | 意義 |
|---|---|---|---|---|
| `wPortStatus` | 0 | `PORT_CONNECTION` | defined | Port 目前是否有連線 |
| `wPortStatus` | 1 | `PORT_ENABLE` | defined | Port 啟用狀態 |
| `wPortStatus` | 2 | `PORT_SUSPEND` | defined | Port 休眠/suspend 狀態 |
| `wPortStatus` | 3 | `PORT_OVER_CURRENT` | defined | Port 過電流狀態 |
| `wPortStatus` | 4 | `PORT_RESET` | defined | Port reset 狀態 |
| `wPortStatus` | 8 | `PORT_POWER` | defined | Port 電源開關狀態 |
| `wPortStatus` | 9 | `PORT_LOW_SPEED` | defined | Port 低速指示位 |
| `wPortStatus` | 10 | `PORT_HIGH_SPEED` | defined | Port 高速指示位 |
| `wPortStatus` | 11 | `PORT_TEST` | defined | Port test-mode 狀態 |
| `wPortStatus` | 12 | `PORT_INDICATOR` | defined | Port 指示燈狀態 |
| `wPortStatus` | 15 | `PORT_STATUS_HIGH_BIT_BOUNDARY` | reserved | 16-bit status 欄位邊界標記 |
| `wPortChange` | 0 | `C_PORT_CONNECTION` | defined | 表示自上次 clear 後連線狀態有變更 |
| `wPortChange` | 1 | `C_PORT_ENABLE` | defined | 表示自上次 clear 後 enable 狀態有變更 |
| `wPortChange` | 2 | `C_PORT_SUSPEND` | defined | 表示自上次 clear 後 suspend 狀態有變更 |
| `wPortChange` | 3 | `C_PORT_OVER_CURRENT` | defined | 表示自上次 clear 後過電流狀態有變更 |
| `wPortChange` | 4 | `C_PORT_RESET` | defined | 表示自上次 clear 後 reset 狀態有變更 |
| `wPortChange` | 15 | `PORT_CHANGE_HIGH_BIT_BOUNDARY` | reserved | 16-bit change 欄位邊界標記 |

Not all tracked status/change entries are verified.  
目前只有下列 19 筆有進入 entry-level promotion：

| Entry | Field | Bit | Verified Scope |
|---|---|---|---|
| `PORT_CONNECTION` | `wPortStatus` | bit 0 | bit name 與 bit position |
| `PORT_ENABLE` | `wPortStatus` | bit 1 | bit name 與 bit position |
| `PORT_SUSPEND` | `wPortStatus` | bit 2 | bit name 與 bit position |
| `PORT_OVER_CURRENT` | `wPortStatus` | bit 3 | bit name 與 bit position |
| `PORT_RESET` | `wPortStatus` | bit 4 | bit name 與 bit position |
| `PORT_POWER` | `wPortStatus` | bit 8 | bit name 與 bit position |
| `PORT_LOW_SPEED` | `wPortStatus` | bit 9 | bit name 與 bit position |
| `PORT_HIGH_SPEED` | `wPortStatus` | bit 10 | bit name 與 bit position |
| `PORT_TEST` | `wPortStatus` | bit 11 | bit name 與 bit position |
| `PORT_INDICATOR` | `wPortStatus` | bit 12 | bit name 與 bit position |
| `C_PORT_CONNECTION` | `wPortChange` | bit 0 | bit name 與 bit position |
| `C_PORT_ENABLE` | `wPortChange` | bit 1 | bit name 與 bit position |
| `C_PORT_SUSPEND` | `wPortChange` | bit 2 | bit name 與 bit position |
| `C_PORT_OVER_CURRENT` | `wPortChange` | bit 3 | bit name 與 bit position |
| `C_PORT_RESET` | `wPortChange` | bit 4 | bit name 與 bit position |
| `HUB_LOCAL_POWER` | `wHubStatus` | bit 0 | bit name 與 bit position |
| `HUB_OVER_CURRENT` | `wHubStatus` | bit 1 | bit name 與 bit position |
| `C_HUB_LOCAL_POWER` | `wHubChange` | bit 0 | bit name 與 bit position |
| `C_HUB_OVER_CURRENT` | `wHubChange` | bit 1 | bit name 與 bit position |

這個 verified 範圍刻意窄化，只涵蓋：

- bit name
- bit position

它不代表本 repo 已完成：

- timing、debounce、reset、state-transition 行為
- host-side `SET_FEATURE` / `CLEAR_FEATURE` semantics
- `PORT_ENABLE` 全面的 enable/disable 狀態機
- 全頁或完整 `port_status_bit_matrix` 驗證

所以 frontmatter 仍維持：

- `claim_level: inferred`
- `status: review_required`
- `semantic_verification_claimed: false`

## Reviewed Entries Outside Verified Scope

目前除兩個高位 boundary placeholder 外，沒有其他 `reviewed` 但未 `verified` 的 live entries。

這些 boundary entry 只提升 namespace 覆蓋，不代表已驗證：

- timing、state machine
- clear sequencing
- error recovery
- speed decode
- test-mode
- power-switch 政策
- indicator 行為

## Reviewed Boundary Placeholders

兩個 high-bit placeholder 只保留 boundary marker 的 role：

| Entry | Field | Bit | Reviewed Scope |
|---|---|---|---|
| `PORT_STATUS_HIGH_BIT_BOUNDARY` | `wPortStatus` | bit 15 | 16-bit status 欄位長度標記 |
| `PORT_CHANGE_HIGH_BIT_BOUNDARY` | `wPortChange` | bit 15 | 16-bit change 欄位長度標記 |

這些 boundary markers 不定義額外的 status semantics。  
它們是 boundary-only review marker，僅宣告欄位為 16-bit 的邊界，不改變 verified 計數或 scope。

## Change Bits 與 `CLEAR_FEATURE`

可把 `wPortChange` / `wHubChange` 當作 latch 的事件旗標：

- bit = `1`：自上次 clear 後該狀態至少變過一次
- bit = `0`：自上次 clear 後未記錄到變化
- `CLEAR_FEATURE(...)`：host 先 ack 該事件，清除已記錄變更

示例：

- `C_PORT_CONNECTION = 1` 代表自上次 clear 後連線狀態有變更
- 讀取 `GET_STATUS` 後，host 可執行 `CLEAR_FEATURE(C_PORT_CONNECTION)` 清除事件紀錄
- 若連線再次變更，bit 可再次被設為 `1`

## PORT_* 與 C_PORT_* 行為註解

以下維持行為邊界的最小註解，不延伸到完整時序或 state machine 證明。

### `PORT_*`（status bits）

- `PORT_CONNECTION`
  - `1` 代表 port 目前為活躍連線，`0` 代表無有效連線。
  - 「剛剛連上」這種轉移通常搭配 `C_PORT_CONNECTION` 來推論。
- `PORT_ENABLE`
  - 表示控制器觀點下 port 已被邏輯啟用。
  - 本頁只保留 bit 意義，enable/disable state machine 未宣告完整。
- `PORT_SUSPEND`
  - `1` 一般表示 suspend-like 行為中，`0` 表示未 suspend。
  - 完整 suspend/resume 時序與轉態仍不在本頁範圍。
- `PORT_OVER_CURRENT`
  - `1` 表示 status context 下回報過電流。
  - 過電流恢復門檻與重試時序仍屬 firmware / 專案責任。
- `PORT_RESET`
  - 表示 port reset 狀態是否 active（status context）。
- `PORT_POWER`
  - 表示 port 電源是否 currently enabled。
  - 實務上可能有瞬態延遲，需與韌體 telemetry 對齊。
- `PORT_LOW_SPEED`、`PORT_HIGH_SPEED`
  - 速度 bits 必須成對解讀，見下一節。
- `PORT_TEST`
  - 表示 test-mode 相關狀態，但不能單獨證明 test 流程完成。
- `PORT_INDICATOR`
  - 表示 port indicator 狀態；本頁只保留角色層摘要。

### `C_PORT_*`（change bits）

- `C_PORT_CONNECTION`
  - `1` 代表自上次 clear 後發生連線狀態變更事件。
- `C_PORT_ENABLE`
  - `1` 代表自上次 clear 後偵測到 enable 相關變更。
- `C_PORT_SUSPEND`
  - `1` 代表自上次 clear 後 suspend 相關狀態變更（進入/離開）。
- `C_PORT_OVER_CURRENT`
  - `1` 代表自上次 clear 後發生過電流相關變更。
- `C_PORT_RESET`
  - `1` 代表自上次 clear 後發生 reset 相關變更事件。

一般提醒：

- `C_PORT_*` 先描述的是「有事件被記錄」，不是完整當前狀態本身。
- 正常解讀路徑是：先搭配 `GET_STATUS` 讀取對應 status，再以 `CLEAR_FEATURE` 清除事件。

## Speed Bits 必須共同解碼

`PORT_LOW_SPEED` 與 `PORT_HIGH_SPEED` 不可單獨解讀，必須一起看：

| `PORT_LOW_SPEED` | `PORT_HIGH_SPEED` | 解讀 |
|---|---|---|
| 0 | 0 | Full-speed |
| 1 | 0 | Low-speed |
| 0 | 1 | High-speed |
| 1 | 1 | 保留 / 異常組合 |

所以「`PORT_LOW_SPEED = 0` 表示 full-speed」是不完整的；  
它僅在 `PORT_HIGH_SPEED = 0` 時才成立。

## Section Anchor 與 Verified 範圍邊界

目前本 repo 同時有兩類 evidence 訊號：

- `section_refs` 作為 evidence 附件 metadata
- live `verified` promotion，現列於 `PORT_CONNECTION`、`PORT_ENABLE`、`PORT_SUSPEND`、`PORT_OVER_CURRENT`、`PORT_RESET`、`PORT_POWER`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED`、`PORT_TEST`、`PORT_INDICATOR`、`C_PORT_CONNECTION`、`C_PORT_ENABLE`、`C_PORT_SUSPEND`、`C_PORT_OVER_CURRENT`、`C_PORT_RESET`、`HUB_LOCAL_POWER`、`HUB_OVER_CURRENT`、`C_HUB_LOCAL_POWER`、`C_HUB_OVER_CURRENT`

兩者不能混用。

目前狀態：

- 已有選定項帶有 `section_refs`
- `wPortStatus.bit0.PORT_CONNECTION`、`wPortStatus.bit1.PORT_ENABLE`、`wPortStatus.bit2.PORT_SUSPEND`、`wPortStatus.bit3.PORT_OVER_CURRENT`、`wPortStatus.bit4.PORT_RESET`、`wPortStatus.bit8.PORT_POWER`、`wPortStatus.bit9.PORT_LOW_SPEED`、`wPortStatus.bit10.PORT_HIGH_SPEED`、`wPortStatus.bit11.PORT_TEST`、`wPortStatus.bit12.PORT_INDICATOR`、`wPortChange.bit0.C_PORT_CONNECTION`、`wPortChange.bit1.C_PORT_ENABLE`、`wPortChange.bit2.C_PORT_SUSPEND`、`wPortChange.bit3.C_PORT_OVER_CURRENT`、`wPortChange.bit4.C_PORT_RESET`、`wHubStatus.bit0.HUB_LOCAL_POWER`、`wHubStatus.bit1.HUB_OVER_CURRENT`、`wHubChange.bit0.C_HUB_LOCAL_POWER`、`wHubChange.bit1.C_HUB_OVER_CURRENT` 為 live `verified`
- 所有 verified scopes 仍只到 `bit_name_and_position_only`
- 剩餘定義好的 port status/change entries 目前是 reviewed namespace entries only（目前沒有其餘）
- 這仍不代表 USB 2.0 規格語意驗證完整

若未來 wiki claim block 需要 `section_refs`，請採用 Phase 7A metadata 格式，例如：

```yaml
section_refs:
  - spec: usb20
    section: "11.24.2.7.1"
    anchor_type: section
    evidence_status: review_required
    applies_to: "PORT_CONNECTION summary block"
```

這段 metadata 只作 evidence 附件，不會自動把區塊升到 verified。

## Governed Linkage

- `tables/port_status_bit_matrix.yaml`：selector 狀態位元 namespace 的主要機器可讀來源
- `specs/hub_class_requests.md`：`GET_STATUS`、`SET_FEATURE`、`CLEAR_FEATURE` request 摘要
- `specs/feature_selectors.md`：`C_PORT_*` 的 selector 邊界
- `specs/escalation_table.md`：如 E-02、E-03、E-09 escalation 觸發

## Non-claims

- 本頁不聲明所有 port status bits 已完成 PDF-level verification。
- 本頁不聲明 speed、reset、power、或相鄰 semantics 全部完成 verify。
- 本頁不將 19 筆 verified 擴展成整頁 verified 的主張。
- 本頁不把高位 boundary placeholder 當成實際 status/change semantics。
- 本頁不將 status-bit summary 提升為 firmware 實作權威。
