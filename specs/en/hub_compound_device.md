---
title: Hub Compound Device
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Compound Device

> Source scope: USB 2.0 Specification Rev 2.0, §11.12 and §11.23.2.  
> This page is a reviewed reference summary for USB 2.0 hub compound device identification, `DeviceRemovable` handling, and `PortPwrCtrlMask` semantics. It is not a compound device compliance verification record.

## Page Purpose

This page answers:

- What a compound device is in the USB 2.0 hub context.
- What `wHubCharacteristics bit 2` and the `DeviceRemovable` field mean.
- What `PortPwrCtrlMask` is and how it should be interpreted in USB 2.0.

This page does not answer:

- Complete implementation rules for a compound device hub firmware.
- Whether any specific device combination meets compound device requirements.

## Compound Device Definition

A **compound device** is a USB device that contains an embedded hub and one or more permanently attached downstream devices. The hub and those attached devices share a single enclosure and are not independently removable by the user.

`wHubCharacteristics bit 2` in the hub class descriptor identifies compound device status:

| Bit 2 | Meaning |
|---|---|
| `0` | Hub is **not** a compound device; all downstream ports are independently removable |
| `1` | Hub **is** part of a compound device; some ports may have non-removable attached devices |

## `DeviceRemovable` Bitmap

The hub class descriptor includes a variable-length `DeviceRemovable` bitmap with one bit per port:

| Bit index | Assignment |
|---|---|
| Bit 0 | Reserved; must be 0 |
| Bit N (N = 1 to bNbrPorts) | Port N removability indicator |

Bit encoding:

| Bit N value | Meaning |
|---|---|
| `0` | The device attached to port N is user-removable (standard behavior) |
| `1` | The device attached to port N is **not** user-removable; it is a fixed part of the compound unit |

The `DeviceRemovable` field is followed immediately by `PortPwrCtrlMask` in the hub class descriptor. Both fields are variable length and rounded up to full bytes.

## `PortPwrCtrlMask`

`PortPwrCtrlMask` is a legacy bitmap inherited from USB 1.x. In USB 1.x it indicated which ports could be independently switched. In **USB 2.0 all bits must be set to `0xFF`** (all ones). The field carries no actionable port power control information in USB 2.0 and should not be parsed for power switching decisions.

## Host Interpretation for Non-Removable Ports

When `DeviceRemovable bit N = 1` for port N:

- The host should not present the attached device as user-removable in system interfaces.
- A `C_PORT_CONNECTION` change event on a non-removable port under normal operation may indicate a hardware failure rather than intentional user removal.
- The host typically skips user notification flows (e.g., "safe to remove hardware") for non-removable devices.

When `wHubCharacteristics bit 2 = 1` (compound device):

- The hub and its non-removable downstream devices behave as a single logical unit.
- Power state transitions on the hub affect the entire compound unit.

## Relationship to `wHubCharacteristics` Bit Layout

`wHubCharacteristics` carries several hub-level configuration fields. Bit 2 is the compound device indicator:

| Bits | Field | Reference |
|---|---|---|
| `[1:0]` | Logical Power Switching Mode | `specs/en/hub_power_management.md` |
| `[2]` | Compound Device Indicator | This page |
| `[4:3]` | Over-current Protection Mode | `specs/en/hub_power_management.md` |
| `[6:5]` | TT Think Time | `specs/en/transaction_translator.md` |
| `[7]` | Port Indicators Supported | `specs/en/hub_descriptor.md` |
| `[15:8]` | Reserved | Must be zero |

## Governed Linkage

- `specs/en/hub_descriptor.md`: full hub class descriptor layout including `DeviceRemovable`, `PortPwrCtrlMask`, and `wHubCharacteristics`
- `specs/en/hub_power_management.md`: power switching modes and over-current fields in `wHubCharacteristics`
- `specs/en/hub_enumeration.md`: hub enumeration sequence and how `DeviceRemovable` is read during initialization
- `specs/en/port_state_machine.md`: port attachment and detachment state transitions

## Non-claims

- This page does not claim compound device behavior on any specific hub has been verified.
- This page does not override the hub descriptor field definitions in `specs/en/hub_descriptor.md`.
- This page does not claim `PortPwrCtrlMask` carries actionable information in USB 2.0.
- This page does not override confirmed project facts in consuming repos.

## Reference Navigation

- specs/en/usb2.md: USB 2.0 topic index (en).
- specs/hub_compound_device.md: 中文對應主題（中文頁）
