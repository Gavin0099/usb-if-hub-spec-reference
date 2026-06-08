---
title: SS Standard Descriptors
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

# SS Standard Descriptors

> Scope: USB 3.2 Specification Rev 1.0, §9.5–9.6 / §10.14.2.
> This page is a reviewed reference summary of standard descriptor types relevant to USB 3.x SuperSpeed hubs. For SS Hub class-specific descriptor fields, see [SS Hub Descriptor](ss_hub_descriptor.md).

## Purpose

This page answers:

- Which new descriptor types USB 3.x introduces (BOS, SuperSpeed Endpoint Companion).
- The hub-specific field values in a SS hub's device descriptor.
- The primary differences from USB 2.0 standard descriptors.

This page does not answer:

- SS Hub class-specific descriptor (type 0x2A) field details — see [SS Hub Descriptor](ss_hub_descriptor.md).
- Vendor-specific or other class-specific descriptor extensions.

## Descriptor Type Reference

| `bDescriptorType` | Name | Scope |
|---|---|---|
| `0x01` | Device Descriptor | Standard (USB 2.0 + USB 3.x) |
| `0x02` | Configuration Descriptor | Standard (USB 2.0 + USB 3.x) |
| `0x04` | Interface Descriptor | Standard (USB 2.0 + USB 3.x) |
| `0x05` | Endpoint Descriptor | Standard (USB 2.0 + USB 3.x) |
| `0x06` | Device Qualifier | USB 2.0 (HS/FS dual-mode devices) |
| `0x0F` | BOS Descriptor | **USB 3.x new (required)** |
| `0x10` | Device Capability Descriptor | **USB 3.x new** (inside BOS) |
| `0x2A` | SS Hub Descriptor | **USB 3.x SS hub class-specific** |
| `0x30` | SuperSpeed Endpoint Companion | **USB 3.x new (required per SS endpoint)** |

## Device Descriptor (USB 3.x Hub)

Size: **18 bytes**. Descriptor type: `0x01`.

| Offset | Field | Size | SS Hub Value |
|---|---|---|---|
| 0 | `bLength` | 1 | `18` |
| 1 | `bDescriptorType` | 1 | `0x01` |
| 2–3 | `bcdUSB` | 2 | `0x0300` or higher (USB 3.0/3.1/3.2) |
| 4 | `bDeviceClass` | 1 | `0x09` (Hub class) |
| 5 | `bDeviceSubClass` | 1 | `0x00` |
| 6 | `bDeviceProtocol` | 1 | `0x03` (SuperSpeed hub) |
| 7 | `bMaxPacketSize0` | 1 | `9` (exponent: 2^9 = 512 bytes for SS EP0) |
| 8–9 | `idVendor` | 2 | Vendor ID (vendor-specific) |
| 10–11 | `idProduct` | 2 | Product ID (vendor-specific) |
| 12–13 | `bcdDevice` | 2 | Device version (vendor-specific) |
| 14 | `iManufacturer` | 1 | String descriptor index |
| 15 | `iProduct` | 1 | String descriptor index |
| 16 | `iSerialNumber` | 1 | String descriptor index |
| 17 | `bNumConfigurations` | 1 | `1` (typically) |

> SS hub `bMaxPacketSize0 = 9`: EP0 max packet size is encoded as an exponent; 2^9 = 512 bytes. This is a USB 3.x encoding change from USB 2.0 (which uses the direct byte value).

## BOS Descriptor (type 0x0F)

USB 3.x **requires** all devices to provide a BOS descriptor; USB 2.0 devices do not (optional).

```
BOS Descriptor (5 bytes)
  └── SuperSpeed USB Device Capability (10 bytes) [bDevCapabilityType=0x03]
  └── SuperSpeed Plus USB Device Capability (optional, Gen 2 devices) [bDevCapabilityType=0x0A]
  └── Other capability descriptors (LTM, Container ID, etc., device-dependent)
```

The BOS lets the host discover a device's SuperSpeed capabilities (U1/U2 exit latency, LTM support, etc.) during enumeration.

## SuperSpeed USB Device Capability (in BOS, bDevCapabilityType=0x03)

| Field | Size | Description |
|---|---|---|
| `bLength` | 1 | 10 bytes |
| `bDescriptorType` | 1 | `0x10` (Device Capability) |
| `bDevCapabilityType` | 1 | `0x03` (SuperSpeed USB) |
| `bmAttributes` | 1 | bit 1 = LTM support |
| `wSpeedsSupported` | 2 | Supported speeds bitmask (bit 3 = SS) |
| `bFunctionalitySupport` | 1 | Lowest fully functional speed (typically 0x03 = SS) |
| `bU1DevExitLat` | 1 | U1 exit latency (μs; 0–10) |
| `wU2DevExitLat` | 2 | U2 exit latency (μs; 0–2047) |

## SuperSpeed Endpoint Companion Descriptor (type 0x30)

Every non-EP0 endpoint in a USB 3.x device **must** be immediately followed by this descriptor:

| Field | Size | SS Hub Interrupt IN Typical | Description |
|---|---|---|---|
| `bLength` | 1 | `6` | |
| `bDescriptorType` | 1 | `0x30` | |
| `bMaxBurst` | 1 | `0` | Interrupt: no burst support (0 = 1 packet per service interval) |
| `bmAttributes` | 1 | `0x00` | Reserved for interrupt; must be 0 |
| `wBytesPerInterval` | 2 | ≥ 1 | Maximum bytes per polling interval (hub status bitmap) |

## Key Differences from USB 2.0 Standard Descriptors

| Aspect | USB 2.0 | USB 3.x SuperSpeed |
|---|---|---|
| `bDeviceProtocol` | 0x00 / 0x01 / 0x02 | 0x03 |
| `bMaxPacketSize0` | Direct byte value (8 or 64) | Exponent value (9 = 2^9 = 512 bytes) |
| BOS descriptor | Optional | **Required** |
| Endpoint Companion | Does not exist | **Required** (per SS endpoint) |
| Device Qualifier | Used by FS/HS dual-mode devices | Not used by SS devices |
| Hub class descriptor type | `0x29` (USB 2.0 Hub Descriptor) | `0x2A` (SuperSpeed Hub Descriptor) |

## Governed Linkage

- [SS Hub Descriptor](ss_hub_descriptor.md): SS Hub Descriptor (type 0x2A) fields
- [SS Hub Configuration](ss_hub_configuration.md): SS hub configuration / BOS / Companion descriptor structure
- [SS Hub Device Class](ss_hub_device_class.md): `bDeviceProtocol = 0x03` explanation

## Non-claims

- This page is not a descriptor dump verification for any specific SS hub.
- This page does not claim BOS or SuperSpeed Capability U1/U2 latency values have been verified.
- This page does not claim `bMaxPacketSize0 = 9` has been verified for any specific hub.
- This page does not override confirmed project facts in consuming repos.

→ [SS Hub Configuration](ss_hub_configuration.md) | [SS Hub Descriptor](ss_hub_descriptor.md) | [Verification Status](../verification_status.md)
