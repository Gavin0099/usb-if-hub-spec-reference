---
title: USB Transfer Types
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# USB Transfer Types

> Source scope: USB 2.0 Specification Rev 2.0, §5.4–§5.7.  
> This page is a reviewed reference summary for the four USB 2.0 transfer types and their relevance to hub operation.

## Page Purpose

This page answers:

- What are the four USB 2.0 transfer types and their properties.
- Which transfer types a USB 2.0 hub uses.
- How each transfer type maps to a specific endpoint type.

## The Four USB 2.0 Transfer Types

| Transfer Type | `bmAttributes[1:0]` | Direction | Error Recovery | Timing Guarantee | Hub Use |
|---|---|---|---|---|---|
| **Control** | `00` | Both (setup+data+status) | Yes (retry) | None | Endpoint 0 — all requests |
| **Isochronous** | `01` | IN or OUT | No (no retry) | Guaranteed bandwidth | None |
| **Bulk** | `10` | IN or OUT | Yes (retry) | No (best-effort) | None |
| **Interrupt** | `11` | IN or OUT | Yes (retry) | Bounded latency | Status change endpoint |

## Control Transfer

**Used by hub**: Yes — endpoint 0 handles all standard and hub class requests.

Structure:
- **SETUP phase**: host sends 8-byte setup packet to endpoint 0.
- **DATA phase** (optional): host or device transfers data payload.
- **STATUS phase**: device (or host for IN) acknowledges completion.

Properties:
- Guaranteed delivery: errors trigger retries.
- Up to 64 bytes per packet for HS (8 bytes for LS, 8/16/32/64 for FS).
- Host scheduler allocates up to 10% of bus bandwidth for control transfers.

Hub role: Responds to standard requests (`GET_DESCRIPTOR`, `SET_ADDRESS`, `SET_CONFIGURATION`) and hub class requests (`GET_STATUS`, `SET_FEATURE`, `CLEAR_FEATURE`, TT requests) on endpoint 0.

## Interrupt Transfer

**Used by hub**: Yes — the single interrupt IN endpoint is the status change endpoint.

Properties:
- Periodic: host polls the endpoint at `bInterval` intervals.
- Bounded latency: transfers complete within a bounded time after they are available.
- Error recovery: errors trigger retries within the same period.
- FS: `bInterval` = 1–255 ms polling interval.
- HS: `bInterval` = 2^(`bInterval`–1) × 125µs (encoded exponent).

Hub role: The hub reports port status changes (connect, disconnect, overcurrent, reset complete, etc.) via a single status change bitmap on this endpoint. See `specs/en/hub_interrupt_endpoint.md`.

## Bulk Transfer

**Used by hub**: No. Hubs do not have bulk endpoints.

Properties:
- Large, reliable data transfers with no timing guarantee.
- Fills available bus bandwidth after other transfer types are served.
- FS max 64 bytes/packet; HS max 512 bytes/packet.

Not used by any hub endpoint.

## Isochronous Transfer

**Used by hub**: No. Hubs do not have isochronous endpoints.

Properties:
- Real-time, constant-rate transfers.
- No error recovery — missed data is not retransmitted.
- Reserved bandwidth allocation guarantees delivery timing.
- Used by audio, video, and other real-time class devices.

Not used by any hub endpoint.

## Transfer Type and Endpoint Descriptor

The `bmAttributes[1:0]` field in the endpoint descriptor declares the transfer type:

| `bmAttributes[1:0]` | Transfer Type |
|---|---|
| `00` | Control (endpoint 0 only; not encoded in endpoint descriptor) |
| `01` | Isochronous |
| `10` | Bulk |
| `11` | Interrupt |

Hub endpoint 0 is always Control. The single additional hub endpoint has `bmAttributes=0x03` (Interrupt).

## Split Transactions and Transfer Types

For FS/LS downstream devices connected to an HS hub, the hub's Transaction Translator (TT) converts HS split transactions into FS/LS transactions. This applies to control and bulk transactions from FS/LS devices; isochronous transactions are also split but have special handling. See `specs/en/transaction_translator.md`.

## Governed Linkage

- `specs/en/hub_interrupt_endpoint.md`: the hub status change interrupt endpoint descriptor fields
- `specs/en/hub_configuration.md`: endpoint descriptor in the hub configuration context
- `specs/en/transaction_translator.md`: how the TT bridges HS and FS/LS transfer timing

## Non-claims

- This page does not claim transfer type implementation has been verified against a physical hub.
- This page does not specify the full USB 2.0 scheduler or bandwidth allocation algorithm.
- This page does not override confirmed project facts in consuming repos.
