---
title: Standard Escalation Trigger Table
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Standard Escalation Trigger Table

> **Usage:** This table is for consuming firmware repositories.
> When any trigger condition is met, Standard Escalation Mode defined by the consuming repo must be activated.

## Trigger Conditions

| # | Condition | Spec Reference | Escalation Required |
|---|---|---|---|
| E-01 | Firmware `bNbrPorts` does not match the hub descriptor field value | 11.23.2.1 offset 2 | Yes |
| E-02 | Port status bit 3 is used for a non-over-current purpose | 11.24.2.7.1 bit 3 | Yes |
| E-03 | Reserved port status bits `(7:5, 15:13)` are used by firmware | 11.24.2.7.1 | Yes |
| E-04 | Hub descriptor `GET_DESCRIPTOR` is not implemented | 11.24.2 | Yes |
| E-05 | A vendor command selector overlaps with the standard selector range `(0-22)` | 11.24.2 table | Yes |
| E-06 | TT behavior appears in a full-speed-only hub | 11.17-11.18 | Yes |
| E-07 | Descriptor TT Think Time does not match hardware timing | 11.23.2.1 `wHubCharacteristics[6:5]` | Yes |
| E-08 | Descriptor power switching mode does not match a confirmed project fact | 11.23.2.1 `wHubCharacteristics[1:0]` | Yes |
| E-09 | `PORT_HIGH_SPEED` is tested in a full-speed-only hub | 11.24.2.7.1 bit 10 | Yes |
| E-10 | A TT-capable hub requires `CLEAR_TT_BUFFER` / `RESET_TT` but does not implement them | 11.24.2 | Yes |

## Non-Escalation Cases

The following reference usage does not by itself require escalation:

- Using `specs/port_status_bits.md` to clarify port status bit semantics
- Using `specs/hub_class_requests.md` as a field-encoding reference
- Using `specs/hub_descriptor.md` to confirm the `GET_DESCRIPTOR` response format

## Escalation Output Format

When escalation is triggered, record the issue in the consuming repo:

```text
[Standard Conflict Detected]

Trigger: <E-NN from this table>

Standard says: <standard-based interpretation from this repo>

Project fact says: <confirmed project-specific behavior>

Classification: Project Implementation Constraint | Standards Compliance Risk | Documentation Error

Resolution: <chosen path>
```
