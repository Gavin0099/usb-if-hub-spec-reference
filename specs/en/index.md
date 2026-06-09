---
layout: home
title: USB-IF Hub Spec Reference
titleTemplate: false

hero:
  name: USB-IF Hub Spec Reference
  text: USB Hub standards clarification layer
  tagline: "A structured reference for USB hub specification details — descriptor fields, class requests, port status bits, and feature selectors for USB 2.0 and USB 3.2 hubs."
  actions:
    - theme: brand
      text: Hub Class Requests
      link: /en/hub_class_requests
    - theme: alt
      text: Verification Status
      link: /en/verification_status
    - theme: alt
      text: Glossary
      link: /en/glossary

features:
  - title: Hub Class Requests
    details: Summarizes USB 2.0 hub class-specific requests, including GET_STATUS, SET_FEATURE, CLEAR_FEATURE, and TT-related requests.
    link: /en/hub_class_requests
  - title: Feature Selectors
    details: Fully exposes the USB 2.0 hub/port selector namespace, including reviewed selector boundaries, reserved boundaries, and non-claims.
    link: /en/feature_selectors
  - title: Port Status Bits
    details: Organizes wPortStatus, wPortChange, wHubStatus, and wHubChange bit semantics, verified entries, and boundary placeholders.
    link: /en/port_status_bits
  - title: Hub Descriptor
    details: Explains USB 2.0 hub descriptor fields and the meaning of wHubCharacteristics.
    link: /en/hub_descriptor
  - title: Transaction Translator
    details: Summarizes TT rules and the request boundaries specific to HS hubs with embedded TT.
    link: /en/transaction_translator
  - title: Escalation Table
    details: Lists when a consuming firmware repository should enter Standard Escalation Mode.
    link: /en/escalation_table
  - title: Version Source Map
    details: Maps hub-related USB 2.0, 2.1, 3.2, and USB4 sources and authority boundaries.
    link: /en/version_source_map
  - title: Port State Machine
    details: Describes the 7 standard USB 2.0 hub port states and state transition triggers. Reviewed boundary only.
    link: /en/port_state_machine
  - title: Hub Device Class Codes
    details: Documents bDeviceClass, bDeviceSubClass, and bDeviceProtocol values for hub class identification and TT type advertising.
    link: /en/hub_device_class
  - title: Hub Interrupt Endpoint
    details: Describes the status change endpoint descriptor fields, wMaxPacketSize calculation, and bInterval encoding for FS and HS hubs.
    link: /en/hub_interrupt_endpoint
  - title: Hub Power Management
    details: Power switching modes (ganged vs. per-port), bPwrOn2PwrGood timing, over-current protection, and suspend/resume semantics.
    link: /en/hub_power_management
  - title: Hub Configuration Descriptors
    details: Configuration and interface descriptor fields for hub class, including bInterfaceClass=0x09, bNumEndpoints, and alternate settings for multi-TT hubs.
    link: /en/hub_configuration
  - title: Hub Enumeration Sequence
    details: The USB 2.0 hub enumeration request sequence, GET_STATUS 4-byte response format, speed detection after port reset, and port power-on timing constraints.
    link: /en/hub_enumeration
  - title: Hub Compound Device
    details: Compound device identification via wHubCharacteristics bit 2, DeviceRemovable bitmap semantics, and PortPwrCtrlMask interpretation in USB 2.0.
    link: /en/hub_compound_device
  - title: Standard Device Requests
    details: All standard USB 2.0 device requests (Chapter 9 §9.4) applicable to hubs — setup packet format, bmRequestType breakdown, GET_DESCRIPTOR, SET_ADDRESS, SET_CONFIGURATION, and standard feature selectors.
    link: /en/standard_device_requests
  - title: Standard USB Descriptors
    details: Standard USB 2.0 descriptor field tables — device, Device_Qualifier, configuration, interface, endpoint, and string descriptors with hub-specific values.
    link: /en/standard_descriptors
  - title: USB Device States
    details: USB device-level states (Chapter 9 §9.1) — Attached, Powered, Default, Address, Configured, Suspended — and how they differ from hub port states.
    link: /en/usb_device_states
  - title: USB Transfer Types
    details: The four USB 2.0 transfer types (Control, Interrupt, Bulk, Isochronous) and which ones a hub uses — endpoint 0 for Control, interrupt IN for status change.
    link: /en/usb_transfer_types
  - title: USB Signaling
    details: USB bus signal states (J, K, SE0), NRZI encoding, bit stuffing, reset/suspend/resume signaling events, and FS vs. HS bus differences.
    link: /en/usb_signaling
  - title: High-Speed Detection
    details: HS chirp handshake sequence during port reset — device Chirp K, hub KJ response pattern, outcome matrix, and timing reference for HS speed negotiation.
    link: /en/hs_detection
  - title: USB Packet Types
    details: PID encoding (4-bit type + 4-bit complement), all token/data/handshake/special packet types, PID values, and hub operation packet table (Chapter 8).
    link: /en/usb_packet_types
  - title: USB Transactions
    details: Transaction structure (token + data + handshake), SETUP/IN/OUT flows, control transfer 3-phase sequence, data toggle, and error response table.
    link: /en/usb_transactions
  - title: Split Transaction Packets
    details: SPLIT PID structure (4-byte SSPLIT/CSPLIT), SSPLIT/CSPLIT transaction flows, NYET retry behavior, and endpoint type split semantics for TT hubs.
    link: /en/split_transaction_packets
  - title: USB Test Modes
    details: HS electrical compliance test modes (TEST_J/K/SE0_NAK/PACKET/FORCE_ENABLE), SET_FEATURE(TEST_MODE) encoding, entry rules, and power-cycle-only exit.
    link: /en/usb_test_modes
  - title: Port Indicators
    details: PORT_INDICATOR LED control (Auto/Amber/Green/Off), wHubCharacteristics bit 7 indicator support flag, and PORT_TEST feature selector encoding.
    link: /en/port_indicators
  - title: Hub Power Budget
    details: Self-powered vs. bus-powered hub power rules, per-port current limits (500 mA vs. 100 mA), bHubContrCurrent (mA direct) vs. bMaxPower (×2) units.
    link: /en/hub_power_budget
  - title: Consumer Integration Contract
    details: "Consuming repo CI contract: unified governed surface manifest (12 tables), fingerprint drift baseline, two-step CI gate, allowed/forbidden usage, and failure interpretation. Smoke-tested: manifest PASS, no-drift PASS, drift FAIL with table attribution."
    link: /en/verification_status
  - title: Verification Status
    details: "Current entry-level verification maturity, reviewed packet status, and non-claims. USB 2.0: 151 tracked / 105 verified / 46 reviewed (freeze). USB 3.x: 38 tracked / 34 verified / 4 reviewed (matrix-level closeout)."
    link: /en/verification_status
  - title: Glossary
    details: Standardizes terminology for this repo to reduce document and LLM answer drift.
    link: /en/glossary
---

> **What this is:** A structured reference for USB hub spec details — descriptor fields, request codes, and status bit definitions for USB 2.0 and USB 3.2. Each entry has a clear source and defined scope.
>
> **What this is not:** This is not a guide for hub runtime behavior. It does not cover timing, state machines, or compliance testing. It clarifies what the spec says; it does not override firmware design decisions.
