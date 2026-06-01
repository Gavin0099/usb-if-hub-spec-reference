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

> Usage: This table is for consuming firmware repositories.
> When any trigger condition is met, Standard Escalation Mode in the consuming repo's
> AGENTS.md Section 10 must be activated.

## Trigger Conditions

| # | Condition | Spec Reference | Escalation Required |
|---|-----------|---------------|-------------------|
| E-01 | Firmware bNbrPorts ≠ hub descriptor field value | 11.23.2.1 offset 2 | Yes |
| E-02 | Port status bit 3 used for non-OC purpose | 11.24.2.7.1 bit 3 | Yes |
| E-03 | Reserved port status bits (7:5, 15:13) used by firmware | 11.24.2.7.1 | Yes |
| E-04 | Hub descriptor GET_DESCRIPTOR not supported | 11.24.2 | Yes |
| E-05 | Vendor command selector overlaps with standard selector (0–22) | 11.24.2 table | Yes |
| E-06 | TT behavior present in full-speed-only hub | 11.17–11.18 | Yes |
| E-07 | TT Think Time in descriptor does not match hardware timing | 11.23.2.1 wHubCharacteristics[6:5] | Yes |
| E-08 | Power switching mode in descriptor ≠ confirmed project fact | 11.23.2.1 wHubCharacteristics[1:0] | Yes |
| E-09 | PORT_HIGH_SPEED bit tested in full-speed-only hub | 11.24.2.7.1 bit 10 | Yes |
| E-10 | Hub class request CLEAR_TT_BUFFER/RESET_TT required but not implemented in TT-capable hub | 11.24.2 | Yes |

## Non-Escalation Cases

Standard reference usage that does NOT require escalation:

- Using port status bit definitions from `specs/port_status_bits.md` to clarify semantics
- Using hub class request table from `specs/hub_class_requests.md` for field encoding reference
- Confirming GET_DESCRIPTOR response format from `specs/hub_descriptor.md`

## Escalation Output Format

When escalation is triggered, record in the consuming repo's `memory/03_decisions.md`:

```
[Standard Conflict Detected]

Trigger: <E-NN from this table>

Standard says: <standard-based interpretation from this repo>

Project fact says: <confirmed project-specific behavior>

Classification: Project Implementation Constraint | Standards Compliance Risk | Documentation Error

Resolution: <chosen path>
```
