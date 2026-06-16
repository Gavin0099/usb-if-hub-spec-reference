---
title: Hub Enumeration Sequence
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Enumeration Sequence

> Source scope: USB 2.0 Specification Rev 2.0, §11.9 and §11.24.  
> This page is a reviewed reference summary for the USB 2.0 hub enumeration sequence. It is not a step-by-step firmware implementation guide or a section-level USB 2.0 compliance verification record.

## Page Purpose

This page answers:

- What sequence of USB requests does a host issue to enumerate a USB 2.0 hub.
- What is the format of the `GET_STATUS` response data (4-byte structure).
- How does the host detect device speed after port reset completes.

This page does not answer:

- Complete timing requirements for every enumeration step.
- Error recovery procedures when enumeration fails.
- Full bus segment timing requirements for HS or FS downstream devices.

## Hub Enumeration Overview

When a USB 2.0 hub is connected to a host, the host enumerates the hub as a standard USB device, then performs hub-specific initialization to activate the ports.

### Phase 1: Standard USB Device Enumeration

1. Hub appears at default address 0 (bus reset state).
2. Host issues `GET_DESCRIPTOR (device)` at address 0 — identifies `bDeviceClass=0x09` (Hub class).
3. Host assigns a bus address: `SET_ADDRESS(n)`.
4. Host reads configuration descriptor: `GET_DESCRIPTOR (configuration)`.
5. Host sets the active configuration: `SET_CONFIGURATION(1)` (hubs typically have one configuration).

After `SET_CONFIGURATION`, the hub becomes fully addressed and the status change endpoint is active.

### Phase 2: Hub-Specific Initialization

After standard device enumeration, the host reads the hub class descriptor and powers the ports:

1. Host issues `GET_DESCRIPTOR` with `wValue = 0x2900` (class descriptor type 0x29, index 0) to read the hub class descriptor.
2. Hub returns the hub descriptor: `bNbrPorts`, `wHubCharacteristics`, `bPwrOn2PwrGood`, `DeviceRemovable`.
3. Host issues `SET_FEATURE(PORT_POWER)` for each port from 1 to `bNbrPorts`.
4. Host waits at least `bPwrOn2PwrGood × 2ms` after the last `SET_FEATURE(PORT_POWER)`.
5. Host begins polling the status change endpoint (interrupt IN endpoint).

> `bPwrOn2PwrGood × 2ms` is the power-on stabilization delay. The host must not issue `SET_FEATURE(PORT_RESET)` until this period has elapsed.

### Phase 3: Port Monitoring and Device Attachment

Once ports are powered, the host monitors the status change endpoint and handles change events:

1. Hub returns a non-zero status change bitmap on the interrupt endpoint when a change occurs.
2. Bit 0 = hub status change; bit N = port N status change.
3. Host issues `GET_STATUS(port N)` to read `wPortStatus` and `wPortChange` for the changed port.
4. If `C_PORT_CONNECTION=1`: a connection-state change occurred. Host acknowledges with `CLEAR_FEATURE(C_PORT_CONNECTION)`.
5. If `PORT_CONNECTION=1`: a device is now attached. Host issues `SET_FEATURE(PORT_RESET)`.
6. After reset completes, hub sets `C_PORT_RESET=1` in `wPortChange`.
7. Host reads `GET_STATUS(port N)` again, then clears with `CLEAR_FEATURE(C_PORT_RESET)`.
8. Host checks `PORT_LOW_SPEED` and `PORT_HIGH_SPEED` bits to determine device speed.
9. Host proceeds with standard USB device enumeration for the attached device.

## `GET_STATUS` Response Format

`GET_STATUS` always returns exactly 4 bytes. The layout is identical for hub-recipient and port-recipient requests:

| Bytes | Field | Hub recipient | Port recipient |
|---|---|---|---|
| `[1:0]` | `wStatus` | `wHubStatus` | `wPortStatus` |
| `[3:2]` | `wChange` | `wHubChange` | `wPortChange` |

- **`wStatus`** (bytes 0–1): current hardware state — connection, enable, suspend, overcurrent, reset, power, speed bits.
- **`wChange`** (bytes 2–3): accumulated event record — each bit is set when the corresponding status bit transitions, and remains set until the host clears it via `CLEAR_FEATURE`.

For bit definitions of `wPortStatus`, `wPortChange`, `wHubStatus`, and `wHubChange`, see `specs/en/port_status_bits.md`.

## Speed Detection After Port Reset

After `SET_FEATURE(PORT_RESET)` and reset completes (`C_PORT_RESET=1`), the host reads `GET_STATUS(port)` and checks the speed bits in `wPortStatus`:

| `PORT_LOW_SPEED` (bit 9) | `PORT_HIGH_SPEED` (bit 10) | Device speed |
|---|---|---|
| `0` | `0` | Full-speed (FS) |
| `1` | `0` | Low-speed (LS) |
| `0` | `1` | High-speed (HS) |
| `1` | `1` | Not a valid combination |

- Speed bits are only valid after port reset completes and the port reaches the Enabled state.
- A hub that is not HS-capable (`bDeviceProtocol=0x00`) will never set `PORT_HIGH_SPEED`.
- Speed detection is a read-only observation from `GET_STATUS`; there is no speed-select command.

## Timing Reference

| Constraint | Value | Source |
|---|---|---|
| Port power-on stabilization | `bPwrOn2PwrGood × 2ms` | §11.11, hub descriptor |
| PORT_RESET minimum assertion | 10 ms | §11.5.1.5 |
| Port reset recovery time (debounce) | 10 ms | §7.1.7.3 |

> The 10 ms minimum reset assertion is a hub requirement; the hub holds the USB reset signal and signals completion by setting `C_PORT_RESET`. The host does not time the reset assertion directly.

## Governed Linkage

- `specs/en/hub_descriptor.md`: hub class descriptor fields (`bNbrPorts`, `bPwrOn2PwrGood`, `DeviceRemovable`)
- `specs/en/hub_class_requests.md`: `GET_DESCRIPTOR`, `GET_STATUS`, `SET_FEATURE`, `CLEAR_FEATURE` request families
- `specs/en/port_status_bits.md`: `wPortStatus`, `wPortChange`, speed bits, change-bit semantics
- `specs/en/port_state_machine.md`: port state transitions during enumeration
- `specs/en/hub_power_management.md`: power-on timing and `bPwrOn2PwrGood` semantics
- `specs/en/hub_configuration.md`: device and configuration descriptor structure for hub class
- `specs/en/hub_compound_device.md`: `DeviceRemovable` bitmap and non-removable port handling

## Non-claims

- This page does not claim the hub enumeration sequence has been step-by-step verified against a physical hub.
- This page does not establish firmware-level timing correctness for any enumeration step.
- This page does not override confirmed project facts in consuming repos.

## Reference Navigation

- specs/en/usb2.md: USB 2.0 topic index (en).
- specs/hub_enumeration.md: 中文對應主題（中文頁）
