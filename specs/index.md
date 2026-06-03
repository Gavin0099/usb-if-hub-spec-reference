---
layout: home
title: USB-IF Hub Spec Reference
titleTemplate: false

hero:
  name: USB-IF Hub Spec Reference
  text: USB Hub 標準語意澄清層
  tagline: "claim_level: inferred，semantic_verification_claimed: false，僅用於 standards clarification"
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
    details: 整理 USB 2.0 hub class-specific requests，包括 GET_STATUS、SET_FEATURE、CLEAR_FEATURE 與 TT 相關 request families。
    link: /hub_class_requests
  - title: Port Status Bits
    details: 整理 wPortStatus、wPortChange、wHubStatus、wHubChange 的 bit semantics、change-bit 邊界與已驗證 entry surface。
    link: /port_status_bits
  - title: Hub Descriptor
    details: 說明 USB 2.0 hub descriptor 欄位與 wHubCharacteristics 的基本語意。
    link: /hub_descriptor
  - title: Transaction Translator
    details: 整理 TT 規則，以及 HS hub 內嵌 TT request surfaces 的邊界。
    link: /transaction_translator
  - title: Version Source Map
    details: 對照 hub 相關的 USB 2.0、2.1、3.2 與 USB4 來源和 authority boundary。
    link: /version_source_map
  - title: Escalation Table
    details: 列出 consuming firmware repo 何時應進入 Standard Escalation Mode。
    link: /escalation_table
  - title: Verification Status
    details: 目前共有 47 筆 tracked entries，其中 8 筆 verified、21 筆 reviewed、18 筆 inferred，並附 non-claims 與 evidence packet 狀態。
    link: /verification_status
---

> **重要邊界：** 本站內容目前仍維持 `claim_level: inferred` 與 `semantic_verification_claimed: false`。  
> 這個 repo 是 standards clarification layer，不是 consuming firmware repos 的 project-fact authority。
