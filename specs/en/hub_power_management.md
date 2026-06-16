---
title: Hub Power Management
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Power Management

> Source scope: USB 2.0 Specification Rev 2.0, §11.11 / §11.4 / §11.7.  
> This page is a reviewed reference summary for hub power management. It is not a power sequencing or firmware behavior verification.

## Page Purpose

This page answers:

- How hub power switching modes (ganged vs. per-port) affect `SET_FEATURE(PORT_POWER)` behavior.
- The delay semantics represented by `bPwrOn2PwrGood`.
- The conceptual boundary for hub suspend and resume.
- An overview of the remote wakeup mechanism.

This page does not answer:

- Whether any specific hub hardware's power specifications have been verified.
- Whether hub firmware power switching timing is correct.
- The complete power management state machine.

## Power Switching Modes

`wHubCharacteristics bits[1:0]` defines the hub power switching mode (see `specs/en/hub_descriptor.md`):

| Mode | bits[1:0] | Description |
|---|---:|---|
| Ganged power switching | `0b00` | All ports powered on/off together; the effect of `SET_FEATURE(PORT_POWER)` on a single port depends on hub implementation |
| Individual (per-port) power switching | `0b01` | Each port can be powered independently; `SET_FEATURE(PORT_POWER)` and `CLEAR_FEATURE(PORT_POWER)` apply individually |
| No power switching | `0b10` / `0b11` | Power cannot be controlled (reserved; some hubs use this to indicate always-on) |

### Ganged vs. Per-port Implementation Differences

- **Ganged hub**: `SET_FEATURE(PORT_POWER)` may power on all ports simultaneously even when only a single port number is specified. The host should confirm the mode by reading `wHubCharacteristics` during enumeration.
- **Per-port hub**: `SET_FEATURE(PORT_POWER, portN)` powers on only port N; requests must be issued to each port individually.

## bPwrOn2PwrGood Delay

The hub descriptor field `bPwrOn2PwrGood` (offset 5) defines the wait time from port power-on to power-good:

- Unit: 2 ms (value × 2 ms = actual wait time)
- The host must wait until the power-good delay expires before proceeding with enumeration (e.g., issuing `SET_FEATURE(PORT_RESET)`).
- Example: bPwrOn2PwrGood = 50 → wait 100 ms.

This page does not verify that any hub's bPwrOn2PwrGood value is correct, nor does it claim whether the delay is conservative or exact.

## Over-current Protection

`wHubCharacteristics bits[4:3]` defines the over-current protection mode:

| Mode | bits[4:3] | Description |
|---|---:|---|
| Global over-current | `0b00` | Shared over-current protection for the entire hub; any port triggering it affects all ports |
| Per-port over-current | `0b01` | Each port has independent over-current detection; hub-level over-current is reflected in `HUB_OVER_CURRENT`, individual ports in `PORT_OVER_CURRENT` |
| No over-current reporting | `0b10` | Hub does not report over-current; host cannot rely on `PORT_OVER_CURRENT` or `HUB_OVER_CURRENT` |

When a hub detects over-current, it should set the appropriate bit in `wPortStatus.PORT_OVER_CURRENT` (port level) or `wHubStatus.HUB_OVER_CURRENT` (hub overall), and notify the host through the interrupt endpoint.

## Hub Suspend and Resume

### Suspend Triggers

A hub port can enter the Suspended state via:

- Host issuing `SET_FEATURE(PORT_SUSPEND)` → port enters Suspended state (`wPortStatus.PORT_SUSPEND = 1`)
- Downstream device idle for 3 ms → hub detects inactivity and the device auto-suspends

### Resume Triggers

Two paths from Suspended to Enabled:

1. **Host-initiated resume**: Host issues `CLEAR_FEATURE(PORT_SUSPEND)` → hub drives resume signaling (20 ms K-state) → port returns to Enabled.
2. **Device-initiated remote wakeup**: Downstream device generates resume signaling → hub propagates wakeup upstream → host detects and handles.

### Full Hub Suspend

USB 2.0 spec §11.7 describes how a hub itself may enter suspend via USB suspend signaling. All ports typically maintain their current state (usually Suspended) and recover when the hub resumes.

## Remote Wakeup

- A hub that supports remote wakeup can be woken from suspend by a downstream device when the host permits it.
- The hub notifies the host of a port resume via the `C_PORT_SUSPEND` change event.
- Whether remote wakeup is enabled is controlled by `SET_FEATURE(DEVICE_REMOTE_WAKEUP)` (a standard USB request, not a hub class request).

## Safe Interpretation Boundary

- This page describes the conceptual framework for power management; it does not provide specific timing guarantees or electrical specifications.
- `bPwrOn2PwrGood` and over-current behavior vary by hub hardware design; consult the hardware datasheet.
- If a consuming repo's hub power behavior does not match expectations, enter Standard Escalation Mode (E-07 or E-08).

## Governed Linkage

- `specs/en/hub_descriptor.md`: `wHubCharacteristics` bit fields (power switching and over-current modes)
- `specs/en/port_state_machine.md`: Suspended and Powered-off state transitions
- `specs/en/port_status_bits.md`: `PORT_SUSPEND`, `PORT_OVER_CURRENT`, `HUB_OVER_CURRENT` bits
- `specs/en/hub_class_requests.md`: `SET_FEATURE(PORT_POWER)`, `SET_FEATURE(PORT_SUSPEND)`, and related requests

## Non-claims

- This page does not claim that the power management implementation on any hub has been verified.
- This page does not provide power sequencing guarantees or electrical specifications.
- This page does not override confirmed project facts in consuming repos.

## Reference Navigation

- specs/en/usb2.md: USB 2.0 topic index (en).
- specs/hub_power_management.md: 中文對應主題（中文頁）
