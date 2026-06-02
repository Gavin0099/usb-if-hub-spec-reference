---
layout: home

hero:
  name: USB-IF Hub 規格參考
  text: USB Hub 標準語意澄清層
  tagline: "claim_level: inferred，semantic_verification_claimed: false，僅供標準語意澄清"
  actions:
    - theme: brand
      text: Hub 類別請求
      link: /hub_class_requests
    - theme: alt
      text: 連接埠狀態位元
      link: /port_status_bits
    - theme: alt
      text: Hub 描述符
      link: /hub_descriptor

features:
  - title: Hub 類別請求
    details: 整理 USB 2.0 Hub class-specific requests，包括 GET_STATUS、SET_FEATURE、CLEAR_FEATURE 與 TT 相關請求。
    link: /hub_class_requests
  - title: 連接埠狀態位元
    details: 說明 wPortStatus、wPortChange、wHubStatus、wHubChange 的位元語意與觀察邊界。
    link: /port_status_bits
  - title: Hub 描述符
    details: 說明 USB 2.0 Hub descriptor 的欄位配置與 wHubCharacteristics 語意。
    link: /hub_descriptor
  - title: Transaction Translator
    details: 整理 TT 規則與 HS hub 專屬 request 邊界。
    link: /transaction_translator
  - title: 術語表
    details: 固定中英文專有名詞寫法，降低 LLM 與文件漂移。
    link: /glossary
  - title: 升級觸發表
    details: 列出 consuming firmware repo 何時應進入 Standard Escalation Mode。
    link: /escalation_table
  - title: 驗證狀態
    details: 查看目前 entry-level 驗證成熟度、reviewed packet 狀態與非宣告範圍。目前 47 個 tracked entries 中有 1 個 verified。
    link: /verification_status
---

> **重要邊界：** 本站所有內容目前仍為 `claim_level: inferred`，且 `semantic_verification_claimed: false`。  
> 這個 repo 是標準語意澄清層，不是 consuming firmware repo 的 project-fact authority。
