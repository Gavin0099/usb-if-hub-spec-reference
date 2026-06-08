---
title: SS Packet Types
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

# SS Packet Types

> Scope: USB 3.2 Specification Rev 1.0, Sections 7.2–8 (Link Layer Packets).
> This page is a consumer reference summary, not a packet format or protocol behavior verification record.

## Purpose

This page answers:

- The main packet types in USB 3.x SuperSpeed.
- The key differences between SS and USB 2.0 packet structures.
- Hub-relevant packet types.

This page does not answer:

- Bit-level packet field format verification.
- Packet routing, flow control, or retry mechanism runtime behavior.
- USB-IF packet compliance or interoperability testing.

## USB 3.x SuperSpeed Packet Types

USB 3.x SuperSpeed uses a completely different packet format from USB 2.0. Main packet types (based on USB 3.2 Section 7.2):

### Link Layer Packets (LLP)

| Packet type | Abbreviation | Purpose |
|---|---|---|
| Link Management Packet | LMP | Link initialization, capability exchange, configuration |
| Transaction Packet | TP | Transaction control (ACK, NRDY, ERDY, STATUS, etc.) |
| Data Packet | DP | Data payload transfer |
| Isochronous Timestamp Packet | ITP | Timestamp for isochronous transfers |

### Transaction Packets (TP) Types

| TP type | Purpose |
|---|---|
| ACK | Confirms successful reception |
| NRDY | Endpoint not ready (back-pressure) |
| ERDY | Endpoint ready notification (proactive wake) |
| STATUS | Control transfer status stage |
| STALL | Endpoint stalled |
| DEV_NOTIFICATION | Device notifies host (U1/U2 policy, function wake, etc.) |
| PING / PING_RESPONSE | Latency measurement |

## Key Differences from USB 2.0 Packets

| Feature | USB 2.0 | USB 3.x SuperSpeed |
|---|---|---|
| Token/Data/Handshake structure | SOF + Token + Data + Handshake | TP + DP (no separate Token) |
| Transaction Translator | Required (HS hub bridges FS/LS) | **Not required** (SS is purely packet-based) |
| Per-packet acknowledgment | Per-packet ACK | Link layer flow control |
| Isochronous transfer | SOF timing | ITP (Isochronous Timestamp Packet) |

## Hub-Related Packets

SS hubs act as packet routers at the link layer:

- Hub routes downstream transaction packets to the corresponding port.
- Hub aggregates upstream status change interrupt endpoint packets.
- Unlike USB 2.0 TT hubs, SS hubs do not need to split transactions between speed domains (USB 3.x has no TT).

Hub packet routing runtime behavior is outside this page's verified scope.

## This Page Does Not Claim

- Bit-level packet field format verification.
- Packet routing, flow control, or retry mechanism runtime behavior.
- Link layer state machine or LTSSM behavior.
- USB-IF packet compliance or interoperability testing.
- Firmware packet handling implementation correctness.

→ [SS Transactions](ss_transactions.md) | [SS Signaling](ss_signaling.md) | [Verification Status](../verification_status.md)
