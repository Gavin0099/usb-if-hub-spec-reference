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

> Source scope: USB 2.0 Specification Rev 2.0, Section 11.24.2.7.  
> This page is a reference summary, not a full bit-by-bit verified reconstruction of the source spec.

## Page Purpose

This page is meant to answer:

- what hub-level and port-level fields `GET_STATUS` can return
- how `Status` bits differ from `Change` bits
- which hub/port status and change bits are currently exposed through the machine-readable layer
- which entries currently have live `verified` promotion, and how narrow that verified scope is

This page is not meant to answer:

- whether all port bits have completed PDF section-level verification
- whether timing, debounce, reset, and error-recovery semantics have completed correctness verification
- the full host behavior model for `SET_FEATURE` / `CLEAR_FEATURE`

## Status Field Model

- `GET_STATUS` can return hub-level `wHubStatus` / `wHubChange`
- it can also return port-level `wPortStatus` / `wPortChange`
- `Status` bits describe current state
- `Change` bits describe whether that state has changed since the last clear
- for change bits, `CLEAR_FEATURE(...)` is best read as "acknowledge and clear this recorded change event"

## Hub-Level Bits

| Field | Bit | Name | Meaning |
|---|---|---|---|
| `wHubStatus` | 0 | `HUB_LOCAL_POWER` | Hub local power status |
| `wHubStatus` | 1 | `HUB_OVER_CURRENT` | Hub over-current status |
| `wHubChange` | 0 | `C_HUB_LOCAL_POWER` | Records whether local power status has changed since the last clear |
| `wHubChange` | 1 | `C_HUB_OVER_CURRENT` | Records whether over-current status has changed since the last clear |

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
| `wPortStatus` | 15 | `PORT_STATUS_HIGH_BIT_BOUNDARY` | reserved | Boundary placeholder for the 16-bit field |
| `wPortChange` | 0 | `C_PORT_CONNECTION` | defined | Records whether connection status has changed since the last clear |
| `wPortChange` | 1 | `C_PORT_ENABLE` | defined | Records whether enable status has changed since the last clear |
| `wPortChange` | 2 | `C_PORT_SUSPEND` | defined | Records whether suspend status has changed since the last clear |
| `wPortChange` | 3 | `C_PORT_OVER_CURRENT` | defined | Records whether over-current status has changed since the last clear |
| `wPortChange` | 4 | `C_PORT_RESET` | defined | Records whether reset status has changed since the last clear |
| `wPortChange` | 15 | `PORT_CHANGE_HIGH_BIT_BOUNDARY` | reserved | Boundary placeholder for the 16-bit change field |

Not all tracked status/change entries are verified.
Only the 19 live entries listed below have completed entry-level promotion.

## Live Verified Entries

Nineteen live governed entries are currently promoted to `verified`:

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
| `C_PORT_SUSPEND` | `wPortChange` | bit 2 | bit name and bit position only |
| `C_PORT_OVER_CURRENT` | `wPortChange` | bit 3 | bit name and bit position only |
| `C_PORT_RESET` | `wPortChange` | bit 4 | bit name and bit position only |
| `HUB_LOCAL_POWER` | `wHubStatus` | bit 0 | bit name and bit position only |
| `HUB_OVER_CURRENT` | `wHubStatus` | bit 1 | bit name and bit position only |
| `C_HUB_LOCAL_POWER` | `wHubChange` | bit 0 | bit name and bit position only |
| `C_HUB_OVER_CURRENT` | `wHubChange` | bit 1 | bit name and bit position only |

That verified scope is intentionally narrow. It covers only:

- bit name
- bit position

It does **not** mean that this repo has verified:

- timing, debounce, reset, or state-transition behavior
- host-side `SET_FEATURE` / `CLEAR_FEATURE` semantics
- the full `PORT_ENABLE` enable/disable state machine
- the full page or the full `port_status_bit_matrix`

So this page frontmatter still remains:

- `claim_level: inferred`
- `status: review_required`
- `semantic_verification_claimed: false`

