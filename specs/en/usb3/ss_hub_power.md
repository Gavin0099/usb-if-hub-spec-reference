---
title: SS Hub Power Management
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

# SS Hub Power Management

> Scope: USB 3.2 Specification Rev 1.0, Section 10.14 / 10.14.2.
> This page is a consumer reference summary, not a power management runtime behavior verification record.

## Purpose

This page answers:

- How USB 3.x SS hub port power is controlled (ganged vs. per-port).
- How U1/U2 link power states affect SS hub ports.
- What `bPwrOn2PwrGood` means.

This page does not answer:

- Whether firmware correctly implements each power state.
- LTSSM runtime behavior for U1/U2 entry and exit.
- Electrical or power compliance.

## SS Hub Port Power Control

The USB 3.x SS hub power switching mode is defined by `wHubCharacteristics bits[1:0]`:

| Mode | Description |
|---|---|
| Ganged (00) | All ports powered on/off together |
| Per-port (01) | Each port independently controlled via SET_FEATURE(PORT_POWER) |
| No switching (1x) | Hub does not support power switching |

Power switching mode bit identity has been promoted to verified (`ss_hub_characteristics_bit_matrix`).

> **No Transaction Translator**: USB 3.x SS hubs have no TT, so there are no TT Think Time bits or TT-related power management.

## U1/U2 Link Power States

SuperSpeed hub ports support U1/U2 link power states (low-power standby):

- **U0**: Active (normal operation)
- **U1**: Standby (short wake latency, < 10 μs)
- **U2**: Standby (longer wake latency, < 2 ms)
- **U3**: Suspend (deepest power saving)

**PORT_U1_ENABLE / PORT_U2_ENABLE feature selectors** control whether a port accepts device-initiated U1/U2 entry requests.

LTSSM state transition behavior following U1/U2 entry or exit is outside this page's verified scope.

## bPwrOn2PwrGood

`wHubDescriptor.bPwrOn2PwrGood` (in 2 ms units):

- Defines how long the hub needs after power-on or resume before port power is stable.
- The host should not issue port requests during this interval.
- Actual power stabilization behavior is outside this page's verified scope; this field's identity has been verified in ss_hub_descriptor_matrix.

## Over-current Protection

The SS hub over-current protection mode is defined by `wHubCharacteristics bits[4:3]`:

- `00`: Global (hub-level) OC reporting.
- `01`: Individual port OC reporting.
- `1x`: No OC protection.

Over-current detection hardware behavior, thresholds, and C_PORT_OVER_CURRENT notification behavior are outside this page's verified scope.

## This Page Does Not Claim

- LTSSM behavior for U1/U2 power state entry or exit.
- Port power sequencing or timing correctness.
- Over-current detection hardware behavior or thresholds.
- Firmware power management implementation correctness.
- Electrical or power compliance.

→ [SS Hub Characteristics](ss_hub_characteristics.md) | [SS Feature Selectors](ss_feature_selectors.md) | [Verification Status](../verification_status.md)
