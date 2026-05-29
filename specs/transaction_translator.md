# Transaction Translator (TT) Rules

> Source: USB 2.0 Specification, Revision 2.0, Sections 11.17–11.18
> Usage: Reference layer only. Do not use to override confirmed project facts.

## Purpose

A Transaction Translator (TT) is required in high-speed capable hubs to allow low-speed
and full-speed devices to connect to a high-speed bus.

The TT buffers full-speed/low-speed transactions and translates them for the high-speed
upstream port.

## TT Configuration

| Configuration | wHubCharacteristics bits 6:5 | Think Time |
|---------------|------------------------------|------------|
| Single TT | — | hub has one TT shared across all ports |
| Multiple TT | — | hub has one TT per port |
| TT Think Time | 00 | 8 FS bit times |
| TT Think Time | 01 | 16 FS bit times |
| TT Think Time | 10 | 24 FS bit times |
| TT Think Time | 11 | 32 FS bit times |

## TT Request Behavior

- **CLEAR_TT_BUFFER**: Clears the TT buffer for a specific endpoint. Required after a
  halted transaction to the TT.
- **RESET_TT**: Resets the TT to a known state. The hub must complete ongoing transactions
  before resetting.
- **GET_TT_STATE**: Returns TT state for diagnostic purposes.
- **STOP_TT**: Stops processing split transactions on the TT.

## Split Transaction Overview

Full-speed/low-speed traffic on a high-speed hub is handled via split transactions:

1. Host issues Start Split (SSPLIT) to hub
2. Hub buffers the full-speed/low-speed transaction
3. Host issues Complete Split (CSPLIT) to retrieve the result
4. Hub returns transaction status or data

## Standard Conflict Notes

- If a project's hub is **full-speed only** (no high-speed upstream): TT does not apply.
  Do not require TT support in this case.
- If a project uses single TT but the descriptor reports multiple TT (or vice versa):
  flag for Standard Escalation Mode.
- TT Think Time must match actual bus timing requirements of the downstream devices.
  Do not change without hardware validation evidence.
