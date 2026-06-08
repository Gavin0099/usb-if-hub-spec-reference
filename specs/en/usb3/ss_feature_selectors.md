---
title: SS Feature Selectors
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

# SS Feature Selectors

> Scope: USB 3.2 Specification Rev 1.0, Section 10.14 Table 10-8 (SuperSpeed Hub Feature Selectors).
> This page is a consumer reference summary, not a per-selector PDF verification record.
> Governed matrix: `tables/ss_feature_selector_matrix.yaml` (6 SS-only port feature selectors, all verified).

## Purpose

This page answers:

- Which SS-only port feature selectors exist in USB 3.x SS hubs (not present in USB 2.0).
- The numeric value, recipient (port), and applicable requests (SetFeature/ClearFeature) for each selector.
- What U1/U2 Link Power Management (LPM) selectors do.

This page does not answer:

- LTSSM state transition behavior after U1/U2 enable.
- xHCI port power policy or U1/U2 policy enforcement implementation.
- Whether firmware compliance has been verified.

## SS-Only Port Feature Selectors

The following 6 feature selectors exist only in USB 3.x SuperSpeed hubs; they are not present in the USB 2.0 hub feature selector namespace.

| Selector name | Value | Hex | Recipient | SetFeature | ClearFeature |
|---|---:|---|---|---|---|
| PORT_U1_ENABLE | 17 | 0x11 | port | ✓ | ✓ |
| PORT_U2_ENABLE | 18 | 0x12 | port | ✓ | ✓ |
| PORT_U1_TIMEOUT | 23 | 0x17 | port | ✓ | — |
| PORT_U2_TIMEOUT | 24 | 0x18 | port | ✓ | — |
| PORT_REMOTE_WAKE_MASK | 27 | 0x1B | port | ✓ | — |
| BH_PORT_RESET | 28 | 0x1C | port | ✓ | — |

Source: USB 3.2 Specification §10.14 Table 10-8.

## U1/U2 Link Power Management (LPM) Selectors

**PORT_U1_ENABLE (0x11)** and **PORT_U2_ENABLE (0x12)**:
- Allow a hub port to accept U1/U2 link power state entry requests from the downstream device.
- SET_FEATURE: permits the SS hub port to accept device-initiated U1/U2 entry requests.
- CLEAR_FEATURE: disables acceptance of U1/U2 entry requests.

**PORT_U1_TIMEOUT (0x17)** and **PORT_U2_TIMEOUT (0x18)**:
- Set the U1/U2 timeout threshold for an SS hub port.
- SET_FEATURE(wValue): wValue high byte encodes the timeout value; low byte is the port number.
- Detailed timeout encoding semantics are outside this page's verified scope.

## PORT_REMOTE_WAKE_MASK (0x1B)

- Sets the remote wake event mask for an SS hub port.
- wValue high byte encodes the wake mask; each bit corresponds to a different wake event type.
- Wake mask encoding semantics are outside this page's verified scope.

## BH_PORT_RESET (0x1C)

- Also called Warm Reset. Initiates the BH (Buffered Host) reset sequence on an SS hub port.
- SET_FEATURE: initiates Warm Reset to recover from link layer issues.
- BH reset timing, LFPS signaling, and xHCI warm reset behavior are outside this page's verified scope.

## Verified Gate

The governed matrix (`tables/ss_feature_selector_matrix.yaml`) verified gate: **PARTIAL (allowlist, all 6 entries promoted)**.

Verified scope is limited to: selector name, value, applicability (SetFeature/ClearFeature), and recipient (port) identity only.

Evidence packets: `evidence/entry_verification_packets/usb3/ss_feature_selector_*.yaml` (6 packets).

## This Page Does Not Claim

- U1/U2 LTSSM state transition behavior.
- U1/U2 timeout encoding semantics or wValue field behavior.
- xHCI port power policy or U1/U2 policy enforcement.
- Remote wake event routing or OS power management.
- BH reset timing, LFPS signaling, or link recovery outcome.
- Firmware compliance.

→ [Verification Status](../verification_status.md)
