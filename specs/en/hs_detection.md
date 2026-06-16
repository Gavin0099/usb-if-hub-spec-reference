---
title: High-Speed Detection
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# High-Speed Detection

> Source scope: USB 2.0 Specification Rev 2.0, §7.1.7.1.  
> This page is a reviewed reference summary for the USB 2.0 high-speed (HS) device detection mechanism via the chirp handshake sequence during port reset.

## Page Purpose

This page answers:

- How a USB 2.0 hub detects whether a newly connected device is HS-capable.
- What the chirp K/J sequence is and how it works.
- What the hub does for HS vs. FS/LS devices after reset.

This page does not answer:

- FS and LS signal state definitions — those are in `specs/en/usb_signaling.md`.
- Port state machine transitions after reset — those are in `specs/en/port_state_machine.md`.

## HS Detection Overview

When a device connects to an HS-capable hub, both the hub and device negotiate speed during the bus reset sequence. The negotiation uses a **chirp handshake** — a specific pattern of short K/J pulses — to confirm both sides support HS.

If either side does not support HS (or does not respond to the chirp), the device operates at FS or LS.

## Chirp Handshake Sequence

### Step 1: Hub Asserts Reset (SE0)

The hub asserts SE0 (D+=0, D−=0) on the port for ≥10ms. This is the standard USB bus reset signal.

### Step 2: Device Responds with Chirp K

Within 2.5ms of detecting the SE0 reset assertion, an **HS-capable device** drives a **Chirp K** (a brief K state) for approximately 1–7ms. This signals to the hub that the device is HS-capable.

- FS/LS devices do not drive Chirp K → hub continues with FS/LS mode.

### Step 3: Hub Detects Chirp K and Responds

An **HS-capable hub** that detects the device Chirp K responds with an alternating sequence of KJ pulses:

```
Hub response: K J K J K J  (3 KJ pairs, ~100µs each)
```

This confirms to the device that the hub supports HS.

### Step 4: Device Confirms HS Mode

The device detects the hub's KJ chirp sequence and switches to HS mode. The device is now enumerated as an HS device.

### Step 5: HS Bus Idle

After the chirp exchange, both hub and device switch to HS bus signaling (480 Mbps). The hub ends SE0, and normal HS communication begins.

## Outcome Matrix

| Device HS-capable | Hub HS-capable | Device Chirp K | Hub KJ Response | Result |
|---|---|---|---|---|
| Yes | Yes | ✓ (sent) | ✓ (sent) | **HS operation** |
| Yes | No (FS hub) | ✓ (sent) | ✗ (not sent) | **FS fallback** (device sees no response) |
| No (FS device) | Yes | ✗ (not sent) | N/A | **FS operation** |
| No (LS device) | Yes/No | ✗ (not sent) | N/A | **LS operation** |

After the reset sequence, the host confirms speed via `GET_STATUS(port)` and checks `PORT_LOW_SPEED` and `PORT_HIGH_SPEED` bits.

## Timing Reference

| Event | Timing |
|---|---|
| Hub SE0 assertion | ≥10ms |
| Device Chirp K onset after SE0 | ≤2.5ms |
| Device Chirp K duration | 1–7ms |
| Hub KJ response (each K or J) | ~100µs |
| Hub KJ pairs | 3 pairs (6 transitions) |

## HS vs. FS Hub Behavior

| Hub type | `bDeviceProtocol` | Chirp detection | Chirp response |
|---|---|---|---|
| FS hub (no TT) | `0x00` | No | No |
| HS hub, single TT | `0x01` | Yes | Yes |
| HS hub, multi TT | `0x02` | Yes | Yes |

Only HS hubs (`bDeviceProtocol=0x01` or `0x02`) participate in chirp detection. An FS device connected to an HS hub will operate at FS (via TT if needed).

## Governed Linkage

- `specs/en/usb_signaling.md`: J/K/SE0 bus states and reset signaling
- `specs/en/port_state_machine.md`: port reset timing and speed bits after reset
- `specs/en/hub_device_class.md`: `bDeviceProtocol` values indicating hub speed and TT type
- `specs/en/transaction_translator.md`: TT operation for FS/LS devices on HS hub ports

## Non-claims

- This page does not claim the chirp handshake sequence has been verified against a physical hub or device.
- This page does not specify all electrical timing tolerances for the chirp sequence.
- This page does not override confirmed project facts in consuming repos.

## Reference Navigation

- specs/en/usb2.md: USB 2.0 topic index (en).
- specs/hs_detection.md: 中文對應主題（中文頁）
