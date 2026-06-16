---
title: Transaction Translator
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Transaction Translator

> Source scope: USB 2.0 Specification Rev 2.0, Sections 11.17-11.18.
> This page is a TT behavior summary and does not claim full split-transaction verification.

## Core Concept

A Transaction Translator (TT) exists inside a high-speed hub to bridge host-issued high-speed split transactions and actual traffic to full-speed or low-speed downstream devices.

- A hub without TT should not claim TT-specific request support.
- TT behavior should not appear in a full-speed-only hub.
- TT behavior is tied to descriptor-declared TT type and TT think time settings.

## TT Type and Think Time

| Item | Related Field | Summary |
|---|---|---|
| Single TT | TT type in `wHubCharacteristics` | One TT is shared across downstream ports |
| Multiple TT | TT type in `wHubCharacteristics` | Independent TT instances exist per port or per port group |
| TT Think Time = `00` | `wHubCharacteristics[6:5]` | 8 FS bit times |
| TT Think Time = `01` | `wHubCharacteristics[6:5]` | 16 FS bit times |
| TT Think Time = `10` | `wHubCharacteristics[6:5]` | 24 FS bit times |
| TT Think Time = `11` | `wHubCharacteristics[6:5]` | 32 FS bit times |

## TT Requests

- `CLEAR_TT_BUFFER`
- `RESET_TT`
- `GET_TT_STATE`
- `STOP_TT`

These requests apply only to HS hubs with embedded TT.

## TT Request Opcode Map

| Request | bRequest | Summary |
|---|---:|---|
| `CLEAR_TT_BUFFER` | `0x08` | Clears TT buffer state (TT-capable HS hub only). |
| `RESET_TT` | `0x09` | Resets the TT (TT-capable HS hub only). |
| `GET_TT_STATE` | `0x0A` | Reads TT diagnostic state (TT-capable HS hub only). |
| `STOP_TT` | `0x0B` | Stops TT split-transaction processing (TT-capable HS hub only). |

The mapping above is request-level orientation only; behavioral limits for `wValue`, `wIndex`, and `wLength` remain defined in the matrix and related pages.

The current reviewed request surface in this repo is:

- `CLEAR_TT_BUFFER`: `wValue` carries TT buffer selector fields; `wIndex` selects the TT port / context
- `RESET_TT`: `wValue = 0x0000`; `wIndex` selects the TT port number
- `GET_TT_STATE`: `wValue = 0x0000`; `wIndex` selects the TT port / diagnostic context; `wLength` is the TT state data length
- `STOP_TT`: `wValue = 0x0000`; `wIndex` selects the TT port number

That still does not amount to full field-level verified encoding, and it does not claim TT behavior has completed semantic verification.

## Governed Linkage

- `tables/transaction_translator_matrix.yaml`: governed TT type, think-time, and TT request-linkage surface.
- `tables/hub_descriptor_matrix.yaml`: links TT think-time to `wHubCharacteristics[6:5]`.
- `tables/class_request_matrix.yaml`: links TT request names to class request setup surfaces.
- `specs/escalation_table.md`: `E-06`, `E-07`, and `E-10` describe TT-related escalation triggers.

The TT table is a reviewed reference boundary only. It does not verify split-transaction timing, TT buffer selector encoding, diagnostic payload semantics, or firmware support.

## Split Transaction Flow

1. The host sends a Start Split to the HS hub.
2. The hub TT translates the request for the downstream FS/LS device.
3. The host later issues a Complete Split.
4. The hub / TT aggregates the result and returns it upstream.

## Usage Notes

- This page must not override a confirmed project decision about Single TT vs Multiple TT.
- A mismatch between TT think time and descriptor-declared settings is an escalation trigger.
- If firmware behavior would change because of this page, architecture review should happen first.

## Reference Navigation

- specs/en/usb2.md: USB 2.0 topic index (en).
- specs/transaction_translator.md: 中文對應主題（中文頁）
