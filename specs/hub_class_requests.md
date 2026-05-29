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
