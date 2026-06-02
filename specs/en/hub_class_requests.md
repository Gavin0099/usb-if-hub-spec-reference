---
title: Hub Class Requests
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Class Requests

> Source scope: USB 2.0 Specification Rev 2.0, Section 11.24.2.
> This page is a structured summary only; section-level packet verification is still pending.

## Request Families

| bRequest | Value | Direction | Recipient | Summary |
|---|---|---|---|---|
| `GET_STATUS` | `0x00` | Device-to-Host | Hub / Port | Reads hub or port status and change fields |
| `CLEAR_FEATURE` | `0x01` | Host-to-Device | Hub / Port | Clears a feature, or clears the recorded event represented by a change bit |
| `SET_FEATURE` | `0x03` | Host-to-Device | Hub / Port | Sets hub or port features |
| `GET_DESCRIPTOR` | `0x06` | Device-to-Host | Hub | Reads the hub class-specific descriptor |
| `SET_DESCRIPTOR` | `0x07` | Host-to-Device | Hub | Writes the hub class-specific descriptor; support is implementation-dependent |
| `CLEAR_TT_BUFFER` | `0x08` | Host-to-Device | TT-capable Hub | Clears TT buffer state |
| `RESET_TT` | `0x09` | Host-to-Device | TT-capable Hub | Resets the Transaction Translator |
| `GET_TT_STATE` | `0x0A` | Device-to-Host | TT-capable Hub | Returns TT diagnostic state |
| `STOP_TT` | `0x0B` | Host-to-Device | TT-capable Hub | Stops TT split-transaction processing |

## How to Read `CLEAR_FEATURE`

Inside the hub class model, `CLEAR_FEATURE` is not only “turn a feature off.” It is also how the host clears change-event flags:

- for `wPortChange` / `wHubChange`, `CLEAR_FEATURE(...)` means the host has observed and acknowledged that change event
- for example, `CLEAR_FEATURE(C_PORT_CONNECTION)` does not mean “disconnect the port”; it means “clear the recorded connection-change event”
- when reading `GET_STATUS`, change bits and `CLEAR_FEATURE` should be understood together

## Common Setup Packet Shapes

| Request | `bmRequestType` | `wValue` | `wIndex` | `wLength` |
|---|---|---|---|---|
| Hub `GET_STATUS` | `0xA0` | `0x0000` | `0x0000` | `4` |
| Port `GET_STATUS` | `0xA3` | `0x0000` | `port_number` | `4` |
| Hub `SET_FEATURE` / `CLEAR_FEATURE` | `0x20` | `feature_selector` | `0x0000` | `0` |
| Port `SET_FEATURE` / `CLEAR_FEATURE` | `0x23` | `feature_selector` | `port_number` | `0` |
| TT family requests | usually `0x23` or `0xA3` | `spec_defined` or `0x0000` | `spec_defined` | request-specific |

## Feature Selector Boundary

- Hub-recipient and port-recipient selector namespaces must be treated separately.
- The standard port selector range is `0-22`; vendor selectors must not overlap that range.
- Bit semantics returned by `GET_STATUS` should be read together with `specs/port_status_bits.md`.
- Selector details should be cross-checked with `tables/feature_selector_matrix.yaml`.

## TT Request Constraints

- `CLEAR_TT_BUFFER`, `RESET_TT`, `GET_TT_STATE`, and `STOP_TT` apply only to HS hubs with embedded TT.
- Several fields still remain `spec_defined`, which means section-level verification is not complete.
- A consuming repo should not change TT behavior from this page alone without escalation review.
