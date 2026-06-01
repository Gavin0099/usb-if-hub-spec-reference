---
title: Hub Descriptor Fields
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Descriptor Fields

> Source: USB 2.0 Specification, Revision 2.0, Section 11.23.2.1
> Usage: Reference layer only. Do not use to override confirmed project facts.

## Hub Descriptor Format

The Hub Descriptor is returned by a GET_DESCRIPTOR request with Descriptor Type = 0x29 (Hub).

| Offset | Field | Size (bytes) | Description |
|--------|-------|-------------|-------------|
| 0 | bDescLength | 1 | Number of bytes in this descriptor |
| 1 | bDescriptorType | 1 | Hub descriptor type (0x29) |
| 2 | bNbrPorts | 1 | Number of downstream-facing ports |
| 3 | wHubCharacteristics | 2 | Hub characteristics (see below) |
| 5 | bPwrOn2PwrGood | 1 | Time (in 2ms units) from power-on to power-good |
| 6 | bHubContrCurrent | 1 | Maximum current requirement of hub controller (mA) |
| 7 | DeviceRemovable | variable | Indicates if a port has a non-removable device |
| 7+x | PortPwrCtrlMask | variable | Reserved (set to 0xFF) |

## wHubCharacteristics Bit Definitions

| Bits | Field | Values |
|------|-------|--------|
| 1:0 | Logical Power Switching Mode | 00=ganged, 01=individual port, 10-11=reserved |
| 2 | Compound Device | 0=not compound, 1=compound |
| 4:3 | Over-current Protection Mode | 00=global, 01=individual port, 10-11=no protection |
| 6:5 | TT Think Time | 00=8 FS bit times, 01=16, 10=24, 11=32 |
| 7 | Port Indicators Supported | 0=not supported, 1=supported |
| 15:8 | Reserved | 0 |

## Standard Conflict Notes

- `bNbrPorts` is a standard field. If a project uses a different port count in firmware
  than this field reports, flag for Standard Escalation Mode.
- `bPwrOn2PwrGood` timing is project-specific. Do not override with a generic value.
- `wHubCharacteristics[1:0]` power switching mode must match the project's confirmed
  power switching mode fact. Conflict → escalate.
