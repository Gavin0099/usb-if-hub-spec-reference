---
title: SS Hub Enumeration
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

# SS Hub Enumeration

> Scope: USB 3.2 Specification Rev 1.0, Section 10.14 / 10.14.2.
> This page is a consumer reference summary, not an enumeration runtime behavior verification record.

## Purpose

This page answers:

- The key steps in a USB 3.x SS hub enumeration sequence.
- The purpose and requirement of the `SET_HUB_DEPTH` request.
- The main differences between SS hub and USB 2.0 hub enumeration.

This page does not answer:

- How the xHCI host controller implements SS hub enumeration internally.
- Whether firmware enumeration logic conforms to the specification.
- USB-IF certification procedures or test specifications.

## SS Hub Enumeration Sequence (Summary)

1. **Reset + Speed Detection**: Host issues bus reset to port; link training determines SuperSpeed or fallback.
2. **GET_DESCRIPTOR(DeviceDescriptor)**: Read device descriptor; confirm bDeviceClass=0x09 (Hub).
3. **SET_ADDRESS**: Assign USB address.
4. **GET_DESCRIPTOR(HubDescriptor)**: Read SS Hub Descriptor (USB 3.x-specific bDescriptorType=0x2A).
5. **SET_HUB_DEPTH** (required for SS hubs): Inform hub of its depth in the bus topology.
6. **SET_CONFIGURATION**: Activate configuration.
7. **Port power on**: Apply port power per wHubCharacteristics (ganged or per-port).
8. **Wait bPwrOn2PwrGood × 2 ms**: Wait for port power to stabilize.

> **Step 5 (SET_HUB_DEPTH) is a mandatory step unique to USB 3.x SS hubs**; USB 2.0 hubs do not require this request.

## SET_HUB_DEPTH Request

| Field | Value |
|---|---|
| bmRequestType | 0x20 (Class, Device, host-to-device) |
| bRequest | 0x0C |
| wValue | Hub depth (0 = root hub or hub directly attached to root hub; max 5) |
| wIndex | 0 |
| wLength | 0 |

- Root hub or SS hub directly attached to root hub: depth = 0.
- Each additional hub tier: depth +1; maximum depth = 5.
- xHCI must send this request before completing hub configuration.

## Key Differences from USB 2.0 Hub Enumeration

| Feature | USB 2.0 Hub | USB 3.x SS Hub |
|---|---|---|
| Hub Descriptor type | 0x29 | **0x2A** (SS-specific) |
| SET_HUB_DEPTH | Not required | **Mandatory** |
| Transaction Translator (TT) | Present (HS hub) | **Absent** |
| TT-related requests (CLEAR_TT_BUFFER, etc.) | Present | **Not supported** |
| U1/U2 feature selectors | None | **6 available** |
| bInterval encoding | Speed-dependent (FS ms, HS microframe) | **Microframe (same as HS USB 2.0)** |

## SS Hub Descriptor Type

USB 3.x SS hubs use the **SuperSpeed Hub Descriptor** (bDescriptorType=0x2A), with different fields from the USB 2.0 Hub Descriptor (0x29). See [SS Hub Descriptor](ss_hub_descriptor.md).

## This Page Does Not Claim

- xHCI host controller internal SS hub enumeration implementation.
- Firmware enumeration behavior correctness.
- Link training or LTSSM negotiation behavior.
- USB-IF certification procedures or test compliance.

→ [SS Hub Descriptor](ss_hub_descriptor.md) | [SS Hub Class Requests](ss_hub_class_requests.md) | [Verification Status](../verification_status.md)
