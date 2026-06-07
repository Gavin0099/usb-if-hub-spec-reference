---
title: SS Hub Class Requests
claim_level: inferred
spec_family: usb3
status: review_required
last_reviewed: "2026-06-07"
usb_versions:
  - usb_3_2
source_refs:
  - usb32_spec
semantic_verification_claimed: false
---

# SS Hub Class Requests

> Source scope: USB 3.2 Specification Rev 1.0, Section 10.14.2 (Hub Class Requests for SuperSpeed).
> This page is a consumer-facing reference summary, not a request-by-request PDF verification record.

## Page Purpose

This page answers:

- The two SS-specific hub class requests added in USB 3.x: `SET_HUB_DEPTH` and `GET_PORT_ERR_COUNT`.
- Which USB 2.0 hub requests are not applicable to SS hubs.
- SS-specific feature selectors (U1/U2 timeout, BH reset-related).

This page does not answer:

- How xHCI internally drives these requests.
- Whether any firmware implementation correctly handles these requests.

## SS-Specific Hub Class Requests

### SET_HUB_DEPTH (0x0C)

| Field | Value |
|---|---|
| bmRequestType | 0x20 (class, device, host-to-device) |
| bRequest | 0x0C |
| wValue | Hub depth (0 = root hub or hub directly attached to root hub; max 5) |
| wIndex | 0 |
| wLength | 0 |

**Purpose**: Informs the hub of its tier depth in the SS bus topology. xHCI must issue this request when configuring a SS hub before addressing downstream devices. SS hubs support a maximum of 5 hops from the root hub (root hub = depth 0). **Mandatory for all SS hubs.**

### GET_PORT_ERR_COUNT (0x0D)

| Field | Value |
|---|---|
| bmRequestType | 0xA0 (class, device, device-to-host) |
| bRequest | 0x0D |
| wValue | 0 |
| wIndex | Port number |
| wLength | 2 |

**Purpose**: Reads the 16-bit link error count for the specified port; counter resets to 0 on read. Used for link quality diagnostics. **Optional for SS hubs.**

## Requests Not Applicable to SS Hubs

The following USB 2.0 hub class requests do not apply to SS hubs because SS hubs have no Transaction Translator (TT):

| Request | bRequest | Reason not applicable |
|---|---|---|
| CLEAR_TT_BUFFER | 0x08 | SS hub has no TT |
| RESET_TT | 0x09 | SS hub has no TT |
| GET_TT_STATE | 0x0A | SS hub has no TT |
| STOP_TT | 0x0B | SS hub has no TT |

SET_FEATURE PORT_SUSPEND / CLEAR_FEATURE PORT_SUSPEND also do not apply: SS hubs use U1/U2 link state policy instead of PORT_SUSPEND.

## SS-Specific Feature Selectors

The following feature selectors are new or redefined for USB 3.x SS hubs:

| Selector Name | Value | Description |
|---|---|---|
| PORT_U1_TIMEOUT | 0x23 | Set U1 entry timeout (host-initiated) |
| PORT_U2_TIMEOUT | 0x24 | Set U2 entry timeout (host-initiated) |
| PORT_BH_PORT_RESET | 0x1C | Trigger Warm Reset (BH Port Reset) |
| C_PORT_LINK_STATE | 0x19 | Clear C_PORT_LINK_STATE change bit |
| C_PORT_CONFIG_ERROR | 0x1E | Clear C_PORT_CONFIG_ERROR change bit |

## Requests Shared with USB 2.0

The following requests are shared between SS and USB 2.0 hubs with broadly compatible semantics:

| Request | Description |
|---|---|
| GET_STATUS (hub/port) | Get hub or port status (SS port status layout differs — see SS Port Status Bits page) |
| SET_FEATURE / CLEAR_FEATURE (hub/port) | Set or clear features (SS adds new selectors) |
| GET_DESCRIPTOR / SET_DESCRIPTOR | Get or set hub descriptor (SS uses 0x2A descriptor type) |

## Non-claims

- Does not claim that the hub depth calculation for SET_HUB_DEPTH has been verified as correctly implemented in any firmware.
- Does not claim the complete xHCI and SS hub request interaction sequence.
- Does not claim best-practice or compliance requirements for U1/U2 timeout policy values.
