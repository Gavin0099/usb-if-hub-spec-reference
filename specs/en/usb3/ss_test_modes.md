---
title: SS Test Modes
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

# SS Test Modes

> Scope: USB 3.2 Specification Rev 1.0, Section 10.14 (Hub Class Requests) and Sections 6–7 (Physical Layer).
> This page is a consumer reference summary, not a test mode behavior verification record.
> **Important**: This page does not claim any electrical compliance or USB-IF certification.

## Purpose

This page answers:

- An overview of which test modes USB 3.x SS hubs support.
- The purpose of Compliance Mode and Loopback.
- The `PORT_LINK_STATE` values corresponding to test modes.

This page does not answer:

- Electrical specifications or compliance test procedures for test modes.
- USB-IF certification test procedures.
- Firmware implementation of test mode entry and exit.

## USB 3.x SuperSpeed Test Modes Overview

USB 3.x SS hubs support several test modes, typically triggered via SET_FEATURE(PORT_LINK_STATE) or hub class request mechanisms (implementation-dependent).

### Compliance Mode (0xA)

- **Purpose**: Places the SS port in a fixed Compliance signaling mode for electrical interoperability testing (eye diagram, signal quality).
- **Corresponding PORT_LINK_STATE**: 0xA (Compliance Mode).
- Once triggered, the port continuously outputs the Compliance pattern; exit typically requires a reset.
- Electrical specifications and test standards are outside this page's verified scope.

### Loopback (0xB)

- **Purpose**: Places the SS port in loopback mode, retransmitting received data verbatim (used for PHY testing).
- **Corresponding PORT_LINK_STATE**: 0xB (Loopback).
- Loopback test behavior and trigger mechanisms are outside this page's verified scope.

## PORT_LINK_STATE and Test Mode Mapping

The following PORT_LINK_STATE values relate to test/diagnostic modes (encoding identity is verified):

| PORT_LINK_STATE value | Link state | Description |
|---|---|---|
| 0xA | Compliance Mode | Electrical compliance test mode |
| 0xB | Loopback | PHY loopback test mode |
| 0x7 | Polling | Link training/polling (not a test mode per se, but observable during testing) |

**Verified scope**: encoding identity only (bit range [8:5] and 12-value table). Test mode behavior is outside the verified scope.

## Differences from USB 2.0 Test Modes

| Feature | USB 2.0 | USB 3.x SuperSpeed |
|---|---|---|
| Test trigger | SET_FEATURE(PORT_TEST, wValue=test_mode) | PORT_LINK_STATE mechanism etc. |
| Test modes | Test_J, Test_K, Test_SE0_NAK, Test_Packet, Test_Force_Enable | Compliance Mode, Loopback |
| Signaling | D+/D- differential | SS TX+/TX- (differential serial) |

## This Page Does Not Claim

- Test mode electrical specifications or eye diagram standards.
- USB-IF Compliance test procedures or certification requirements.
- Firmware test mode entry/exit implementation correctness.
- Compliance pattern or loopback test behavior details.

→ [SS Signaling](ss_signaling.md) | [SS Port State Machine](ss_port_state_machine.md) | [Verification Status](../verification_status.md)
