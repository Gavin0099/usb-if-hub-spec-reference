---
title: SS Port Indicators
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

# SS Port Indicators

> Scope: USB 3.2 Specification Rev 1.0, §10.14.2 (wHubCharacteristics bit[5]).
> This page covers the optional port indicator (LED) control feature for USB 3.x SuperSpeed hubs.

## Purpose

This page answers:

- How `wHubCharacteristics bit[5]` signals port indicator support in a USB 3.x SS hub.
- Whether the `SET_FEATURE(PORT_INDICATOR)` encoding is the same in USB 3.x as in USB 2.0.
- The key differences between USB 3.x and USB 2.0 port indicator features.

This page does not answer:

- LED hardware behavior for any specific hub implementation.
- USB-IF indicator compliance testing requirements.
- A hub's automatic-mode LED color logic (firmware-defined).

## Port Indicator Support Flag

USB 3.x SS hub `wHubCharacteristics bit[5]` signals port indicator support:

| `wHubCharacteristics bit[5]` | Meaning |
|---|---|
| `0` | Port indicators **not supported** |
| `1` | Port indicators supported; host may use `SET_FEATURE(PORT_INDICATOR)` |

> **Difference from USB 2.0**: In USB 2.0, the port indicator flag is at `wHubCharacteristics bit[7]`. In USB 3.x, it moves to **bit[5]** because the TT Think Time field (bits[6:5] in USB 2.0) no longer exists in USB 3.x.

The bit[5] encoding identity has been verified via the `usb3_ss_whc_port_indicators` evidence packet (bit name and value identity only).

## SET_FEATURE(PORT_INDICATOR) Request Encoding

When `wHubCharacteristics bit[5] = 1`, the host may control port LEDs using:

```
bmRequestType: 0x23  (Host→Device, Class, Other recipient)
bRequest:      0x03  (SET_FEATURE)
wValue:        PORT_INDICATOR selector value (0–3, see table below)
wIndex:        port_number (1-based)
wLength:       0
```

LED state encoding (same as USB 2.0):

| Selector Value | LED State | Meaning |
|---|---|---|
| `0` | Automatic | Hub controls the LED (default behavior) |
| `1` | Amber | Host forces amber (e.g., needs attention) |
| `2` | Green | Host forces green (e.g., device active) |
| `3` | Off | Host turns LED off |

## wHubCharacteristics Bit Layout Differences

| Bit | USB 2.0 wHubCharacteristics | USB 3.x wHubCharacteristics |
|---|---|---|
| bit[1:0] | Logical Power Switching Mode | Same |
| bit[2] | Compound Device | Same |
| bit[4:3] | Over-Current Protection Mode | Same |
| bit[6:5] | **TT Think Time** (USB 2.0 only) | **Reserved** (no TT in USB 3.x) |
| bit[7] | **Port Indicators** (USB 2.0) | Reserved |
| bit[5] | (Part of TT Think Time in USB 2.0) | **Port Indicators** (USB 3.x) |
| bit[15:8] | Reserved | — |
| bit[15:6] | — | Reserved (USB 3.x) |

Port Indicators moved from bit[7] in USB 2.0 to bit[5] in USB 3.x due to the removal of the TT Think Time field.

## Governed Linkage

- `tables/ss_hub_characteristics_bit_matrix.yaml`: `usb3_ss_whc_port_indicators` (bit[5]) — verified
- [SS Hub Characteristics](ss_hub_characteristics.md): Full wHubCharacteristics bit description
- [SS Feature Selectors](ss_feature_selectors.md): Complete SS hub feature selector list
- [SS Hub Class Requests](ss_hub_class_requests.md): SET_FEATURE request structure

## Non-claims

- This page does not claim any specific SS hub's port indicator LED color behavior has been verified.
- This page does not claim the firmware correctness of automatic-mode LED color logic.
- This page does not claim PORT_INDICATOR feature selector runtime request behavior has been verified.
- This page does not override confirmed project facts in consuming repos.

→ [SS Hub Characteristics](ss_hub_characteristics.md) | [SS Feature Selectors](ss_feature_selectors.md) | [Verification Status](../verification_status.md)
