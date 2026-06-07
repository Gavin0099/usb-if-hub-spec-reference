---
title: SuperSpeed Hub Descriptor
claim_level: inferred
spec_family: usb3
status: review_required
last_reviewed: "2026-06-07"
usb_versions:
  - usb_3_2
source_refs:
  - usb32_spec
semantic_verification_claimed: false
---

# SuperSpeed Hub Descriptor

> Source scope: USB 3.2 Specification Rev 1.0, Section 10.14.2.1.
> This page is a consumer-facing reference summary, not a field-by-field PDF verification record.

## Page Purpose

This page answers:

- Which fields exist in the SuperSpeed hub descriptor, and how they differ from the USB 2.0 hub descriptor.
- The `wHubCharacteristics` bit definitions under USB 3.x (no TT Think Time field).
- The purpose of the new `bHubDecLat` and `wHubDelay` fields.

This page does not answer:

- Whether a specific firmware descriptor dump has been verified bit-by-bit.
- Whether a specific SS hub implementation is correct.

## Field Overview

| Offset | Field | Size | Description |
|---|---|---|---|
| 0 | bLength | 1B | Total descriptor length (minimum 12B, excluding DeviceRemovable) |
| 1 | bDescriptorType | 1B | **0x2A** (SuperSpeed Hub Descriptor; USB 2.0 uses 0x29) |
| 2 | bNbrPorts | 1B | Number of downstream ports, maximum 15 |
| 3 | wHubCharacteristics | 2B | Hub characteristic bit field (see table below) |
| 5 | bPwrOn2PwrGood | 1B | Power-on to power-good wait time, in units of 2ms |
| 6 | bHubContrCurrent | 1B | Max hub controller current draw (mA) |
| 7 | bHubDecLat | 1B | Hub packet header decode latency, in units of 0.1μs (0 for root hub) |
| 8 | wHubDelay | 2B | Average delay added by hub (ns), used for U1/U2 exit latency calculation |
| 10 | DeviceRemovable | variable | 1 bit per port; bit N=1 means port N+1 is non-removable |

## wHubCharacteristics Bit Definitions (USB 3.x)

| Bits | Field | Description |
|---|---|---|
| bits[1:0] | Logical Power Switching Mode | 00b=ganged, 01b=individual, 10b/11b=no switching |
| bit[2] | Compound Device | 0=standalone, 1=compound device |
| bits[4:3] | Over-Current Protection Mode | 00b=global, 01b=individual, 10b/11b=none |
| bit[5] | Port Indicators Supported | 0=not supported, 1=PORT_INDICATOR feature supported |
| bits[15:6] | Reserved | Must be zero |

## Differences from USB 2.0 Hub Descriptor

| Difference | USB 2.0 (0x29) | USB 3.x (0x2A) |
|---|---|---|
| bDescriptorType | 0x29 | **0x2A** |
| TT Think Time (wHubCharacteristics bits[9:8]) | Present (8/16/24/32 FS bit times) | **Not present** (SS hub has no TT) |
| Port Indicators bit | bit[7] | **bit[5]** |
| PortPwrCtrlMask field | Present (all 0xFF in USB 2.0) | **Not present** |
| bHubDecLat | Not present | **New**: packet header decode latency |
| wHubDelay | Not present | **New**: U1/U2 exit latency calculation |

## bHubDecLat and wHubDelay

- **bHubDecLat**: The latency required by the hub to decode a packet header, in units of 0.1μs. Used by the system to calculate total U1/U2 exit latency budget. Root hubs report 0.
- **wHubDelay**: The average propagation delay added by the hub, in nanoseconds. Used by xHCI to calculate the allowed U1/U2 entry latency budget. Typical values: 200–400 ns.

## Non-claims

- Does not claim full semantic verification of all SS hub descriptor fields against the USB 3.2 PDF.
- Does not claim that specific bHubDecLat or wHubDelay values are correctly implemented in any firmware.
- Does not claim USB 3.x hub descriptor electrical or interoperability compliance.
