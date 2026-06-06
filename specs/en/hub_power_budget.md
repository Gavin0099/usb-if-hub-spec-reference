---
title: Hub Power Budget
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Power Budget

> Source scope: USB 2.0 Specification Rev 2.0, §11.11.  
> This page is a reviewed reference summary for USB 2.0 hub power budget rules — self-powered vs. bus-powered operation, per-port current limits, and `bHubContrCurrent`.

## Page Purpose

This page answers:

- What is the difference between a self-powered and bus-powered hub.
- How much current a hub may draw from the USB bus and supply to its ports.
- What role `bHubContrCurrent` and `bMaxPower` play in hub power accounting.

## Self-Powered vs. Bus-Powered Hubs

| Attribute | Self-Powered Hub | Bus-Powered Hub |
|---|---|---|
| Power source | External (wall adapter or internal PSU) | USB bus (VBUS from upstream port) |
| `bmAttributes bit 6` (config descriptor) | `1` | `0` |
| Max current per downstream port | 500 mA | 100 mA (or 500 mA with ganged power) |
| `bMaxPower` in config descriptor | Hub's bus-current draw / 2 (mA) | Hub's bus-current draw / 2 (mA) |
| Typical `bMaxPower` | Low (hub controller only) | Up to 250 (= 500 mA total) |

A hub advertises its power source in `bmAttributes bit 6` of the configuration descriptor. Hosts may use this to decide port power allocation.

## Per-Port Current Limits (§11.11)

### Before Configuration (Default State)

- A USB device may draw up to **100 mA** from a port before `SET_CONFIGURATION`.
- This applies to the hub itself before the host issues `SET_CONFIGURATION`.

### After Configuration

- A self-powered hub may provide up to **500 mA** per downstream port.
- A bus-powered hub is limited by its total available bus power; typically **100 mA** per port.
- The host allocates per-port power based on the downstream device's `bMaxPower` in its configuration descriptor.

## `bHubContrCurrent`

`bHubContrCurrent` is a field in the hub class descriptor (not the configuration descriptor):

- Units: **mA** (direct milliamp value, not ×2).
- Meaning: the maximum current the hub controller itself draws from VBUS (excluding downstream devices).
- Used by the host for power budget accounting.

For a self-powered hub, `bHubContrCurrent` may be 0 (hub draws power from its own supply, not the USB bus).  
For a bus-powered hub, `bHubContrCurrent` should reflect the actual hub controller consumption.

## `bMaxPower` (Configuration Descriptor)

`bMaxPower` in the configuration descriptor:

- Units: **2 mA per LSB** (multiply by 2 to get mA).
- Meaning: maximum current the hub (entire device) draws from VBUS when configured.
- For a self-powered hub: typically low (hub electronics only).
- For a bus-powered hub: the sum of `bHubContrCurrent` + (ports × estimated per-port draw).

## Power Budget Example

**Bus-powered hub, 4 ports:**

```
VBUS current available from upstream host port: 500 mA
Hub controller draw (bHubContrCurrent): 50 mA
Available for downstream ports: 500 - 50 = 450 mA
Per-port available (4 ports): ~112 mA each (limited to 100 mA per USB spec)
```

**Self-powered hub, 7 ports:**

```
External PSU provides: 3500 mA (7 × 500 mA)
Hub controller draw: 100 mA from PSU
Bus draw (bMaxPower × 2): e.g. 10 mA (only hub controller from USB)
Each port can supply: 500 mA from PSU
```

## Overcurrent and Power Switching Interaction

Power budget connects to the overcurrent protection mode in `wHubCharacteristics[4:3]`:

- **Global overcurrent** (`00`): hub monitors total current and cuts all ports if exceeded.
- **Per-port overcurrent** (`01`): hub monitors each port independently and cuts only the affected port.

See `specs/en/hub_power_management.md` for power switching and overcurrent protection modes.

## Governed Linkage

- `specs/en/hub_descriptor.md`: `bHubContrCurrent` field in the hub class descriptor
- `specs/en/hub_power_management.md`: power switching modes, `bPwrOn2PwrGood`, overcurrent
- `specs/en/standard_descriptors.md`: `bMaxPower` and `bmAttributes` in the configuration descriptor
- `specs/en/hub_configuration.md`: hub configuration descriptor structure in context

## Non-claims

- This page does not claim power budget calculations have been verified against a physical hub.
- This page does not claim host power allocation algorithms are implementation-verified.
- This page does not define USB-IF certification power requirements.
- This page does not override confirmed project facts in consuming repos.
