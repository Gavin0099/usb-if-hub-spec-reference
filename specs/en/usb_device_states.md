---
title: USB Device States
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# USB Device States

> Source scope: USB 2.0 Specification Rev 2.0, §9.1.  
> This page describes USB device-level states (Chapter 9). These are distinct from hub port states (Chapter 11) described in `specs/en/port_state_machine.md`.

## Page Purpose

This page answers:

- What USB device states exist at the USB device framework level (§9.1).
- How a USB 2.0 hub transitions between these states during enumeration.

This page does not answer:

- Hub port states — those are in `specs/en/port_state_machine.md`.
- State transition timing or error recovery.

## USB Device States

USB 2.0 §9.1 defines the following device states:

| State | Description |
|---|---|
| **Attached** | Device is physically connected; VBUS may not be applied yet |
| **Powered** | VBUS is present; device is not yet reset |
| **Default** | Device has received a USB reset; responds at address 0; no address assigned |
| **Address** | Host has issued `SET_ADDRESS`; device has a unique bus address |
| **Configured** | Host has issued `SET_CONFIGURATION`; all interface endpoints are active |
| **Suspended** | No bus activity for more than 3ms; device enters low-power state |

## State Transitions

```
Attached ──VBUS applied──> Powered
Powered ──USB reset received──> Default
Default ──SET_ADDRESS(n)──> Address
Address ──SET_CONFIGURATION(1)──> Configured
Configured ──no bus activity >3ms──> Suspended
Suspended ──resume signal / SOF received──> Configured (or Address, if not configured)
Any ──USB reset received──> Default
```

## State Transition Table

| From State | Trigger | To State |
|---|---|---|
| Attached | VBUS applied (hub/root port powered) | Powered |
| Powered | USB reset received (SE0 ≥10ms) | Default |
| Default | `SET_ADDRESS(n)` | Address |
| Address | `SET_CONFIGURATION(bConfigurationValue)` | Configured |
| Configured | No bus activity >3ms | Suspended |
| Suspended | Resume signal received | Configured |
| Any (except Attached) | USB reset received | Default |
| Any (except Attached) | VBUS removed | Attached |

## Request Availability by State

Not all requests are valid in all device states:

| Request | Default | Address | Configured |
|---|---|---|---|
| `SET_ADDRESS` | ✓ | ✓ | — |
| `GET_DESCRIPTOR` | ✓ | ✓ | ✓ |
| `SET_CONFIGURATION` | — | ✓ | ✓ |
| `GET_CONFIGURATION` | — | ✓ | ✓ |
| Hub class requests | — | — | ✓ (only when configured) |

> Hub class requests (`GET_STATUS` port, `SET_FEATURE` port, TT requests) are only valid after `SET_CONFIGURATION`.

## Device States vs. Port States

| Aspect | USB Device States (§9.1) | Hub Port States (§11.5) |
|---|---|---|
| Subject | The hub device itself | A downstream port on the hub |
| States | Attached, Powered, Default, Address, Configured, Suspended | Powered-off, Disconnected, Disabled, Enabled, Suspended, Resetting, Port Error |
| Triggered by | Standard requests (`SET_ADDRESS`, `SET_CONFIGURATION`) | Hub class requests (`SET_FEATURE PORT_RESET`, `SET_FEATURE PORT_POWER`) |
| Status check | Standard `GET_STATUS` (device, 2 bytes) | Hub class `GET_STATUS` (port, 4 bytes) |

A hub is simultaneously a **USB device** (with its own §9.1 device states) and a **hub** (with downstream port states per §11.5).

## Governed Linkage

- `specs/en/port_state_machine.md`: hub port states (§11.5) — distinct from device states
- `specs/en/hub_enumeration.md`: enumeration sequence showing Default → Address → Configured transitions
- `specs/en/standard_device_requests.md`: `SET_ADDRESS`, `SET_CONFIGURATION` requests
- `specs/en/hub_power_management.md`: Suspended state and remote wakeup

## Non-claims

- This page does not claim device state transitions have been verified against a physical hub.
- This page does not establish complete recovery behavior after reset.
- This page does not override confirmed project facts in consuming repos.

## Reference Navigation

- specs/en/usb2.md: USB 2.0 topic index (en).
- specs/usb_device_states.md: 中文對應主題（中文頁）
