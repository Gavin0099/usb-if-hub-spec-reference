---
title: SS Hub — No Transaction Translator
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

# SS Hub — No Transaction Translator

> Scope: USB 3.2 Specification Rev 1.0, §10, §11 (Hub Class); USB 2.0 Specification, §11.14 (Transaction Translator).
> This page explains why SuperSpeed hubs do not use a Transaction Translator (TT) and describes the architectural difference from USB 2.0 TT-capable hubs.

## Purpose

This page answers:

- Why USB 2.0 uses Transaction Translators and their architectural role.
- Why SuperSpeed hubs do not need a TT.
- How hub descriptor fields differ when TT is absent.

This page does not answer:

- TT runtime transaction timing or the Split Transaction flow in detail.
- How xHCI manages TT-less device enumeration under an SS hub.
- USB-IF TT compliance testing.
- Behavior of FS/LS devices connected to an SS hub (SS hubs do not support FS/LS directly).

## Role of the USB 2.0 Transaction Translator

A USB 2.0 hub connecting a High-Speed (HS) upstream host to Full-Speed / Low-Speed (FS/LS) downstream devices requires a Transaction Translator (TT) to bridge the speed domains:

| Function | Description |
|---|---|
| Speed-domain bridging | HS host and FS/LS devices cannot communicate directly; TT performs the bridge |
| Split Transaction | Host issues SSPLIT/CSPLIT Tokens; TT completes the transfer in the FS/LS speed domain |
| TT Think Time | `wHubCharacteristics[6:5]` records the maximum HS microframes required for one FS transaction |

USB 2.0 Hub Descriptor (type 0x29) includes TT Think Time, and `bDeviceProtocol` identifies TT type as `0x01` (Single TT) or `0x02` (Multiple TT).

## SuperSpeed Hubs Have No TT

SuperSpeed (USB 3.x) hub downstream ports all operate at SuperSpeed; there is no speed-domain conversion requirement:

| Feature | USB 2.0 Hub (HS-capable) | USB 3.x SS Hub |
|---|---|---|
| Downstream port speeds | HS + FS/LS (mixed) | SS only |
| TT required | Yes (for FS/LS devices) | **No** |
| Split Transaction | Required (SSPLIT/CSPLIT Tokens) | **Does not exist** |
| TT Think Time field | `wHubCharacteristics[6:5]` valid | **Not present** (SS Hub Descriptor has no TT field) |
| `bDeviceProtocol` | `0x01` / `0x02` (Single/Multiple TT) | **`0x03`** (SS hub, no TT) |

## Descriptor Differences

### `bDeviceProtocol` (Device Descriptor)

| Value | Description |
|---|---|
| `0x00` | Root hub or Full-Speed-only hub |
| `0x01` | USB 2.0 hub, Single Transaction Translator |
| `0x02` | USB 2.0 hub, Multiple Transaction Translators |
| `0x03` | **USB 3.x SuperSpeed hub (no TT)** |

### Hub Descriptor Type

| Spec | Descriptor Type | TT Think Time Field |
|---|---|---|
| USB 2.0 | `0x29` | `wHubCharacteristics[6:5]`: valid |
| USB 3.x | **`0x2A`** | **Not present** (SS Hub Descriptor has no TT field) |

### `wHubCharacteristics` Bit Layout Differences

| Bit | USB 2.0 Hub | USB 3.x SS Hub |
|---|---|---|
| `[1:0]` | Power Switching Mode | Power Switching Mode (same) |
| `[2]` | Compound Device | Compound Device (same) |
| `[4:3]` | Over-current Protection Mode | Over-current Protection Mode (same) |
| `[6:5]` | **TT Think Time** | **Reserved** (no TT Think Time in SS hub) |
| `[7]` | Port Indicators | **Reserved** (USB 3.x hub: bit position shifted) |
| `[5]` | Reserved | **Port Indicators** (USB 3.x hub: moved to bit[5]) |

## Non-claims

- This page does not claim TT runtime transaction timing has been verified.
- This page does not claim xHCI TT-less hub handling behavior has been verified.
- This page does not claim USB-IF TT compliance test results.
- This page does not claim behavior for FS/LS devices connected to an SS hub (SS hubs do not support FS/LS directly).
- This page does not override confirmed project facts in consuming repos.

## Governed Linkage

- `tables/ss_hub_characteristics_bit_matrix.yaml`: `usb3_ss_whc_port_indicators` (bit[5]), `usb3_ss_whc_reserved_high` (TT Think Time bits absent) — verified
- [SS Hub Descriptor](ss_hub_descriptor.md): `bDeviceProtocol = 0x03`, SS Hub Descriptor type 0x2A
- [SS Hub Characteristics](ss_hub_characteristics.md): `wHubCharacteristics` bit layout (USB3 vs USB2)
- [SS Transactions](ss_transactions.md): Split Transaction does not exist in SS context

→ [SS Hub Characteristics](ss_hub_characteristics.md) | [SS Transactions](ss_transactions.md) | [SS Hub Descriptor](ss_hub_descriptor.md) | [Verification Status](../verification_status.md)
