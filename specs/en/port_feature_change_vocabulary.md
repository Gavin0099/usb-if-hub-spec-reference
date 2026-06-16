---
title: Port Feature/Change Vocabulary
claim_level: inferred
status: review_required
last_reviewed: "2026-06-16"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Port Feature / Change Vocabulary

> This page aligns the meaning of `PORT_*` and `C_PORT_*` terms used across this repo.
> It is a terminology boundary page only; it does not expand behavior correctness claims.

## Scope

- Align `PORT_*` status terms from `wPortStatus` with `C_PORT_*` change terms from `wPortChange`.
- Align selector-based naming expectations with `feature_selector_matrix` and status/change matrix naming.
- Keep boundary markers and reserved slots as explicit "namespaced non-behavior" surfaces.

## Non-goals

- This page does not claim full `PORT_*` state-machine behavior.
- This page does not treat `C_PORT_*` values as complete port state.
- This page does not claim `SET_FEATURE` / `CLEAR_FEATURE` timing or transition correctness.

## Vocabulary Alignment

### `PORT_*` status vocabulary (`wPortStatus`)

| Term | Field/Bit | Canonical meaning |
|---|---|---|
| `PORT_CONNECTION` | `wPortStatus.bit0` | Port connection presence |
| `PORT_ENABLE` | `wPortStatus.bit1` | Port enabled state marker |
| `PORT_SUSPEND` | `wPortStatus.bit2` | Suspend-related state marker |
| `PORT_OVER_CURRENT` | `wPortStatus.bit3` | Over-current condition marker |
| `PORT_RESET` | `wPortStatus.bit4` | Reset condition marker |
| `PORT_POWER` | `wPortStatus.bit8` | Port power state marker |
| `PORT_LOW_SPEED` | `wPortStatus.bit9` | Speed-encoding bit (interpret together with `PORT_HIGH_SPEED`) |
| `PORT_HIGH_SPEED` | `wPortStatus.bit10` | Speed-encoding bit (interpret together with `PORT_LOW_SPEED`) |
| `PORT_TEST` | `wPortStatus.bit11` | Test-mode related status marker |
| `PORT_INDICATOR` | `wPortStatus.bit12` | Indicator-related status marker |

#### `PORT_*` boundary markers

| Term | Field/Bit | Meaning |
|---|---|---|
| `PORT_STATUS_HIGH_BIT_BOUNDARY` | `wPortStatus.bit15` | 16-bit status field width marker |
| `PORT_STATUS_RESERVED_BIT5` | `wPortStatus.bit5` | Reserved slot (namespace marker) |
| `PORT_STATUS_RESERVED_BIT6` | `wPortStatus.bit6` | Reserved slot (namespace marker) |
| `PORT_STATUS_RESERVED_BIT7` | `wPortStatus.bit7` | Reserved slot (namespace marker) |
| `PORT_STATUS_RESERVED_BIT13` | `wPortStatus.bit13` | Reserved slot (namespace marker) |
| `PORT_STATUS_RESERVED_BIT14` | `wPortStatus.bit14` | Reserved slot (namespace marker) |

### `C_PORT_*` change vocabulary (`wPortChange`)

| Term | Field/Bit | Canonical meaning |
|---|---|---|
| `C_PORT_CONNECTION` | `wPortChange.bit0` | Event-record for connection-state change |
| `C_PORT_ENABLE` | `wPortChange.bit1` | Event-record for enable-state change |
| `C_PORT_SUSPEND` | `wPortChange.bit2` | Event-record for suspend-state change |
| `C_PORT_OVER_CURRENT` | `wPortChange.bit3` | Event-record for over-current change |
| `C_PORT_RESET` | `wPortChange.bit4` | Event-record for reset condition change |

#### `C_PORT_*` boundary markers

| Term | Field/Bit | Meaning |
|---|---|---|
| `PORT_CHANGE_HIGH_BIT_BOUNDARY` | `wPortChange.bit15` | 16-bit change field width marker |
| `PORT_CHANGE_RESERVED_BIT5` | `wPortChange.bit5` | Reserved slot (namespace marker) |
| `PORT_CHANGE_RESERVED_BIT6` | `wPortChange.bit6` | Reserved slot (namespace marker) |
| `PORT_CHANGE_RESERVED_BIT7` | `wPortChange.bit7` | Reserved slot (namespace marker) |
| `PORT_CHANGE_RESERVED_BIT8` | `wPortChange.bit8` | Reserved slot (namespace marker) |
| `PORT_CHANGE_RESERVED_BIT9` | `wPortChange.bit9` | Reserved slot (namespace marker) |
| `PORT_CHANGE_RESERVED_BIT10` | `wPortChange.bit10` | Reserved slot (namespace marker) |
| `PORT_CHANGE_RESERVED_BIT11` | `wPortChange.bit11` | Reserved slot (namespace marker) |
| `PORT_CHANGE_RESERVED_BIT12` | `wPortChange.bit12` | Reserved slot (namespace marker) |
| `PORT_CHANGE_RESERVED_BIT13` | `wPortChange.bit13` | Reserved slot (namespace marker) |
| `PORT_CHANGE_RESERVED_BIT14` | `wPortChange.bit14` | Reserved slot (namespace marker) |

## Consistency Rules

- `PORT_*` maps to status fields; `C_PORT_*` maps to change fields.
- `PORT_*` expresses a current-state dimension, while `C_PORT_*` expresses "an event was recorded".
- `C_PORT_*` values are often paired with `CLEAR_FEATURE` acknowledgment semantics before re-reading status changes.
- Selector linkage and value space are handled in `specs/feature_selectors.md`.

## Cross References

- `specs/port_status_bits.md`: main status/change bit summary (Chinese page)
- `specs/feature_selectors.md`: selector namespace summary for hub requests (Chinese page)
- `specs/en/port_status_bits.md`: main status/change bit summary (English page)
- `specs/en/feature_selectors.md`: selector namespace summary for hub requests (English page)
- `specs/hub_class_requests.md`: request-family context for `GET_STATUS` / `SET_FEATURE` / `CLEAR_FEATURE` (Chinese page)
- `specs/en/hub_class_requests.md`: request-family context for `GET_STATUS` / `SET_FEATURE` / `CLEAR_FEATURE` (English page)
- `tables/port_status_bit_matrix.yaml`: source matrix for status bits
- `tables/feature_selector_matrix.yaml`: source matrix for selectors
