---
title: Glossary
claim_level: inferred
status: review_required
last_reviewed: "2026-06-02"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
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

## Boundary Reminder

- This page standardizes wording only; it does not establish new spec truth.
- This page does not elevate terminology choices into verified authority.
- If a consuming repo finds a conflict between project facts and this repo's terminology summary, Standard Escalation Mode still applies.
