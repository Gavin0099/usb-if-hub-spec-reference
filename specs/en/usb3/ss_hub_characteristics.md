---
title: SS Hub Characteristics
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

# SS Hub Characteristics

> Scope: USB 3.2 Specification Rev 1.0, Section 10.14.2 Table 10-10 (wHubCharacteristics for SuperSpeed Hub).
> This page is a consumer reference summary, not a per-bit-group PDF verification record.
> Governed matrix: `tables/ss_hub_characteristics_bit_matrix.yaml` (4 verified + 1 reviewed reserved).

## Purpose

This page answers:

- Which bit groups exist in the USB 3.x SS hub `wHubCharacteristics` field and their semantics.
- The key differences between USB 3.x and USB 2.0 `wHubCharacteristics`.
- The bit position of Port Indicators in USB 3.x.

This page does not answer:

- How the firmware implements each power switching mode.
- Over-current detection hardware thresholds.
- Port indicator LED color encoding or control protocol.

## USB 3.x wHubCharacteristics Bit Layout

| Bit range | Semantic group | Claim level | Description |
|---|---|---|---|
| bits[1:0] | Power Switching Mode | **verified** | 00=ganged, 01=per-port, 1x=no switching |
| bit[2] | Compound Device | **verified** | 0=not compound, 1=compound |
| bits[4:3] | Over-current Protection Mode | **verified** | 00=global, 01=per-port, 1x=no OC |
| bit[5] | Port Indicators Supported | **verified** | 0=not supported, 1=supported |
| bits[15:6] | Reserved | reviewed | Reserved, shall be zero (permanent boundary) |

Source: USB 3.2 Specification §10.14.2 Table 10-10.

## Key Differences from USB 2.0

| Difference | USB 2.0 | USB 3.x |
|---|---|---|
| TT Think Time bits | bits[6:5] (4 TT timing values) | **Absent** (USB 3.x has no Transaction Translator) |
| Port Indicators bit | bit[7] | **bit[5]** (shifted due to TT bit removal) |
| Reserved bits | bits[15:8] | **bits[15:6]** (wider range) |

> **Important**: USB 3.x hubs have no Transaction Translator (TT), so there are no TT Think Time bits. The TT-related wHubCharacteristics bits present in USB 2.0 do not exist in USB 3.x hubs.

## Power Switching Mode (bits[1:0])

| Value | Semantics |
|---|---|
| 00 | Ganged power switching (all ports powered together) |
| 01 | Individual port power switching (each port controlled independently) |
| 1x | No power switching (hub does not support power switching) |

## Compound Device (bit[2])

- `0`: Hub is not part of a compound device.
- `1`: Hub is part of a compound device.

Compound device topology behavior and DeviceRemovable bitmap interpretation are outside this page's verified scope.

## Over-current Protection Mode (bits[4:3])

| Value | Semantics |
|---|---|
| 00 | Global (hub-level) over-current protection |
| 01 | Individual port over-current protection |
| 1x | No over-current protection |

Over-current detection hardware behavior, thresholds, and C_PORT_OVER_CURRENT notification behavior are outside this page's verified scope.

## Port Indicators Supported (bit[5])

- `0`: Hub does not support port indicators.
- `1`: Hub supports LED port indicators, controllable via SET_FEATURE(PORT_INDICATOR).

LED hardware behavior, color encoding, and firmware indicator state management are outside this page's verified scope.

## Verified Gate

The governed matrix (`tables/ss_hub_characteristics_bit_matrix.yaml`) verified gate: **PARTIAL (allowlist, 4 defined bit groups promoted)**.

Verified scope: bit group name, bit range, and value encoding identity only.

Evidence packets: `evidence/entry_verification_packets/usb3/ss_whc_*.yaml` (4 packets).

## This Page Does Not Claim

- SET_FEATURE(PORT_POWER) firmware behavior.
- Per-port power sequencing or timing.
- Over-current detection hardware behavior or thresholds.
- LED indicator hardware behavior or color encoding.
- Compound device topology behavior.
- Firmware compliance.

→ [Verification Status](../verification_status.md)
