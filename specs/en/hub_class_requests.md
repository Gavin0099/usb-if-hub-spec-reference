---
title: Hub Class Requests
claim_level: inferred
status: review_required
last_reviewed: "2026-06-05"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Class Requests

> Source scope: USB 2.0 Specification Rev 2.0, Section 11.24.2.
> This page is a request-family reference summary, not a complete setup-packet truth table and not a section-level PDF verification record.

## Page Purpose

This page answers:

- Which USB 2.0 hub class request families exist.
- The high-level direction, recipient, target, and setup-field meaning for each family.
- Which fields should link back to `class_request_matrix`, `feature_selector_matrix`, and `port_status_bit_matrix`.

This page does not answer:

- Whether every field in every request has already been verified at PDF section level.
- Whether TT request field encodings have already been correctness-verified.
- Whether `SET_FEATURE` / `CLEAR_FEATURE` already have a complete state-transition model in this repo.

## Request Family Overview

| bRequest | Value | Direction | Target | High-Level Role |
|---|---|---|---|---|
| `GET_STATUS` | `0x00` | Device-to-Host | Hub / Port | Reads hub or port status/change fields |
| `CLEAR_FEATURE` | `0x01` | Host-to-Device | Hub / Port | Clears a feature, or clears the event record represented by a change bit |
| `SET_FEATURE` | `0x03` | Host-to-Device | Hub / Port | Sets hub or port features |
| `GET_DESCRIPTOR` | `0x06` | Device-to-Host | Hub | Reads the hub class-specific descriptor |
| `SET_DESCRIPTOR` | `0x07` | Host-to-Device | Hub | Writes the hub class-specific descriptor; support is implementation-dependent |
| `CLEAR_TT_BUFFER` | `0x08` | Host-to-Device | TT-capable Hub | Clears TT buffer-related state |
| `RESET_TT` | `0x09` | Host-to-Device | TT-capable Hub | Resets the Transaction Translator |
| `GET_TT_STATE` | `0x0A` | Device-to-Host | TT-capable Hub | Reads TT diagnostic state |
| `STOP_TT` | `0x0B` | Host-to-Device | TT-capable Hub | Stops TT split-transaction processing |

## Boundary Conditions for Reading This Page

- `bmRequestType` is summarized here only at the direction / type / recipient level.
- If `wValue`, `wIndex`, or `wLength` still appear as abstract field-role names rather than fixed constants, this repo has narrowed the field role but has not upgraded the full encoding into verified truth.
- Port-recipient and hub-recipient requests must not be merged, and TT requests apply only to HS hubs with embedded TT.

## `GET_STATUS`

**Purpose**

- Reads hub or port status and change fields.

**Direction / recipient**

- Hub: Device-to-Host, class, device recipient.
- Port: Device-to-Host, class, other recipient.

**Target**

- The hub itself or a specific port.

**Setup-field summary**

- `bRequest`: `GET_STATUS`
- `wValue`: `0x0000`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `4`

**Governed linkage**

- Hub request maps to `wHubStatus` + `wHubChange`.
- Port request maps to `wPortStatus` + `wPortChange`.
- The current reviewed scope covers only this request-to-status-field linkage.
- The related context-only selector surface includes `PORT_CONNECTION`, `PORT_OVER_CURRENT`, `PORT_LOW_SPEED`, and `PORT_HIGH_SPEED` as `GET_STATUS` comparison anchors.

**Reviewed surface**

- This repo now narrows `GET_STATUS` to the hub/port status-field linkage surface.
- This still does not claim returned-bit behavior, host polling strategy, debounce behavior, or combined speed decoding correctness.

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- This page does not claim all returned bits have bit-level verification.
- This page does not define host-side polling or debounce behavior.

## `CLEAR_FEATURE`

**Purpose**

- Clears a hub or port feature.
- For change bits, it means the host has observed and acknowledged the event and is now clearing the event record.

**Direction / recipient**

- Hub: Host-to-Device, class, device recipient.
- Port: Host-to-Device, class, other recipient.

**Target**

- The hub itself or a specific port.

**Setup-field summary**

