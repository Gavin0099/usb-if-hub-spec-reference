---
title: SS USB Transfer Types
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

# SS USB Transfer Types

> Scope: USB 3.2 Specification Rev 1.0, §8 (Transaction Layer) / Chapter 5.
> This page is a reviewed reference summary of the four USB 3.x SuperSpeed transfer types and their relevance to SS hub operation.

## Purpose

This page answers:

- The four USB 3.x transfer types and how they differ from USB 2.0.
- Which transfer types a SS hub uses.
- How NRDY/ERDY flow control affects SS transfer efficiency.

This page does not answer:

- Transaction layer runtime behavior or retransmission mechanisms — see [SS Transactions](ss_transactions.md).
- NRDY/ERDY runtime flow control behavior.
- xHCI SS transfer scheduling implementation.

## USB 3.x Four Transfer Types

USB 3.x retains the same four transfer types as USB 2.0, but the underlying mechanisms differ fundamentally:

| Transfer Type | `bmAttributes[1:0]` | SS Hub Use | Key USB 3.x Difference |
|---|---|---|---|
| **Control** | `00` | Endpoint 0 — all requests | Max packet 512 bytes (vs HS 64 bytes) |
| **Interrupt** | `11` | Status change endpoint | Periodic, bounded latency; uses NRDY/ERDY |
| **Bulk** | `10` | None (hub does not use) | Max packet 1024 bytes (vs HS 512 bytes) |
| **Isochronous** | `01` | None (hub does not use) | Uses ITP instead of SOF for timing |

## Control Transfer

**SS Hub uses**: Yes — Endpoint 0 handles all standard and hub class requests.

USB 3.x Control Transfer characteristics:
- EP0 max packet size: **512 bytes** (vs USB 2.0 HS: 64 bytes)
- `bMaxPacketSize0` encoded as `9` (exponent: 2^9 = 512 bytes)
- Same three-phase structure as USB 2.0: SETUP + DATA (optional) + STATUS

## Interrupt Transfer

**SS Hub uses**: Yes — the single interrupt IN endpoint is the status change endpoint.

USB 3.x Interrupt Transfer characteristics:
- Periodic polling: host polls at the interval specified by `bInterval` (in 125 μs microframe units).
- Bounded latency: transfer completes within a bounded time.
- Flow control: uses NRDY (endpoint not ready) and ERDY (endpoint proactively signals readiness).
- No split transaction: SS hub requires no TT and performs no speed-domain conversion.

SS hub status change endpoint characteristics:
- Direction: IN (hub → host)
- Packet size: 1 byte per 8 ports (same calculation as USB 2.0)
- `bInterval`: 2^(bInterval-1) × 125 μs; range 1–16 (same encoding as USB 2.0 High-Speed)

## Bulk Transfer

**SS Hub uses**: No. Hubs have no Bulk endpoints.

USB 3.x Bulk Transfer characteristics (for reference):
- Max packet: **1024 bytes** (vs USB 2.0 HS: 512 bytes)
- Error recovery: yes (ACK/NACK retry)
- Flow control: NRDY/ERDY (proactive notification replaces polling)

## Isochronous Transfer

**SS Hub uses**: No. Hubs have no Isochronous endpoints.

USB 3.x Isochronous Transfer characteristics (for reference):
- Uses **ITP (Isochronous Timestamp Packet)** for timing reference (replaces USB 2.0 SOF)
- Max packet: 1024 bytes
- No error retransmission (same as USB 2.0)

## NRDY / ERDY Flow Control

USB 3.x introduces NRDY/ERDY to replace the USB 2.0 polling-retry model:

| Packet | Direction | Description |
|---|---|---|
| **NRDY** | Device → Host | Endpoint not ready; host should pause polling this endpoint |
| **ERDY** | Device → Host | Endpoint proactively signals readiness (reduces unnecessary polling) |

ERDY allows devices to notify the host when data is ready, significantly reducing polling overhead. NRDY/ERDY runtime behavior details are outside this page's verified scope.

## No Split Transactions

**SS hubs require no split transactions (no Transaction Translator)**:
- USB 2.0 HS hubs need a TT to bridge the speed difference between the HS bus and downstream FS/LS devices.
- USB 3.x SS hubs connect downstream devices at SuperSpeed; the SuperSpeed protocol layer handles flow control natively without speed-domain translation.

See [SS Transactions](ss_transactions.md) for details.

## Differences from USB 2.0

| Aspect | USB 2.0 Hub | USB 3.x SS Hub |
|---|---|---|
| Control EP0 max packet | 64 bytes (HS) | **512 bytes** (2^9) |
| Bulk max packet | 512 bytes (HS) | **1024 bytes** |
| Interrupt flow control | Host polling, no extra signaling | NRDY/ERDY proactive notification |
| Isochronous timing | SOF (Start of Frame) | **ITP** (Isochronous Timestamp Packet) |
| Split transactions | Required for HS hub (TT) | **Not required** (SS hub has no TT) |

## Governed Linkage

- [SS Transactions](ss_transactions.md): SS transaction model and NRDY/ERDY description
- [SS Hub Interrupt Endpoint](ss_hub_interrupt_endpoint.md): hub status change interrupt endpoint descriptor
- [SS Packet Types](ss_packet_types.md): SS packet types (TP/DP/LMP/ITP)

## Non-claims

- This page does not claim transfer type implementations have been verified for a physical SS hub.
- This page does not claim NRDY/ERDY runtime flow control behavior has been verified.
- This page does not define the complete xHCI scheduler or bandwidth allocation algorithm.
- This page does not override confirmed project facts in consuming repos.

→ [SS Transactions](ss_transactions.md) | [SS Packet Types](ss_packet_types.md) | [Verification Status](../verification_status.md)
