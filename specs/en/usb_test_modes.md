---
title: USB Test Modes
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# USB Test Modes

> Source scope: USB 2.0 Specification Rev 2.0, §7.1.20 and §9.4.9.  
> This page is a reviewed reference summary for USB 2.0 high-speed test modes. Test modes are required for HS electrical compliance testing and are entered via a standard `SET_FEATURE(TEST_MODE)` request.

## Page Purpose

This page answers:

- What USB 2.0 test modes exist and what each does.
- How a host enters a test mode on a hub or downstream device.
- How to exit a test mode.

## Overview

USB 2.0 defines five **Test Mode** selectors for HS electrical compliance. Test modes cause the device or hub to transmit a specific fixed signal pattern on the bus. They are used with USB 2.0 compliance test equipment and should not be entered in normal operation.

Test modes apply to **HS-capable devices and hubs** only (`bDeviceProtocol = 0x01` or `0x02`).

## Test Mode Feature Selectors

Entered via `SET_FEATURE(TEST_MODE)` with `wIndex[15:8]` = test mode number:

| Test Mode | `wIndex[15:8]` | Signal Pattern | Purpose |
|---|---|---|---|
| `TEST_J` | `0x01` | Continuous J state | Tests differential `1` signal level |
| `TEST_K` | `0x02` | Continuous K state | Tests differential `0` signal level |
| `TEST_SE0_NAK` | `0x03` | SE0 (NAK response to IN tokens) | Tests single-ended zero and quiescent levels |
| `TEST_PACKET` | `0x04` | Specific test data packet (repeated) | Tests signal quality across full data pattern |
| `TEST_FORCE_ENABLE` | `0x05` | Normal HS signaling enabled | Forces HS upstream port enable |

`wIndex[7:0]` = `0x00` (reserved).

## `SET_FEATURE(TEST_MODE)` Request

```
bmRequestType: 0x00  (Host→Device, Standard, Device recipient)
bRequest:      0x03  (SET_FEATURE)
wValue:        0x0002  (TEST_MODE feature selector)
wIndex:        [test_mode_number << 8]  (test mode in high byte)
wLength:       0
```

The device must enter the test mode after the status stage of the `SET_FEATURE` request completes.

## Test Mode Entry Rules

- Only a device in the `Address` or `Configured` state may receive `SET_FEATURE(TEST_MODE)`.
- Once entered, the device transmits the specified pattern and **does not respond to any further USB traffic**.
- The host must not issue any additional requests after the `SET_FEATURE` status stage.

## Exiting Test Mode

**Test modes can only be exited by:**
- A hardware power cycle (VBUS removed and reapplied), or
- A hardware reset (physical reset button, if present).

Software reset (`SET_FEATURE(PORT_RESET)`) or USB bus reset are **not** sufficient to exit test mode.

## Hub Port Test Mode (`wIndex[7:0]` = port number)

For hub upstream port tests, `wIndex[7:0] = 0x00`.  
For hub downstream port tests, `wIndex[7:0]` = the port number (1-based).

This allows the host to put a specific downstream port into test mode independently.

## `TEST_PACKET` Data

`TEST_PACKET` mode transmits a specific 53-byte packet repeatedly. The packet is defined in USB 2.0 §7.1.20 and contains a mix of data patterns designed to stress signal integrity across all bit combinations.

## Hub Role in Test Mode

- `TEST_FORCE_ENABLE` on a hub causes the hub to enable its upstream-facing HS port regardless of normal enumeration state.
- When a downstream port is placed in test mode, the hub propagates the test signal to that port only.
- The hub's TT does not participate in downstream port test modes.

## Governed Linkage

- `specs/en/standard_device_requests.md`: `SET_FEATURE` standard request encoding
- `specs/en/hs_detection.md`: HS-capable hub identification (`bDeviceProtocol`)
- `specs/en/usb_signaling.md`: J/K/SE0 bus states referenced by test mode signal patterns
- `specs/en/hub_device_class.md`: `bDeviceProtocol` values identifying HS hubs

## Non-claims

- This page does not claim test mode signal levels or patterns have been verified against test equipment.
- This page does not specify USB 2.0 compliance test procedures.
- This page does not claim the 53-byte TEST_PACKET content has been reproduced here.
- This page does not override confirmed project facts in consuming repos.
