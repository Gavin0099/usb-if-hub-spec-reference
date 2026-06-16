---
title: Standard USB Device Requests
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Standard USB Device Requests

> Source scope: USB 2.0 Specification Rev 2.0, §9.3 and §9.4.  
> This page covers the standard USB device requests that all USB devices — including hubs — must implement or acknowledge. It is a reviewed reference summary, not a section-level compliance verification record.

## Page Purpose

This page answers:

- What is the 8-byte USB setup packet structure.
- How `bmRequestType` encodes direction, type, and recipient.
- Which standard USB device requests apply to a USB 2.0 hub.

This page does not answer:

- Hub class-specific requests (`GET_STATUS` hub/port, `SET_FEATURE` port, TT requests) — those are in `specs/en/hub_class_requests.md`.
- Whether any specific request has been correctness-verified against a physical hub.

## Setup Packet Format

Every USB control transfer begins with an 8-byte setup packet:

| Byte(s) | Field | Description |
|---|---|---|
| 0 | `bmRequestType` | Encodes direction, type, and recipient |
| 1 | `bRequest` | Request code |
| 2–3 | `wValue` | Request-specific value (little-endian) |
| 4–5 | `wIndex` | Request-specific index (little-endian) |
| 6–7 | `wLength` | Length of the data phase (0 if no data) |

### `bmRequestType` Breakdown

| Bits | Field | Values |
|---|---|---|
| `[7]` | Data direction | `0` = Host→Device; `1` = Device→Host |
| `[6:5]` | Request type | `00` = Standard; `01` = Class; `10` = Vendor; `11` = Reserved |
| `[4:0]` | Recipient | `00000` = Device; `00001` = Interface; `00010` = Endpoint; `00011` = Other |

Common `bmRequestType` values for standard requests:

| Value | Direction | Type | Recipient |
|---|---|---|---|
| `0x00` | Host→Device | Standard | Device |
| `0x01` | Host→Device | Standard | Interface |
| `0x02` | Host→Device | Standard | Endpoint |
| `0x80` | Device→Host | Standard | Device |
| `0x81` | Device→Host | Standard | Interface |
| `0x82` | Device→Host | Standard | Endpoint |

> **Hub class requests** use type=`01` (Class): `0x20` / `0x23` / `0xA0` / `0xA3`. Standard requests use type=`00`.

## Standard Device Requests (§9.4)

All USB devices must respond to standard requests. The table below shows all standard `bRequest` codes and their applicability to a USB 2.0 hub:

| `bRequest` | Value | Direction | Hub Relevance |
|---|---|---|---|
| `GET_STATUS` | `0x00` | Device→Host | Required (device, interface, endpoint) |
| `CLEAR_FEATURE` | `0x01` | Host→Device | Required (DEVICE_REMOTE_WAKEUP, ENDPOINT_HALT) |
| `SET_FEATURE` | `0x03` | Host→Device | Required (DEVICE_REMOTE_WAKEUP, TEST_MODE) |
| `SET_ADDRESS` | `0x05` | Host→Device | Required during enumeration |
| `GET_DESCRIPTOR` | `0x06` | Device→Host | Required (device, config, string, hub class) |
| `SET_DESCRIPTOR` | `0x07` | Host→Device | Optional |
| `GET_CONFIGURATION` | `0x08` | Device→Host | Required |
| `SET_CONFIGURATION` | `0x09` | Host→Device | Required |
| `GET_INTERFACE` | `0x0A` | Device→Host | Required for multi-TT hubs (alternate settings) |
| `SET_INTERFACE` | `0x0B` | Host→Device | Required for multi-TT hubs |
| `SYNCH_FRAME` | `0x0C` | Device→Host | Not applicable to hubs (isochronous only) |

### `GET_STATUS` (standard, §9.4.5)

Returns 2 bytes of status for the specified recipient:

- **Device recipient** (`wIndex=0x0000`): bits 0=Self-Powered, 1=Remote-Wakeup-Enabled.
- **Interface recipient** (`wIndex=interface_number`): returns `0x0000` (reserved).
- **Endpoint recipient** (`wIndex=endpoint_address`): bit 0=Halt.

> Distinct from hub class `GET_STATUS` (which returns 4 bytes of `wPortStatus`/`wPortChange`).

### `GET_DESCRIPTOR` (standard, §9.4.3)

`wValue` encodes descriptor type in the high byte and descriptor index in the low byte:

| Descriptor Type | High byte of `wValue` | Notes |
|---|---|---|
| Device | `0x01` | Standard device descriptor |
| Configuration | `0x02` | Configuration + interface + endpoint |
| String | `0x03` | String descriptor at index |
| Interface | `0x04` | Not directly requested; returned in config set |
| Endpoint | `0x05` | Not directly requested |
| Device_Qualifier | `0x06` | HS only (describes FS behavior of HS device) |
| Other_Speed_Configuration | `0x07` | HS only |
| Hub (class-specific) | `0x29` | Hub class descriptor; requires class-type bmRequestType |

### `SET_ADDRESS` (standard, §9.4.6)

Assigns a USB bus address to the device:

- `wValue`: new device address (1–127).
- `wIndex`: `0x0000`.
- `wLength`: `0`.
- After this request, the device must respond at the new address on the next transaction.

### `SET_CONFIGURATION` / `GET_CONFIGURATION` (§9.4.7, §9.4.2)

`SET_CONFIGURATION(bConfigurationValue)` activates a device configuration:
- For hubs, `bConfigurationValue=1` (single configuration).
- After `SET_CONFIGURATION`, the status change interrupt endpoint becomes active.

### `SET_INTERFACE` / `GET_INTERFACE` (§9.4.9, §9.4.4)

Used by multi-TT hubs to select between single-TT (`bAlternateSetting=0`) and multi-TT (`bAlternateSetting=1`) operating modes. See `specs/en/hub_configuration.md`.

### Standard Feature Selectors (§9.4.1, §9.4.9)

Standard feature selectors used with `SET_FEATURE` / `CLEAR_FEATURE`:

| Selector | Value | Recipient | Description |
|---|---|---|---|
| `ENDPOINT_HALT` | `0x00` | Endpoint | Halt (stall) an endpoint |
| `DEVICE_REMOTE_WAKEUP` | `0x01` | Device | Enable remote wakeup |
| `TEST_MODE` | `0x02` | Device | Enter USB 2.0 electrical test mode |

> These are **standard** feature selectors and must not be confused with hub **class** feature selectors (`PORT_POWER`, `PORT_RESET`, etc.) used in hub class requests.

## Governed Linkage

- `specs/en/hub_class_requests.md`: hub class-specific requests (type=Class, `bmRequestType[6:5]=01`)
- `specs/en/standard_descriptors.md`: all standard USB descriptor field definitions
- `specs/en/hub_configuration.md`: hub interface alternate settings for multi-TT
- `specs/en/hub_enumeration.md`: enumeration sequence showing GET_DESCRIPTOR, SET_ADDRESS, SET_CONFIGURATION ordering
- `tables/standard_device_request_matrix.yaml`: machine-readable standard request entries

## Non-claims

- This page does not claim any standard request implementation has been verified against a physical hub.
- This page does not claim GET_STATUS (standard, 2 bytes) behavior is interchangeable with GET_STATUS (hub class, 4 bytes).
- This page does not claim TEST_MODE or ENDPOINT_HALT semantics have been correctness-verified for hubs.
- This page does not override confirmed project facts in consuming repos.

## Reference Navigation

- specs/en/usb2.md: USB 2.0 topic index (en).
- specs/standard_device_requests.md: 中文對應主題（中文頁）
