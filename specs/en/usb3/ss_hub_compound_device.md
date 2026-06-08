---
title: SS Hub Compound Device
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

# SS Hub Compound Device

> Scope: USB 3.2 Specification Rev 1.0, Section 10.14.2 (wHubCharacteristics bit[2]).
> This page is a consumer reference summary, not a compound device behavior verification record.

## Purpose

This page answers:

- What a USB 3.x compound device hub is.
- The semantics of `wHubCharacteristics bit[2]` (Compound Device flag).
- The meaning of compound device in a USB 3.x topology.

This page does not answer:

- Whether firmware correctly implements compound device topology behavior.
- DeviceRemovable bitmap interpretation semantics.
- USB-IF compound device certification requirements.

## Compound Device Definition

A **compound device** is a USB device in which a hub and one or more functions (downstream devices) are integrated in the same physical enclosure, with the functions permanently and non-removably attached to the hub's downstream ports.

The USB 3.x SS hub `wHubCharacteristics bit[2]` reflects this:

| bit[2] | Semantics |
|---|---|
| 0 | Hub is not part of a compound device |
| 1 | Hub is part of a compound device (some downstream functions are permanently attached) |

This bit's identity has been promoted to verified in `ss_hub_characteristics_bit_matrix` (bit name and value encoding identity only).

## Compound Device in USB 3.x Topology

- When the compound device bit = 1, the host should treat certain downstream ports as non-removable.
- The `DeviceRemovable` bitmap (in the Hub Descriptor) marks which ports are permanently connected (compound ports).
- DeviceRemovable bitmap interpretation semantics are outside this page's verified scope.

## Differences from USB 2.0

The USB 3.x `wHubCharacteristics bit[2]` compound device flag has the same semantics as the USB 2.0 bit[2] (identical encoding).

Key topology differences:
- USB 2.0 compound device functions are typically Full-Speed or High-Speed.
- USB 3.x compound device functions can be SuperSpeed.
- Both use the same `wHubCharacteristics bit[2]` encoding (0=not compound, 1=compound).

## This Page Does Not Claim

- Compound device topology behavior or link routing.
- DeviceRemovable bitmap interpretation semantics.
- Firmware compound device implementation correctness.
- USB-IF compound device certification requirements or test standards.

→ [SS Hub Characteristics](ss_hub_characteristics.md) | [SS Hub Descriptor](ss_hub_descriptor.md) | [Verification Status](../verification_status.md)
