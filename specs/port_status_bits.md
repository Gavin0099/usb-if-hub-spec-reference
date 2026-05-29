# Port Status and Change Bits

> Source: USB 2.0 Specification, Revision 2.0, Section 11.24.2.7.1 and 11.24.2.7.2
> Usage: Reference layer only. Do not use to override confirmed project facts.

## Port Status Field (wPortStatus)

Returned by GET_PORT_STATUS request. 16-bit field.

| Bit | Name | Meaning when set |
|-----|------|-----------------|
| 0 | PORT_CONNECTION | Device is present on this port |
| 1 | PORT_ENABLE | Port is enabled |
| 2 | PORT_SUSPEND | Port is suspended |
| 3 | PORT_OVER_CURRENT | Over-current condition detected |
| 4 | PORT_RESET | Port is in reset |
| 7:5 | Reserved | Must be 0 |
| 8 | PORT_POWER | Port power is on |
| 9 | PORT_LOW_SPEED | Low-speed device attached (0 = full-speed) |
| 10 | PORT_HIGH_SPEED | High-speed device attached |
| 11 | PORT_TEST | Port is in test mode |
| 12 | PORT_INDICATOR | Port indicator is controlled by software |
| 15:13 | Reserved | Must be 0 |

## Port Change Field (wPortChange)

Tracks changes since last read. Cleared by CLEAR_FEATURE.

| Bit | Name | Clears with |
|-----|------|------------|
| 0 | C_PORT_CONNECTION | C_PORT_CONNECTION feature |
| 1 | C_PORT_ENABLE | C_PORT_ENABLE feature |
| 2 | C_PORT_SUSPEND | C_PORT_SUSPEND feature |
| 3 | C_PORT_OVER_CURRENT | C_PORT_OVER_CURRENT feature |
| 4 | C_PORT_RESET | C_PORT_RESET feature |
| 15:5 | Reserved | — |

## Standard Conflict Notes

- **Bit 3 (PORT_OVER_CURRENT)**: Standard defines this as a hardware-detected condition.
  If a project uses this bit for an internal cascade hub status signal, that is a
  confirmed Project Implementation Constraint — do not replace with generic standard behavior.
- **Bits 15:13 and 7:5**: USB-IF reserves these bits as 0. If a project uses any of these
  bits for vendor-specific purposes, flag for Standard Escalation Mode.
- **PORT_HIGH_SPEED (bit 10)**: Only valid for high-speed capable hubs. Full-speed-only
  hub firmware must not set or test this bit.
