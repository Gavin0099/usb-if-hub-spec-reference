---
title: Hub Device Class Codes
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Device Class Codes

> Source scope: USB 2.0 Specification Rev 2.0, §11.3 / §11.23.1.  
> This page documents the class code field values a hub presents in its standard USB device descriptor. This is a reviewed boundary; it is not a descriptor dump verification or firmware behavior verification.

## Page Purpose

This page answers:

- Why `bDeviceClass = 0x09` identifies the hub class.
- What `bDeviceSubClass` and `bDeviceProtocol` mean in the hub context.
- How single-TT and multi-TT hubs are distinguished via `bDeviceProtocol`.

This page does not answer:

- Whether the other USB 2.0 device descriptor fields (VID, PID, bcdUSB, etc.) for any specific hub are verified.
- Whether any specific hub firmware's device descriptor is correct.
- Whether all HS hubs must advertise TT capability.

## Device Descriptor Class Code Fields

The USB device descriptor at offsets 4–6 contains three class code fields that have specific meanings for hubs:

| Offset | Field | Size | Hub Spec Value |
|---|---|---|---|
| 4 | `bDeviceClass` | 1 byte | `0x09` (Hub class) |
| 5 | `bDeviceSubClass` | 1 byte | `0x00` |
| 6 | `bDeviceProtocol` | 1 byte | `0x00` / `0x01` / `0x02` (see below) |

### `bDeviceClass = 0x09`

- The hub class code is `0x09`, reserved by USB-IF for the hub class.
- The host stack or driver uses this to identify a hub class device and apply the hub class request set.
- If `bDeviceClass = 0x00` (indicating interface-level class), the hub still requires `bInterfaceClass = 0x09` in the interface descriptor.

### `bDeviceSubClass = 0x00`

- The hub class SubClass is fixed at `0x00`; the USB 2.0 spec defines no hub subclass.

### `bDeviceProtocol`: TT Capability Identifier

| `bDeviceProtocol` | Hub Type | Description |
|---:|---|---|
| `0x00` | Full-speed hub or hub not advertising TT | FS hub; or HS hub that does not advertise TT capability via the device descriptor |
| `0x01` | HS hub, single Transaction Translator | The entire hub has one TT (shared across all ports) |
| `0x02` | HS hub, multiple Transaction Translators | Each port has a dedicated TT (multi-TT hub) |

TT capability is only meaningful for HS hubs. FS hubs use `0x00` because they do not support HS downstream and therefore do not need a TT.

## Relationship to TT Matrix

- `tables/transaction_translator_matrix.yaml` entries `usb20_tt_type_single` and `usb20_tt_type_multiple` correspond to protocol codes `0x01` and `0x02` here.
- `bDeviceProtocol` is the host's entry point for identifying single-TT vs multi-TT during enumeration.
- TT behavior details for `SET_FEATURE(PORT_*)` are documented in `specs/en/transaction_translator.md`.

## Safe Interpretation Boundary

- This page records the identity boundary for class code fields. It does not claim that any specific hub's TT implementation is correct.
- `bDeviceProtocol = 0x01` means only that the hub advertises single-TT; it does not verify TT think-time or buffer behavior.
- If a consuming repo's hub hardware has a `bDeviceProtocol` that does not match expectations, enter Standard Escalation Mode.

## Governed Linkage

- `tables/transaction_translator_matrix.yaml`: governed surface for TT type and TT think-time
- `specs/en/transaction_translator.md`: reference summary for TT type and multi-TT behavior
- `specs/en/hub_descriptor.md`: hub class descriptor fields (bDescLength through PortPwrCtrlMask)

## Non-claims

- This page is not a complete field verification for the USB device descriptor.
- This page does not claim any hub's `bDeviceClass`, `bDeviceSubClass`, or `bDeviceProtocol` values have been verified as correct.
- This page does not override confirmed project facts in consuming repos.
