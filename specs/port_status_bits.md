---
title: Port Status Bits
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Port Status Bits

> Source scope: USB 2.0 Specification Rev 2.0, Section 11.24.2.7.  
> 本頁是 reference summary，不是逐 bit 完整驗證過的 spec reconstruction。

## Page Purpose

本頁主要回答：

- `GET_STATUS` 可能回傳哪些 hub-level 與 port-level 欄位
- `Status` bits 與 `Change` bits 的差異
- machine-readable layer 目前暴露了哪些 hub/port status 與 change bits
- 哪些 entries 已完成 live `verified` promotion，以及 verified scope 有多窄

本頁不打算回答：

- 是否所有 port bits 都已完成 PDF section-level verification
- timing、debounce、reset、error recovery semantics 是否已完成 correctness verification
- `SET_FEATURE` / `CLEAR_FEATURE` 的完整 host behavior model

## Status Field Model

- `GET_STATUS` 可以回傳 hub-level 的 `wHubStatus` / `wHubChange`
- 也可以回傳 port-level 的 `wPortStatus` / `wPortChange`
- `Status` bits 描述目前狀態
- `Change` bits 描述該狀態自上次 clear 之後是否發生變化
- 對 change bits 來說，`CLEAR_FEATURE(...)` 最適合讀成「acknowledge 並清除此記錄中的 change event」

## Hub-Level Bits

| Field | Bit | Name | Meaning |
|---|---|---|---|
| `wHubStatus` | 0 | `HUB_LOCAL_POWER` | Hub local power status |
| `wHubStatus` | 1 | `HUB_OVER_CURRENT` | Hub over-current status |
| `wHubChange` | 0 | `C_HUB_LOCAL_POWER` | 記錄 local power status 自上次 clear 之後是否改變 |
| `wHubChange` | 1 | `C_HUB_OVER_CURRENT` | 記錄 over-current status 自上次 clear 之後是否改變 |

## Port-Level Bits

| Field | Bit | Name | State | Meaning |
|---|---|---|---|---|
| `wPortStatus` | 0 | `PORT_CONNECTION` | defined | Port connection status |
| `wPortStatus` | 1 | `PORT_ENABLE` | defined | Port enabled status |
| `wPortStatus` | 2 | `PORT_SUSPEND` | defined | Port suspend status |
| `wPortStatus` | 3 | `PORT_OVER_CURRENT` | defined | Port over-current status |
| `wPortStatus` | 4 | `PORT_RESET` | defined | Port reset status |
| `wPortStatus` | 8 | `PORT_POWER` | defined | Port power status |
| `wPortStatus` | 9 | `PORT_LOW_SPEED` | defined | Port low-speed status indicator |
| `wPortStatus` | 10 | `PORT_HIGH_SPEED` | defined | Port high-speed status indicator |
| `wPortStatus` | 11 | `PORT_TEST` | defined | Port test-mode status |
| `wPortStatus` | 12 | `PORT_INDICATOR` | defined | Port indicator status |
| `wPortStatus` | 15 | `PORT_STATUS_HIGH_BIT_BOUNDARY` | reserved | 16-bit status field 的 high-boundary placeholder |
| `wPortChange` | 0 | `C_PORT_CONNECTION` | defined | 記錄 connection status 自上次 clear 之後是否改變 |
| `wPortChange` | 1 | `C_PORT_ENABLE` | defined | 記錄 enable status 自上次 clear 之後是否改變 |
| `wPortChange` | 2 | `C_PORT_SUSPEND` | defined | 記錄 suspend status 自上次 clear 之後是否改變 |
| `wPortChange` | 3 | `C_PORT_OVER_CURRENT` | defined | 記錄 over-current status 自上次 clear 之後是否改變 |
| `wPortChange` | 4 | `C_PORT_RESET` | defined | 記錄 reset status 自上次 clear 之後是否改變 |
| `wPortChange` | 15 | `PORT_CHANGE_HIGH_BIT_BOUNDARY` | reserved | 16-bit change field 的 high-boundary placeholder |

新追蹤的 status/change entries 並不都代表 verified。  
目前只有下面列出的 16 個 live verified entries 完成 entry-level promotion。

## Live Verified Entries