- `bRequest`: `CLEAR_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `0`

**Governed linkage**

- Hub and port selector spaces must be interpreted separately.
- Hub-recipient reviewed linkage currently includes `C_HUB_LOCAL_POWER` <-> `wHubChange bit 0` and `C_HUB_OVER_CURRENT` <-> `wHubChange bit 1`.
- Port-recipient reviewed linkage currently includes `C_PORT_CONNECTION`, `C_PORT_ENABLE`, `C_PORT_SUSPEND`, `C_PORT_OVER_CURRENT`, and `C_PORT_RESET` within the standard port change-selector boundary.
- Common change-bit semantics should be read together with `GET_STATUS`.

- Reviewed change selectors are boundary-level evidence only:
  - `C_PORT_CONNECTION`, `C_PORT_ENABLE`, `C_PORT_SUSPEND`, `C_PORT_OVER_CURRENT`, and `C_PORT_RESET` are treated as event-record selectors for the host to acknowledge and clear.
  - This does not assert full control-state transitions, timing, or error-recovery behavior.

**Reviewed surface**

- This repo now narrows `CLEAR_FEATURE` to a selector-linkage surface for the reviewed `C_HUB_*` and `C_PORT_*` change selectors.
- This still does not claim host-side event-acknowledgement sequencing, full change-bit lifecycle correctness, or a complete `CLEAR_FEATURE` behavior model.

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`
- `tables/port_status_bit_matrix.yaml`
- `specs/port_status_bits.md`

**Non-claims**

- This page does not establish a complete `CLEAR_FEATURE` state-transition model.
- This page does not claim all selectors already have section-level packet verification.

## `SET_FEATURE`

**Purpose**

- Sets a hub or port feature.

**Direction / recipient**

- Hub: Host-to-Device, class, device recipient.
- Port: Host-to-Device, class, other recipient.

**Target**

- The hub itself or a specific port.

**Setup-field summary**

- `bRequest`: `SET_FEATURE`
- `wValue`: `feature_selector`
- `wIndex`:
  - Hub request: `0x0000`
  - Port request: `port_number`
- `wLength`: `0`

**Governed linkage**

- Hub and port selector namespaces must remain distinct.
- Some selectors affect port power, reset, or suspend behavior, but this page remains a request summary only.
- The reviewed request surface here is namespace-level only: hub-recipient selectors must not be merged with the standard port selector range.
- Port-recipient reviewed anchors currently include `PORT_ENABLE`, `PORT_SUSPEND`, `PORT_RESET`, and `PORT_POWER`.

- `PORT_TEST` and `PORT_INDICATOR` are currently on-namespace-only for selector coverage.
  - This repo does not claim full test-mode or indicator control semantics from these request entries yet.

**Reviewed surface**

- This repo now narrows `SET_FEATURE` to a reviewed selector-namespace boundary: hub-recipient and port-recipient selector spaces are intentionally distinct.
- This still does not claim selector side-effect verification for power, reset, suspend, or other port-feature behaviors.

**Related tables**

- `tables/class_request_matrix.yaml`
- `tables/feature_selector_matrix.yaml`

**Non-claims**

- This page does not claim `SET_FEATURE` side effects have been correctness-verified.
- This page does not turn selector summaries into a firmware control truth table.

## `GET_DESCRIPTOR`

**Purpose**

- Reads the hub class-specific descriptor.

**Direction / recipient**

- Device-to-Host, class, device recipient.

**Target**

- The hub itself.

**Setup-field summary**

- `bRequest`: `GET_DESCRIPTOR`
- `wValue`: encodes hub descriptor type `0x29` together with the descriptor index
- `wIndex`: `0x0000`
- `wLength`: depends on hub descriptor length; this repo does not hardcode it to a single fixed constant

**Governed linkage**

- This is the request family that exposes the fields summarized in `specs/hub_descriptor.md`.

**Reviewed surface**

- This repo has now narrowed the class-specific `GET_DESCRIPTOR` descriptor type surface to `0x29`
- This still does not claim that every host request-length strategy has completed correctness verification

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- This page does not upgrade `wValue` / `wLength` encoding details into section-level verified truth.
- This page does not claim all hubs must support some consumer-side descriptor workflow.

## `SET_DESCRIPTOR`

**Purpose**

- Writes the hub class-specific descriptor.

**Direction / recipient**

- Host-to-Device, class, device recipient.

**Target**

- The hub itself.

**Setup-field summary**

- `bRequest`: `SET_DESCRIPTOR`
- `wValue`: encodes hub descriptor type `0x29` together with the descriptor index
- `wIndex`: `0x0000`
- `wLength`: depends on descriptor payload size

**Governed linkage**

- Belongs to the same descriptor family as `GET_DESCRIPTOR`, but support should not be assumed.

**Reviewed surface**