## Reviewed Entries Outside Verified Scope

No port status/change defined entries are currently `reviewed` but not `verified`.

These entries improve namespace coverage, but they do not verify timing, state machines, clear sequencing, error recovery, speed decoding, test-mode behavior, power-switch policy, or indicator behavior.

## Reviewed Boundary Placeholders

Two high-bit placeholders remain reviewed as boundary markers only:

| Entry | Field | Bit | Reviewed Scope |
|---|---|---|---|
| `PORT_STATUS_HIGH_BIT_BOUNDARY` | `wPortStatus` | bit 15 | 16-bit status-field high boundary only |
| `PORT_CHANGE_HIGH_BIT_BOUNDARY` | `wPortChange` | bit 15 | 16-bit change-field high boundary only |

These reviewed placeholders do not define additional status semantics.
They are intentionally boundary-only review markers and do not alter any verified scope or count.
They keep the machine-readable layer explicit that the status and change fields are 16-bit fields with boundary markers.

## Change Bits and `CLEAR_FEATURE`

You can think of `wPortChange` / `wHubChange` as latched change-event flags:

- bit = `1`: the corresponding state changed at least once since the last clear
- bit = `0`: no such change has been recorded since the last clear
- `CLEAR_FEATURE(...)`: the host acknowledges the event and clears that recorded change bit

Example:

- `C_PORT_CONNECTION = 1` means the connection state changed since the last clear
- after reading `GET_STATUS`, the host may issue `CLEAR_FEATURE(C_PORT_CONNECTION)` to clear that event record
- if the connection changes again later, the bit can be set again

## PORT_* and C_PORT_* behavior notes

These notes keep behavior boundaries intentionally narrow and do not extend to full timing or state-machine proof.

### `PORT_*` (status bits)

- `PORT_CONNECTION`
  - `1` generally indicates the port currently has a live logical connection; `0` indicates no active connection.
  - It is useful as a current-state visibility bit; "just connected" transitions are typically inferred with `C_PORT_CONNECTION`.
- `PORT_ENABLE`
  - Indicates the port is logically enabled from the controller perspective.
  - This page only tracks the meaning of the bit; the enabling/disabling state machine is not claimed complete.
- `PORT_SUSPEND`
  - `1` generally means suspend-like port behavior is active (power-management pause path) and `0` means not suspended.
  - Complete suspend/resume semantics and transitions are intentionally outside this page.
- `PORT_OVER_CURRENT`
  - `1` indicates the port reports an over-current condition in status context.
  - Over-current recovery thresholds and retry timing remain in firmware/project scope.
- `PORT_RESET`
  - Exposes whether reset state for the port is active in the returned status.
- `PORT_POWER`
  - Indicates whether the port power supply is currently enabled.
  - In practice there can be transient enable timing; implementations should align with firmware telemetry where needed.
- `PORT_LOW_SPEED`, `PORT_HIGH_SPEED`
  - Speed bits are a pair and must be interpreted together; see next section.
- `PORT_TEST`
  - Indicates test-mode related status, but does not by itself prove test progression success.
- `PORT_INDICATOR`
  - Indicates the port indicator state; this page stores a role-level summary only.

### `C_PORT_*` (change bits)

- `C_PORT_CONNECTION`
  - `1` indicates a connection-status change event has occurred since the last clear.
- `C_PORT_ENABLE`
  - `1` indicates enable-related change was observed since the last clear.
- `C_PORT_SUSPEND`
  - `1` indicates suspend-related status changed since the last clear (enter/exit suspend).
- `C_PORT_OVER_CURRENT`
  - `1` indicates over-current-related state changed since the last clear.
- `C_PORT_RESET`
  - `1` indicates a reset-related change event was observed since the last clear.

General note:

- `C_PORT_*` values represent "an event was recorded", not the full current state by themselves.
- In normal interpretation, pair `GET_STATUS` with the status bits and then clear recorded events with `CLEAR_FEATURE`.

## Speed Bits Must Be Decoded Together