目前有 16 個 live governed entries 已提升為 `verified`：

| Entry | Field | Bit | Verified Scope |
|---|---|---|---|
| `PORT_CONNECTION` | `wPortStatus` | bit 0 | bit name and bit position only |
| `PORT_ENABLE` | `wPortStatus` | bit 1 | bit name and bit position only |
| `PORT_SUSPEND` | `wPortStatus` | bit 2 | bit name and bit position only |
| `PORT_OVER_CURRENT` | `wPortStatus` | bit 3 | bit name and bit position only |
| `PORT_RESET` | `wPortStatus` | bit 4 | bit name and bit position only |
| `PORT_POWER` | `wPortStatus` | bit 8 | bit name and bit position only |
| `PORT_LOW_SPEED` | `wPortStatus` | bit 9 | bit name and bit position only |
| `PORT_HIGH_SPEED` | `wPortStatus` | bit 10 | bit name and bit position only |
| `PORT_TEST` | `wPortStatus` | bit 11 | bit name and bit position only |
| `PORT_INDICATOR` | `wPortStatus` | bit 12 | bit name and bit position only |
| `C_PORT_CONNECTION` | `wPortChange` | bit 0 | bit name and bit position only |
| `C_PORT_ENABLE` | `wPortChange` | bit 1 | bit name and bit position only |
| `HUB_LOCAL_POWER` | `wHubStatus` | bit 0 | bit name and bit position only |
| `HUB_OVER_CURRENT` | `wHubStatus` | bit 1 | bit name and bit position only |
| `C_HUB_LOCAL_POWER` | `wHubChange` | bit 0 | bit name and bit position only |
| `C_HUB_OVER_CURRENT` | `wHubChange` | bit 1 | bit name and bit position only |

這個 verified scope 是刻意收窄的，只涵蓋：

- bit name
- bit position

它**不代表**本 repo 已驗證：

- timing、debounce、reset 或 state-transition behavior
- host-side `SET_FEATURE` / `CLEAR_FEATURE` semantics
- 完整的 `PORT_ENABLE` enable/disable state machine
- 整頁內容或整張 `port_status_bit_matrix`

因此本頁 frontmatter 仍維持：

- `claim_level: inferred`
- `status: review_required`
- `semantic_verification_claimed: false`

## Reviewed Entries Outside Verified Scope

下列 port status/change entries 目前仍是 `reviewed`，不是 `verified`：

| Entry | Field | Bit | Reviewed Scope |
|---|---|---|---|
| `C_PORT_SUSPEND` | `wPortChange` | bit 2 | bit name and bit position only |
| `C_PORT_OVER_CURRENT` | `wPortChange` | bit 3 | bit name and bit position only |
| `C_PORT_RESET` | `wPortChange` | bit 4 | bit name and bit position only |

這些 entries 提升了 namespace coverage，但不表示 timing、state machine、clear sequencing、error recovery、speed decoding、test mode、power-switch policy 或 indicator behavior 已被驗證。

## Reviewed Boundary Placeholders

目前另外有 2 個 high-bit placeholders 只以 boundary markers 身分保留為 `reviewed`：

| Entry | Field | Bit | Reviewed Scope |
|---|---|---|---|
| `PORT_STATUS_HIGH_BIT_BOUNDARY` | `wPortStatus` | bit 15 | 16-bit status-field high boundary only |
| `PORT_CHANGE_HIGH_BIT_BOUNDARY` | `wPortChange` | bit 15 | 16-bit change-field high boundary only |

這些 reviewed placeholders 不定義新的 status semantics。  
它們只是讓 machine-readable layer 明確標示 status 與 change fields 都是 16-bit 欄位，且帶有 high-boundary marker。

## Change Bits and `CLEAR_FEATURE`

可以把 `wPortChange` / `wHubChange` 看成 latched change-event flags：

- bit = `1`：對應狀態自上次 clear 以來至少改變過一次
- bit = `0`：自上次 clear 以來沒有記錄到該變化
- `CLEAR_FEATURE(...)`：host acknowledge 這個事件並清除此記錄中的 change bit

例子：

