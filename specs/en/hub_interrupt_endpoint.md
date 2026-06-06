---
title: Hub Interrupt Endpoint
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Interrupt Endpoint (Status Change Endpoint)

> Source scope: USB 2.0 Specification Rev 2.0, §11.13 / §11.15.1.  
> This page is a reviewed reference summary for the hub status change endpoint. It is not a firmware or driver behavior verification.

## Page Purpose

This page answers:

- Why a hub requires an interrupt IN endpoint.
- What each descriptor field for the status change endpoint means (bEndpointAddress, bmAttributes, wMaxPacketSize, bInterval).
- How the minimum wMaxPacketSize is calculated from the port count.
- How bInterval encoding differs between FS and HS hubs.

This page does not answer:

- Host driver interrupt polling implementation details.
- How hub firmware manages status change bit latching.
- Whether the interrupt endpoint on any specific device has been verified.

## Status Change Endpoint Overview

A hub must implement one **interrupt IN endpoint**, called the status change endpoint (§11.13).  
Whenever the hub itself or any downstream port changes status, the hub notifies the host through this endpoint.

The host uses interrupt polling to retrieve status change notifications. The payload format is:

- bit 0: whether the hub itself has a status change (corresponding to `wHubStatus.C_*` bits)
- bit N (N ≥ 1): whether port N has a status change (corresponding to `wPortChange` bits)

## Endpoint Descriptor Fields

Summary derived from `tables/hub_interrupt_endpoint_matrix.yaml`:

| Field | Spec Requirement | Notes |
|---|---|---|
| `bEndpointAddress` | bit 7=1 (IN), bits\[3:0\] implementation-defined | endpoint number commonly 1 |
| `bmAttributes` | bits\[1:0\]=`0b11` (Interrupt transfer) | FS/LS hub bits\[7:2\]=0 |
| `wMaxPacketSize` | ≥ `ceil((bNbrPorts + 1) / 8)` bytes | see calculation below |
| `bInterval` | FS/LS: 1–255 ms; HS: 2^(n-1) × 125 µs (n=1–16) | see speed-dependent encoding below |

### `wMaxPacketSize` Calculation

The status change bitmap requires:
- 1 bit for hub status change (bit 0)
- 1 bit per downstream port (bit N for port N)

Therefore `wMaxPacketSize` must be at least `ceil((bNbrPorts + 1) / 8)` bytes.

| `bNbrPorts` | Minimum `wMaxPacketSize` |
|---:|---:|
| 1–7 | 1 byte |
| 8–15 | 2 bytes |
| 16–23 | 3 bytes |
| 24–31 | 4 bytes |

In practice, most hubs have ≤ 7 ports, so 1 byte is by far the most common.

### `bInterval` Speed Differences

| Hub Speed | `bInterval` Encoding | Notes |
|---|---|---|
| Full-speed (FS) | Direct millisecond value, range 1–255 | Depends on host implementation |
| Low-speed (LS) | Same as FS | Same as FS |
| High-speed (HS) | 2^(bInterval-1) × 125 µs, bInterval range 1–16 | Determined by bInterval |

Example: HS hub with bInterval=6 yields a polling interval of 2^(6-1) × 125 µs = 4000 µs = 4 ms.

## Status Change Bitmap Format

The interrupt IN data the host receives is a bitmap:

```
bit 0   : hub's own status change (wHubStatus C_HUB_LOCAL_POWER or C_HUB_OVER_CURRENT)
bit 1   : port 1 status change (any bit set in wPortChange)
bit 2   : port 2 status change
...
bit N   : port N status change
```

When the host receives a non-zero bitmap, it issues a `GET_STATUS` request (§11.24.2.6) to the corresponding port or hub to obtain detailed status.

## Governed Linkage

- `tables/hub_interrupt_endpoint_matrix.yaml`: governed reviewed surface for endpoint descriptor fields
- `specs/en/port_status_bits.md`: wPortChange and wHubChange bit definitions
- `specs/en/hub_class_requests.md`: `GET_STATUS` hub/port request family

## Non-claims

- This page does not claim that the interrupt endpoint implementation on any hub has been verified.
- This page does not describe host driver interrupt polling behavior or latency guarantees.
- This page does not override confirmed project facts in consuming repos.
