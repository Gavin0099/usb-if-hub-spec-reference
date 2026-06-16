---
title: Feature Selectors
claim_level: inferred
status: review_required
last_reviewed: "2026-06-05"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Feature Selectors

> Source scope: USB 2.0 Specification Rev 2.0, Section 11.24.2.  
> This page is a reference summary for the `SET_FEATURE` / `CLEAR_FEATURE` selector namespace, not a complete control truth table and not a section-level PDF verification record.

## Page Purpose

This page answers:

- Which USB 2.0 feature selectors exist in the hub request space.
- Which selectors belong to the hub recipient vs. the port recipient.
- Why `0-22` is the E-05 standard port selector boundary.
- Which selectors mainly appear in `SET_FEATURE`, `CLEAR_FEATURE`, or `GET_STATUS` interpretation contexts.

This page does not answer:

- Whether every selector already has PDF section-level verification.
- Whether every selector side effect has correctness verification.
- The full state-transition model for `SET_FEATURE` / `CLEAR_FEATURE`.

## Boundary Before Reading

- Hub selectors and port selectors may share numeric values, but they use different recipients and must not be merged.
- E-05 is specifically about **vendor command selectors not overlapping the standard port selector range `0-22`**.
- Some matrix entries are present as `GET_STATUS` context and should not be read as directly settable feature targets.

## Namespace Summary

| Namespace | Range | Recipient | Meaning |
|---|---:|---|---|
| Hub change selectors | `0-1` | device | Used by hub-recipient `CLEAR_FEATURE` |
| Port standard selectors | `0-22` | other | E-05 standard boundary; vendor selectors must not overlap |

## Hub Selectors

The current matrix includes these hub selectors:

| Value | Name | Main Use |
|---:|---|---|
| `0` | `C_HUB_LOCAL_POWER` | Clears the hub local power change condition |
| `1` | `C_HUB_OVER_CURRENT` | Clears the hub over-current change condition |

These selectors:

- must be interpreted with hub recipient only
- primarily belong to the `CLEAR_FEATURE` family
- must not be merged into the port selector namespace

The current repo-local reviewed linkage surface includes:

- `PORT_CONNECTION` <-> `wPortStatus bit 0` as `GET_STATUS` context only
- `PORT_OVER_CURRENT` <-> `wPortStatus bit 3` as `GET_STATUS` context only
- `PORT_LOW_SPEED` <-> speed indication in `wPortStatus` as `GET_STATUS` context only
- `PORT_HIGH_SPEED` <-> speed indication in `wPortStatus` as `GET_STATUS` context only
- reserved port selector slots `5-7` and `11-15` as reserved-boundary surface only
- `C_HUB_LOCAL_POWER` <-> `wHubChange bit 0`
- `C_HUB_OVER_CURRENT` <-> `wHubChange bit 1`
- `C_PORT_CONNECTION` <-> `wPortChange` change selector (event-record bit 0)
- `C_PORT_ENABLE` <-> `wPortChange` change selector (event-record bit 1)
- `C_PORT_SUSPEND` <-> `wPortChange` change selector (event-record bit 2)
- `C_PORT_OVER_CURRENT` <-> `wPortChange` change selector (event-record bit 3)
- `C_PORT_RESET` <-> `wPortChange` change selector (event-record bit 4)
- `PORT_ENABLE` <-> standard port enable feature selector boundary
- `PORT_SUSPEND` <-> standard port suspend feature selector boundary
- `PORT_RESET` <-> standard port reset feature selector boundary
- `PORT_POWER` <-> standard port power feature selector boundary
- `PORT_TEST` <-> standard port test feature selector boundary
- `PORT_INDICATOR` <-> standard port indicator feature selector boundary

This means the selector namespace boundary has been reviewed as a boundary-only reference surface.
It does **not** mean host-side sequencing, selector side effects, or broader request behavior is verified.
For the `PORT_CONNECTION`, `PORT_OVER_CURRENT`, `PORT_LOW_SPEED`, and `PORT_HIGH_SPEED` rows, the reviewed surface is context-only `GET_STATUS` linkage; it does not make them direct `SET_FEATURE` / `CLEAR_FEATURE` targets.
For the reserved rows, the reviewed surface only means those numeric slots remain inside the standard port selector boundary; it does not make them usable selectors or vendor-extension slots.
For `PORT_TEST` and `PORT_INDICATOR`, the reviewed surface is selector-boundary only; it does not verify test-mode behavior, indicator policy, or hardware support.

## `PORT_*` / `C_PORT_*` behavior boundary (selector layer)

- `PORT_CONNECTION`
  - The selector value maps to the port connection concept only; full host connect/disconnect transition semantics are not claimed.
- `PORT_ENABLE`, `PORT_SUSPEND`, `PORT_RESET`, `PORT_POWER`
  - These selectors are in the standard namespace; the complete `SET_FEATURE` / `CLEAR_FEATURE` transition effects are not fully verified here.
- `PORT_OVER_CURRENT`
  - `PORT_OVER_CURRENT` is reported in status context; `C_PORT_OVER_CURRENT` is the associated change-selector event-acknowledge path, and this page does not extend to recovery policy or timing truth.
- `C_PORT_CONNECTION`, `C_PORT_ENABLE`, `C_PORT_SUSPEND`, `C_PORT_OVER_CURRENT`, `C_PORT_RESET`
  - These are treated as change selectors over `wPortChange`.
  - The page records the event-record / clear-acknowledgment role instead of timing or control-state-machine truth.
- `PORT_TEST`, `PORT_INDICATOR`
  - This slice only keeps selector boundary currently; it does not advance to test-mode or indicator behavior verification.

