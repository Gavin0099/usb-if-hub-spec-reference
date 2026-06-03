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
> 本頁是 hub / port status 與 change fields 的 reference summary，不是逐 bit 完整 verified reconstruction。

## Page Purpose

本頁要回答的是：

- `GET_STATUS` 可能回傳哪些 hub-level 與 port-level fields
- `Status` bits 與 `Change` bits 的基本差異
- repo 目前 machine-readable 層實際整理了哪些核心 bits
- 哪些 entries 目前已有 live `verified` promotion，以及那個 scope 有多窄

本頁不打算回答：

- 所有 port bits 是否都已完成 PDF section-level verification
- timing、debounce、reset、error recovery 是否已完成 correctness verification
- host 端 `SetPortFeature` / `ClearPortFeature` 的完整行為模型

## Status Field Model

- `GET_STATUS` 可以回傳 hub-level `wHubStatus` / `wHubChange`
- 也可以回傳 port-level `wPortStatus` / `wPortChange`
- `Status` bits 描述目前狀態
- `Change` bits 描述自上次 clear 之後，該狀態是否發生過變化
- 對 change bits 而言，`CLEAR_FEATURE(...)` 比較適合讀成「acknowledge and clear this recorded change event」

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

目前共有 6 筆 live governed entries 已升級為 `verified`：

| Entry | Field | Bit | Verified Scope |
|---|---|---|---|
| `PORT_CONNECTION` | `wPortStatus` | bit 0 | bit name and bit position only |
| `PORT_ENABLE` | `wPortStatus` | bit 1 | bit name and bit position only |
| `C_PORT_CONNECTION` | `wPortChange` | bit 0 | bit name and bit position only |
| `C_PORT_ENABLE` | `wPortChange` | bit 1 | bit name and bit position only |
| `HUB_LOCAL_POWER` | `wHubStatus` | bit 0 | bit name and bit position only |
| `HUB_OVER_CURRENT` | `wHubStatus` | bit 1 | bit name and bit position only |

目前 verified scope 仍刻意只涵蓋：

- bit 名稱
- bit 位置

以下內容都不是這個 repo 已 verified 的範圍：

- timing、debounce、reset、state-transition behavior
- `SetPortFeature` / `ClearPortFeature` 的 host-side semantics
- `PORT_ENABLE` 的完整 enable/disable state machine
- 整個 page 或整份 `port_status_bit_matrix` 已完成 verified promotion

因此本頁 frontmatter 仍維持：

- `claim_level: inferred`
- `status: review_required`
- `semantic_verification_claimed: false`

## Change Bits and `CLEAR_FEATURE`

可以把 `wPortChange` / `wHubChange` 想成 latched change-event flags：

- bit = `1`：代表對應狀態自上次 clear 後至少變動過一次
- bit = `0`：代表自上次 clear 後沒有記錄到這種變化
- `CLEAR_FEATURE(...)`：host acknowledge 這個 event，並清除對應的 recorded change bit

例子：

- `C_PORT_CONNECTION = 1` 代表 connection state 自上次 clear 後發生過變化
- host 讀完 `GET_STATUS` 之後，可以送 `CLEAR_FEATURE(C_PORT_CONNECTION)` 清除這筆事件紀錄
- 如果之後 connection 又變了，這個 bit 仍然可以再次被設成 `1`

## Speed Bits Must Be Decoded Together

`PORT_LOW_SPEED` 與 `PORT_HIGH_SPEED` 不應分開獨立解讀，它們形成的是聯合 speed encoding：

| `PORT_LOW_SPEED` | `PORT_HIGH_SPEED` | Interpretation |
|---|---|---|
| 0 | 0 | Full-speed |
| 1 | 0 | Low-speed |
| 0 | 1 | High-speed |
| 1 | 1 | Reserved / unexpected combination |

所以像 `PORT_LOW_SPEED = 0` 就是 full-speed 這種說法本身不完整。  
只有在 `PORT_HIGH_SPEED` 同時也是 `0` 時，才能判成 full-speed。

## Section Anchor and Verified-Scope Boundary

這個 repo 目前有兩種 evidence-related signals：

- `section_refs`，作為 evidence attachment metadata
- live `verified` promotions，目前是 `PORT_CONNECTION`、`PORT_ENABLE`、`C_PORT_CONNECTION`、`C_PORT_ENABLE`、`HUB_LOCAL_POWER`、`HUB_OVER_CURRENT`

兩者不能混為一談。

目前狀態是：

- 部分 pilot entries 帶有 `section_refs`
- `wPortStatus.bit0.PORT_CONNECTION`、`wPortStatus.bit1.PORT_ENABLE`、`wPortChange.bit0.C_PORT_CONNECTION`、`wPortChange.bit1.C_PORT_ENABLE`、`wHubStatus.bit0.HUB_LOCAL_POWER`、`wHubStatus.bit1.HUB_OVER_CURRENT` 都是 live `verified`
- 所有 verified scope 仍限定為 `bit_name_and_position_only`
- 這仍然不代表 USB 2.0 PDF semantic verification 已完成

如果未來 wiki claim block 需要 `section_refs`，仍應維持 Phase 7A 的 metadata 結構，例如：

```yaml
section_refs:
  - spec: usb20
    section: "11.24.2.7.1"
    anchor_type: section
    evidence_status: review_required
    applies_to: "PORT_CONNECTION summary block"
```

這個 metadata block 只是 evidence attachment，不會自動把 page 或 claim block 升成 `verified`。

## Governed Linkage

- `tables/port_status_bit_matrix.yaml`: hub / port status bit namespace 的 primary machine-readable source
- `specs/hub_class_requests.md`: `GET_STATUS`、`SET_FEATURE`、`CLEAR_FEATURE` 的 request-family summary
- `specs/feature_selectors.md`: `C_PORT_*` selectors 的 feature-selector boundary
- `specs/escalation_table.md`: E-02、E-03、E-09 等 escalation triggers

## Non-claims

- 本頁不宣告所有 port status bits 都已完成 PDF-level verification。
- 本頁不宣告 speed bits、reset bits、power bits 或相鄰語意都已 fully verified。
- 本頁不會把少數 verified entries 擴張成整頁都 verified 的宣告。
- 本頁不會把 status-bit summary 升格成 firmware implementation authority。
