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
> 本頁是 reference summary，不是逐 bit 的完整 verified spec reconstruction。

## Page Purpose

本頁主要回答：

- `GET_STATUS` 可能回傳哪些 hub-level 與 port-level 欄位
- `Status` bits 與 `Change` bits 有何差異
- 目前 machine-readable layer 已暴露哪些 hub/port status 與 change bits
- 哪些 entries 目前已進入 live `verified` promotion，以及這個 verified scope 有多窄

本頁不回答：

- 是否所有 port bits 都已完成 PDF section-level verification
- timing、debounce、reset 與 error-recovery semantics 是否都已完成 correctness verification
- `SET_FEATURE` / `CLEAR_FEATURE` 的完整 host behavior model

## Status Field Model

- `GET_STATUS` 可回傳 hub-level 的 `wHubStatus` / `wHubChange`
- 也可回傳 port-level 的 `wPortStatus` / `wPortChange`
- `Status` bits 描述目前狀態
- `Change` bits 描述自上次 clear 之後，該狀態是否發生過變化
- 對 change bits 來說，`CLEAR_FEATURE(...)` 最好理解為「確認並清除此已記錄的 change event」

## Hub-Level Bits

| Field | Bit | Name | Meaning |
|---|---|---|---|
| `wHubStatus` | 0 | `HUB_LOCAL_POWER` | Hub local power status |
| `wHubStatus` | 1 | `HUB_OVER_CURRENT` | Hub over-current status |
| `wHubChange` | 0 | `C_HUB_LOCAL_POWER` | 記錄 local power status 自上次 clear 之後是否有變化 |
| `wHubChange` | 1 | `C_HUB_OVER_CURRENT` | 記錄 over-current status 自上次 clear 之後是否有變化 |

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
| `wPortStatus` | 15 | `PORT_STATUS_HIGH_BIT_BOUNDARY` | reserved | 16-bit status field 的高位邊界 placeholder |
| `wPortChange` | 0 | `C_PORT_CONNECTION` | defined | 記錄 connection status 自上次 clear 之後是否有變化 |
| `wPortChange` | 1 | `C_PORT_ENABLE` | defined | 記錄 enable status 自上次 clear 之後是否有變化 |
| `wPortChange` | 2 | `C_PORT_SUSPEND` | defined | 記錄 suspend status 自上次 clear 之後是否有變化 |
| `wPortChange` | 3 | `C_PORT_OVER_CURRENT` | defined | 記錄 over-current status 自上次 clear 之後是否有變化 |
| `wPortChange` | 4 | `C_PORT_RESET` | defined | 記錄 reset status 自上次 clear 之後是否有變化 |
| `wPortChange` | 15 | `PORT_CHANGE_HIGH_BIT_BOUNDARY` | reserved | 16-bit change field 的高位邊界 placeholder |

這些新增追蹤的 status/change entries 目前只是 reviewed namespace entries。  
它們不會把 verified scope 擴大到下方列出的 8 個 live verified entries 之外。

## Live Verified Entries

目前有 8 個 live governed entries 已升級為 `verified`：

| Entry | Field | Bit | Verified Scope |
|---|---|---|---|
| `PORT_CONNECTION` | `wPortStatus` | bit 0 | bit name and bit position only |
| `PORT_ENABLE` | `wPortStatus` | bit 1 | bit name and bit position only |
| `C_PORT_CONNECTION` | `wPortChange` | bit 0 | bit name and bit position only |
| `C_PORT_ENABLE` | `wPortChange` | bit 1 | bit name and bit position only |
| `HUB_LOCAL_POWER` | `wHubStatus` | bit 0 | bit name and bit position only |
| `HUB_OVER_CURRENT` | `wHubStatus` | bit 1 | bit name and bit position only |
| `C_HUB_LOCAL_POWER` | `wHubChange` | bit 0 | bit name and bit position only |
| `C_HUB_OVER_CURRENT` | `wHubChange` | bit 1 | bit name and bit position only |

這個 verified scope 是刻意保持狹窄的，只涵蓋：

- bit name
- bit position

它**不代表**本 repo 已驗證：

- timing、debounce、reset 或 state-transition behavior
- host-side `SET_FEATURE` / `CLEAR_FEATURE` semantics
- `PORT_ENABLE` 的完整 enable/disable state machine
- 整頁內容或整份 `port_status_bit_matrix`

因此本頁 frontmatter 仍維持：

- `claim_level: inferred`
- `status: review_required`
- `semantic_verification_claimed: false`

## Reviewed Entries Outside Verified Scope

下列 port status/change entries 目前屬於 `reviewed`，不是 `verified`：

| Entry | Field | Bit | Reviewed Scope |
|---|---|---|---|
| `PORT_SUSPEND` | `wPortStatus` | bit 2 | bit name and bit position only |
| `PORT_OVER_CURRENT` | `wPortStatus` | bit 3 | bit name and bit position only |
| `PORT_RESET` | `wPortStatus` | bit 4 | bit name and bit position only |
| `PORT_POWER` | `wPortStatus` | bit 8 | bit name and bit position only |
| `PORT_LOW_SPEED` | `wPortStatus` | bit 9 | bit name and bit position only |
| `PORT_HIGH_SPEED` | `wPortStatus` | bit 10 | bit name and bit position only |
| `PORT_TEST` | `wPortStatus` | bit 11 | bit name and bit position only |
| `PORT_INDICATOR` | `wPortStatus` | bit 12 | bit name and bit position only |
| `C_PORT_SUSPEND` | `wPortChange` | bit 2 | bit name and bit position only |
| `C_PORT_OVER_CURRENT` | `wPortChange` | bit 3 | bit name and bit position only |
| `C_PORT_RESET` | `wPortChange` | bit 4 | bit name and bit position only |

