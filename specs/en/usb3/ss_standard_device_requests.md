---
title: SS Standard Device Requests
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

# SS Standard Device Requests

> Scope: USB 3.2 Specification Rev 1.0, Section 9.4 (Standard Device Requests).
> This page is a consumer reference summary, not a request behavior verification record.

## Purpose

This page answers:

- Which standard device requests apply to USB 3.x SS hubs.
- Which requests are the same as USB 2.0 and which are new or modified for USB 3.x.
- LPM (U1/U2)-related standard request feature selectors.

This page does not answer:

- Whether firmware correctly implements each request.
- How xHCI drives these requests.

## Standard Device Requests Applicable to USB 3.x SS Hubs

Most USB 2.0 standard device requests are retained in USB 3.x (USB 3.2 Section 9.4):

| Request | bmRequestType | bRequest | Notes |
|---|---|---|---|
| GET_STATUS | 0x80/0x81/0x82 | 0x00 | Device/interface/endpoint status |
| CLEAR_FEATURE | 0x00/0x01/0x02 | 0x01 | Clear feature selector |
| SET_FEATURE | 0x00/0x01/0x02 | 0x03 | Set feature selector |
| SET_ADDRESS | 0x00 | 0x05 | Assign USB address |
| GET_DESCRIPTOR | 0x80 | 0x06 | Read descriptor |
| SET_DESCRIPTOR | 0x00 | 0x07 | Write descriptor (optional) |
| GET_CONFIGURATION | 0x80 | 0x08 | Read current configuration |
| SET_CONFIGURATION | 0x00 | 0x09 | Set configuration |
| GET_INTERFACE | 0x81 | 0x0A | Read interface alternate setting |
| SET_INTERFACE | 0x01 | 0x0B | Set interface alternate setting |

## USB 3.x New Standard Feature Selectors

USB 3.x adds LPM-related standard device feature selectors for SET_FEATURE / CLEAR_FEATURE:

| Feature selector | Value | Recipient | Description |
|---|---|---|---|
| U1_ENABLE | 48 (0x30) | Device | Allows device to initiate U1 entry requests |
| U2_ENABLE | 49 (0x31) | Device | Allows device to initiate U2 entry requests |
| LTM_ENABLE | 50 (0x32) | Device | Enables Latency Tolerance Messaging (LTM) |

> Note: These are **standard device feature selectors**, distinct from SS hub port feature selectors (PORT_U1_ENABLE, etc.). Hub port feature selectors operate via hub class requests; standard device feature selectors apply to the device itself.

## GET_DESCRIPTOR (USB 3.x New Descriptor Types)

USB 3.x adds the following descriptor types:

| bDescriptorType | Name | Description |
|---|---|---|
| 0x0F | BOS (Binary Device Object Store) | Container descriptor for device capability descriptors |
| 0x10 | Device Capability | Device capability descriptor within a BOS descriptor |
| 0x2A | SuperSpeed Hub Descriptor | SS hub-specific descriptor (see ss_hub_descriptor.md) |

## This Page Does Not Claim

- Firmware implementation correctness for each request.
- xHCI internal mechanisms for driving standard requests.
- LTM or U1/U2 device feature selector semantics or behavior.
- USB-IF certification compliance.

→ [SS Hub Class Requests](ss_hub_class_requests.md) | [SS Hub Descriptor](ss_hub_descriptor.md) | [Verification Status](../verification_status.md)
