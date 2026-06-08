---
title: SS USB Device States
claim_level: inferred
spec_family: usb3
status: review_required
last_reviewed: "2026-06-08"
usb_versions:
  - usb_3_2
source_refs:
  - usb32_spec
semantic_verification_claimed: false
---

# SS USB Device States

> Scope: USB 3.2 Specification Rev 1.0, §9.1 / Chapter 10.
> This page describes the USB 3.x SuperSpeed hub device-level states (§9.1) and the link power states (U0–U3) added in USB 3.x. For hub port states, see [SS Port State Machine](ss_port_state_machine.md).

## Purpose

This page answers:

- How USB 3.x SS hub device states compare to USB 2.0.
- How U0–U3 link power states overlay the Configured device state.
- When a SS hub can accept hub class requests.

This page does not answer:

- Hub port states (Disconnected, Enabled, Resetting, etc.) — see [SS Port State Machine](ss_port_state_machine.md).
- U1/U2 timeout selector rules — see [SS Link Power Management](ss_lpm.md).
- LTSSM training details or xHCI device state management.

## USB Device States (§9.1, Shared by USB 2.0 and USB 3.x)

USB 3.x retains the same device state framework as USB 2.0:

| State | Description |
|---|---|
| **Attached** | Device physically connected; VBUS may not yet be applied |
| **Powered** | VBUS present; device not yet reset |
| **Default** | Device has received a USB reset; responds at address 0; no address assigned yet |
| **Address** | Host issued `SET_ADDRESS`; device has a unique bus address |
| **Configured** | Host issued `SET_CONFIGURATION`; device fully functional |
| **Suspended** | No SS bus activity for > 2 ms; device enters low-power state |

## State Transitions

```
Attached ──VBUS applied──> Powered
Powered ──USB reset received──> Default
Default ──SET_ADDRESS(n)──> Address
Address ──SET_CONFIGURATION(1)──> Configured
Configured ──no SS activity >2ms──> Suspended
Suspended ──resume / LFPS received──> Configured
Any state ──USB reset received──> Default
```

## USB 3.x Addition: U0–U3 Link Power States

USB 3.x overlays **link power states (U0–U3)** on the Configured state:

| State | Description | USB 2.0 Analog |
|---|---|---|
| **U0** | Link fully active | Similar to Active (after Resume) |
| **U1** | Brief low-power link state (exit latency in hundreds of μs) | No direct equivalent |
| **U2** | Deeper low-power link state (exit latency in a few ms) | No direct equivalent |
| **U3** | Link Suspend (equivalent to USB 2.0 device Suspend) | Equivalent to Suspended |

U1 and U2 are USB 3.x-specific link-layer power saving mechanisms. U3 corresponds to device-level Suspended. See [SS Link Power Management](ss_lpm.md) for details.

## Requests Valid by State

| Request | Default | Address | Configured |
|---|---|---|---|
| `SET_ADDRESS` | ✓ | ✓ | — |
| `GET_DESCRIPTOR` | ✓ | ✓ | ✓ |
| `SET_CONFIGURATION` | — | ✓ | ✓ |
| `GET_CONFIGURATION` | — | ✓ | ✓ |
| `SET_HUB_DEPTH` | — | — | ✓ (mandatory before enabling ports) |
| Hub class requests (GET_STATUS port, SET_FEATURE port) | — | — | ✓ |

**`SET_HUB_DEPTH` is mandatory for USB 3.x SS hubs** and must be issued after `SET_CONFIGURATION` before any downstream port is enabled. See [SS Hub Class Requests](ss_hub_class_requests.md).

## Device States vs. Port States vs. Link States

| Layer | Concept | Key States |
|---|---|---|
| USB device layer (§9.1) | The hub device itself | Default → Address → Configured → Suspended |
| Hub port states (§10.14.2) | Downstream ports on the hub | Disconnected → Enabled → Resetting… |
| Link power states (§10.14.2) | SS link-layer power saving | U0 (active) → U1 → U2 → U3 (suspend) |

These three layers are independent but related. A SS hub simultaneously manages its own device state, each port's port state, and the link power state for each connected downstream device.

## Differences from USB 2.0

| Aspect | USB 2.0 Hub | USB 3.x SS Hub |
|---|---|---|
| Device state framework | Same (§9.1) | Same (§9.1) |
| Suspend threshold | No activity > 3 ms | No SS activity > 2 ms |
| Link power states | No U1/U2 concept | U0/U1/U2/U3 (SET_FEATURE PORT_U1/U2_TIMEOUT) |
| Reset trigger | SE0 ≥ 10 ms (Warm Reset) | SS reset (Warm Reset or Hot Reset) |
| SET_HUB_DEPTH | Not applicable | **Mandatory** (unique mandatory enumeration step for SS hubs) |

## Governed Linkage

- [SS Port State Machine](ss_port_state_machine.md): Hub port state machine (PORT_LINK_STATE 12 values)
- [SS Link Power Management](ss_lpm.md): U0–U3 link power states and timeout selectors
- [SS Hub Enumeration](ss_hub_enumeration.md): SS hub enumeration sequence (including SET_HUB_DEPTH)
- [SS Hub Class Requests](ss_hub_class_requests.md): SS hub class requests (SET_HUB_DEPTH mandatory)

## Non-claims

- This page does not claim device state transitions have been verified for a physical SS hub.
- This page does not claim U1/U2/U3 link power state behavior or exit latency has been verified.
- This page does not claim LTSSM training behavior or xHCI device state management has been verified.
- This page does not override confirmed project facts in consuming repos.

→ [SS Port State Machine](ss_port_state_machine.md) | [SS LPM](ss_lpm.md) | [Verification Status](../verification_status.md)
