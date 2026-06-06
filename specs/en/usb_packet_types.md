---
title: USB Packet Types
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# USB Packet Types

> Source scope: USB 2.0 Specification Rev 2.0, §8.3.  
> This page is a reviewed reference summary for USB 2.0 packet types, PID encoding, and packet structure. Understanding packet types is prerequisite to understanding transactions, error handling, and split transactions.

## Page Purpose

This page answers:

- What USB 2.0 packet types exist and how they are identified.
- What fields each packet type contains.
- Which packets are relevant to hub and hub-port operation.

## PID (Packet Identifier)

Every USB packet begins with a **PID byte** that identifies the packet type:

- Bits `[3:0]`: PID type code.
- Bits `[7:4]`: One's complement of bits `[3:0]` (check field — ensures at least 4 signal transitions).

If the received check bits do not match, the packet is discarded silently.

## Token Packets

Token packets initiate a transaction. They identify the target device and endpoint.

**Structure**: `PID` (1B) + `ADDR[6:0] + ENDP[3:0]` (2B) + `CRC5` (bits within 2B)

| Packet | PID | Initiator | Purpose |
|---|---|---|---|
| `OUT` | `0xE1` | Host | Host will send data to device endpoint |
| `IN` | `0x69` | Host | Host requests data from device endpoint |
| `SOF` | `0xA5` | Host | Start-of-Frame marker; sent every 1ms (FS) or 125µs (HS) |
| `SETUP` | `0x2D` | Host | Initiates a control transfer SETUP phase (EP0 only) |

**SOF packet** carries an 11-bit `Frame Number` field instead of `ADDR+ENDP`, plus `CRC5`.

Token packets are host-originated; devices never send token packets.

## Data Packets

Data packets carry payload bytes. They follow a token packet.

**Structure**: `PID` (1B) + `DATA[0..N]` (0 to 1024B) + `CRC16` (2B)

| Packet | PID | Speeds | Notes |
|---|---|---|---|
| `DATA0` | `0xC3` | FS / LS / HS | Alternates with DATA1 for error detection |
| `DATA1` | `0x4B` | FS / LS / HS | Alternates with DATA0 |
| `DATA2` | `0x87` | HS only | Used in high-bandwidth isochronous transactions |
| `MDATA` | `0x0F` | HS only | Used in split transactions and high-bandwidth ISO |

**Data toggle** (DATA0↔DATA1): sender and receiver maintain matching toggle bits. A mismatch indicates a retransmitted or lost ACK; receiver discards duplicate data.

## Handshake Packets

Handshake packets acknowledge or reject a data transaction. They are **1 byte only** (PID).

| Packet | PID | Sender | Meaning |
|---|---|---|---|
| `ACK` | `0xD2` | Receiver | Data accepted; toggle advances |
| `NAK` | `0x5A` | Device | Busy — cannot accept/send data; host should retry |
| `STALL` | `0x1E` | Device | Endpoint halted; requires `CLEAR_FEATURE(ENDPOINT_HALT)` to recover |
| `NYET` | `0x96` | Device | HS only: not yet ready (used in split transactions) |
| `ERR` | `0x3C` | Hub (TT) | HS only: split transaction error on FS/LS segment |

`NAK` is a **temporary** condition (device is busy); the host retries automatically.  
`STALL` is a **permanent** halted state; it requires explicit host action to clear.

## Special Packets

| Packet | PID | Notes |
|---|---|---|
| `PRE` (Preamble) | `0x3C` | FS hub signals LS preamble before LS downstream token |
| `PING` | `0xB4` | HS only: host asks if device can accept OUT data before sending |
| `SPLIT` | `0x78` | HS only: introduces a split transaction (SSPLIT or CSPLIT) |
| `EXT` | `0xF0` | Extended token (reserved for future use) |

Note: `PRE` and `ERR` share PID `0x3C`; the interpretation is context-dependent (PRE appears as a standalone packet before a LS token; ERR appears as a handshake response from a TT hub).

## Packet Types and Hub Operation

| Hub activity | Packets involved |
|---|---|
| Host enumerating the hub | SETUP token + DATA0 (setup packet) + ACK → hub responds with ACK/NAK/STALL |
| Hub reporting status change | Host sends IN token to interrupt endpoint; hub responds with DATA0/DATA1 bitmap or NAK |
| Host issuing hub class request | SETUP + DATA0 (8B setup) + ACK; optional IN data phase; STATUS phase |
| HS hub forwarding FS/LS transaction | SPLIT + SSPLIT token → hub executes downstream → host sends CSPLIT to collect result |
| Hub halting an endpoint | Hub sends STALL; host must issue `CLEAR_FEATURE(ENDPOINT_HALT)` to resume |

## Governed Linkage

- `specs/en/usb_transactions.md`: how packets combine to form SETUP, IN, and OUT transactions
- `specs/en/split_transaction_packets.md`: SPLIT packet structure and SSPLIT/CSPLIT fields
- `specs/en/usb_signaling.md`: bus-level signal encoding (NRZI, bit stuffing) that carries these packets
- `specs/en/standard_device_requests.md`: control transfer content carried in DATA0 packets
- `specs/en/transaction_translator.md`: how TT hubs translate HS split transactions to FS/LS

## Non-claims

- This page does not claim PID values or packet structures have been verified against the USB 2.0 PDF.
- This page does not claim CRC computation algorithms are correctness-verified.
- This page does not establish a complete USB protocol layer implementation specification.
- This page does not override confirmed project facts in consuming repos.