`PORT_LOW_SPEED` and `PORT_HIGH_SPEED` should not be interpreted independently. They form a combined speed encoding:

| `PORT_LOW_SPEED` | `PORT_HIGH_SPEED` | Interpretation |
|---|---|---|
| 0 | 0 | Full-speed |
| 1 | 0 | Low-speed |
| 0 | 1 | High-speed |
| 1 | 1 | Reserved / unexpected combination |

So wording like "`PORT_LOW_SPEED = 0` means full-speed" is incomplete by itself.  
It is only full-speed when `PORT_HIGH_SPEED` is also `0`.

## Section Anchor and Verified-Scope Boundary

This repo currently carries two different evidence-related signals:

- `section_refs` as evidence attachment metadata
- live `verified` promotions, currently for `PORT_CONNECTION`, `PORT_ENABLE`, `PORT_SUSPEND`, `PORT_OVER_CURRENT`, `PORT_RESET`, `PORT_POWER`, `PORT_LOW_SPEED`, `PORT_HIGH_SPEED`, `PORT_TEST`, `PORT_INDICATOR`, `C_PORT_CONNECTION`, `C_PORT_ENABLE`, `HUB_LOCAL_POWER`, `HUB_OVER_CURRENT`, `C_HUB_LOCAL_POWER`, and `C_HUB_OVER_CURRENT`

They should not be conflated.

Current state:

- selected pilot entries carry `section_refs`
- `wPortStatus.bit0.PORT_CONNECTION`, `wPortStatus.bit1.PORT_ENABLE`, `wPortStatus.bit2.PORT_SUSPEND`, `wPortStatus.bit3.PORT_OVER_CURRENT`, `wPortStatus.bit4.PORT_RESET`, `wPortStatus.bit8.PORT_POWER`, `wPortStatus.bit9.PORT_LOW_SPEED`, `wPortStatus.bit10.PORT_HIGH_SPEED`, `wPortStatus.bit11.PORT_TEST`, `wPortStatus.bit12.PORT_INDICATOR`, `wPortChange.bit0.C_PORT_CONNECTION`, `wPortChange.bit1.C_PORT_ENABLE`, `wPortChange.bit2.C_PORT_SUSPEND`, `wPortChange.bit3.C_PORT_OVER_CURRENT`, `wPortChange.bit4.C_PORT_RESET`, `wHubStatus.bit0.HUB_LOCAL_POWER`, `wHubStatus.bit1.HUB_OVER_CURRENT`, `wHubChange.bit0.C_HUB_LOCAL_POWER`, and `wHubChange.bit1.C_HUB_OVER_CURRENT` are live `verified`
- all verified scopes remain `bit_name_and_position_only`
- the remaining defined port status/change entries are reviewed namespace entries only (currently none)
- this still does not mean USB 2.0 PDF semantic verification is complete

If a future wiki claim block needs `section_refs`, it should keep the Phase 7A metadata structure, for example:

```yaml
section_refs:
  - spec: usb20
    section: "11.24.2.7.1"
    anchor_type: section
    evidence_status: review_required
    applies_to: "PORT_CONNECTION summary block"
```

That metadata block is evidence attachment only. It does not automatically promote the page or claim block to `verified`.

## Governed Linkage

- `tables/port_status_bit_matrix.yaml`: primary machine-readable source for hub/port status bit namespaces
- `specs/hub_class_requests.md`: request-family summary for `GET_STATUS`, `SET_FEATURE`, and `CLEAR_FEATURE`
- `specs/feature_selectors.md`: feature-selector boundary for `C_PORT_*` selectors
- `specs/escalation_table.md`: escalation triggers such as E-02, E-03, and E-09

## Non-claims

- This page does not claim that all port status bits have completed PDF-level verification.
- This page does not claim that speed bits, reset bits, power bits, or adjacent semantics are fully verified.
- This page does not expand 19 verified entries into a claim that the whole page is verified.
- This page does not treat high-bit boundary placeholders as defined status or change semantics.
- This page does not elevate the status-bit summary into firmware implementation authority.
