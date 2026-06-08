---
title: SS Hub Interrupt Endpoint
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

# SS Hub Interrupt Endpoint

> Scope: USB 3.2 Specification Rev 1.0, Section 10.15.1 (SuperSpeed Hub Interrupt Endpoint Descriptor).
> This page is a consumer reference summary, not a per-field PDF verification record.
> Governed matrix: `tables/ss_hub_interrupt_endpoint_matrix.yaml` (4 fields, all verified).

## Purpose

This page answers:

- Which fields make up the USB 3.x SS hub status-change (interrupt) endpoint descriptor.
- How `bInterval` is encoded for a SuperSpeed hub endpoint (and how this differs from USB 2.0).
- How the minimum `wMaxPacketSize` is calculated.

This page does not answer:

- How the host actually schedules interrupt polling.
- How firmware selects the endpoint number or bInterval value.
- Actual polling latency guarantees.

## SS Hub Interrupt Endpoint Field Summary

| Field | Constraint / Encoding | Claim level |
|---|---|---|
| `bEndpointAddress` | bit7=1 (IN direction); bits[3:0]=endpoint number (firmware-defined) | **verified** |
| `bmAttributes` | bits[1:0]=0b11 (Interrupt transfer type) | **verified** |
| `wMaxPacketSize` | ceil((bNbrPorts + 1) / 8) bytes minimum | **verified** |
| `bInterval` | 2^(bInterval-1) × 125 μs; bInterval range 1–16 | **verified** |

Source: USB 3.2 Specification §10.15.1.

## bEndpointAddress

- **bit 7 must be 1** (IN direction; hub reports status changes to host).
- **bits[3:0]**: endpoint number, defined by hub firmware; commonly 1.
- The IN direction constraint is a spec requirement; the actual endpoint number assignment is firmware behavior, outside this page's verified scope.

## bmAttributes

- **bits[1:0] = 0b11**: Interrupt transfer type.
- The SS hub status-change endpoint must be an Interrupt endpoint.
- USB 3.x interrupt endpoint burst or stream behavior is outside this page's verified scope.

## wMaxPacketSize

Minimum size calculation:

```
wMaxPacketSize ≥ ceil((bNbrPorts + 1) / 8) bytes
```

The +1 accounts for the hub's own status bit (hub device status change bit).

| Number of downstream ports | Minimum wMaxPacketSize |
|---|---|
| 1–7 ports | 1 byte |
| 8–15 ports | 2 bytes |
| 16–23 ports | 3 bytes |

## bInterval (SuperSpeed endpoint microframe encoding)

| Mode | Encoding | Range |
|---|---|---|
| SuperSpeed | 2^(bInterval-1) × 125 μs | bInterval 1–16 |

> **USB 3.x SuperSpeed uses the same bInterval encoding as USB 2.0 High-Speed** (microframe-based, 2^(n-1) × 125 μs).
> The USB 2.0 Full-Speed/Low-Speed direct-ms encoding (1–255 ms) **does not apply** to SuperSpeed hubs.

Common bInterval values:

| bInterval | Polling period |
|---|---|
| 1 | 125 μs |
| 4 | 1 ms |
| 8 | 16 ms |
| 12 | 256 ms |

## Verified Gate

The governed matrix (`tables/ss_hub_interrupt_endpoint_matrix.yaml`) verified gate: **PARTIAL (allowlist, all 4 entries promoted)**.

Verified scope: field identity and constraint encoding only.

Evidence packets: `evidence/entry_verification_packets/usb3/ss_iep_*.yaml` (4 packets).

## This Page Does Not Claim

- Actual host interrupt polling scheduling or latency guarantees.
- Firmware endpoint address assignment or bInterval selection correctness.
- USB 3.x interrupt endpoint burst or stream behavior.
- Runtime polling behavior verification.

→ [Verification Status](../verification_status.md)
