---
title: Port Indicators and Test Mode
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Port Indicators and Test Mode

> Source scope: USB 2.0 Specification Rev 2.0, §11.5.3 and §11.24.2.7.  
> This page covers the optional USB 2.0 hub port indicator (LED) control feature and the PORT_TEST feature selector behavior.

## Page Purpose

This page answers:

- How `PORT_INDICATOR` feature control works and what LED states are defined.
- What `PORT_TEST` does and how it relates to electrical test modes.
- How `wHubCharacteristics bit 7` indicates indicator support.

## Port Indicators

USB 2.0 hubs may include per-port LEDs whose color can be host-controlled. This is optional hardware; support is indicated by `wHubCharacteristics bit 7`.

| `wHubCharacteristics bit 7` | Meaning |
|---|---|
| `0` | Port indicators **not** supported |
| `1` | Port indicators supported; host may use `SET_FEATURE(PORT_INDICATOR)` |

### `SET_FEATURE(PORT_INDICATOR)` Encoding

```
bmRequestType: 0x23  (Host→Device, Class, Other recipient)
bRequest:      0x03  (SET_FEATURE)
wValue:        port_indicator_selector  (see table below)
wIndex:        port_number  (1-based)
wLength:       0
```

The feature selector value encodes the desired LED state:

| Selector Value | LED State | Meaning |
|---|---|---|
| `0` | Automatic | Hub controls the indicator (default behavior) |
| `1` | Amber | Host forces amber (e.g., attention required) |
| `2` | Green | Host forces green (e.g., device active) |
| `3` | Off | Host turns off the indicator |

When a hub powers up, all indicators default to **Automatic** mode. In automatic mode, the hub applies its own logic (typically green when connected and enabled, amber for error conditions).

### Indicator State vs. Port State (Automatic Mode)

In automatic mode, hubs typically display:

| Port State | Typical Auto Color |
|---|---|
| Powered-off | Off |
| Disconnected (powered) | Off or dim |
| Disabled | Amber |
| Enabled | Green |
| Suspended | Amber |
| Port Error | Amber |

This mapping is hub-implementation-defined; the spec does not mandate specific auto-color behavior.

## PORT_TEST Feature

`PORT_TEST` places a specific downstream port into USB 2.0 electrical test mode. This is distinct from the device-level `TEST_MODE` described in `specs/en/usb_test_modes.md`.

```
bmRequestType: 0x23  (Host→Device, Class, Other recipient)
bRequest:      0x03  (SET_FEATURE)
wValue:        PORT_TEST  (feature selector = 21 / 0x15)
wIndex[15:8]:  test_selector  (1=TEST_J, 2=TEST_K, 3=TEST_SE0_NAK, 4=TEST_PACKET, 5=TEST_FORCE_ENABLE)
wIndex[7:0]:   port_number  (1-based)
wLength:       0
```

After `SET_FEATURE(PORT_TEST)`, the hub places the designated downstream port into the specified test mode. The port no longer participates in normal USB communication.

Exiting `PORT_TEST` requires a power cycle; USB bus reset is not sufficient.

## Feature Selector Reference

| Feature Selector | Value | Applicable | Notes |
|---|---|---|---|
| `PORT_INDICATOR` | `22` (0x16) | Port | Controls LED color; requires bit 7 of wHubCharacteristics = 1 |
| `PORT_TEST` | `21` (0x15) | Port | Places port in electrical test mode |

Both `PORT_INDICATOR` and `PORT_TEST` use `bmRequestType=0x23` (class, other recipient).

## Governed Linkage

- `specs/en/hub_descriptor.md`: `wHubCharacteristics bit 7` indicator support flag
- `specs/en/feature_selectors.md`: feature selector value table (PORT_TEST=21, PORT_INDICATOR=22)
- `specs/en/usb_test_modes.md`: device-level `SET_FEATURE(TEST_MODE)` for HS electrical compliance
- `specs/en/hub_class_requests.md`: `SET_FEATURE` port-recipient request structure

## Non-claims

- This page does not claim port indicator LED colors have been verified against any specific hub implementation.
- This page does not claim PORT_TEST behavior is implementation-verified.
- This page does not define the complete automatic indicator color logic for any specific hub.
- This page does not override confirmed project facts in consuming repos.

## Reference Navigation

- specs/en/usb2.md: USB 2.0 topic index (en).
- specs/port_indicators.md: 中文對應主題（中文頁）
