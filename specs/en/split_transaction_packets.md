---
title: Split Transaction Packets
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Split Transaction Packets

> Source scope: USB 2.0 Specification Rev 2.0, §8.4.2 and §11.17.  
> This page covers the SPLIT packet structure and SSPLIT/CSPLIT transaction flow used by HS hubs with embedded Transaction Translators. For TT high-level semantics see `specs/en/transaction_translator.md`.

## Page Purpose

This page answers:

- What the SPLIT packet looks like at the byte/field level.
- How SSPLIT and CSPLIT tokens are encoded.
- What the complete split transaction timing sequence looks like.

## Why Split Transactions Exist

An HS hub operates its upstream port at 480 Mbps but its downstream ports may be FS (12 Mbps) or LS (1.5 Mbps). The host controller communicates with the hub's Transaction Translator (TT) using HS split transactions; the TT handles the FS/LS segment independently.

Without split transactions, the host would have to time FS/LS bus segments directly, which is incompatible with the HS frame schedule.

## SPLIT Packet Structure

The SPLIT packet precedes the token in a split transaction. PID = `0x78`.

**SPLIT token fields** (4 bytes total: PID + 3 payload bytes):

| Bits | Field | Description |
|---|---|---|
| `[6:0]` | Hub Address | 7-bit USB address of the TT hub |
| `[7]` | SC | 0 = Start-Split (SSPLIT); 1 = Complete-Split (CSPLIT) |
| `[14:8]` | Port | 7-bit port number on the TT hub |
| `[15]` | S | Speed indicator: 0 = FS; 1 = LS (for isochronous: start-of-payload) |
| `[16]` | E/U | SSPLIT isochronous end indicator / CSPLIT unused |
| `[18:17]` | ET | Endpoint type: 00=Control, 01=Isochronous, 10=Bulk, 11=Interrupt |
| `[23:19]` | CRC5 | 5-bit CRC over Hub Addr + SC + Port + S + E/U + ET |

## SSPLIT Transaction (Start Split)

The host initiates a split transaction by sending SSPLIT to the TT hub:

```
HS segment (host → TT hub):
  SPLIT(SC=0) + token (IN/OUT/SETUP) + [data for OUT/SETUP] + [handshake]
```

After receiving SSPLIT + token, the TT hub:
1. Sends ACK to the host (transaction delivered to TT).
2. Queues and executes the full FS/LS transaction on the downstream port.

## CSPLIT Transaction (Complete Split)

The host retrieves the result from the TT by sending CSPLIT:

```
HS segment (host → TT hub):
  SPLIT(SC=1) + token (IN or OUT)
TT hub → host:
  DATA (for IN) or ACK/NAK/STALL (for OUT) — or NYET if result not yet ready
```

If the TT has not yet completed the downstream FS/LS transaction: hub returns `NYET`, and the host retries CSPLIT in the next micro-frame.

## Split Transaction Flow: Control Transfer Example

```
Micro-frame 0: Host → Hub: SSPLIT(SETUP) + SETUP token + DATA0(8B) + ACK from hub
Micro-frame 0: Hub → FS device: SETUP token + DATA0(8B) + ACK from FS device

Micro-frame 2+: Host → Hub: CSPLIT(IN) + IN token
               Hub → Host: NYET  (still executing FS DATA phase)

Micro-frame 3+: Host → Hub: CSPLIT(IN) + IN token
               Hub → Host: DATA1(payload)  (FS device replied)
               Host → Hub: ACK
```

## SSPLIT/CSPLIT Timing Constraints

| Phase | Constraint |
|---|---|
| SSPLIT issued in | Any micro-frame |
| CSPLIT earliest issue | Micro-frame `start + 2` (at minimum) |
| Hub NYET response | TT still executing downstream segment; host retries next micro-frame |
| Hub ERR response | Error on FS/LS segment; host-side error recovery |

## Endpoint Type and Split Behavior

| ET (Endpoint Type) | SSPLIT behavior | CSPLIT behavior |
|---|---|---|
| `00` Control | Full SETUP/DATA/STATUS | HOST issues CSPLIT for each result phase |
| `01` Isochronous | S/E bits indicate payload segment | No CSPLIT (isochronous: no error recovery) |
| `10` Bulk | Standard start | CSPLIT retrieves ACK/NAK/STALL |
| `11` Interrupt | Standard start | CSPLIT retrieves DATA/NAK/STALL |

Isochronous split transactions do not use CSPLIT; the hub discards the result if there is no CSPLIT (consistent with ISO no-retry semantics).

## Governed Linkage

- `specs/en/transaction_translator.md`: TT high-level semantics, think-time, and TT request families
- `specs/en/usb_packet_types.md`: SPLIT PID value and packet framing
- `specs/en/usb_transactions.md`: transaction-level control flow (SSPLIT/CSPLIT build on IN/OUT/SETUP)
- `specs/en/hub_class_requests.md`: `CLEAR_TT_BUFFER`, `RESET_TT`, `GET_TT_STATE`, `STOP_TT`

## Non-claims

- This page does not claim split transaction field encoding has been verified against the USB 2.0 PDF.
- This page does not claim isochronous split transaction behavior is correctness-verified.
- This page does not define a complete TT scheduling model.
- This page does not override confirmed project facts in consuming repos.

## Reference Navigation

- specs/en/usb2.md: USB 2.0 topic index (en).
- specs/split_transaction_packets.md: 中文對應主題（中文頁）
