---
title: SS Hub Configuration Descriptors
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

# SS Hub Configuration Descriptors

> Scope: USB 3.2 Specification Rev 1.0, §10.14.2 / §10.15.1.
> This page is a reviewed reference summary of the configuration, interface, BOS, and SuperSpeed Endpoint Companion descriptor fields a SS hub presents during enumeration. It is not a descriptor dump verification.

## Purpose

This page answers:

- What descriptor types are included in a SS hub's configuration descriptor set.
- The role of the BOS (Binary Device Object Store) descriptor in USB 3.x.
- The class code field values in the SS hub interface descriptor.
- The purpose of the SuperSpeed Endpoint Companion Descriptor (type 0x30).

This page does not answer:

- Vendor-specific fields (VID, PID, `bcdUSB`, `iProduct`, etc.).
- SS Hub class-specific descriptor field details — see [SS Hub Descriptor](ss_hub_descriptor.md).
- Whether any specific hub's descriptor dump has been verified.

## SS Hub Descriptor Hierarchy During Enumeration

```
GET_DESCRIPTOR(DEVICE)          → device descriptor (bDeviceProtocol=0x03)
GET_DESCRIPTOR(CONFIGURATION)   → configuration descriptor set:
    configuration descriptor (9 bytes)
    interface descriptor (9 bytes)
    endpoint descriptor (7 bytes, interrupt IN)
    SuperSpeed Endpoint Companion Descriptor (6 bytes)
GET_DESCRIPTOR(BOS)             → BOS descriptor + capability descriptors
GET_DESCRIPTOR(HUB_CLASS=0x2A)  → SS Hub class-specific descriptor
```

A SS hub adds a **BOS descriptor** and a **SuperSpeed Endpoint Companion Descriptor** that do not exist in USB 2.0.

## Configuration Descriptor

A SS hub typically presents one configuration:

| Field | Typical Value | Description |
|---|---|---|
| `bNumConfigurations` | `1` | SS hubs typically have one configuration |
| `bConfigurationValue` | `1` | Selected by host with `SET_CONFIGURATION(1)` |
| `bNumInterfaces` | `1` | One interface for the hub class |
| `bmAttributes` | Design-dependent | bit 6 = self-powered (1) / bus-powered (0); bit 5 = remote wakeup |
| `bMaxPower` | Design-dependent | Maximum current drawn from VBUS (in 2 mA units) |

> A USB 3.x self-powered hub can provide up to 900 mA per port; a bus-powered hub is more limited. See [SS Hub Power Budget](ss_hub_power_budget.md).

## Interface Descriptor

The SS hub uses a single interface. Key differences from USB 2.0:

| Field | Value | Description |
|---|---|---|
| `bInterfaceClass` | `0x09` | Hub class (same as device descriptor) |
| `bInterfaceSubClass` | `0x00` | No hub interface subclass defined in USB 3.x |
| `bInterfaceProtocol` | `0x00` | SS hub has no TT; no alternate setting needed |
| `bNumEndpoints` | `1` | One interrupt IN endpoint only |

**No alternate settings**: USB 2.0 multi-TT hubs may have alternate settings for single-TT vs multi-TT mode via `SET_INTERFACE`. SS hubs have no TT and therefore no alternate settings.

## BOS Descriptor (Binary Device Object Store, type 0x0F)

USB 3.x **requires** all devices to provide a BOS descriptor; USB 2.0 devices do not:

| Field | Size | Description |
|---|---|---|
| `bLength` | 1 | 5 bytes (BOS header) |
| `bDescriptorType` | 1 | `0x0F` (BOS) |
| `wTotalLength` | 2 | Total length of BOS header + all capability descriptors |
| `bNumDeviceCaps` | 1 | Number of Device Capability Descriptors contained |

SS hubs include at minimum a **SuperSpeed USB Device Capability** (`bDevCapabilityType = 0x03`).

## SuperSpeed USB Device Capability (in BOS, bDevCapabilityType=0x03)

| Field | Description |
|---|---|
| `bmAttributes` | bit 1 = LTM (Latency Tolerance Messaging) support |
| `wSpeedsSupported` | Supported speeds bitmask (bit 3 = SuperSpeed) |
| `bFunctionalitySupport` | Lowest fully functional speed (typically 0x03 = SS) |
| `bU1DevExitLat` | U1 exit latency (μs; 0–10) |
| `wU2DevExitLat` | U2 exit latency (μs; 0–2047) |

The specific U1/U2 latency values in the SuperSpeed Device Capability are device-specific; this page does not claim any particular values have been verified.

## SuperSpeed Endpoint Companion Descriptor (type 0x30)

Every non-EP0 endpoint in a SS hub must be followed by a SuperSpeed Endpoint Companion Descriptor:

| Field | Size | SS Hub Interrupt IN Typical | Description |
|---|---|---|---|
| `bLength` | 1 | `6` | Descriptor size |
| `bDescriptorType` | 1 | `0x30` | SuperSpeed Endpoint Companion |
| `bMaxBurst` | 1 | `0` | Interrupt does not support burst (0 = 1 packet per service interval) |
| `bmAttributes` | 1 | `0x00` | Reserved for interrupt endpoints; must be 0 |
| `wBytesPerInterval` | 2 | ≥ 1 | Maximum bytes per polling interval (hub status bitmap size) |

## Differences from USB 2.0

| Aspect | USB 2.0 Hub | USB 3.x SS Hub |
|---|---|---|
| BOS descriptor | Optional | **Required** |
| Endpoint Companion | Does not exist | **Required** (per SS endpoint) |
| Interface alternate settings | Multi-TT hub may have 2 | None (SS hub has no TT) |
| `bInterfaceProtocol` | 0x00 (FS or not advertising TT) | 0x00 (no TT; always 0 for SS hub) |

## Governed Linkage

- [SS Hub Descriptor](ss_hub_descriptor.md): SS Hub Descriptor (type 0x2A) fields
- [SS Hub Device Class](ss_hub_device_class.md): `bDeviceProtocol = 0x03` explanation
- [SS Hub Interrupt Endpoint](ss_hub_interrupt_endpoint.md): interrupt IN endpoint descriptor fields
- [SS Hub Power Budget](ss_hub_power_budget.md): SS hub power budget rules (900 mA per port)

## Non-claims

- This page is not a descriptor dump verification for any specific SS hub.
- This page does not claim any vendor-specific field values (`bMaxPower`, `bmAttributes`, U1/U2 latency) have been verified.
- This page does not claim BOS or SuperSpeed Capability behavioral semantics have been verified.
- This page does not override confirmed project facts in consuming repos.

→ [SS Hub Descriptor](ss_hub_descriptor.md) | [SS Standard Descriptors](ss_standard_descriptors.md) | [Verification Status](../verification_status.md)
