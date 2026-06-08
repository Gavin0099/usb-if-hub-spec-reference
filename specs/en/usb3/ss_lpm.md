---
title: SS Link Power Management (U1/U2/U3)
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

# SS Link Power Management (U1/U2/U3)

> Scope: USB 3.2 Specification Rev 1.0, Section 7.2 (Link Power Management) and Section 10.14.
> This page is a consumer reference summary, not an LPM runtime behavior verification record.
> **Important**: This page does not claim any LTSSM state transition behavior.

## Purpose

This page answers:

- A summary of the four USB 3.x link power states (U0–U3).
- Prerequisites overview for U1/U2 entry.
- Which feature selectors hub ports use to control U1/U2.

This page does not answer:

- LTSSM state transition behavior for U1/U2/U3 entry and exit.
- xHCI U1/U2 policy enforcement implementation.
- Detailed U1/U2 timeout semantics and wValue encoding.

## USB 3.x Link Power States (U0–U3)

| State | Description | Typical wake latency |
|---|---|---|
| U0 | Active (normal operation) | N/A |
| U1 | Standby (short wake latency) | < 10 μs (reference; hardware-dependent) |
| U2 | Standby (longer wake latency) | < 2 ms (reference; hardware-dependent) |
| U3 | Suspend (deepest power saving) | Full Suspend/Resume sequence |

> Wake latency values are spec reference figures; actual hardware behavior is outside this page's verified scope.

## U1/U2 Entry Overview

In USB 3.x, U1/U2 entry can be initiated by either the device or the host (subject to policy). Hub ports must be enabled via feature selectors:

- **SET_FEATURE(PORT_U1_ENABLE)**: Allows the hub port to accept device-initiated U1 entry requests.
- **SET_FEATURE(PORT_U2_ENABLE)**: Allows the hub port to accept device-initiated U2 entry requests.

The U1/U2 entry and exit sequence within the LTSSM is outside this page's verified scope.

## U1/U2 Timeout Selectors

- **PORT_U1_TIMEOUT (0x17)**: Sets the U1 inactivity timeout for an SS hub port.
- **PORT_U2_TIMEOUT (0x18)**: Sets the U2 inactivity timeout for an SS hub port.

The timeout encoding semantics in the wValue high byte are outside this page's verified scope; actual timeout behavior is firmware-defined.

## U3 (Suspend)

- U3 is the deepest power-saving state; the USB 3.x equivalent of USB 2.0 Suspend.
- The host triggers U3 via SET_FEATURE(PORT_SUSPEND).
- The `PORT_SUSPEND` bit (wPortStatus bit 2) reflects U3 state (verified).
- The full U3 entry and exit sequence (including resume signaling) is outside this page's verified scope.

## LPM-Related Bits in wPortStatus

The following bits have been promoted to verified in `ss_port_status_bit_matrix` (bit identity only):

| Bit | Name | Description |
|---|---|---|
| wPortStatus bit 2 | PORT_SUSPEND | Port is in U3 suspend state |
| wPortStatus bits[8:5] | PORT_LINK_STATE | Current link state (12 values) |

## This Page Does Not Claim

- LTSSM state transition behavior for U1/U2/U3 entry or exit.
- xHCI U1/U2 policy enforcement or power management implementation.
- U1/U2 timeout encoding semantics or inactivity timeout behavior.
- Resume signaling or wakeup behavior.
- Actual wake latency guarantees.

→ [SS Feature Selectors](ss_feature_selectors.md) | [SS Port State Machine](ss_port_state_machine.md) | [Verification Status](../verification_status.md)
