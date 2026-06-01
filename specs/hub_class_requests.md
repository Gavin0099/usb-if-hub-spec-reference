---
title: Hub Class Requests
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Class Requests

> Source: USB 2.0 Specification, Revision 2.0, Section 11.24.2
> Usage: Reference layer only. Do not use to override confirmed project facts.

## Request Summary

| bRequest | Value | Direction | Description |
|----------|-------|-----------|-------------|
| GET_STATUS | 0x00 | Device→Host | Get hub or port status |
| CLEAR_FEATURE | 0x01 | Host→Device | Clear hub or port feature |
| SET_FEATURE | 0x03 | Host→Device | Set hub or port feature |
| GET_DESCRIPTOR | 0x06 | Device→Host | Get hub descriptor |
| SET_DESCRIPTOR | 0x07 | Host→Device | Set hub descriptor |
| CLEAR_TT_BUFFER | 0x08 | Host→Device | Clear TT buffer |
| RESET_TT | 0x09 | Host→Device | Reset TT |
| GET_TT_STATE | 0x0A | Device→Host | Get TT state |
| STOP_TT | 0x0B | Host→Device | Stop TT |

## Hub Feature Selectors

| Feature | Selector Value | Recipient |
|---------|----------------|-----------|
| C_HUB_LOCAL_POWER | 0 | Hub |
| C_HUB_OVER_CURRENT | 1 | Hub |
| PORT_CONNECTION | 0 | Port |
| PORT_ENABLE | 1 | Port |
| PORT_SUSPEND | 2 | Port |
| PORT_OVER_CURRENT | 3 | Port |
| PORT_RESET | 4 | Port |
| PORT_POWER | 8 | Port |
| PORT_LOW_SPEED | 9 | Port |
| C_PORT_CONNECTION | 16 | Port |
| C_PORT_ENABLE | 17 | Port |
| C_PORT_SUSPEND | 18 | Port |
| C_PORT_OVER_CURRENT | 19 | Port |
| C_PORT_RESET | 20 | Port |
| PORT_TEST | 21 | Port |
| PORT_INDICATOR | 22 | Port |

## GET_DESCRIPTOR (Hub Descriptor)

- bmRequestType: 1010 0000b (0xA0)
- bRequest: GET_DESCRIPTOR (0x06)
- wValue: 0x2900 (Hub Descriptor type)
- wIndex: 0x0000
- wLength: descriptor length

## Vendor Command Boundary

USB-IF hub class requests stop at selector value 22 (PORT_INDICATOR).
Any request code or selector outside this table is vendor-defined and must be
documented in the project's vendor command protocol spec.

## Standard Conflict Notes

- GET_DESCRIPTOR for hub type (0x29) must be supported by all USB hubs per spec.
  If a project does not support it, flag as Standards Compliance Risk.
- CLEAR_TT_BUFFER and RESET_TT apply only to hubs with an embedded TT.
  Full-speed-only hub controllers without TT may omit these.

---

## Request Family Descriptions

> **claim_level: inferred** — content inferred from USB 2.0 Specification §11.24.2.
> **semantic_verification_claimed: false** — bit-level behavior and timing not verified.
> **Source reference:** usb20_spec (normative — not directly verified in this page).

### GET_STATUS

**Purpose:** Returns status information for a hub or one of its ports. The response includes current state bits and change indicator bits.

**Direction:** Device-to-host.

**Target:** Hub (wIndex=0) or a specific port (wIndex=1-based port number).

**Response:** 4 bytes — 2-byte status field + 2-byte change field. Hub target: wHubStatus + wHubChange. Port target: wPortStatus + wPortChange.

**Governed table linkage:**
- `class_request_matrix`: GET_STATUS (usb20_get_status_hub, usb20_get_status_port)
- `port_status_bit_matrix`: bit definitions for wPortStatus/wPortChange when target is port

**Non-claims:** This section does not verify response bit layout, timing, or error behavior. Bit-level semantics require PDF section-level review (Phase 6).

---

### CLEAR_FEATURE

**Purpose:** Clears a feature — typically resets a change-indicator bit — on a hub or a port.

**Direction:** Host-to-device. No data stage.

**Target:** Hub (feature selector applies to hub) or port (feature selector applies to specified port number).

**Feature selector:** Passed in wValue. Hub selectors include C_HUB_LOCAL_POWER and C_HUB_OVER_CURRENT. Port change selectors include C_PORT_CONNECTION, C_PORT_ENABLE, C_PORT_SUSPEND, C_PORT_OVER_CURRENT, and C_PORT_RESET.

**Governed table linkage:**
- `class_request_matrix`: CLEAR_FEATURE (usb20_clear_feature_hub, usb20_clear_feature_port)
- `feature_selector_matrix`: valid selector values and per-selector recipient constraints

