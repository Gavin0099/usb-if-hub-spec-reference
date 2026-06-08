---
title: SS Signaling
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

# SS Signaling

> Scope: USB 3.2 Specification Rev 1.0, Sections 6–7 (Physical Layer / Link Layer).
> This page is a consumer reference summary, not an electrical/signaling verification record.
> **Important**: This page does not claim any electrical compliance or LTSSM behavior.

## Purpose

This page answers:

- A summary of the main USB 3.x SuperSpeed signaling characteristics (physical layer).
- Speed differences between Gen 1 and Gen 2.
- The purpose of LFPS (Low Frequency Periodic Signaling).

This page does not answer:

- Electrical specification compliance (voltage, impedance, eye diagram).
- LTSSM signaling sequence runtime behavior.
- USB-IF signaling certification or test standards.

## USB 3.x SuperSpeed Physical Layer Overview

USB 3.x SuperSpeed uses **differential serial** signaling, distinct from USB 2.0's differential half-duplex:

| Feature | USB 2.0 High-Speed | USB 3.x SuperSpeed Gen 1 | USB 3.x SuperSpeed Gen 2 |
|---|---|---|---|
| Data rate | 480 Mbps | 5 Gbps | 10 Gbps |
| Encoding | NRZI | 8b/10b | 128b/132b |
| Direction | Half-duplex | **Full-duplex** (separate TX/RX) | Full-duplex |
| Physical layer | D+/D- (2 lines) | SS TX+/TX- + SS RX+/RX- (4 lines) | SS TX+/TX- + SS RX+/RX- |

Electrical specification values are outside this page's verified scope.

## LFPS (Low Frequency Periodic Signaling)

LFPS is a USB 3.x low-frequency periodic signal used for:

- **Rx.Detect**: Detecting receiver presence.
- **Polling.LFPS**: Initiating link training.
- **U1/U2 Exit**: Waking from low-power standby.
- **U3 Exit (Remote Wake)**: Initiating remote wake from Suspend.
- **Loopback / Compliance**: Test mode signaling.
- **Warm Reset**: BH reset uses LFPS sequence.

LFPS signal timing, electrical specifications, and LTSSM state correlations are outside this page's verified scope.

## Gen 1 / Gen 2 Differences

| Feature | SuperSpeed Gen 1 | SuperSpeedPlus Gen 2 |
|---|---|---|
| Data rate | 5 Gbps | 10 Gbps per lane |
| Encoding | 8b/10b | 128b/132b |
| Effective throughput | ~500 MB/s | ~1250 MB/s (per lane) |
| Multi-lane | 1x | 1x or 2x (Gen 2×2) |

Effective throughput figures are theoretical; actual performance is outside this page's verified scope.

## This Page Does Not Claim

- Electrical specification compliance (voltage, impedance, eye diagram).
- LFPS signal timing or LTSSM state machine behavior.
- USB-IF signaling or interoperability certification.
- Actual throughput or latency guarantees.
- Firmware or hardware signaling implementation correctness.

→ [SS Port State Machine](ss_port_state_machine.md) | [SS LPM](ss_lpm.md) | [Verification Status](../verification_status.md)
