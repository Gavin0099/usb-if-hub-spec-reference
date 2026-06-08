---
title: Standard Escalation Trigger Table
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

# Standard Escalation Trigger Table

> **Usage:** This table is for consuming firmware repositories.
> When any trigger condition is met, Standard Escalation Mode defined by the consuming repo must be activated.

## USB 2.0 Trigger Conditions

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

## SS (USB 3.x) Trigger Conditions

The following conditions apply to SuperSpeed hubs and are independent of USB 2.0 triggers E-01 through E-10.

| # | Condition | Spec Reference | Escalation Required |
|---|---|---|---|
| SE-01 | Firmware `bDeviceProtocol` is `0x01` or `0x02` (TT types) but device claims to be an SS hub | USB 3.2 §10.14 / Device Descriptor | Yes |
| SE-02 | SS hub does not implement `GET_DESCRIPTOR(0x2A)` (SS Hub Descriptor) | USB 3.2 §10.14.2 | Yes |
| SE-03 | `SET_HUB_DEPTH` is not sent after `SET_CONFIGURATION` for an SS hub | USB 3.2 §10.14.1 | Yes |
| SE-04 | Firmware decoding of SS port status bits `wPortStatus[8:5]` (PORT_LINK_STATE) does not match the spec encoding table | USB 3.2 §10.14.2.1 | Yes |
| SE-05 | SS feature selector values (PORT_U1_ENABLE=17, PORT_U2_ENABLE=18, PORT_U1_TIMEOUT=23, PORT_U2_TIMEOUT=24, PORT_REMOTE_WAKE_MASK=27, BH_PORT_RESET=28) do not match firmware's actual selector assignments | USB 3.2 §10.14.1 Table | Yes |

## Escalation Scope Boundary

This table defines a minimum standard-side escalation boundary.  
Even when these conditions are not met, consuming projects may still introduce additional triggers based on confirmed project facts, architecture decisions, or safety governance requirements.

The purpose of this page is to separate what should enter the consuming repo's escalation flow from what should remain documentation-only usage.

## Non-Escalation Cases

The following reference usage does not by itself require escalation:

- Using `specs/port_status_bits.md` to clarify port status bit semantics
- Using `specs/hub_class_requests.md` as a field-encoding reference
- Using `specs/hub_descriptor.md` to confirm the `GET_DESCRIPTOR` response format

## Governed Linkage

**USB 2.0 (E-01 through E-10):**
- `tables/escalation_trigger_matrix.yaml`: governed trigger-boundary surface for E-01 through E-10.
- `tables/hub_descriptor_matrix.yaml`: descriptor fields involved in E-01, E-07, and E-08.
- `tables/port_status_bit_matrix.yaml`: port status bits involved in E-02, E-03, and E-09.
- `tables/feature_selector_matrix.yaml`: selector namespace involved in E-05.
- `tables/transaction_translator_matrix.yaml`: TT applicability and request surfaces involved in E-06, E-07, and E-10.

**USB 3.x (SE-01 through SE-05):**
- `tables/ss_hub_descriptor_matrix.yaml`: descriptor fields for SE-01, SE-02 (bDeviceProtocol, Descriptor type 0x2A).
- `tables/ss_hub_class_request_matrix.yaml`: SE-03 (SET_HUB_DEPTH mandatory requirement).
- `tables/ss_port_status_bit_matrix.yaml`: SE-04 (PORT_LINK_STATE bits[8:5]).
- `tables/ss_feature_selector_matrix.yaml`: SE-05 (6 SS-only feature selectors).

The governed trigger table is a standard-side reference boundary only. It does not execute escalation, resolve consuming-repo project facts, or authorize firmware behavior changes.

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
