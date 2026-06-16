---
title: Hub Configuration Descriptors
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Configuration Descriptors

> Source scope: USB 2.0 Specification Rev 2.0, §11.23 / §11.21.  
> This page is a reviewed reference summary for the configuration and interface descriptor fields a hub presents during USB enumeration. It is not a descriptor dump verification.

## Page Purpose

This page answers:

- What characteristics a hub configuration descriptor typically has.
- The values of `bInterfaceClass`, `bInterfaceSubClass`, and `bInterfaceProtocol` in the hub class interface descriptor.
- Which endpoints a hub provides (interrupt IN).

This page does not answer:

- Vendor-specific fields for any specific hub (VID, PID, `bcdUSB`, `iProduct`, etc.).
- Hub class-specific descriptor fields (see `specs/en/hub_descriptor.md`).
- Whether any specific hub's descriptor dump has been verified.

## Descriptor Hierarchy During USB Hub Enumeration

The descriptor flow during hub enumeration:

```
GET_DESCRIPTOR(DEVICE) → device descriptor (with bDeviceClass=0x09)
GET_DESCRIPTOR(CONFIGURATION) → configuration descriptor + interface + endpoint + hub class descriptor
GET_DESCRIPTOR(HUB_CLASS, type=0x29) → hub class-specific descriptor (bDescLength, bNbrPorts, wHubCharacteristics...)
```

## Device Descriptor Hub-Specific Fields

(See `specs/en/hub_device_class.md` for details)

| Field | Hub Spec Value |
|---|---|
| `bDeviceClass` | `0x09` |
| `bDeviceSubClass` | `0x00` |
| `bDeviceProtocol` | `0x00`/`0x01`/`0x02` |

## Configuration Descriptor Typical Fields

A USB 2.0 hub typically presents one configuration:

| Field | Typical Value | Description |
|---|---|---|
| `bNumConfigurations` | `1` | Hubs typically have only one configuration |
| `bConfigurationValue` | `1` | Host selects it via `SET_CONFIGURATION(1)` |
| `bNumInterfaces` | `1` | Hub class requires only one interface |
| `bmAttributes` | implementation-defined | Remote wakeup support (bit 5), bus-powered or self-powered (bit 6) |
| `bMaxPower` | implementation-defined | Maximum current drawn from VBUS (in 2 mA units) |

> These are typical values, not spec-mandated values. Consuming firmware should verify by reading via actual GET_DESCRIPTOR.

## Interface Descriptor Hub Class Fields

Hubs use a single interface. The class code fields in the interface descriptor are:

| Field | Value | Description |
|---|---|---|
| `bInterfaceClass` | `0x09` | Hub class (same as bDeviceClass in device descriptor) |
| `bInterfaceSubClass` | `0x00` | USB 2.0 defines no hub interface subclass |
| `bInterfaceProtocol` | `0x00` | Interface-level protocol (usually 0; TT capability is expressed via bDeviceProtocol in the device descriptor) |
| `bNumEndpoints` | `1` | Hub class interface normally has one endpoint (interrupt IN) |

## Hub Endpoints Overview

The hub class interface provides:

1. **Endpoint 0 (Control)**: Implicitly present; used for all hub class requests (GET_STATUS, SET_FEATURE, etc.).
2. **Interrupt IN endpoint**: Status change endpoint; used to notify the host of port/hub status changes. See `specs/en/hub_interrupt_endpoint.md`.

Hubs do not require Bulk or Isochronous endpoints.

## GET_DESCRIPTOR Request for the Hub Class Descriptor

The host retrieves the hub class-specific descriptor with a GET_DESCRIPTOR request:

| Field | Value |
|---|---|
| `bmRequestType` | `0xA0` (device→host, class, device recipient) |
| `bRequest` | `GET_DESCRIPTOR` (class-specific, bRequest=6) |
| `wValue` | `0x2900` (descriptor type=0x29, index=0) |
| `wLength` | Hub descriptor length (minimum 7 bytes, scales with port count) |

See `specs/en/hub_descriptor.md` for detailed field descriptions.

## Multi-TT Hub Alternate Interface Setting

An HS multi-TT hub (`bDeviceProtocol = 0x02`) may support both single-TT and multi-TT modes via alternate interface settings:

- `SET_INTERFACE(alternateSetting=0)` → single-TT mode (all ports share one TT)
- `SET_INTERFACE(alternateSetting=1)` → multi-TT mode (each port has a dedicated TT)

The host selects the alternate setting after enumeration based on its needs.

## Governed Linkage

- `specs/en/hub_device_class.md`: details of bDeviceClass/SubClass/Protocol
- `specs/en/hub_descriptor.md`: hub class-specific descriptor fields (§11.23.2.1)
- `specs/en/hub_interrupt_endpoint.md`: interrupt IN endpoint descriptor fields
- `specs/en/transaction_translator.md`: multi-TT and single-TT hub behavior

## Non-claims

- This page is not a descriptor dump verification for any specific hub.
- This page does not claim correct values for vendor-specific fields like `bMaxPower` or `bmAttributes`.
- This page does not override confirmed project facts in consuming repos.

## Reference Navigation

- specs/en/usb2.md: USB 2.0 topic index (en).
- specs/hub_configuration.md: 中文對應主題（中文頁）
