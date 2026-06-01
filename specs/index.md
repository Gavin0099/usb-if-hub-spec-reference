---
layout: home

hero:
  name: USB-IF Hub Spec Reference
  text: Governed specification reference
  tagline: claim_level&#58; inferred · semantic_verification_claimed&#58; false
  actions:
    - theme: brand
      text: Hub Class Requests
      link: /hub_class_requests
    - theme: alt
      text: Port Status Bits
      link: /port_status_bits
    - theme: alt
      text: Hub Descriptor
      link: /hub_descriptor

features:
  - title: Hub Class Requests
    details: 9 governed USB 2.0 hub class request families — GET_STATUS, SET_FEATURE, CLEAR_FEATURE, TT requests, GET/SET_DESCRIPTOR.
    link: /hub_class_requests
  - title: Port Status Bits
    details: wPortStatus / wPortChange / wHubStatus / wHubChange bit field reference (claim_level&#58; inferred, review_required).
    link: /port_status_bits
  - title: Hub Descriptor
    details: USB 2.0 hub descriptor field definitions — §11.23.2.1.
    link: /hub_descriptor
  - title: Transaction Translator
    details: TT rules summary — applies to HS hubs with embedded TT only.
    link: /transaction_translator
  - title: Version Source Map
    details: USB 2.0 / 2.1 / 3.2 / 4.0 hub-focused source authority map.
    link: /version_source_map
  - title: Escalation Table
    details: Standard Escalation trigger table for consuming firmware repos.
    link: /escalation_table
---

> **Governance note:** All pages are `claim_level: inferred` and `semantic_verification_claimed: false`.
> Content clarifies semantics only — it does not override confirmed project facts in consuming repos.
