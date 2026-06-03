---
title: Hub Descriptor
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Descriptor

> Source scope: USB 2.0 Specification Rev 2.0, Section 11.23.2.1.
> This page is a consumer-facing reference summary, not a field-by-field PDF verification record; without section-level evidence, it does not upgrade to `verified`.

## Page Purpose

This page answers:

- Which main fields exist in the hub descriptor.
- Which fields are commonly referenced by firmware, enumeration logs, descriptor dumps, and consuming-repo rules.
- Which fields relate to port count, power switching, over-current behavior, and TT behavior.

This page does not answer:

- Whether a specific descriptor dump has been verified bit-by-bit against the USB-IF PDF.
- Whether a specific firmware implementation is correct.
- Whether every `wHubCharacteristics` bit pattern has already been semantically verified in this repo.

## Main Descriptor Fields

The hub descriptor is returned by the class-specific `GET_DESCRIPTOR` request, with descriptor type `0x29`.
In this repo's current reviewed request surface, both `GET_DESCRIPTOR` and `SET_DESCRIPTOR` are now explicitly linked back to that descriptor-type boundary, but this still does not upgrade the page into a page-level verified claim.

| Offset | Field | Size | Role Summary |
|---|---|---|---|
| 0 | `bDescLength` | 1 byte | Total hub descriptor length. |
| 1 | `bDescriptorType` | 1 byte | Hub descriptor type; this reference summary expects `0x29`. |
| 2 | `bNbrPorts` | 1 byte | Number of downstream ports reported by the hub. |
| 3 | `wHubCharacteristics` | 2 bytes | Bitfield covering power switching, compound device, over-current mode, TT think time, and port indicators. |
| 5 | `bPwrOn2PwrGood` | 1 byte | Delay from power-on to power-good, in 2 ms units. |
| 6 | `bHubContrCurrent` | 1 byte | Hub controller current requirement, typically interpreted in mA. |
| 7 | `DeviceRemovable` | variable | Bitmap describing whether each port is removable. |
| 7+x | `PortPwrCtrlMask` | variable | Reserved / mask field related to per-port power control; `0xFF`-like patterns are common in practice, but this page does not elevate them to verified truth. |

## Field Summaries

### `bDescLength`

- Defines the total hub descriptor length.
- A consuming repo can use it as a structural sanity check when reading descriptor dumps.
- This page does not claim that any specific device value is correct.

### `bDescriptorType`

- Identifies the class-specific hub descriptor type.
- In this repo's reference summary, the hub descriptor type is represented as `0x29`.
- If firmware or dumps report a different type than expected, compare against the spec section and descriptor capture first rather than using this page to overwrite project facts.

### `bNbrPorts`

- This is the direct descriptor field for downstream port count.
- It is frequently compared against actual hardware port count, firmware-exposed port count, and consuming-repo topology assumptions.
- If `bNbrPorts` conflicts with confirmed hardware or firmware facts, treat it as escalation-sensitive and cross-check `E-01`.

### `wHubCharacteristics`

- This 16-bit field carries multiple descriptor semantics and should not be treated as a single boolean property.
- The most commonly consumed groups are:
  - power switching mode
  - over-current protection mode
  - TT think time
  - port indicators support
- This page only summarizes field roles; it does not claim all bit patterns have section-level verification.

### `bPwrOn2PwrGood`

- Represents the delay between power-on and power-good.
- The field often affects how host or firmware reasoning talks about power sequencing, but this page does not establish a timing guarantee.
- If a consuming repo needs to convert it into concrete timing facts, it should verify against the original PDF and project-side hardware data.

### `bHubContrCurrent`

- Describes the hub controller current requirement.
- It is useful as a comparison point for descriptor dumps and design documentation.
- This page does not upgrade it into a board-level current validation claim.

### `DeviceRemovable`

- This bitmap indicates whether downstream ports are marked removable.
- A consuming repo can use it as descriptor-side semantic context, but it should not rely on this page alone to override confirmed facts about fixed devices, soldered devices, or topology.
- If removable vs non-removable behavior is disputed, preserve escalation.

### `PortPwrCtrlMask`

- This field is commonly interpreted alongside per-port power-control semantics.
- `0xFF`-style values are common in practice, but that is a common pattern, not a verified universal truth in this repo.
- If a consuming repo wants to make firmware decisions from this field, it should first confirm project facts and spec anchors.

## `wHubCharacteristics` Bit Groups

| Bits | Group | Role Summary |
|---|---|---|
| `1:0` | Logical Power Switching Mode | Describes the hub power-switching mode. |
| `2` | Compound Device | Describes whether the hub is a compound device. |
| `4:3` | Over-current Protection Mode | Describes the over-current protection mode. |
| `6:5` | TT Think Time | Describes the Transaction Translator think-time category. |
| `7` | Port Indicators Supported | Describes whether port indicators are supported. |
| `15:8` | Reserved | Reserved bits; this page does not claim firmware may repurpose them. |

### Safe Interpretation Boundary for `wHubCharacteristics`

- `1:0` and `6:5` often directly affect power switching and TT behavior, so they are easy for consuming repos to over-apply.
- This repo provides a standards-side reference summary, not project-truth authority.
- If descriptor power switching mode or TT think time conflicts with confirmed project facts, enter Standard Escalation Mode instead of directly rewriting firmware assumptions.

## Governed Linkage

- `tables/class_request_matrix.yaml`: the `GET_DESCRIPTOR` family provides request-level linkage for hub descriptor access.
- `specs/escalation_table.md`: `E-01`, `E-07`, and `E-08` directly involve `bNbrPorts`, `wHubCharacteristics[6:5]`, and `wHubCharacteristics[1:0]`.
- `specs/transaction_translator.md`: provides the higher-level TT type and TT think-time summary.

There is currently no dedicated governed hub-descriptor table, so this page links through request-family coverage, escalation rules, and adjacent summary pages.

## What This Page Can and Cannot Answer

This page can answer:

- Which core fields exist in the hub descriptor.
- Which fields relate to port count, power switching, over-current behavior, TT behavior, and removable bitmaps.
- Which fields are escalation-sensitive comparison points.

This page cannot answer:

- Whether a specific device descriptor has been verified at section level.
- Whether every `DeviceRemovable` or `PortPwrCtrlMask` bit pattern has been fully verified in this repo.
- Whether a consuming repo should directly change firmware descriptor values based only on this page.

## Non-claims

- This page is not a field-by-field or bit-by-bit USB 2.0 PDF verification record.
- This page does not declare any specific descriptor dump to be correct or incorrect.
- This page does not establish a complete semantic truth table for `wHubCharacteristics`.
- This page does not override confirmed project facts in consuming repos.
