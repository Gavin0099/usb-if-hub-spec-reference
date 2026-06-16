---
title: Standard USB Descriptors
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Standard USB Descriptors

> Source scope: USB 2.0 Specification Rev 2.0, §9.5 and §9.6.  
> This page is a reviewed reference summary for the standard USB 2.0 descriptor types. Hub-specific descriptor fields are covered in `specs/en/hub_descriptor.md`.

## Page Purpose

This page answers:

- What standard USB 2.0 descriptors exist and what each contains.
- Which fields in each descriptor are relevant to USB hub identification.

This page does not answer:

- Hub class descriptor fields — those are in `specs/en/hub_descriptor.md`.
- Vendor-specific or class-specific descriptor extensions beyond the hub class.

## Descriptor Hierarchy

When a host reads `GET_DESCRIPTOR (configuration)`, the device returns the full configuration descriptor set in this order:

```
Configuration Descriptor (9 bytes)
  └── Interface Descriptor (9 bytes)  [one per interface]
        └── Endpoint Descriptor (7 bytes)  [one per endpoint]
  └── Hub Class Descriptor (variable)  [for hub class interfaces]
```

The hub class descriptor is requested separately via `GET_DESCRIPTOR` with `bmRequestType=0xA0`.

## Device Descriptor (§9.6.1)

Size: **18 bytes**. Descriptor type: `0x01`.

| Offset | Field | Size | Hub value |
|---|---|---|---|
| 0 | `bLength` | 1 | `18` |
| 1 | `bDescriptorType` | 1 | `0x01` |
| 2–3 | `bcdUSB` | 2 | `0x0200` (USB 2.0) |
| 4 | `bDeviceClass` | 1 | `0x09` (Hub class) |
| 5 | `bDeviceSubClass` | 1 | `0x00` |
| 6 | `bDeviceProtocol` | 1 | `0x00` FS/no-TT, `0x01` HS/single-TT, `0x02` HS/multi-TT |
| 7 | `bMaxPacketSize0` | 1 | Max packet size for endpoint 0 (FS: 8, HS: 64) |
| 8–9 | `idVendor` | 2 | Vendor ID (USB-IF assigned) |
| 10–11 | `idProduct` | 2 | Product ID (vendor assigned) |
| 12–13 | `bcdDevice` | 2 | Device release number (BCD) |
| 14 | `iManufacturer` | 1 | String descriptor index (0 = no string) |
| 15 | `iProduct` | 1 | String descriptor index (0 = no string) |
| 16 | `iSerialNumber` | 1 | String descriptor index (0 = no string) |
| 17 | `bNumConfigurations` | 1 | Number of configurations (typically `1`) |

> For hub class codes (`bDeviceClass`, `bDeviceSubClass`, `bDeviceProtocol`) see `specs/en/hub_device_class.md`.

## Device_Qualifier Descriptor (§9.6.2)

Size: **10 bytes**. Descriptor type: `0x06`. **HS-capable devices only.**

