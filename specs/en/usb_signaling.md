---
title: USB Signaling and Bus States
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# USB Signaling and Bus States

> Source scope: USB 2.0 Specification Rev 2.0, §7.1.  
> This page is a reviewed reference summary for USB 2.0 electrical bus states, data encoding, and signaling events relevant to hub operation.

## Page Purpose

This page answers:

- What are the USB 2.0 bus signal states (J, K, SE0, SE1).
- How USB data is encoded (NRZI + bit stuffing).
- What bus events correspond to reset, suspend, and resume.

This page does not answer:

- High-speed chirp sequence for HS detection — that is in `specs/en/hs_detection.md`.
- Electrical specifications (voltage levels, impedance, ESD) — outside this repo's scope.

## USB D+ and D- Signal Pairs

USB uses a differential signal pair (D+ and D−):

| Bus State | D+ | D− | FS/HS Meaning | LS Meaning |
|---|---|---|---|---|
| **J** | High | Low | Idle (no activity) | Active (differential 1) |
| **K** | Low | High | Active (differential 1 / start of packet / resume) | Idle |
| **SE0** | Low | Low | Reset / End-of-Packet (EOP) | Reset / EOP |
| **SE1** | High | High | Illegal (not used in normal operation) | Illegal |

> LS (Low-Speed) devices invert J and K relative to FS/HS.

## NRZI Encoding

USB 2.0 uses **NRZI (Non-Return-to-Zero Inverted)** encoding:

| Data bit | Effect on signal |
|---|---|
| `0` | Signal **transitions** (J→K or K→J) |
| `1` | Signal **holds** (no transition) |

NRZI ensures the receiver can recover the clock from signal transitions.

## Bit Stuffing

After **6 consecutive `1` bits**, the transmitter inserts a `0` bit to force a signal transition (maintains clock synchronization). The receiver strips these inserted zeros.

Implication: the raw bitstream on the bus may be longer than the logical data due to stuffed zero bits.

## Packet Framing

Each USB packet begins with a SYNC pattern and ends with an EOP (End-of-Packet):

- **SYNC**: `00000001` (7 zeros + 1 one), establishes bit-clock alignment.
- **EOP**: SE0 for 2 bit times followed by J for 1 bit time.

## Bus Events and Signaling

### USB Reset

- Signaled by: SE0 (D+=0, D−=0) held for ≥10ms.
- Issued by: host (root hub) or hub (port reset via `SET_FEATURE(PORT_RESET)`).
- Device response: device resets to Default state (address 0), all configuration lost.

### Suspend

- Signaled by: J state (idle) held for >3ms.
- Effect: device enters Suspended state; device may reduce power.
- Note: hubs propagate suspend to downstream ports unless explicitly configured otherwise.

### Resume

- Signaled by: K state driven by the hub/host for 20ms (±1ms).
- Effect: downstream device returns to active operation.
- Remote wakeup: a suspended downstream device may initiate resume by driving K state for 1–15ms.

### SOF (Start of Frame)

- Sent by host every 1ms (FS) or 125µs (HS) micro-frame.
- Keeps devices from entering suspend during active operation.
- Hubs regenerate SOF for downstream FS/LS segments.

## FS vs. HS Bus Signaling

| Aspect | Full-Speed (FS) | High-Speed (HS) |
|---|---|---|
| Bit rate | 12 Mbps | 480 Mbps |
| Idle state | J (D+=High, D−=Low) | HS idle (both terminations active) |
| Reset detection | SE0 ≥10ms | SE0 ≥10ms + chirp sequence |
| SOF interval | 1ms | 125µs micro-frame |

HS devices and hubs negotiate speed during reset via the chirp sequence. See `specs/en/hs_detection.md`.

## Governed Linkage

- `specs/en/hs_detection.md`: high-speed chirp negotiation sequence during port reset
- `specs/en/port_state_machine.md`: port reset timing (10ms minimum SE0 assertion)
- `specs/en/hub_power_management.md`: suspend/resume from hub perspective
- `specs/en/hub_enumeration.md`: reset signaling during port enumeration

## Non-claims

- This page does not claim USB electrical specifications (voltage thresholds, impedance) have been verified.
- This page does not claim NRZI or bit-stuffing implementation has been verified.
- This page does not define complete USB 2.0 protocol layer behavior.
- This page does not override confirmed project facts in consuming repos.
