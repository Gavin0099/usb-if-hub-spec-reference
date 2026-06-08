---
title: Glossary
claim_level: inferred
status: review_required
last_reviewed: "2026-06-08"
usb_versions:
  - usb_2_0
  - usb_3_2
source_refs:
  - usb20_spec
  - usb32_spec
semantic_verification_claimed: false
---

# Glossary

> This page standardizes terminology for this repo to reduce document and LLM drift. It does not add new USB 2.0 section-level verification.

## Usage Rules

- Keep spec field names, request names, and bit names in original form: for example `GET_STATUS`, `CLEAR_FEATURE`, `wHubCharacteristics`, `PORT_CONNECTION`.
- On first mention, bilingual wording is acceptable; after that, keep one stable term.
- If translation reduces technical precision, keep the original English term.

## Core Terms

| Preferred Term | Notes |
|---|---|
| Hub Class Requests | Used for request-family pages such as `specs/hub_class_requests.md`. |
| Hub Descriptor | Used for the class-specific hub descriptor. |
| Port Status Bits | Used for `wPortStatus` / `wPortChange` summary pages. |
| Escalation Table | Used for Standard Escalation Mode trigger summaries. |
| Glossary | Used for repo-level terminology normalization. |

## Terms Kept in English

| Preferred Term | Reason |
|---|---|
| Transaction Translator (TT) | This is a stable USB hub term; translating it often reduces recognizability. |
| TT Think Time | This is treated as an established field/group name. |
| Port Indicator | The field name is clearer if kept in English; local explanation can be added in prose. |

## Request and Field Terms

| Preferred Term | Notes |
|---|---|
| Feature Selector | Prose may translate it locally, but field identifiers remain `feature_selector`. |
| Descriptor Type | Safe as prose; request names and literal values remain unchanged. |
| Change Bit | Refers to latched event bits in `wPortChange` / `wHubChange`. |
| Reserved Bit | Refers to spec-reserved bits that must not be casually repurposed. |
| Device-to-Host | Safe for `bmRequestType` direction summaries. |
| Host-to-Device | Safe for `bmRequestType` direction summaries. |

## Speed Terms

| Preferred Term | Notes |
|---|---|
| Low-speed | Safe direct usage. |
| Full-speed | Safe direct usage. |
| High-speed | Safe direct usage. |
| Combined speed decoding | Used for the joint interpretation of `PORT_LOW_SPEED` and `PORT_HIGH_SPEED`. |

## Descriptor Terms

| Preferred Term | Notes |
|---|---|
| downstream port count | Used when describing `bNbrPorts`. |
| removable bitmap | High-level summary for `DeviceRemovable`. |
| Power Switching Mode | Safe descriptor prose. |
| Over-current Protection Mode | Safe descriptor prose. |

## USB 3.x / SuperSpeed Terms

| Preferred Term | Notes |
|---|---|
| SS / SuperSpeed | USB 3.x speed tier: Gen 1 5 Gbps or Gen 2 10 Gbps SuperSpeed mode. |
| SSP / SuperSpeed Plus | USB 3.2 Gen 2 10 Gbps or Gen 2×2 20 Gbps; the higher-speed variant of USB 3.1/3.2. |
| BOS (Binary Device Object Store) | Required USB 3.x descriptor (type 0x0F); retrieved via GET_DESCRIPTOR(BOS); contains Device Capability Descriptor. |
| LPM (Link Power Management) | SS link power management: U1/U2 auto-transitions (short/longer idle) and U3 Suspend. |
| U0 / U1 / U2 / U3 | SS link power states: U0 = Active, U1 = Idle (short exit latency), U2 = Idle (longer exit latency), U3 = Suspend. |
| LFPS (Low-Frequency Periodic Signaling) | Low-frequency pulse mechanism for SS link power state transitions and wake; governed by LTSSM; runtime timing outside this repo's verified scope. |
| TSEQ (Training Sequence EQ) | Equalization training ordered set sent during SS link training (LTSSM Polling.RxEQ); detailed timing outside this repo's verified scope. |
| ITP (Isochronous Timestamp Packet) | SS isochronous synchronization timestamp packet; replaces USB 2.0 SOF (Start of Frame). |
| NRDY / ERDY | SS endpoint flow control packets: NRDY = endpoint Not Ready; ERDY = endpoint proactively signals Endpoint Ready. |
| SET_HUB_DEPTH | SS-only hub request; mandatory after SET_CONFIGURATION; sets the hub's depth in the SS routing tree. |

## Boundary Reminder

- This page standardizes wording only; it does not establish new spec truth.
- This page does not elevate terminology choices into verified authority.
- If a consuming repo finds a conflict between project facts and this repo's terminology summary, Standard Escalation Mode still applies.
