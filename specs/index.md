---
layout: home
title: USB-IF Hub Spec Reference
titleTemplate: false

hero:
  name: USB-IF Hub Spec Reference
  text: USB Hub 標準語意澄清層
  tagline: "claim_level: inferred, semantic_verification_claimed: false, 僅用於 standards clarification"
  actions:
    - theme: brand
      text: Hub Class Requests
      link: /hub_class_requests
    - theme: alt
      text: Verification Status
      link: /verification_status
    - theme: alt
      text: Glossary
      link: /glossary

features:
  - title: Hub Class Requests
    details: 整理 USB 2.0 hub class-specific requests，包括 GET_STATUS、SET_FEATURE、CLEAR_FEATURE 與 TT 相關 requests。
    link: /hub_class_requests
  - title: Feature Selectors
    details: 完整導入 USB 2.0 hub/port selector namespace，包含 reviewed selector-boundary、reserved-boundary 與 non-claims。
    link: /feature_selectors
  - title: Port Status Bits
    details: 整理 wPortStatus、wPortChange、wHubStatus 與 wHubChange 的 bit semantics、verified entries 與 boundary placeholders。
    link: /port_status_bits
  - title: Hub Descriptor
    details: 說明 USB 2.0 hub descriptor fields 與 wHubCharacteristics 的語意邊界。
    link: /hub_descriptor
  - title: Transaction Translator
    details: 整理 TT rules，以及具 embedded TT 的 HS hubs 專屬 request boundaries。
    link: /transaction_translator
  - title: Escalation Table
    details: 列出 consuming firmware repository 何時應進入 Standard Escalation Mode。
    link: /escalation_table
  - title: Version Source Map
    details: 對照 hub 相關的 USB 2.0、2.1、3.2 與 USB4 sources 和 authority boundaries。
    link: /version_source_map
  - title: Verification Status
    details: 目前共有 86 筆 tracked entries，其中 28 筆 verified、58 筆 reviewed、0 筆 inferred，並附 non-claims 與 evidence packet 狀態。
    link: /verification_status
  - title: Glossary
    details: 固定本 repo 的中英文術語寫法，降低文件與 LLM 回答漂移。
    link: /glossary
---

> **重要邊界：** 本站內容目前仍維持 `claim_level: inferred` 與 `semantic_verification_claimed: false`。
> 本 repo 是 standards clarification layer，不是 consuming firmware repos 的 project-fact authority。
