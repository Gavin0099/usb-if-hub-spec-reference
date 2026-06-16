---
title: Port State Machine
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Port State Machine

> Source scope: USB 2.0 Specification Rev 2.0, §11.5.  
> This page is a reviewed reference summary for the USB 2.0 hub port state machine. It is not a complete state-transition behavior verification or firmware implementation truth.

## Page Purpose

This page answers:

- What are the 7 standard states of a USB 2.0 hub port.
- Which events or requests trigger state transitions.
- How `wPortStatus` bit values relate to port states.

This page does not answer:

- Complete timing guarantees for each state transition.
- Recovery procedures for firmware implementation errors.
- The full device enumeration flow after `PORT_RESET` completes.

## The 7 Standard Port States

A USB 2.0 hub port has the following 7 normative states (§11.5):

| State | Description |
|---|---|
| **Powered-off** | Port is not powered; `wPortStatus.PORT_POWER = 0` |
| **Disconnected** | Port is powered but no device is attached; `PORT_CONNECTION = 0` |
| **Disabled** | Device is attached but the port is not enabled; `PORT_ENABLE = 0` |
| **Enabled** | Port is enabled and the device can communicate; `PORT_ENABLE = 1` |
| **Suspended** | Port is in the suspend state; `PORT_SUSPEND = 1` |
| **Resetting** | Port is undergoing reset; `PORT_RESET = 1` |
| **Port Error** | Hub detected a port error; the port has been disabled |

## State Transition Overview

```
Powered-off ──SET_FEATURE(PORT_POWER)──> Disconnected
Disconnected ──device attach (hardware)──> Disabled
Disabled ──SET_FEATURE(PORT_RESET) + reset complete──> Enabled
Enabled ──SET_FEATURE(PORT_SUSPEND)──> Suspended
Suspended ──CLEAR_FEATURE(PORT_SUSPEND) or device wakeup──> Enabled
Enabled ──device detach or port error──> Disabled
Enabled ──CLEAR_FEATURE(PORT_ENABLE)──> Disabled
Disconnected ──CLEAR_FEATURE(PORT_POWER)──> Powered-off
Any powered state ──overcurrent or hardware error──> Disabled / Port Error
```

## State Transition Table

| From State | Trigger | To State |
|---|---|---|
| Powered-off | `SET_FEATURE(PORT_POWER)` | Disconnected |
| Disconnected | Device attach (hardware event) | Disabled |
| Disabled | `SET_FEATURE(PORT_RESET)` | Resetting |
| Resetting | Reset complete (hardware) | Enabled (if device responds correctly) |
| Enabled | `SET_FEATURE(PORT_SUSPEND)` | Suspended |
| Suspended | `CLEAR_FEATURE(PORT_SUSPEND)` or device wakeup | Enabled |
| Enabled | `CLEAR_FEATURE(PORT_ENABLE)` | Disabled |
| Enabled | Device detach (hardware event) | Disconnected |
| Any (powered) | Overcurrent detected | Disabled / Port Error |
| Any (powered) | `CLEAR_FEATURE(PORT_POWER)` | Powered-off |

## Transition Constraints — Which Paths Are Not Direct

Some transitions require passing through intermediate states. These constraints are defined in §11.5.

| Scenario | Direct? | Notes |
|---|---|---|
| Device attach → Enabled | **No** | Must pass through Disabled → Resetting → Enabled. The host must explicitly issue `SET_FEATURE(PORT_RESET)`. |
| Powered-off → Enabled | **No** | Must pass through Disconnected → Disabled → Resetting → Enabled. |
| Port Error → Enabled | **No** | Error causes the port to become Disabled. Host must re-issue `PORT_RESET` to re-enter Resetting → Enabled. |
| Suspended → Resetting | **Yes** | `SET_FEATURE(PORT_RESET)` is valid from Suspended. The hub exits Suspend and enters Resetting. |
| Any powered state → Powered-off | **Yes** | `CLEAR_FEATURE(PORT_POWER)` is valid from any powered state (ganged or per-port switching). |
| Enabled → Disconnected | **Yes** | Hardware device detach event; no host command needed. |

