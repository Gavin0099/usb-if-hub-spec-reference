---
layout: home
title: USB-IF Hub Spec Reference
titleTemplate: false

hero:
  name: USB-IF Hub Spec Reference
  text: USB Hub standards clarification layer
  tagline: "claim_level: inferred, semantic_verification_claimed: false, for standards clarification only"
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
  - title: Verification Status
    details: Current entry-level verification maturity, reviewed packet status, and non-claims. 133 tracked entries, including 84 verified, 49 reviewed, and 0 inferred.
    link: /en/verification_status
  - title: Glossary
    details: Standardizes terminology for this repo to reduce document and LLM answer drift.
    link: /en/glossary
---

> **Important boundary:** All content on this site currently remains `claim_level: inferred` and `semantic_verification_claimed: false`.
> This repository is a standards clarification layer, not a project-fact authority for consuming firmware repositories.
