---
title: Hub Descriptor
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Descriptor

> Source scope: USB 2.0 Specification Rev 2.0, Section 11.23.2.1.
> This page remains a curated summary and is not yet fully verified field-by-field against the PDF.

## Main Descriptor Fields

The hub descriptor is returned by the class-specific `GET_DESCRIPTOR` request, with descriptor type `0x29`.

| Offset | Field | Size | Meaning |
|---|---|---|---|
| 0 | `bDescLength` | 1 | Total descriptor length |
| 1 | `bDescriptorType` | 1 | Hub descriptor type, expected to be `0x29` |
| 2 | `bNbrPorts` | 1 | Number of downstream ports reported by the hub |
| 3 | `wHubCharacteristics` | 2 | Hub characteristics bitfield |
| 5 | `bPwrOn2PwrGood` | 1 | Delay from power-on to power-good, in 2 ms units |
| 6 | `bHubContrCurrent` | 1 | Hub controller current requirement, in mA |
| 7 | `DeviceRemovable` | variable | Bitmap indicating whether each port is removable |
| 7+x | `PortPwrCtrlMask` | variable | Reserved mask, commonly represented as `0xFF` patterns |

## `wHubCharacteristics`

| Bits | Field | Meaning |
|---|---|---|
| 1:0 | Logical Power Switching Mode | Power switching mode |
| 2 | Compound Device | Whether the hub is a compound device |
| 4:3 | Over-current Protection Mode | Over-current protection mode |
| 6:5 | TT Think Time | Transaction Translator think time |
| 7 | Port Indicators Supported | Whether port indicators are supported |
| 15:8 | Reserved | Reserved bits |

## Escalation-Relevant Points

- A mismatch between `bNbrPorts` and actual firmware-exposed port count is an escalation trigger.
- `wHubCharacteristics[1:0]` and `[6:5]` affect power switching and TT behavior, so they should not override confirmed project facts by themselves.
- A consuming repo should treat this page as a standards comparison aid, not as direct authority to rewrite descriptor values.
