---
title: USB 2.0 Hub Reference
layout: doc
claim_level: inferred
spec_family: usb2
status: review_required
last_reviewed: "2026-06-16"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# USB 2.0 Hub Reference

> Scope: USB 2.0 Specification, Chapter 11 (Hub Class).
> This page is the USB 2.0 topic index. For USB 3.2 SuperSpeed hubs, see [USB 3.2 / SuperSpeed Hub Reference](/en/usb3/).

## Hub Class Topics

These pages cover hub-specific descriptor fields, requests, and behaviors defined in USB 2.0 Chapter 11.

| Topic | Description |
|---|---|
| [Hub Descriptor](/en/hub_descriptor) | Descriptor fields, bDescriptorType=0x29, wHubCharacteristics, bPwrOn2PwrGood |
| [Hub Class Requests](/en/hub_class_requests) | GET_STATUS, SET_FEATURE, CLEAR_FEATURE, GET_DESCRIPTOR, CLEAR_TT_BUFFER, RESET_TT, and related |
| [Feature Selectors](/en/feature_selectors) | Hub and port feature selector namespace, selector values 0-22 |
| [Port Status Bits](/en/port_status_bits) | wPortStatus, wPortChange, wHubStatus, wHubChange bit definitions |
| [Port Feature / Change Vocabulary](/en/port_feature_change_vocabulary) | Terminology alignment for `PORT_*` and `C_PORT_*` |
| [Port State Machine](/en/port_state_machine) | 7 hub port states and state transition triggers |
| [Port Indicators](/en/port_indicators) | LED control, wHubCharacteristics bit 7, PORT_INDICATOR feature selector |
| [Hub Device Class Codes](/en/hub_device_class) | bDeviceClass=0x09, bDeviceSubClass, bDeviceProtocol TT type encoding |
| [Hub Interrupt Endpoint](/en/hub_interrupt_endpoint) | Status change endpoint descriptor, wMaxPacketSize calculation, bInterval encoding |
| [Hub Power Management](/en/hub_power_management) | Power switching modes, bPwrOn2PwrGood timing, over-current protection, suspend/resume |
| [Hub Configuration Descriptors](/en/hub_configuration) | Configuration and interface descriptor fields, multi-TT alternate settings |
| [Hub Enumeration Sequence](/en/hub_enumeration) | Enumeration request sequence, GET_STATUS 4-byte format, port power-on timing |
| [Hub Compound Device](/en/hub_compound_device) | wHubCharacteristics bit 2, DeviceRemovable bitmap, PortPwrCtrlMask |
| [Hub Power Budget](/en/hub_power_budget) | Self-powered vs. bus-powered limits, per-port current (500 mA vs. 100 mA) |
| [Transaction Translator](/en/transaction_translator) | TT rules, CLEAR_TT_BUFFER, RESET_TT, TT Think Time, HS hub TT type encoding |
| [High-Speed Detection](/en/hs_detection) | Chirp K handshake, hub KJ response pattern, HS speed negotiation outcome matrix |

## USB 2.0 Protocol Foundation

These pages cover USB 2.0 protocol fundamentals that apply to hub operation.

| Topic | Description |
|---|---|
| [Standard Device Requests](/en/standard_device_requests) | Chapter 9.4 requests (`GET_DESCRIPTOR`, `SET_ADDRESS`, `SET_CONFIGURATION`, standard feature selectors) |
| [Standard USB Descriptors](/en/standard_descriptors) | Device, configuration, interface, endpoint, and string descriptor field tables |
| [USB Device States](/en/usb_device_states) | Chapter 9.1 states: Attached, Powered, Default, Address, Configured, Suspended |
| [USB Transfer Types](/en/usb_transfer_types) | Control, Interrupt, Bulk, Isochronous and the hub-relevant types |
| [USB Signaling](/en/usb_signaling) | J/K/SE0 states, NRZI encoding, reset/suspend/resume signaling |
| [USB Packet Types](/en/usb_packet_types) | PID encoding, all token/data/handshake/special packet types |
| [USB Transactions](/en/usb_transactions) | SETUP/IN/OUT flows, control transfer 3-phase sequence, data toggle |
| [Split Transaction Packets](/en/split_transaction_packets) | SSPLIT/CSPLIT structure, TT hub split transaction flows, NYET retry |
| [USB Test Modes](/en/usb_test_modes) | TEST_J/K/SE0_NAK/PACKET/FORCE_ENABLE, SET_FEATURE(TEST_MODE) encoding |

## Reference & Governance

| Topic | Description |
|---|---|
| [Escalation Table](/en/escalation_table) | Conditions where firmware behavior may conflict with the spec, requiring review |
| [Version Source Map](/en/version_source_map) | USB 2.0 / 2.1 / 3.2 source authority mapping |
| [Verification Status](/en/verification_status) | Evidence maturity: 151 tracked / 105 verified / 46 reviewed |
| [Glossary](/en/glossary) | USB terminology and abbreviations |