In practice, `PORT_*` / `C_PORT_*` here aligns with status/change classification in `specs/port_status_bits.md`:

- `PORT_*`: role mapping to `wPortStatus` state fields
- `C_PORT_*`: role mapping to `wPortChange` change/event fields

## Port Standard Selector Boundary (`0-22`)

`tables/feature_selector_matrix.yaml` currently captures the standard port selector boundary `0-22`.  
This is the core E-05 boundary: **vendor-defined selectors must not overlap this range**.

Representative selectors:

| Value | Name | Common Context |
|---:|---|---|
| `0` | `PORT_CONNECTION` | `GET_STATUS` context |
| `1` | `PORT_ENABLE` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `2` | `PORT_SUSPEND` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `3` | `PORT_OVER_CURRENT` | `GET_STATUS` context |
| `4` | `PORT_RESET` | `SET_FEATURE` |
| `5-7` | reserved | reserved standard-range slots |
| `8` | `PORT_POWER` | `SET_FEATURE` / `CLEAR_FEATURE` / `GET_STATUS` |
| `9` | `PORT_LOW_SPEED` | `GET_STATUS` context |
| `10` | `PORT_HIGH_SPEED` | `GET_STATUS` context |
| `11-15` | reserved | reserved standard-range slots |
| `16` | `C_PORT_CONNECTION` | `CLEAR_FEATURE` change selector |
| `17` | `C_PORT_ENABLE` | `CLEAR_FEATURE` change selector |
| `18` | `C_PORT_SUSPEND` | `CLEAR_FEATURE` change selector |
| `19` | `C_PORT_OVER_CURRENT` | `CLEAR_FEATURE` change selector |
| `20` | `C_PORT_RESET` | `CLEAR_FEATURE` change selector |
| `21` | `PORT_TEST` | `SET_FEATURE` |
| `22` | `PORT_INDICATOR` | `SET_FEATURE` |

## Defined / Reserved / Context-Only

This repo currently treats selectors in three reading categories:

- **defined selector**: the name and role are explicitly listed in the matrix
- **reserved selector**: still part of the standard range and must not be repurposed as a standard selector
- **context-only selector**: included to complete the namespace or `GET_STATUS` comparison surface, not to claim it is always a direct feature target

## Relationship to Request Families

- `SET_FEATURE` / `CLEAR_FEATURE` `wValue` should link back to `tables/feature_selector_matrix.yaml`.
- `GET_STATUS` does not directly "set a selector", but `PORT_CONNECTION`, `PORT_OVER_CURRENT`, `PORT_LOW_SPEED`, and `PORT_HIGH_SPEED` now have reviewed context-only linkage to the status-field comparison surface.
- `C_PORT_*` selectors should be read together with `change bits` in `specs/port_status_bits.md`.
- Reviewed `PORT_*`, `C_HUB_*`, and `C_PORT_*` linkage should still be treated as selector boundary only, not as behavioral proof for `SET_FEATURE` or `CLEAR_FEATURE`.
- `PORT_TEST` and `PORT_INDICATOR` remain outside behavior verification even though their selector slots are now reviewed.

## `PORT_TEST` Test Mode Selector Encoding (`wIndex` high byte)

> Source: §11.24.2.13 / Table 11-20. Reviewed boundary only; not test-mode electrical or compliance verification.

When `SET_FEATURE(PORT_TEST)` is issued, the test mode is specified in `wIndex[15:8]`:

| `wIndex[15:8]` | Name | Notes |
|---:|---|---|
| `0x00` | Reserved | |
| `0x01` | Test_J | J-state static test |
| `0x02` | Test_K | K-state static test |
| `0x03` | Test_SE0_NAK | SE0 NAK test |
| `0x04` | Test_Packet | Test packet transmission |
| `0x05` | Test_Force_Enable | Force port enable |
| `0x06–0xFF` | Reserved | |

This table records selector-encoding identity only. It does not verify test-mode electrical behavior, compliance test procedures, or device response.

## `PORT_INDICATOR` Indicator Color Encoding (`wIndex` high byte)

> Source: §11.24.2.7.1.1 / Table 11-20. Reviewed boundary only; not indicator hardware or policy verification.

When `SET_FEATURE(PORT_INDICATOR)` is issued, the indicator color is specified in `wIndex[15:8]`:

| `wIndex[15:8]` | Color | Notes |
|---:|---|---|
| `0x00` | Off | Indicator off |
| `0x01` | Amber | Amber indicator |
| `0x02` | Green | Green indicator |
| `0x03` | Undefined | Software-controlled; meaning not defined by USB 2.0 standard |

This table records encoding identity only. It does not verify indicator hardware support, policy, or whether the hub actually implements indicator control.

## Governed Linkage

- `tables/feature_selector_matrix.yaml`: primary machine-readable source for selector namespaces.
- `specs/hub_class_requests.md`: request-family summary for `SET_FEATURE` / `CLEAR_FEATURE`.
- `specs/port_status_bits.md`: relationship between `GET_STATUS`, change bits, and `CLEAR_FEATURE`.
- `specs/port_feature_change_vocabulary.md`: PORT_/C_PORT_* vocabulary alignment between selector and status/change pages.
- `specs/escalation_table.md`: E-05 escalation trigger.

## Non-claims

- This page does not claim value-by-value PDF section-level verification for selector `0-22`.
- This page does not claim correctness verification for all selector side effects.
- This page does not claim request success/failure, timing, or recovery semantics for `SET_FEATURE` / `CLEAR_FEATURE`.
- This page does not upgrade selector summaries into firmware implementation authority.
- This page does not override confirmed project facts in consuming repos.
