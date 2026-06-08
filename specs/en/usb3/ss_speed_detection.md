---
title: SS Speed Detection
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

# SS Speed Detection

> Scope: USB 3.2 Specification Rev 1.0, §6 (Physical Layer); USB 2.0 Specification, §7.1 (Electrical).
> This page summarizes SuperSpeed speed detection mechanisms at reference level, covering LFPS and TSEQ roles and a contrast with USB 2.0 HS Chirp.
> This page does not claim LTSSM behavior verified, PHY electrical specs verified, or firmware compliance.

## Purpose

This page answers:

- The key USB 3.x SuperSpeed speed detection mechanisms (LFPS, TSEQ) at reference level.
- How SS speed detection differs from USB 2.0 HS Chirp.

This page does not answer:

- Full LTSSM (Link Training and Status State Machine) state machine behavior.
- PHY electrical specifications or SS eye diagram requirements.
- How xHCI manages link training sequences.
- USB-IF electrical or interoperability compliance testing.

## USB 2.0 HS Speed Detection (Background Contrast)

USB 2.0 High-Speed detection uses the **Chirp** sequence (performed during USB reset):

| Step | Description |
|---|---|
| Chirp K | Device drives Chirp K on D+/D- differential pair after reset |
| Chirp K/J sequence | Host responds with Chirp K/J/K/J/K/J to confirm HS capability |
| HS mode confirmed | Both sides enter High-Speed mode (480 Mbps) |
| Fallback | If Chirp exchange does not complete, device falls back to Full-Speed (12 Mbps) |

USB 2.0 Chirp uses D+/D- (the USB 2.0 differential pair); no separate SS physical layer is required.

## USB 3.x SS Speed Detection

USB 3.x SuperSpeed uses a separate SS differential pair (TX+/TX-/RX+/RX-); speed detection does not use Chirp:

### LFPS (Low-Frequency Periodic Signaling)

LFPS is a low-frequency pulse signal used when an SS link is establishing, transitioning power states, or waking:

| Feature | Description |
|---|---|
| Frequency | 10–50 MHz (much lower than SS 5 Gbps data signal) |
| Primary use | Link state detection (Polling phase); U1/U2/U3 → U0 wake trigger |
| Physical medium | SS differential pair (TX+/TX-); does not use USB 2.0 D+/D- |
| Runtime scope | LFPS runtime timing and LTSSM state transitions are outside this page's verified scope |

LFPS is the fundamental signal mechanism for SS link training initiation and power management — functionally corresponding to USB 2.0 Chirp, but on a separate physical medium.

### TSEQ (Training Sequence EQ)

TSEQ is the equalization training sequence sent during SS link training:

| Feature | Description |
|---|---|
| Format | Repeated TSEQ ordered sets (sent during LTSSM Polling.RxEQ state) |
| Purpose | Receiver equalizer training; helps receiver acquire optimal sampling point |
| Training flow overview | LFPS → TSEQ → TS1 → TS2 → U0 (link training complete) |
| Runtime scope | Full LTSSM training flow is outside this page's verified scope |

TSEQ electrical parameters and detailed timing are outside this page's verified scope.

## SS vs USB 2.0 HS Speed Detection Comparison

| Feature | USB 2.0 HS | USB 3.x SS |
|---|---|---|
| Detection mechanism | Chirp K / Chirp K+J exchange | LFPS + TSEQ (link training sequence) |
| Physical medium | D+/D- (USB 2.0 differential pair) | TX+/TX-/RX+/RX- (SS differential pair, separate) |
| Negotiation method | Differential drive + J/K voltage patterns | LTSSM Polling.LFPS → Polling.RxEQ → U0 |
| Fallback | Chirp incomplete → Full-Speed (12 Mbps) | SS link training incomplete → SS link not established |
| Hub role | TT speed bridging (HS upstream / FS/LS downstream) | No speed bridging; hub routing handles SS only |
| LTSSM | Not applicable | LTSSM governs link state; behavior outside this page's verified scope |

## Non-claims

- This page does not claim LTSSM state machine behavior has been verified.
- This page does not claim LFPS runtime timing has been verified.
- This page does not claim TSEQ electrical parameters have been verified.
- This page does not claim xHCI link training behavior has been verified.
- This page does not claim USB-IF electrical compliance test results.
- This page does not claim the full SS link training sequence has been implementation-verified.
- This page does not override confirmed project facts in consuming repos.

→ [SS Signaling](ss_signaling.md) | [SS LPM](ss_lpm.md) | [SS No Transaction Translator](ss_no_transaction_translator.md) | [Verification Status](../verification_status.md)
