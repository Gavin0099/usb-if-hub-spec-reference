---
title: SS Port State Machine
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

# SS Port State Machine

> Scope: USB 3.2 Specification Rev 1.0, Section 10.14.2 (SuperSpeed Hub Port Management).
> This page is a consumer reference summary, not an LTSSM runtime state transition verification record.
> **Important**: This page does not claim any LTSSM runtime behavior.

## Purpose

This page answers:

- Which major port states exist for a USB 3.x SS hub port (based on `wPortStatus` bits).
- Which port status bits relate to port state.
- What types of port reset exist in SS hubs.

This page does not answer:

- LTSSM state machine transition timing and behavior.
- How xHCI drives port state transitions.
- Whether firmware correctly implements the port state machine.

## SS Hub Port Major States

These states are derived from `wPortStatus` bits (verified entries in `tables/ss_port_status_bit_matrix.yaml`):

| State | Relevant wPortStatus bits | Description |
|---|---|---|
| Disconnected | PORT_CONNECTION=0 | No device connected |
| Connected (not enabled) | PORT_CONNECTION=1, PORT_ENABLE=0 | Device connected but port not enabled |
| Enabled | PORT_CONNECTION=1, PORT_ENABLE=1 | Port enabled; link in U0 |
| U1/U2 (LPM) | PORT_LINK_STATE=U1/U2 | Link in low-power standby |
| U3 (Suspended) | PORT_LINK_STATE=U3, PORT_SUSPEND=1 | Port suspended |
| In Reset | PORT_RESET=1 | Port executing Warm Reset or Hot Reset |
| Over-current | PORT_OVER_CURRENT=1 | Port detected over-current condition |

> `PORT_LINK_STATE` verified scope: bit range [8:5] and 12-value encoding table identity only; LTSSM state transition behavior is outside the verified scope.

## SS Hub Port Reset Types

USB 3.x SS hubs support two types of port reset:

### Warm Reset (BH_PORT_RESET / 0x1C)

- Triggered by SET_FEATURE(BH_PORT_RESET).
- Executes the BH (Buffered Host) reset sequence to recover from link layer issues.
- Corresponds to the `C_BH_PORT_RESET` change bit (SS-only change bits in wPortChange).
- BH reset timing, LFPS signaling, and xHCI warm reset behavior are outside this page's verified scope.

### Hot Reset (PORT_RESET / 0x04)

- Triggered by SET_FEATURE(PORT_RESET); semantics differ from USB 2.0 bus reset.
- In the SS context, Hot Reset initiates a full SS link re-initialization.

## PORT_LINK_STATE Encoding (wPortStatus bits[8:5])

The `PORT_LINK_STATE` field provides 12 SS link state encoding values (verified):

| Value | Link state | Description |
|---|---|---|
| 0x0 | U0 | Active |
| 0x1 | U1 | U1 LPM |
| 0x2 | U2 | U2 LPM |
| 0x3 | U3 | Suspended |
| 0x4 | Disabled | Port disabled |
| 0x5 | RxDetect | Receiver detection phase |
| 0x6 | Inactive | Inactive |
| 0x7 | Polling | Link polling |
| 0x8 | Recovery | Link recovery |
| 0x9 | Hot Reset | Port hot reset |
| 0xA | Compliance Mode | Compliance test mode |
| 0xB | Loopback | Loopback test |

Source: USB 3.2 Specification §10.14.2 Table 10-9.

**Verified scope**: encoding table identity only (bit range [8:5] and 12 values). LTSSM runtime state transition behavior is outside the verified scope.

## U-State Transition Rules (Hub Port Management Layer)

The U0/U1/U2/U3 transitions below are hub-class-observable via `PORT_LINK_STATE`. This is a hub layer summary; the underlying LFPS signaling and link recovery sequence are LTSSM behaviors outside this page's scope.

| From | To | Direction | How |
|---|---|---|---|
| U0 | U1 | Device or host | Device-initiated LGOU1 (requires `PORT_U1_ENABLE=1`); or host directed |
| U1 | U0 | Either | LFPS handshake exit; link returns to U0 |
| U0 | U2 | Device-initiated | LGOU2 after U2 inactivity timeout (requires `PORT_U2_ENABLE=1`) |
| U2 | U0 | Either | LFPS handshake exit; link returns to U0 |
| U1 | U2 | Device-initiated | U2 inactivity timer expires while in U1 (deeper power saving) |
| U0 | U3 | Host | `SET_FEATURE(PORT_SUSPEND)` |
| U3 | U0 | Host or device | Host resume or device-initiated remote wakeup (LFPS + link resume sequence) |

**Transition constraints:**

| Scenario | Direct? | Notes |
|---|---|---|
| U3 → U1 or U2 | **No** | Must exit U3 to U0 first; U-state LPM may re-enter after that |
| U2 → U1 | **No** | U2 is a deeper power state than U1; exit to U0 required |
| U0 → U1 without PORT_U1_ENABLE | **No** | `SET_FEATURE(PORT_U1_ENABLE)` must be issued first |
| U0 → U2 without PORT_U2_ENABLE | **No** | `SET_FEATURE(PORT_U2_ENABLE)` must be issued first |

> **LTSSM boundary:** The states in the PORT_LINK_STATE encoding table below — Disabled (0x4), RxDetect (0x5), Polling (0x7), Recovery (0x8), Hot Reset (0x9), Compliance Mode (0xA), Loopback (0xB) — are LTSSM physical layer states. The transitions between these states (e.g., SS.Disabled → Rx.Detect → Polling → U0) are not hub class behaviors. For an orientation reference of LTSSM state groups and high-level transition paths, see [SS LTSSM State Reference](ss_ltssm.md). A complete normative LTSSM state machine is in USB 3.2 Spec §7 (Physical Layer).

## PORT_SPEED Encoding (wPortStatus bits[12:10])

| Value | Speed |
|---|---|
| 0x0 | High-speed |
| 0x1 | Full-speed |
| 0x2 | Low-speed |
| 0x3 | SuperSpeed |
| 0x4 | SuperSpeedPlus (Gen 2×1) |
| 0x5 | SuperSpeedPlus (Gen 1×2) |

**Verified scope**: encoding table identity only. Speed detection hardware or link training outcome is outside the verified scope.

## This Page Does Not Claim

- LTSSM runtime state transition timing or behavior.
- xHCI port management behavior.
- Firmware port state machine implementation correctness.
- Link training or speed negotiation outcome.
- USB-IF compliance or certification.

→ [SS Port Status Bits](ss_port_status_bits.md) | [SS Hub Class Requests](ss_hub_class_requests.md) | [Verification Status](../verification_status.md)
