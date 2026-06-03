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
> 本頁是 hub / port status and change fields 的 reference summary，不是完整的逐 bit verified reconstruction。

## Page Purpose

本頁用來回答：

- `GET_STATUS` 回傳的 hub-level 與 port-level fields 是什麼
- `Status` bits 與 `Change` bits 應如何區分
- 目前 repo 已經 machine-readable 追蹤了哪些核心 bits
- 哪兩個 entries 已有窄範圍 `verified` promotion，以及它的邊界在哪裡

本頁不回答：

- 全部 port bits 是否都已完成 PDF section-level verification
- timing、debounce、reset、error recovery 是否已完成 correctness verification
- host 對 `SetPortFeature` / `ClearPortFeature` 的完整行為模型

## Status Field Model

- `GET_STATUS` 可能回傳 hub-level `wHubStatus` / `wHubChange`
- 也可能回傳 port-level `wPortStatus` / `wPortChange`
- `Status` bits 描述目前狀態
- `Change` bits 描述自上次 clear 之後，該狀態是否曾發生變化
- 對 change bits 而言，`CLEAR_FEATURE(...)` 最適合解讀成「acknowledge and clear this recorded change event」

## Hub-Level Bits

| Field | Bit | Name | Meaning |
|---|---|---|---|
| `wHubStatus` | 0 | `HUB_LOCAL_POWER` | Hub local power status |
| `wHubStatus` | 1 | `HUB_OVER_CURRENT` | Hub over-current status |
| `wHubChange` | 0 | `C_HUB_LOCAL_POWER` | Records whether local power status has changed since the last clear |
| `wHubChange` | 1 | `C_HUB_OVER_CURRENT` | Records whether over-current status has changed since the last clear |

## Minimum Port-Level Boundary

| Field | Bit | Name | State | Meaning |
|---|---|---|---|---|
| `wPortStatus` | 0 | `PORT_CONNECTION` | defined | Port connection status |
| `wPortStatus` | 1 | `PORT_ENABLE` | defined | Port enabled status |
| `wPortStatus` | 15 | `PORT_STATUS_HIGH_BIT_BOUNDARY` | reserved | Boundary placeholder for the 16-bit field |
| `wPortChange` | 0 | `C_PORT_CONNECTION` | defined | Records whether connection status has changed since the last clear |
| `wPortChange` | 1 | `C_PORT_ENABLE` | defined | Records whether enable status has changed since the last clear |
| `wPortChange` | 15 | `PORT_CHANGE_HIGH_BIT_BOUNDARY` | reserved | Boundary placeholder for the 16-bit change field |

## Live Verified Entries

目前只有兩個 live governed entries 被提升到 `verified`：

| Entry | Field | Bit | Verified Scope |
|---|---|---|---|
| `PORT_CONNECTION` | `wPortStatus` | bit 0 | bit name and bit position only |
| `PORT_ENABLE` | `wPortStatus` | bit 1 | bit name and bit position only |

這個 verified scope 刻意非常窄，只涵蓋：

- bit 名稱
- bit 位置

這**不代表**本 repo 已驗證：

- timing、debounce、reset 或 state-transition behavior
- `SetPortFeature` / `ClearPortFeature` 的 host-side semantics
- `PORT_ENABLE` 的完整 enable/disable state machine
- 整頁或整份 `port_status_bit_matrix` 已完成 verified promotion

因此本頁 frontmatter 仍然保持：

- `claim_level: inferred`
- `status: review_required`
- `semantic_verification_claimed: false`

## Change Bits and `CLEAR_FEATURE`

可以把 `wPortChange` / `wHubChange` 想成 latched change-event flags：

- bit = `1`：對應狀態自上次 clear 後至少改變過一次
- bit = `0`：自上次 clear 後沒有記錄到這類變化
- `CLEAR_FEATURE(...)`：host 對這個 change event 做 acknowledge，並清除該 record bit

例子：

- `C_PORT_CONNECTION = 1` 表示 connection state 自上次 clear 後曾變化
- host 在讀完 `GET_STATUS` 後，可以送 `CLEAR_FEATURE(C_PORT_CONNECTION)` 來清掉該事件記錄
- 如果之後 connection 再次變化，這個 bit 仍可再被設回 `1`

## Speed Bits Must Be Decoded Together

`PORT_LOW_SPEED` 與 `PORT_HIGH_SPEED` 不應獨立解讀，而應視為組合編碼：

| `PORT_LOW_SPEED` | `PORT_HIGH_SPEED` | Interpretation |
|---|---|---|
| 0 | 0 | Full-speed |
| 1 | 0 | Low-speed |
| 0 | 1 | High-speed |
| 1 | 1 | Reserved / unexpected combination |

因此像「`PORT_LOW_SPEED = 0` 就代表 full-speed」這種說法本身不完整。  
只有在 `PORT_HIGH_SPEED` 也為 `0` 時，才可解讀為 full-speed。

## Section Anchor and Verified-Scope Boundary

本 repo 目前有兩種不同的 evidence-related signals：

- `section_refs`：作為 evidence attachment metadata
- live `verified` promotions：目前只有 `PORT_CONNECTION` 與 `PORT_ENABLE`

這兩者不能混為一談。

目前狀態：

- 部分 pilot entries 帶有 `section_refs`
- `wPortStatus.bit0.PORT_CONNECTION` 與 `wPortStatus.bit1.PORT_ENABLE` 是 live `verified`
- verified scope 仍然只到 `bit_name_and_position_only`
- 這不等於 USB 2.0 PDF semantic verification 已完成

若未來要在 wiki claim block 掛上 `section_refs`，應維持 Phase 7A 的 metadata 結構，例如：

```yaml
section_refs:
  - spec: usb20
    section: "11.24.2.7.1"
    anchor_type: section
    evidence_status: review_required
    applies_to: "PORT_CONNECTION summary block"
```

這類 metadata block 只是 evidence attachment，不會自動把整頁或 claim block 升成 `verified`。

## Governed Linkage

- `tables/port_status_bit_matrix.yaml`: port/hub status bit namespace 的主要 machine-readable source
- `specs/hub_class_requests.md`: `GET_STATUS`、`SET_FEATURE`、`CLEAR_FEATURE` 的 request-family summary
- `specs/feature_selectors.md`: `C_PORT_*` selectors 與 feature namespace 邊界
- `specs/escalation_table.md`: E-02、E-03、E-09 等 escalation triggers

## Non-claims

- 本頁不宣告所有 port status bits 已完成 PDF-level verification
- 本頁不宣告 speed bits、reset bits、power bits 的完整語意都已 verified
- 本頁不把兩個 verified entries 擴張解讀成整頁 verified
- 本頁不把 status-bit summary 升級成 firmware implementation authority
