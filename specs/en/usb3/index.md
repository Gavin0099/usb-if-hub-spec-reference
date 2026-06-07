---
layout: home
title: USB 3.x / SuperSpeed Hub Reference
titleTemplate: false
spec_family: usb3
---

<script setup>
</script>

# USB 3.x / SuperSpeed Hub Reference

> Source scope: USB 3.2 Specification Rev 1.0, Chapter 10 (Hub Class).
> This section is a SuperSpeed hub standards-clarification layer. It does not claim a complete LTSSM behavioral model, xHCI interaction semantics, or electrical compliance.

## Coverage

| Page | Topic |
|---|---|
| [SuperSpeed Hub Descriptor](./ss_hub_descriptor) | bDescriptorType=0x2A, wHubCharacteristics, bHubDecLat, wHubDelay |
| [SS Port Status Bits](./ss_port_status_bits) | wPortStatus / wPortChange bit definitions, PORT_LINK_STATE, PORT_SPEED |
| [SS Hub Class Requests](./ss_hub_class_requests) | SET_HUB_DEPTH, GET_PORT_ERR_COUNT, differences from USB 2.0 |

## USB 2.0 vs USB 3.x Hub: Key Differences

| Aspect | USB 2.0 | USB 3.x / SuperSpeed |
|---|---|---|
| Hub descriptor type | 0x29 | 0x2A |
| Transaction Translator (TT) | Present (HS hub) | Not present |
| Suspend mechanism | PORT_SUSPEND bit | U1/U2/U3 link states |
| Port speed representation | PORT_LOW_SPEED + PORT_HIGH_SPEED | PORT_SPEED 3-bit field |
| Hub routing depth limit | None | Max 5 hops (SET_HUB_DEPTH) |
| Warm reset | None | BH Port Reset |

## Non-claims

- Does not claim a complete LTSSM state machine behavioral model
- Does not claim xHCI host controller interaction semantics
- Does not claim USB 3.x electrical, timing, or interoperability compliance
- Does not claim USB4 / Thunderbolt hub semantics
- Does not override confirmed project facts in consuming repositories
