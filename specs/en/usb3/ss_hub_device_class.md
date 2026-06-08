---
title: SS Hub Device Class Codes
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

# SS Hub Device Class Codes

> Scope: USB 3.2 Specification Rev 1.0, §10.14.2 / §10.15.1.
> This page documents the class code field values a SuperSpeed hub presents in its standard USB device descriptor. This is a reviewed reference; it is not a descriptor dump verification or firmware behavior verification.

## Purpose

This page answers:

- The `bDeviceClass`, `bDeviceSubClass`, and `bDeviceProtocol` values for a USB 3.x SS hub.
- What `bDeviceProtocol = 0x03` means in the USB 3.x context.
- How SS hub class codes differ from USB 2.0 hub class codes.

This page does not answer:

- Whether any specific hub's VID, PID, `bcdUSB`, or other vendor-specific fields are verified.
- Whether any specific hub firmware's device descriptor is correct.
- LTSSM training or speed-identification mechanisms.

## Device Descriptor Class Code Fields

The USB device descriptor at offsets 4–6 contains three class code fields with specific meanings for SS hubs:

| Offset | Field | Size | SS Hub Spec Value |
|---|---|---|---|
| 4 | `bDeviceClass` | 1 byte | `0x09` (Hub class) |
| 5 | `bDeviceSubClass` | 1 byte | `0x00` |
| 6 | `bDeviceProtocol` | 1 byte | `0x03` (SuperSpeed hub) |

### `bDeviceClass = 0x09`

- The hub class code `0x09` is identical between USB 2.0 and USB 3.x; it is reserved by USB-IF for the hub class.
- The host stack uses this to identify a hub class device and apply the hub class request set.

### `bDeviceSubClass = 0x00`

- The hub class SubClass is fixed at `0x00`; USB 3.x defines no hub subclass.

### `bDeviceProtocol = 0x03`: SuperSpeed Hub

USB 3.x SuperSpeed hubs use `bDeviceProtocol = 0x03`, which is distinct from all USB 2.0 protocol codes:

| `bDeviceProtocol` | Hub Type | Description |
|---:|---|---|
| `0x00` | USB 2.0 FS hub or hub not advertising TT | USB 2.0 only |
| `0x01` | USB 2.0 HS hub, single TT | USB 2.0 only |
| `0x02` | USB 2.0 HS hub, multi-TT | USB 2.0 only |
| `0x03` | **SuperSpeed hub** | USB 3.x SS hub (no TT; SS hubs require no Transaction Translator) |

`bDeviceProtocol = 0x03` is the USB 3.x SuperSpeed hub identifier. Because SS hubs have no Transaction Translator, the single-TT / multi-TT distinction of `0x01` / `0x02` does not apply.

## bcdUSB Version Field

A SS hub's `bcdUSB` (device descriptor offsets 2–3) reflects the minimum supported USB specification version:

| `bcdUSB` | USB Version |
|---|---|
| `0x0300` | USB 3.0 |
| `0x0310` | USB 3.1 (when Gen 2 / 10 Gbps capable) |
| `0x0320` | USB 3.2 (when multi-lane Gen 2×2 capable) |

The actual `bcdUSB` value is device-specific; this page does not claim any particular value has been verified.

## Differences from USB 2.0

| Aspect | USB 2.0 Hub | USB 3.x SS Hub |
|---|---|---|
| `bDeviceProtocol` | 0x00 / 0x01 / 0x02 (TT types) | 0x03 (SuperSpeed, no TT) |
| TT capability advertisement | Via protocol code 0x01/0x02 | Not applicable (SS hub has no TT) |
| `bcdUSB` | 0x0200 | 0x0300 or higher |

## Governed Linkage

- [SS Hub Descriptor](ss_hub_descriptor.md): SS hub class-specific descriptor fields
- [SS Hub Configuration](ss_hub_configuration.md): SS hub configuration/interface descriptor structure
- [SS Hub Class Requests](ss_hub_class_requests.md): SS hub class request set (no TT requests)

## Non-claims

- This page is not a complete field verification for the USB device descriptor.
- This page does not claim any SS hub's `bDeviceClass`, `bDeviceSubClass`, or `bDeviceProtocol` values have been verified as correct.
- This page does not claim LTSSM training behavior or speed identification has been verified.
- This page does not override confirmed project facts in consuming repos.

→ [SS Hub Descriptor](ss_hub_descriptor.md) | [SS Hub Configuration](ss_hub_configuration.md) | [Verification Status](../verification_status.md)
