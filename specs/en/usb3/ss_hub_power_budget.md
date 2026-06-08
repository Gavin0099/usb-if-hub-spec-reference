---
title: SS Hub Power Budget
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

# SS Hub Power Budget

> Scope: USB 3.2 Specification Rev 1.0, §10.14.2 / §11.4.
> This page is a reviewed reference summary of USB 3.x SS hub power budget rules — self-powered vs. bus-powered operation, per-port current limits, `bHubContrCurrent`, and key differences from USB 2.0.

## Purpose

This page answers:

- The maximum per-port current a USB 3.x SS hub can provide.
- Power budget rules for self-powered vs. bus-powered SS hubs.
- The roles of `bHubContrCurrent`, `bMaxPower`, and `bPwrOn2PwrGood` in the SS hub context.

This page does not answer:

- USB Power Delivery (USB PD) protocol — a separate standard distinct from USB hub class.
- USB Battery Charging (BC 1.2) — another separate standard.
- Whether any specific hub's actual power budget complies with the specification.

## Self-Powered vs. Bus-Powered SS Hub

| Attribute | Self-Powered SS Hub | Bus-Powered SS Hub |
|---|---|---|
| Power source | External (adapter or internal supply) | USB bus (VBUS from upstream port) |
| `bmAttributes bit 6` (config descriptor) | `1` | `0` |
| Max current per downstream port | **900 mA** | **150 mA** (after configuration) |
| Before configuration (Default state) | ≤ 150 mA per port | ≤ 150 mA per port |

**Key USB 3.x vs USB 2.0 differences**:
- USB 2.0 self-powered hub: up to **500 mA** per port
- USB 3.x self-powered hub: up to **900 mA** per port
- USB 2.0 bus-powered hub: up to **100 mA** per port
- USB 3.x bus-powered hub: up to **150 mA** per port (Default/before configuration), per `bMaxPower` after configuration

## Per-Port Current Limits

### Before Configuration (Default State)

Maximum current a USB 3.x device may draw from a port before `SET_CONFIGURATION`:
- **150 mA** (USB 3.x; vs USB 2.0's 100 mA)

### After Configuration

| Hub Type | Max Per-Port Current |
|---|---|
| Self-powered SS hub | **900 mA** |
| Bus-powered SS hub | Per `bMaxPower` (limited by upstream VBUS) |

## `bHubContrCurrent` (in SS Hub Descriptor)

The `bHubContrCurrent` field in the SS Hub Descriptor (type 0x2A):

- Unit: **mA** (direct milliamp value, not ×2).
- Meaning: maximum current the hub controller itself draws from VBUS (excluding downstream device current).
- A self-powered SS hub may report `bHubContrCurrent = 0` or a small value (controller draws from its own supply, not USB bus).

## `bMaxPower` (in Configuration Descriptor)

The configuration descriptor's `bMaxPower`:

- Unit: **2 mA per LSB** (multiply by 2 to get mA) — same encoding as USB 2.0.
- Meaning: maximum current the entire hub device draws from VBUS during configured state.
- Self-powered SS hub: typically low (only hub electronics).
- Bus-powered SS hub: hub controller current + expected downstream device current.

## `bPwrOn2PwrGood` (in SS Hub Descriptor)

The `bPwrOn2PwrGood` field has the same encoding as in the USB 2.0 Hub Descriptor:

- Unit: **2 ms per LSB** (multiply by 2 to get milliseconds).
- Meaning: time from port power-on to stable port power (ready for reset).
- The host waits `bPwrOn2PwrGood × 2 ms` after `SET_FEATURE(PORT_POWER)` before proceeding.

## Power Budget Examples

**Self-powered SS hub, 4 ports (maximum configuration):**

```
External supply available: 3600 mA (4 × 900 mA)
Hub controller draw (bHubContrCurrent): 100 mA
Max per port: 900 mA (self-powered)
VBUS bus draw (bMaxPower × 2): ~10 mA
```

**Bus-powered SS hub, 4 ports (constrained configuration):**

```
Upstream SS port available VBUS: 900 mA
Hub controller draw: 50 mA
Available for downstream ports: 850 mA
Typical per port: ~200 mA (constrained by upstream)
```

## Over-Current Protection and Power Switching

SS hub over-current protection mode is controlled by `wHubCharacteristics bits[4:3]` (same position as USB 2.0):

| bits[4:3] | Mode |
|---|---|
| `00` | Global over-current: hub monitors total current; cuts all ports if exceeded |
| `01` | Per-port over-current: hub monitors each port independently; cuts only the affected port |
| `10` | No over-current protection (not recommended) |

Power switching and OCP mode bit identity has been verified via `usb3_ss_whc_power_switching` and `usb3_ss_whc_over_current_mode` evidence packets (bit name and value identity only).

## Differences from USB 2.0

| Aspect | USB 2.0 Hub | USB 3.x SS Hub |
|---|---|---|
| Max per-port current (self-powered) | 500 mA | **900 mA** |
| Max per-port current (bus-powered) | 100 mA | **150 mA** (Default), per `bMaxPower` (configured) |
| Default-state max current | 100 mA | **150 mA** |
| `bHubContrCurrent` field location | Hub Descriptor (type 0x29) | SS Hub Descriptor (type 0x2A) |
| Power budget framework | §11.11 | §11.4 (similar framework, higher currents) |

## Governed Linkage

- [SS Hub Descriptor](ss_hub_descriptor.md): SS hub descriptor fields (bHubContrCurrent, bPwrOn2PwrGood)
- [SS Hub Power Management](ss_hub_power.md): SS hub power management modes (U1/U2/U3 link states)
- `tables/ss_hub_characteristics_bit_matrix.yaml`: power switching and OCP mode bit identity — verified
- [SS Hub Configuration](ss_hub_configuration.md): bmAttributes bit 6 (self-powered flag)

## Non-claims

- This page does not claim power budget calculations have been verified for a physical SS hub.
- This page does not claim host power allocation algorithms have been implementation-verified.
- This page does not define USB-IF certification power requirements.
- This page does not cover USB Power Delivery (USB PD) or Battery Charging (BC 1.2) standards.
- This page does not override confirmed project facts in consuming repos.

→ [SS Hub Power Management](ss_hub_power.md) | [SS Hub Descriptor](ss_hub_descriptor.md) | [Verification Status](../verification_status.md)
