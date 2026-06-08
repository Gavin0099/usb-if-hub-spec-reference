---
title: SS Transactions
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

# SS Transactions

> Scope: USB 3.2 Specification Rev 1.0, Section 8 (Transaction Layer).
> This page is a consumer reference summary, not a transaction behavior verification record.

## Purpose

This page answers:

- An overview of the USB 3.x SuperSpeed transaction model.
- Key differences between SS and USB 2.0 transactions.
- The hub's role in SS transaction routing.

This page does not answer:

- Transaction layer runtime behavior or retry mechanisms.
- How xHCI implements SS transaction scheduling.
- USB-IF transaction compliance or interoperability testing.

## USB 3.x SuperSpeed Transaction Model

USB 3.x SuperSpeed uses a **point-to-point** full-duplex link; the transaction model is fundamentally different from USB 2.0:

### USB 2.0 vs USB 3.x Transaction Comparison

| Feature | USB 2.0 | USB 3.x SuperSpeed |
|---|---|---|
| Topology | Shared bus (half-duplex) | Point-to-point (full-duplex) |
| Transaction initiation | Host issues Token packet | Host issues Transaction Packet (TP) |
| Flow control | None (polling-based) | Link layer flow control (NRDY/ERDY) |
| Retransmission | Host polling retry | Link layer ACK/NACK |
| Split Transaction | Required (HS hub TT) | **Not required** (no TT) |

### SS Transaction Steps (Bulk IN Example)

1. **Host → Device**: TP (transaction request)
2. **Device → Host**: DP (Data Packet)
3. **Host → Device**: TP (ACK)

Flow control is achieved via NRDY (not ready) / ERDY (endpoint ready) TPs, allowing devices to proactively notify the host when an endpoint is ready.

## NRDY / ERDY Flow Control

- **NRDY (Not Ready)**: Device notifies host that an endpoint cannot currently accept or provide data.
- **ERDY (Endpoint Ready)**: Device proactively notifies host that an endpoint is ready (reduces host polling overhead).

The NRDY/ERDY mechanism improves SuperSpeed efficiency. ERDY runtime behavior is outside this page's verified scope.

## Hub's Role in SS Transactions

SS hubs act as packet routers:

- **Downstream routing**: Hub routes host-issued TP/DP packets to the corresponding downstream port.
- **Upstream routing**: Hub routes downstream device TP/DP packets back upstream.
- **No TT buffering**: SS hubs do not need a Transaction Translator (all connections are SuperSpeed; no speed-domain translation required).

Hub packet routing runtime behavior is outside this page's verified scope.

## Isochronous Transactions

USB 3.x isochronous transactions use ITP (Isochronous Timestamp Packet) to provide synchronization timestamps, replacing USB 2.0's SOF (Start of Frame).

Isochronous transfer runtime scheduling behavior is outside this page's verified scope.

## Split Transaction Does Not Apply in the SS Context

USB 2.0 High-Speed hubs use Split Transactions (SSPLIT/CSPLIT Tokens) to allow the host to issue requests across speed domains to FS/LS devices. This relies on a Transaction Translator (TT) to complete the transfer in the FS/LS speed domain before reporting completion to the host.

In the USB 3.x SuperSpeed context:

- All ports operate at SuperSpeed; there is no HS/FS/LS mixed-speed-domain issue.
- SS hubs do not include a TT; the split transaction mechanism does not exist in the USB 3.x architecture.
- The "Split Transaction: Not required" row in the §USB 2.0 vs USB 3.x Transaction Comparison table above captures this architectural difference.

This section is a contrast note; USB 2.0 split transaction runtime behavior is outside this repo's verified scope.

See [SS Hub — No Transaction Translator](ss_no_transaction_translator.md) for the full TT contrast.

## This Page Does Not Claim

- Transaction layer runtime behavior or retry mechanisms.
- xHCI SS transaction scheduling implementation.
- NRDY/ERDY runtime flow control behavior.
- Link layer ACK/NACK timing.
- USB-IF transaction compliance or interoperability testing.
- USB 2.0 Split Transaction runtime timing (this belongs to the USB 2.0 TT domain).

→ [SS Packet Types](ss_packet_types.md) | [SS Hub Class Requests](ss_hub_class_requests.md) | [SS Hub — No Transaction Translator](ss_no_transaction_translator.md) | [Verification Status](../verification_status.md)
