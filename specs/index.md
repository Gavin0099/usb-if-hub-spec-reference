---
layout: home
title: USB-IF Hub Spec Reference
titleTemplate: false

hero:
  name: USB-IF Hub Spec Reference
  text: USB Hub 標準語意澄清層
  tagline: "claim_level: inferred，semantic_verification_claimed: false，僅供標準澄清使用"
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
    details: 整理 USB 2.0 hub class-specific requests，包括 GET_STATUS、SET_FEATURE、CLEAR_FEATURE 與 TT 相關 requests。
    link: /hub_class_requests
  - title: Port Status Bits
    details: 組織 wPortStatus、wPortChange、wHubStatus 與 wHubChange 的 bit 語意與觀察邊界。
    link: /port_status_bits
  - title: Hub Descriptor
    details: 說明 USB 2.0 hub descriptor 欄位與 wHubCharacteristics 的高層語意。
    link: /hub_descriptor
  - title: Transaction Translator
    details: 摘要 TT 規則，以及只適用於內嵌 TT 的 HS hub request 邊界。
    link: /transaction_translator
  - title: Version Source Map
    details: 對照 hub 相關的 USB 2.0、2.1、3.2 與 USB4 來源與 authority boundary。
    link: /version_source_map
  - title: Escalation Table
    details: 列出 consuming firmware repo 何時應進入 Standard Escalation Mode。
    link: /escalation_table
  - title: Verification Status
    details: 目前 entry-level verification 成熟度、reviewed packet 狀態與 non-claims。47 個 tracked entries 中有 4 個 verified。
    link: /verification_status
---

> **重要邊界：** 目前本站所有內容仍維持 `claim_level: inferred` 與 `semantic_verification_claimed: false`。  
> 本 repo 是標準澄清層，不是 consuming firmware repo 的 project-fact authority。
