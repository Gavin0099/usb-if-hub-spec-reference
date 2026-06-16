---
title: USB Transactions
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# USB Transactions

> Source scope: USB 2.0 Specification Rev 2.0, §8.5 and §8.6.  
> This page is a reviewed reference summary for USB 2.0 transaction structure and error handling. A transaction is the smallest complete unit of USB communication: one token + optional data + optional handshake.

## Page Purpose

This page answers:

- What is the structure of IN, OUT, and SETUP transactions.
- How a control transfer's three phases (SETUP + DATA + STATUS) work.
- What NAK, STALL, and NYET mean for transaction retry and error recovery.

## Transaction Structure

A **transaction** consists of up to three packets:

```
[Token packet] → [Data packet] → [Handshake packet]
```

Not all transactions have all three phases:

| Transaction type | Token | Data | Handshake |
|---|---|---|---|
| SETUP | SETUP | DATA0 (always) | ACK (from device) |
| IN | IN | DATA0 or DATA1 (from device) | ACK / NAK (from host) |
| OUT | OUT | DATA0 or DATA1 (from host) | ACK / NAK / STALL (from device) |
| SOF | SOF | — | — (no handshake) |

## SETUP Transaction

Used exclusively for control transfer SETUP phase (endpoint 0):

```
Host → Device:   SETUP token
Host → Device:   DATA0  (8-byte setup packet)
Device → Host:   ACK
```

- Device always responds with ACK for a valid SETUP packet.
- After ACK, the device processes the setup packet and prepares a response.
- Data toggle is always DATA0 for the SETUP phase.

## IN Transaction

Host requests data from a device endpoint:

```
Host → Device:   IN token
Device → Host:   DATA0 or DATA1  (payload) — or NAK / STALL
Host → Device:   ACK  (if data received) — or no response on error
```

- If the device is not ready: device sends `NAK`; host retries on next poll interval.
- If the endpoint is halted: device sends `STALL`; host must `CLEAR_FEATURE(ENDPOINT_HALT)`.
- Successful ACK advances the data toggle (DATA0→DATA1→DATA0...).

## OUT Transaction

Host sends data to a device endpoint:

```
Host → Device:   OUT token
Host → Device:   DATA0 or DATA1  (payload)
Device → Host:   ACK / NAK / STALL
```

- `ACK`: data accepted; toggle advances.
- `NAK`: device busy; host retries.
- `STALL`: endpoint halted; requires `CLEAR_FEATURE(ENDPOINT_HALT)`.

## Control Transfer: Three-Phase Sequence

A control transfer combines SETUP + optional DATA + STATUS transactions:

### Phase 1: SETUP

```
SETUP token + DATA0 (8-byte setup packet) + ACK
```

Delivers the request (bmRequestType, bRequest, wValue, wIndex, wLength).

### Phase 2: DATA (optional)

If `wLength > 0`, one or more IN or OUT transactions transfer the data payload:

- Direction matches `bmRequestType[7]`.
- Data toggle starts at DATA1 and alternates.
- Multiple transactions if payload exceeds `bMaxPacketSize0`.

### Phase 3: STATUS

Confirms the entire transfer is complete:

- Direction is **opposite** to the DATA phase.
- Carries a zero-length DATA1 packet.
- Device sends `ACK` (or `NAK` if still processing).

```
Example: GET_DESCRIPTOR (Device→Host, 18 bytes)
  SETUP:   SETUP + DATA0(8B: GET_DESCRIPTOR request) + ACK
  DATA:    IN + DATA1(8B) + ACK   → IN + DATA0(8B) + ACK   → IN + DATA1(2B) + ACK
  STATUS:  OUT + DATA1(0B) + ACK
```

## Interrupt Transfer Transactions

The hub status change endpoint uses interrupt IN transactions:

```
Host → Device (hub):   IN token (at bInterval period)
Device → Host:         DATA0 or DATA1 (status change bitmap) — or NAK if no change
Host → Device:         ACK (if data received)
```

- If no port changed: hub sends `NAK` → host retries at next interval.
- If any port changed: hub sends the status change bitmap; bit 0=hub, bit N=port N.

## Error Handling Summary

| Response | Meaning | Host action |
|---|---|---|
| `ACK` | Success | Advance toggle, continue |
| `NAK` | Temporarily busy | Retry (automatically, within transfer timeout) |
| `STALL` | Endpoint halted | Issue `CLEAR_FEATURE(ENDPOINT_HALT)` to recover |
| `NYET` (HS) | Not yet (split) | Send CSPLIT in next micro-frame |
| No response / CRC error | Packet lost | Retry (up to 3 times); report error if exhausted |

## Data Toggle and Duplicate Detection

Each endpoint maintains a toggle bit (DATA0/DATA1):

- Sender toggles after each successfully ACKed transaction.
- Receiver toggles after ACK is sent.
- If the receiver sees the wrong toggle (e.g., DATA0 when DATA1 expected): the data is a retransmit → receiver sends ACK but discards the data (no duplicate processing).

This allows silent recovery when an ACK is lost but the data was actually delivered.

## Governed Linkage

- `specs/en/usb_packet_types.md`: individual packet types (PID values, structure)
- `specs/en/split_transaction_packets.md`: SSPLIT / CSPLIT transaction structure for TT hubs
- `specs/en/hub_class_requests.md`: control transfer payloads for hub class requests
- `specs/en/hub_interrupt_endpoint.md`: interrupt endpoint details for status change reporting
- `specs/en/standard_device_requests.md`: setup packets carried in SETUP transactions

## Non-claims

- This page does not claim transaction sequencing has been verified against a physical hub.
- This page does not specify the complete USB 2.0 host controller scheduling algorithm.
- This page does not claim error recovery timing is implementation-verified.
- This page does not override confirmed project facts in consuming repos.

## Reference Navigation

- specs/en/usb2.md: USB 2.0 topic index (en).
- specs/usb_transactions.md: 中文對應主題（中文頁）
