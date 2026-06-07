---
title: SS Port Status Bits
claim_level: inferred
spec_family: usb3
status: review_required
last_reviewed: "2026-06-07"
usb_versions:
  - usb_3_2
source_refs:
  - usb32_spec
semantic_verification_claimed: false
---

# SS Port Status Bits

> Source scope: USB 3.2 Specification Rev 1.0, Section 10.14.2.6 (GET_STATUS for SS hub port).
> This page is a consumer-facing reference summary, not a bit-by-bit PDF verification record.

## Page Purpose

This page answers:

- The complete `wPortStatus` / `wPortChange` bit definitions for a USB 3.x SuperSpeed hub port.
- The `PORT_LINK_STATE` (bits[8:5]) link state encoding.
- The `PORT_SPEED` (bits[12:10]) speed encoding.
- Key differences from USB 2.0 port status bits.

This page does not answer:

- The complete LTSSM state machine transitions.
- Electrical or timing characteristics of each link state.

## GET_STATUS Response Format

GET_STATUS (wValue=0x0000, wIndex=port number) returns 4 bytes:

```
Bytes 0–1: wPortStatus  (16-bit)
Bytes 2–3: wPortChange  (16-bit)
```

## wPortStatus Bit Definitions

| Bit | Field | Description |
|---|---|---|
| bit[0] | PORT_CONNECTION | Device currently connected |
| bit[1] | PORT_ENABLE | Port enabled; always 1 when SS device is connected |
| bit[2] | PORT_OVER_CURRENT | Port over-current condition |
| bit[3] | PORT_RESET | Port is undergoing reset signaling |
| bits[8:5] | PORT_LINK_STATE | Current link state (see Link State table) |
| bit[9] | PORT_POWER | Port power state (0=off, 1=on) |
| bits[12:10] | PORT_SPEED | Current connection speed (see Speed table) |
| bit[13] | PORT_U1_ENABLE | U1 entry enabled |
| bit[14] | PORT_U2_ENABLE | U2 entry enabled |
| bit[15] | Reserved | Must be zero |

### PORT_LINK_STATE Encoding (bits[8:5])

| Value | Link State | Description |
|---|---|---|
| 0 | U0 | Active — normal operating state |
| 1 | U1 | Low-power standby; host-initiated; exit latency < 10μs |
| 2 | U2 | Lower-power; host- or device-initiated; exit latency < 2ms |
| 3 | U3 | Suspended (analogous to USB 2.0 SUSPEND) |
| 4 | SS.Disabled | Port disabled |
| 5 | Rx.Detect | Detecting receiver presence (connect detection phase) |
| 6 | SS.Inactive | Inactive after link error |
| 7 | Polling | Link training in progress |
| 8 | Recovery | Recovering from low-power or error state |
| 9 | Hot Reset | Warm reset (BH Port Reset) in progress |
| 10 | Compliance Mode | Electrical compliance test mode |
| 11 | Loopback | Loopback test mode |
| 12–15 | Reserved | — |

### PORT_SPEED Encoding (bits[12:10])

| Value | Speed | Description |
|---|---|---|
| 0 | — | Undefined |
| 1 | Full-speed | 12 Mbps |
| 2 | Low-speed | 1.5 Mbps |
| 3 | High-speed | 480 Mbps |
| 4 | SuperSpeed | 5 Gbps (USB 3.2 Gen 1) |
| 5 | SuperSpeed+ | 10 Gbps (USB 3.2 Gen 2) |
| 6–7 | Reserved | — |

## wPortChange Bit Definitions

| Bit | Field | Description |
|---|---|---|
| bit[0] | C_PORT_CONNECTION | Connection status changed |
| bit[1] | Reserved | Always 0 (PORT_ENABLE does not deassert in SS) |
| bit[2] | C_PORT_OVER_CURRENT | Over-current condition changed |
| bit[3] | C_PORT_RESET | Standard reset complete |
| bit[4] | C_BH_PORT_RESET | Warm Reset (BH Port Reset) complete |
| bit[5] | C_PORT_LINK_STATE | Link state changed |
| bit[6] | C_PORT_CONFIG_ERROR | Configuration error (SS device configuration failed) |
| bits[15:7] | Reserved | Must be zero |

## Differences from USB 2.0 Port Status Bits

| Difference | USB 2.0 | USB 3.x / SuperSpeed |
|---|---|---|
| PORT_SUSPEND (bit[2]) | Present | **Not present** (replaced by U1/U2/U3 link states) |
| PORT_LOW_SPEED / PORT_HIGH_SPEED | Present (bit[9]/bit[10]) | **Not present** (merged into PORT_SPEED 3-bit field) |
| PORT_TEST / PORT_INDICATOR | Present (bit[11]/bit[12]) | **Not present** (SS test modes use different mechanism) |
| PORT_LINK_STATE | Not present | **New**: bits[8:5], 4-bit link state field |
| PORT_SPEED | Not present | **New**: bits[12:10], 3-bit speed field |
| PORT_U1_ENABLE / PORT_U2_ENABLE | Not present | **New**: bit[13] / bit[14] |
| C_BH_PORT_RESET | Not present | **New**: bit[4], warm reset completion |
| C_PORT_LINK_STATE | Not present | **New**: bit[5] |
| C_PORT_CONFIG_ERROR | Not present | **New**: bit[6] |

## Non-claims

- Does not claim that the bit definitions on this page have been verified bit-by-bit against the USB 3.2 PDF.
- Does not claim the complete LTSSM state transition behavior (U1→U0 exit sequence, etc.).
- Does not claim electrical or timing compliance for any link state.
