---
title: Port Status Bits
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Port Status Bits

> Source scope: USB 2.0 Specification Rev 2.0, Section 11.24.2.7.
> This page is currently a reference summary, not a complete bit-by-bit verified rendering of the source spec.

## Status Field Model

- `GET_STATUS` can return hub-level `wHubStatus` / `wHubChange` or port-level `wPortStatus` / `wPortChange`.
- `Status` bits describe the current state; `Change` bits describe whether that state has changed since the last clear.
- For change bits, `CLEAR_FEATURE` is best read as “acknowledge and clear this recorded change event.”

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
| `wPortChange` | 15 | `PORT_CHANGE_HIGH_BIT_BOUNDARY` | reserved | Boundary placeholder for the 16-bit field |

## Change Bits and `CLEAR_FEATURE`

You can think of `wPortChange` / `wHubChange` as latched change-event flags:

- bit = `1`: the corresponding state changed at least once since the last clear
- bit = `0`: no such change has been recorded since the last clear
- `CLEAR_FEATURE(...)`: the host acknowledges the event and clears that recorded change bit

Example:

- `C_PORT_CONNECTION = 1` means the connection state changed since the last clear
- after reading `GET_STATUS`, the host may issue `CLEAR_FEATURE(C_PORT_CONNECTION)` to clear that event record
- if the connection changes again later, the bit can be set again

## Speed Bits Must Be Decoded Together

`PORT_LOW_SPEED` and `PORT_HIGH_SPEED` should not be interpreted independently. They form a combined speed encoding:

| `PORT_LOW_SPEED` | `PORT_HIGH_SPEED` | Interpretation |
|---|---|---|
| 0 | 0 | Full-speed |
| 1 | 0 | Low-speed |
| 0 | 1 | High-speed |
| 1 | 1 | Reserved / unexpected combination |

So wording like “`PORT_LOW_SPEED = 0` means full-speed” is incomplete by itself. It is only full-speed when `PORT_HIGH_SPEED` is also `0`.

## Usage Notes

- This page is not a complete bit encyclopedia; it is the subset currently promoted into the machine-readable layer.
- Semantics for `PORT_OVER_CURRENT`, `PORT_RESET`, `PORT_POWER`, speed-indication bits, and related details still need stronger PDF-level verification.
- Reserved bits should not be repurposed silently by firmware; if they are, that is an escalation condition.