- `C_PORT_CONNECTION = 1` 代表 connection state 自上次 clear 後發生過變化
- host 讀完 `GET_STATUS` 後，可以送出 `CLEAR_FEATURE(C_PORT_CONNECTION)` 來清除此事件紀錄
- 若之後 connection 再次改變，該 bit 可以再被設為 `1`

## Speed Bits Must Be Decoded Together

`PORT_LOW_SPEED` 與 `PORT_HIGH_SPEED` 不能獨立解讀；它們形成一組 speed encoding：

| `PORT_LOW_SPEED` | `PORT_HIGH_SPEED` | Interpretation |
|---|---|---|
| 0 | 0 | Full-speed |
| 1 | 0 | Low-speed |
| 0 | 1 | High-speed |
| 1 | 1 | Reserved / unexpected combination |

所以像「`PORT_LOW_SPEED = 0` 就表示 full-speed」這種說法本身是不完整的。  
只有在 `PORT_HIGH_SPEED` 也等於 `0` 時，才是 full-speed。

## Section Anchor and Verified-Scope Boundary

這個 repo 目前同時存在兩種 evidence-related signals：

- `section_refs`：evidence attachment metadata
- live `verified` promotions：目前包含 `PORT_CONNECTION`、`PORT_ENABLE`、`PORT_SUSPEND`、`PORT_OVER_CURRENT`、`PORT_RESET`、`PORT_POWER`、`PORT_LOW_SPEED`、`PORT_HIGH_SPEED`、`C_PORT_CONNECTION`、`C_PORT_ENABLE`、`HUB_LOCAL_POWER`、`HUB_OVER_CURRENT`、`C_HUB_LOCAL_POWER`、`C_HUB_OVER_CURRENT`

這兩者不能混為一談。

目前狀態：

- 部分 pilot entries 帶有 `section_refs`
- `wPortStatus.bit0.PORT_CONNECTION`、`wPortStatus.bit1.PORT_ENABLE`、`wPortStatus.bit2.PORT_SUSPEND`、`wPortStatus.bit3.PORT_OVER_CURRENT`、`wPortStatus.bit4.PORT_RESET`、`wPortStatus.bit8.PORT_POWER`、`wPortStatus.bit9.PORT_LOW_SPEED`、`wPortStatus.bit10.PORT_HIGH_SPEED`、`wPortChange.bit0.C_PORT_CONNECTION`、`wPortChange.bit1.C_PORT_ENABLE`、`wHubStatus.bit0.HUB_LOCAL_POWER`、`wHubStatus.bit1.HUB_OVER_CURRENT`、`wHubChange.bit0.C_HUB_LOCAL_POWER`、`wHubChange.bit1.C_HUB_OVER_CURRENT` 已是 live `verified`
- 所有 verified scope 仍然都是 `bit_name_and_position_only`
- 其餘已定義的 port status/change entries 仍然只是 reviewed namespace entries
- 這仍然不代表 USB 2.0 PDF semantic verification 已完成

若未來某個 wiki claim block 需要 `section_refs`，應維持 Phase 7A 的 metadata structure，例如：

```yaml
section_refs:
  - spec: usb20
    section: "11.24.2.7.1"
    anchor_type: section
    evidence_status: review_required
    applies_to: "PORT_CONNECTION summary block"
```

這個 metadata block 只是 evidence attachment，不會自動把頁面或 claim block 升級成 `verified`。

## Governed Linkage

- `tables/port_status_bit_matrix.yaml`: hub/port status bit namespaces 的 primary machine-readable source
- `specs/hub_class_requests.md`: `GET_STATUS`、`SET_FEATURE`、`CLEAR_FEATURE` 的 request-family summary
- `specs/feature_selectors.md`: `C_PORT_*` selectors 的 feature-selector boundary
- `specs/escalation_table.md`: `E-02`、`E-03`、`E-09` 等 escalation triggers

## Non-claims

- 本頁不宣告所有 port status bits 都已完成 PDF-level verification。
- 本頁不宣告 speed bits、reset bits、power bits 或相鄰 semantics 已全面 verified。
- 本頁不把 16 個 verified entries 擴張成整頁 verified。
- 本頁不把 high-bit boundary placeholders 視為已定義的 status 或 change semantics。
- 本頁不把 status-bit summary 提升成 firmware implementation authority。