> **Key rule:** A newly attached device always enters **Disabled** first. The port cannot become Enabled without the host explicitly issuing `PORT_RESET` — there is no automatic path from Disabled to Enabled.

## `wPortStatus` Bits and Port State Relationship

| `wPortStatus` bit | Name | Set to `1` in these states |
|---:|---|---|
| 0 | `PORT_CONNECTION` | Disabled, Enabled, Suspended, Resetting |
| 1 | `PORT_ENABLE` | Enabled, Suspended |
| 2 | `PORT_SUSPEND` | Suspended |
| 3 | `PORT_OVER_CURRENT` | When overcurrent is detected |
| 4 | `PORT_RESET` | Resetting |
| 8 | `PORT_POWER` | Disconnected and above (powered) |

> Note: The table above is an overview of state correlations, not a bit-by-bit semantic truth table. Full bit definitions are in `specs/en/port_status_bits.md`.

## Interpretation Boundary

- The state machine presented here is a normative summary, not a complete state chart for firmware correctness verification.
- State transitions may be affected by hub implementation details (for example, the Resetting → Enabled timing).
- The path from `PORT_RESET` completion to Enabled depends on whether the device responds correctly to reset; if the device does not respond, the port should remain Disabled.

## Port Reset Timing

When the host issues `SET_FEATURE(PORT_RESET)`, the hub asserts USB reset on the port. Minimum timing constraints from §11.5.1.5:

| Phase | Duration | Notes |
|---|---|---|
| Reset assertion minimum | 10 ms | Hub must hold reset for at least this long |
| Port reset recovery (debounce) | 10 ms | Host waits before issuing the next request |
| Total minimum reset cycle | ~20 ms | Assertion + recovery |

- The hub (not the host) controls the reset assertion duration and sets `C_PORT_RESET=1` when complete.
- After `C_PORT_RESET=1`, the host reads `GET_STATUS(port)`, clears the bit with `CLEAR_FEATURE(C_PORT_RESET)`, then checks speed bits.
- If the attached device fails to respond during reset, the port remains in the Disabled state.

## Speed Detection After Port Reset

After port reset completes and `C_PORT_RESET` is cleared, the host reads `wPortStatus` to determine device speed:

| `PORT_LOW_SPEED` (bit 9) | `PORT_HIGH_SPEED` (bit 10) | Attached device speed |
|---|---|---|
| `0` | `0` | Full-speed (FS) |
| `1` | `0` | Low-speed (LS) |
| `0` | `1` | High-speed (HS) — only HS-capable hubs |
| `1` | `1` | Not a valid combination |

- Speed bits are set by the hub based on the chirp/handshake result during reset.
- An FS hub (`bDeviceProtocol=0x00`) will never set `PORT_HIGH_SPEED`.
- Speed detection is read-only from `GET_STATUS`; there is no command to select device speed.

## Governed Linkage

- `specs/en/port_status_bits.md`: detailed definitions of wPortStatus / wPortChange bits
- `specs/en/feature_selectors.md`: selector values for `PORT_RESET`, `PORT_ENABLE`, `PORT_SUSPEND`, `PORT_POWER`
- `specs/en/hub_class_requests.md`: `SET_FEATURE` and `CLEAR_FEATURE` request families
- `specs/en/escalation_table.md`: port state-related escalation triggers
- `specs/en/hub_enumeration.md`: full hub enumeration sequence including reset timing

## Non-claims

- This page does not claim that the port state machine implementation on any hub has been verified.
- This page does not claim complete specifications for state transition timing or device responses.
- This page does not override confirmed project facts in consuming repos.

## Reference Navigation

- specs/en/usb2.md: USB 2.0 topic index (en).
- specs/port_state_machine.md: 中文對應主題（中文頁）
