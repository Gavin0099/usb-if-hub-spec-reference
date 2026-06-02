---
layout: home

hero:
  name: USB-IF Hub 規格參考
  text: USB Hub 規格語意參考層
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
    details: 彙整 USB 2.0 Hub class-specific requests，包括 GET_STATUS、SET_FEATURE、CLEAR_FEATURE 與 TT 相關請求。
    link: /hub_class_requests
  - title: 連接埠狀態位元
    details: 整理 wPortStatus、wPortChange、wHubStatus、wHubChange 的位元定義與觀測邊界。
    link: /port_status_bits
  - title: Hub 描述符
    details: 說明 USB 2.0 Hub descriptor 的欄位配置與 wHubCharacteristics 語意。
    link: /hub_descriptor
  - title: Transaction Translator
    details: 彙整 TT 相關規則與 HS hub 專屬請求邊界。
    link: /transaction_translator
  - title: 版本來源對應
    details: 對照 USB 2.0、2.1、3.2、4.0 的 hub 相關來源位置與引用邊界。
    link: /version_source_map
  - title: 升級觸發表
    details: 提供 consuming firmware repo 判定何時需要進入 Standard Escalation Mode 的條件表。
    link: /escalation_table
---

> **重要限制：** 本站所有內容目前維持 `claim_level: inferred`，且 `semantic_verification_claimed: false`。
> 它是標準語意參考層，不是 consuming repo 的專案事實來源，不能直接覆蓋已確認的 firmware 行為。