Describes how the device behaves at the alternate speed (e.g., a HS hub's FS behavior):

| Offset | Field | Notes |
|---|---|---|
| 0 | `bLength` | `10` |
| 1 | `bDescriptorType` | `0x06` |
| 2–3 | `bcdUSB` | USB version |
| 4 | `bDeviceClass` | Same class code |
| 5 | `bDeviceSubClass` | Same |
| 6 | `bDeviceProtocol` | Protocol at other speed |
| 7 | `bMaxPacketSize0` | EP0 max packet at other speed |
| 8 | `bNumConfigurations` | Configs at other speed |
| 9 | `bReserved` | Must be zero |

FS hubs do not have a Device_Qualifier descriptor. Attempting to request it from an FS hub returns STALL.

## Configuration Descriptor (§9.6.3)

Size: **9 bytes**. Descriptor type: `0x02`. Returned as part of the full configuration set.

| Offset | Field | Size | Hub value |
|---|---|---|---|
| 0 | `bLength` | 1 | `9` |
| 1 | `bDescriptorType` | 1 | `0x02` |
| 2–3 | `wTotalLength` | 2 | Total bytes in config descriptor set |
| 4 | `bNumInterfaces` | 1 | `1` (single interface for hub) |
| 5 | `bConfigurationValue` | 1 | Configuration number (typically `1`) |
| 6 | `iConfiguration` | 1 | String descriptor index |
| 7 | `bmAttributes` | 1 | bit 7=1 (required), bit 6=Self-Powered, bit 5=Remote-Wakeup |
| 8 | `bMaxPower` | 1 | Max bus current in units of 2mA |

`bmAttributes` bit 7 must always be set to 1 (per USB 2.0 spec). Bits 4:0 are reserved and must be zero.

## Interface Descriptor (§9.6.5)

Size: **9 bytes**. Descriptor type: `0x04`.

| Offset | Field | Size | Hub value |
|---|---|---|---|
| 0 | `bLength` | 1 | `9` |
| 1 | `bDescriptorType` | 1 | `0x04` |
| 2 | `bInterfaceNumber` | 1 | `0` |
| 3 | `bAlternateSetting` | 1 | `0`=single-TT, `1`=multi-TT (HS only) |
| 4 | `bNumEndpoints` | 1 | `1` (status change endpoint) |
| 5 | `bInterfaceClass` | 1 | `0x09` (Hub class) |
| 6 | `bInterfaceSubClass` | 1 | `0x00` |
| 7 | `bInterfaceProtocol` | 1 | `0x00` |
| 8 | `iInterface` | 1 | String descriptor index |

> Multi-TT hubs expose two alternate settings (0 and 1) under the same interface number. See `specs/en/hub_configuration.md`.

## Endpoint Descriptor (§9.6.6)

Size: **7 bytes**. Descriptor type: `0x05`. Hub has exactly one endpoint: the status change interrupt IN endpoint.

| Offset | Field | Size | Hub value |
|---|---|---|---|
| 0 | `bLength` | 1 | `7` |
| 1 | `bDescriptorType` | 1 | `0x05` |
| 2 | `bEndpointAddress` | 1 | bit 7=1 (IN direction), bits 3:0=endpoint number |
| 3 | `bmAttributes` | 1 | `0x03` (bits[1:0]=11: Interrupt transfer type) |
| 4–5 | `wMaxPacketSize` | 2 | `ceil((bNbrPorts + 1) / 8)` bytes |
| 6 | `bInterval` | 1 | Polling interval (FS: 1–255 ms; HS: 2^(n-1) × 125µs) |

For `wMaxPacketSize` and `bInterval` encoding details, see `specs/en/hub_interrupt_endpoint.md`.

## String Descriptor (§9.6.7)

Size: **variable**. Descriptor type: `0x03`.

- String 0 (language ID list): 4 bytes minimum; contains supported `LANGID` codes.
- String N (language-specific text): 2 + 2×length bytes; UTF-16LE encoded text.

Hubs are not required to implement string descriptors beyond string 0, but iManufacturer, iProduct, and iSerialNumber may point to optional strings.

## Governed Linkage

- `specs/en/hub_descriptor.md`: hub class descriptor fields (type `0x29`) obtained via class GET_DESCRIPTOR
- `specs/en/hub_device_class.md`: `bDeviceClass`, `bDeviceSubClass`, `bDeviceProtocol` values for hub identification
- `specs/en/hub_configuration.md`: hub configuration and interface descriptor usage in context
- `specs/en/hub_interrupt_endpoint.md`: endpoint descriptor fields specific to the hub status change endpoint
- `specs/en/standard_device_requests.md`: `GET_DESCRIPTOR` request encoding and descriptor type codes

## Non-claims

- This page does not claim any descriptor field has been correctness-verified against a physical hub.
- This page does not claim `bMaxPower` or `bmAttributes` semantics have been verified for self-powered vs. bus-powered hub behavior.
- This page does not override confirmed project facts in consuming repos.

## Reference Navigation

- specs/en/usb2.md: USB 2.0 topic index (en).
- specs/standard_descriptors.md: 中文對應主題（中文頁）
