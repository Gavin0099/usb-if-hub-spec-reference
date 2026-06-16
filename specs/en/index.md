---
layout: home
title: USB-IF Hub Spec Reference
titleTemplate: false

hero:
  name: USB-IF Hub Spec Reference
  text: Specification reference for USB 2.0 and USB 3.2 hub firmware
  tagline: "Engineers writing firmware or software for USB hubs often need to look up specific details from the USB specification — which bit means \"device connected\", what value a request code should have, what fields a descriptor must contain. The USB specification is a large document, and getting these details wrong causes subtle bugs. This site extracts those details into searchable pages for USB 2.0 and USB 3.2 hubs. It covers descriptor fields, class requests, port status bits, and feature selectors. It does not cover runtime timing, state machine behavior, host-side driver behavior, or compliance testing."
  actions:
    - theme: brand
      text: USB 2.0 Hub Reference
      link: /en/usb2
    - theme: brand
      text: USB 3.2 / SuperSpeed Hub
      link: /en/usb3/
    - theme: alt
      text: Verification Status
      link: /en/verification_status

features:
  - title: USB 2.0 Hub Reference
    details: "28 pages covering hub descriptors, class requests, port status bits, feature selectors, Transaction Translator, High-Speed detection, and USB 2.0 protocol foundations. Governed surface: 151 tracked entries, 105 verified, 46 reviewed, 0 inferred."
    link: /en/usb2

  - title: USB 3.2 / SuperSpeed Hub Reference
    details: "25 pages covering SS hub descriptors, SS class requests, SS port status bits, SS feature selectors, link power management, speed detection, and differences from USB 2.0 hubs. Governed surface: 53 tracked entries, 48 verified."
    link: /en/usb3/

  - title: Escalation Guide
    details: A checklist of conditions where firmware behavior may conflict with the spec and requires a closer review. USB 2.0 conditions E-01 to E-10. USB 3.x conditions SE-01 to SE-05.
    link: /en/escalation_table

  - title: Governed Surface & Verification
    details: "15 governed machine-readable tables (USB 2.0: 9 tables, USB 3.2: 6 tables). Each entry has a verified scope and evidence packet. Includes consumer CI integration guide and fingerprint drift detection baseline."
    link: /en/verification_status

  - title: Glossary & Source Map
    details: USB terminology definitions and version source authority mapping for USB 2.0 through USB 3.2. Covers SS, SSP, BOS, LPM, U-states, LFPS, and more.
    link: /en/glossary
---

> **What this is:** A structured reference for USB hub spec details — descriptor fields, request codes, and status bit definitions for USB 2.0 and USB 3.2. Each entry has a clear source and defined scope.
>
> **What this is not:** This is not a guide for hub runtime behavior. It does not cover timing, state machines, or compliance testing. It clarifies what the spec says; it does not override firmware design decisions.