**Non-claims:** This section does not verify which selectors are mandatory vs. optional, or error behavior on unsupported selectors.

---

### SET_FEATURE

**Purpose:** Asserts or activates a feature on a hub or a port (e.g., initiates PORT_RESET or enables PORT_POWER).

**Direction:** Host-to-device. No data stage.

**Target:** Hub or port, depending on the feature selector.

**Feature selector:** Passed in wValue. Port features include PORT_CONNECTION, PORT_ENABLE, PORT_SUSPEND, PORT_OVER_CURRENT, PORT_RESET, PORT_POWER, PORT_LOW_SPEED, PORT_TEST, and PORT_INDICATOR.

**Governed table linkage:**
- `class_request_matrix`: SET_FEATURE (usb20_set_feature_hub, usb20_set_feature_port)
- `feature_selector_matrix`: valid selector values and per-selector recipient constraints

**Non-claims:** This section does not verify feature activation timing, side effects, or required response behavior.

---

### GET_DESCRIPTOR (hub class)

**Purpose:** Retrieves the hub class descriptor, which contains hub-specific configuration information such as number of ports, power characteristics, and overcurrent protection mode.

**Direction:** Device-to-host.

**Target:** Hub device.

**Context note:** This is the hub class-specific GET_DESCRIPTOR (bmRequestType type=class, wValue high byte=0x29 hub descriptor type). Distinguished from the standard USB GET_DESCRIPTOR by request type field in bmRequestType.

**Governed table linkage:**
- `class_request_matrix`: GET_DESCRIPTOR (usb20_get_descriptor_hub, request_context: hub_class_specific)

**Non-claims:** Hub descriptor field layout and mandatory vs. optional fields require PDF section review. wValue and wLength encoding are spec_defined in the table.

---

### SET_DESCRIPTOR (hub class)

**Purpose:** Optionally writes or updates the hub descriptor. Implementation support is not mandatory per the USB 2.0 specification.

**Direction:** Host-to-device.

**Target:** Hub device.

**Context note:** Hub class-specific context. A hub may STALL this request without violating the spec. Not to be confused with the standard USB SET_DESCRIPTOR.

**Governed table linkage:**
- `class_request_matrix`: SET_DESCRIPTOR (usb20_set_descriptor_hub, request_context: hub_class_specific)

**Non-claims:** Conditions under which SET_DESCRIPTOR must be supported and the payload structure are spec_defined and not verified here.

---

### CLEAR_TT_BUFFER

**Purpose:** Instructs the hub's embedded Transaction Translator to discard buffered transactions for a specific endpoint/device combination. Used to recover from split transaction errors.

**Direction:** Host-to-device. No data stage.

**Target:** TT port context — TT port number carried in wIndex.

**Applicability:** Only valid on high-speed hubs with an embedded Transaction Translator. Full-speed hubs and hubs without TT must not receive this request.

**Governed table linkage:**
- `class_request_matrix`: CLEAR_TT_BUFFER (usb20_clear_tt_buffer, applies_to: hub_with_tt_only)

**Non-claims:** wValue and wIndex field encoding are spec_defined in the table entry. TT buffer semantics require PDF section review.

---

### RESET_TT

**Purpose:** Resets the Transaction Translator, aborting any pending split transactions. Used during error recovery sequences.

**Direction:** Host-to-device. No data stage.

**Target:** TT port number specified in wIndex.

**Applicability:** Only valid on high-speed hubs with embedded TT.

**Governed table linkage:**
- `class_request_matrix`: RESET_TT (usb20_reset_tt, applies_to: hub_with_tt_only)

**Non-claims:** TT port context encoding and transaction completion requirements before reset are spec_defined; not verified here.

---

### GET_TT_STATE

**Purpose:** Retrieves diagnostic state information from the Transaction Translator. Used for TT diagnostics or error analysis tools.

**Direction:** Device-to-host.

**Target:** TT port context — wIndex carries TT port/context identifier.

**Applicability:** Only valid on high-speed hubs with embedded TT.

**Governed table linkage:**
- `class_request_matrix`: GET_TT_STATE (usb20_get_tt_state, applies_to: hub_with_tt_only)

**Non-claims:** wLength (TT state data payload size) and the state data format are spec_defined in the table entry; not verified here.

---

### STOP_TT

**Purpose:** Stops the Transaction Translator from processing split transactions on a specified TT port. Provides a controlled shutdown path as a counterpart to RESET_TT.

**Direction:** Host-to-device. No data stage.

**Target:** TT port number in wIndex.

**Applicability:** Only valid on high-speed hubs with embedded TT.

**Governed table linkage:**
- `class_request_matrix`: STOP_TT (usb20_stop_tt, applies_to: hub_with_tt_only)

**Non-claims:** TT port context encoding is spec_defined; not verified here.
