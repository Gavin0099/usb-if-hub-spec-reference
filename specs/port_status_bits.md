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
> 本頁是 hub / port status 與 change fields 的 reference summary，不是完整 bit-by-bit verified reconstruction。

## Page Purpose

本頁回答：

- `GET_STATUS` 可能回傳哪些 hub-level 與 port-level fields。
- `Status` bits 與 `Change` bits 的差異。
- 目前 machine-readable layer 暴露哪些核心 bits。
- 哪些 entries 目前已有 live `verified` promotion，以及 verified scope 有多窄。
- 哪些 high-bit placeholders 只是 16-bit field boundary markers。

本頁不回答：

- 所有 port bits 是否已完成 PDF section-level verification。
- Timing、debounce、reset、error-recovery semantics 是否已完成 correctness verification。
- `SetPortFeature` / `ClearPortFeature` 的完整 host behavior model。

## Status Field Model

- `GET_STATUS` 可回傳 hub-level `wHubStatus` / `wHubChange`。
- 也可回傳 port-level `wPortStatus` / `wPortChange`。
- `Status` bits 描述目前狀態。
- `Change` bits 描述該狀態自上次 clear 之後是否改變過。
- 對 change bits 來說，`CLEAR_FEATURE(...)` 最好讀成「acknowledge and clear this recorded change event」。

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

目前有 8 筆 live governed entries promoted to `verified`：

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

Verified scope 刻意很窄，只涵蓋：

- bit name
- bit position

它不代表本 repo 已 verified：

- timing、debounce、reset 或 state-transition behavior
- host-side `SetPortFeature` / `ClearPortFeature` semantics
- 完整 `PORT_ENABLE` enable/disable state machine
- 整頁或完整 `port_status_bit_matrix`

所以本頁 frontmatter 仍維持：

- `claim_level: inferred`
- `status: review_required`
- `semantic_verification_claimed: false`

## Reviewed Boundary Placeholders

兩個 high-bit placeholders 現在只作為 boundary markers reviewed：

| Entry | Field | Bit | Reviewed Scope |
|---|---|---|---|
| `PORT_STATUS_HIGH_BIT_BOUNDARY` | `wPortStatus` | bit 15 | 16-bit status-field high boundary only |
| `PORT_CHANGE_HIGH_BIT_BOUNDARY` | `wPortChange` | bit 15 | 16-bit change-field high boundary only |

這些 reviewed placeholders 不定義額外 status semantics。
它們只讓 machine-readable layer 明確保留 status 與 change fields 的 16-bit high-boundary marker。

## Change Bits and `CLEAR_FEATURE`

可以把 `wPortChange` / `wHubChange` 理解為 latched change-event flags：

- bit = `1`：對應狀態自上次 clear 之後至少改變過一次。
- bit = `0`：自上次 clear 之後沒有記錄到該 change event。
- `CLEAR_FEATURE(...)`：host acknowledge 該 event，並清除 recorded change bit。

Example:

- `C_PORT_CONNECTION = 1` 代表 connection state 自上次 clear 後發生過變化。
- Host 讀完 `GET_STATUS` 後，可以送 `CLEAR_FEATURE(C_PORT_CONNECTION)` 清除該 event record。
- 如果之後 connection 又改變，該 bit 可再次被 set。

## Speed Bits Must Be Decoded Together

`PORT_LOW_SPEED` 與 `PORT_HIGH_SPEED` 不應獨立解讀。它們形成 combined speed encoding：

| `PORT_LOW_SPEED` | `PORT_HIGH_SPEED` | Interpretation |
|---|---|---|
| 0 | 0 | Full-speed |
| 1 | 0 | Low-speed |
| 0 | 1 | High-speed |
| 1 | 1 | Reserved / unexpected combination |

所以「`PORT_LOW_SPEED = 0` means full-speed」這種說法本身不完整。
只有在 `PORT_HIGH_SPEED` 同時也是 `0` 時，才能判成 full-speed。

## Section Anchor and Verified-Scope Boundary

本 repo 目前有兩種 evidence-related signals：

- `section_refs` 作為 evidence attachment metadata。
- live `verified` promotions，目前是 `PORT_CONNECTION`、`PORT_ENABLE`、`C_PORT_CONNECTION`、`C_PORT_ENABLE`、`HUB_LOCAL_POWER`、`HUB_OVER_CURRENT`、`C_HUB_LOCAL_POWER`、`C_HUB_OVER_CURRENT`。

這兩者不應混淆。

Current state:

- selected pilot entries carry `section_refs`
- `wPortStatus.bit0.PORT_CONNECTION`、`wPortStatus.bit1.PORT_ENABLE`、`wPortChange.bit0.C_PORT_CONNECTION`、`wPortChange.bit1.C_PORT_ENABLE`、`wHubStatus.bit0.HUB_LOCAL_POWER`、`wHubStatus.bit1.HUB_OVER_CURRENT`、`wHubChange.bit0.C_HUB_LOCAL_POWER`、`wHubChange.bit1.C_HUB_OVER_CURRENT` 是 live `verified`
- 所有 verified scopes 仍限制為 `bit_name_and_position_only`
- high-bit boundary placeholders 是 reviewed boundary markers，不是 verified bit semantics
- 這仍不代表 USB 2.0 PDF semantic verification 已完成

如果 future wiki claim block 需要 `section_refs`，應保留 Phase 7A metadata structure，例如：

```yaml
section_refs:
  - spec: usb20
    section: "11.24.2.7.1"
    anchor_type: section
    evidence_status: review_required
    applies_to: "PORT_CONNECTION summary block"
```

這個 metadata block 只是 evidence attachment，不會自動把 page 或 claim block promote to `verified`。

## Governed Linkage

- `tables/port_status_bit_matrix.yaml`: hub / port status bit namespace 的 primary machine-readable source。
- `specs/hub_class_requests.md`: `GET_STATUS`、`SET_FEATURE`、`CLEAR_FEATURE` 的 request-family summary。
- `specs/feature_selectors.md`: `C_PORT_*` selectors 的 feature-selector boundary。
- `specs/escalation_table.md`: E-02、E-03、E-09 escalation triggers。

## Non-claims

- 本頁不宣告所有 port status bits 已完成 PDF-level verification。
- 本頁不宣告 speed bits、reset bits、power bits 或 adjacent semantics 已 fully verified。
- 本頁不把 8 筆 verified entries 擴張成整頁 verified claim。
- 本頁不把 high-bit boundary placeholders 視為已定義的 status 或 change semantics。
- 本頁不把 status-bit summary 升級成 firmware implementation authority。