這些 entries 改善了 namespace coverage，但仍不驗證 timing、state machines、clear sequencing、error recovery、speed decoding、test-mode behavior、power-switch policy 或 indicator behavior。

## Reviewed Boundary Placeholders

目前有兩個高位 placeholders 被當作 boundary markers 而標記為 reviewed：

| Entry | Field | Bit | Reviewed Scope |
|---|---|---|---|
| `PORT_STATUS_HIGH_BIT_BOUNDARY` | `wPortStatus` | bit 15 | 16-bit status-field high boundary only |
| `PORT_CHANGE_HIGH_BIT_BOUNDARY` | `wPortChange` | bit 15 | 16-bit change-field high boundary only |

這些 reviewed placeholders 不定義額外的 status semantics。  
它們只是讓 machine-readable layer 明確保留 status 與 change fields 為 16-bit 欄位，並標出高位邊界。

## Change Bits and `CLEAR_FEATURE`

你可以把 `wPortChange` / `wHubChange` 想成 latched change-event flags：

- bit = `1`：對應狀態自上次 clear 之後至少變化過一次
- bit = `0`：自上次 clear 之後未記錄到此類變化
- `CLEAR_FEATURE(...)`：host 確認此事件，並清除該記錄的 change bit

例子：

- `C_PORT_CONNECTION = 1` 代表 connection state 自上次 clear 之後發生過變化
- host 在讀完 `GET_STATUS` 之後，可以送出 `CLEAR_FEATURE(C_PORT_CONNECTION)` 來清除此事件紀錄
- 若之後 connection 再次變化，該 bit 仍可再次被設為 `1`

## Speed Bits Must Be Decoded Together

`PORT_LOW_SPEED` 與 `PORT_HIGH_SPEED` 不應被獨立解讀；它們共同形成速度編碼：

| `PORT_LOW_SPEED` | `PORT_HIGH_SPEED` | Interpretation |
|---|---|---|
| 0 | 0 | Full-speed |
| 1 | 0 | Low-speed |
| 0 | 1 | High-speed |
| 1 | 1 | Reserved / unexpected combination |

因此像「`PORT_LOW_SPEED = 0` 就表示 full-speed」這種說法本身不完整。  
只有在 `PORT_HIGH_SPEED` 也為 `0` 時，才可解讀為 full-speed。

## Section Anchor and Verified-Scope Boundary

本 repo 目前同時帶有兩種 evidence-related signals：

- `section_refs`：作為 evidence attachment metadata
- live `verified` promotions：目前包括 `PORT_CONNECTION`、`PORT_ENABLE`、`C_PORT_CONNECTION`、`C_PORT_ENABLE`、`HUB_LOCAL_POWER`、`HUB_OVER_CURRENT`、`C_HUB_LOCAL_POWER`、`C_HUB_OVER_CURRENT`

兩者不應混為一談。

目前狀態：

- 部分 pilot entries 已帶有 `section_refs`
- `wPortStatus.bit0.PORT_CONNECTION`、`wPortStatus.bit1.PORT_ENABLE`、`wPortChange.bit0.C_PORT_CONNECTION`、`wPortChange.bit1.C_PORT_ENABLE`、`wHubStatus.bit0.HUB_LOCAL_POWER`、`wHubStatus.bit1.HUB_OVER_CURRENT`、`wHubChange.bit0.C_HUB_LOCAL_POWER` 與 `wHubChange.bit1.C_HUB_OVER_CURRENT` 為 live `verified`
- 所有 verified scopes 仍維持 `bit_name_and_position_only`
- 其餘已定義的 port status/change entries 仍是 reviewed namespace entries
- 這仍不表示 USB 2.0 PDF semantic verification 已經完成

如果未來某個 wiki claim block 需要 `section_refs`，應保留 Phase 7A 的 metadata structure，例如：

```yaml
section_refs:
  - spec: usb20
    section: "11.24.2.7.1"
    anchor_type: section
    evidence_status: review_required
    applies_to: "PORT_CONNECTION summary block"
```

這類 metadata block 只是 evidence attachment。它不會自動把頁面或 claim block 升級成 `verified`。

## Governed Linkage

- `tables/port_status_bit_matrix.yaml`：hub/port status bit namespaces 的 primary machine-readable source
- `specs/hub_class_requests.md`：`GET_STATUS`、`SET_FEATURE` 與 `CLEAR_FEATURE` 的 request-family summary
- `specs/feature_selectors.md`：`C_PORT_*` selectors 的 feature-selector boundary
- `specs/escalation_table.md`：E-02、E-03 與 E-09 等 escalation triggers

## Non-claims

- 本頁不宣告所有 port status bits 都已完成 PDF-level verification。
- 本頁不宣告 speed bits、reset bits、power bits 或鄰近 semantics 已完整驗證。
- 本頁不把 8 個 verified entries 擴大解讀為整頁皆已 verified。
- 本頁不把高位 boundary placeholders 視為已定義的 status 或 change semantics。
- 本頁不把 status-bit summary 升級為 firmware implementation authority。