- This repo has now narrowed the class-specific `SET_DESCRIPTOR` descriptor type surface to `0x29`
- This does not mean all hubs implement `SET_DESCRIPTOR`

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/hub_descriptor.md`

**Non-claims**

- This page does not claim `SET_DESCRIPTOR` is implemented on all hubs.
- This page does not elevate descriptor-write support into a normative compatibility claim.

## `CLEAR_TT_BUFFER`

**Purpose**

- Clears TT buffer-related state.

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- An HS hub with embedded TT.

**Setup-field summary**

- `bRequest`: `CLEAR_TT_BUFFER`
- `wValue`: carries TT buffer selector fields
- `wIndex`: carries TT port or related context
- `wLength`: `0`

**Governed linkage**

- Belongs to the TT request family and is meaningful only on TT-capable hubs.

**`wValue` sub-field encoding (§11.24.2.3 Table 11-17)**

`wValue` carries the endpoint information identifying the TT buffer to clear:

| bits | Field | Description |
|---|---|---|
| `[3:0]` | Endpoint number | Endpoint number of the buffer to clear (4 bits) |
| `[10:4]` | Device address | USB address of the target device (7 bits) |
| `[12:11]` | Endpoint type | `00`=Control, `01`=Isochronous, `10`=Bulk, `11`=Interrupt |
| `[14:13]` | Reserved | Reserved, must be 0 |
| `[15]` | Direction | `0`=OUT, `1`=IN |

`wIndex`: TT port number (1-based; the port number associated with the target TT).

**Reviewed surface**

- This repo now narrows `wValue` to TT buffer selector fields rather than an arbitrary opaque value
- `wIndex` is used to select the TT port or related TT context
- The `wValue` sub-field encoding is a reviewed boundary; it is not a TT buffer clearing behavior verification.

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- This page does not verify TT buffer field encoding correctness.
- This page does not establish a TT state machine.

## `RESET_TT`

**Purpose**

- Resets the Transaction Translator.

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- An HS hub with embedded TT.

**Setup-field summary**

- `bRequest`: `RESET_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- Belongs to the TT request family and relates to TT recovery / restart concerns.

**Reviewed surface**

- This repo now narrows `RESET_TT` to `wValue = 0x0000`
- `wIndex` selects the TT port or TT target instance to reset

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- This page does not claim TT behavior before and after reset has been validated.
- This page does not establish correctness claims for split-transaction completion rules.

## `GET_TT_STATE`

**Purpose**

- Reads TT diagnostic state data.

**Direction / recipient**

- Device-to-Host, class, other recipient.

**Target**

- An HS hub with embedded TT.

**Setup-field summary**

- `bRequest`: `GET_TT_STATE`
- `wValue`: `0x0000`
- `wIndex`: TT port or related diagnostic context
- `wLength`: TT state data length

**Governed linkage**

- The returned content belongs to the TT diagnostic surface and should not be merged with general port status semantics.

**Reviewed surface**

- This repo now narrows `wValue` to `0x0000`
- `wIndex` points to the TT port / diagnostic context
- `wLength` names the TT state data length, but this repo still does not hardcode it to a single constant

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- This page does not claim TT state payload bit meanings have section-level verification.
- This page does not prescribe how a host stack should consume TT state data.

## `STOP_TT`

**Purpose**

- Stops TT split-transaction processing.

**Direction / recipient**

- Host-to-Device, class, other recipient.

**Target**

- An HS hub with embedded TT.

**Setup-field summary**

- `bRequest`: `STOP_TT`
- `wValue`: `0x0000`
- `wIndex`: TT port number
- `wLength`: `0`

**Governed linkage**

- Belongs to the TT request family and is typically relevant to TT diagnostics or recovery scenarios.

**Reviewed surface**

- This repo now narrows `STOP_TT` to `wValue = 0x0000`
- `wIndex` selects the TT port or TT target instance whose split-transaction processing is being stopped

**Related tables**

- `tables/class_request_matrix.yaml`
- `specs/transaction_translator.md`

**Non-claims**

- This page does not claim downstream timing behavior after TT stop.
- This page does not establish a correctness model for TT traffic control.

## Governed Table Linkage Summary

- `tables/class_request_matrix.yaml`: primary structural source for the 9 hub class request families.
- `tables/feature_selector_matrix.yaml`: selector boundary reference for `SET_FEATURE` / `CLEAR_FEATURE`.
- `tables/port_status_bit_matrix.yaml`: comparison source for `GET_STATUS` and change-bit interpretation.
- `specs/hub_descriptor.md`: descriptor-side reference page for `GET_DESCRIPTOR` / `SET_DESCRIPTOR`.
- `specs/transaction_translator.md`: high-level semantic summary for the TT request family.

## Non-claims

- This page is not a complete setup-packet truth table.
- This page is not a per-request section-level USB 2.0 PDF verification record.
- This page does not claim TT request field encodings are correctness-verified.
- This page does not override confirmed project facts in consuming repos.
