---
layout: home
title: USB-IF Hub 規格參考
titleTemplate: false

hero:
  name: USB-IF Hub 規格參考
  text: USB Hub 標準語意澄清層
  tagline: "claim_level: inferred，semantic_verification_claimed: false，僅供標準語意澄清"
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
    details: 整理 USB 2.0 Hub class-specific requests，包括 GET_STATUS、SET_FEATURE、CLEAR_FEATURE 與 TT 相關請求。
    link: /hub_class_requests
  - title: Port Status Bits
    details: 彙整 wPortStatus、wPortChange、wHubStatus、wHubChange 的 bit 名稱、位置與觀測邊界。
    link: /port_status_bits
  - title: Hub Descriptor
    details: 說明 USB 2.0 hub descriptor 欄位，以及 wHubCharacteristics 的語意邊界。
    link: /hub_descriptor
  - title: Transaction Translator
    details: 整理 HS hub 內嵌 TT 的規則摘要與 request 邊界。
    link: /transaction_translator
  - title: 術語表
    details: 提供中英對照的最低限度術語層，讓 consuming repo 與 LLM 使用同一套名稱。
    link: /glossary
  - title: Escalation Table
    details: 列出 consuming firmware repo 何時應進入 Standard Escalation Mode。
    link: /escalation_table
  - title: Verification Status
    details: 查看目前 entry-level 驗證成熟度、reviewed packet 狀態與非宣告範圍。目前 47 個 tracked entries 中有 2 個 verified。
    link: /verification_status
---

> **重要邊界：** 本站所有內容目前仍為 `claim_level: inferred`，且 `semantic_verification_claimed: false`。  
> 本 repo 的角色是標準語意澄清層，不是 consuming firmware repo 的 project-fact authority。
