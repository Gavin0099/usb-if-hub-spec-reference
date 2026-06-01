---
layout: home

hero:
  name: USB-IF Hub 規格參考
  text: USB Hub 治理規格文件
  tagline: claim_level&#58; inferred · semantic_verification_claimed&#58; false · 僅供語意參考
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
    details: 9 個 USB 2.0 Hub 類別請求家族 — GET_STATUS、SET_FEATURE、CLEAR_FEATURE、TT 請求、GET/SET_DESCRIPTOR。
    link: /hub_class_requests
  - title: 連接埠狀態位元
    details: wPortStatus / wPortChange / wHubStatus / wHubChange 位元欄位參考（claim_level&#58; inferred，review_required）。
    link: /port_status_bits
  - title: Hub 描述符
    details: USB 2.0 Hub 描述符欄位定義 — §11.23.2.1。
    link: /hub_descriptor
  - title: Transaction Translator
    details: TT 規則摘要 — 僅適用於含內嵌 TT 的 HS Hub。
    link: /transaction_translator
  - title: 版本來源對應
    details: USB 2.0 / 2.1 / 3.2 / 4.0 Hub 相關來源授權對應表。
    link: /version_source_map
  - title: 升級觸發表
    details: 供 consuming firmware repo 使用的標準升級觸發條件表。
    link: /escalation_table
---

> **治理說明：** 所有頁面均為 `claim_level: inferred`，`semantic_verification_claimed: false`。
> 本文件僅供語意澄清，不覆蓋 consuming repo 中已確認的專案事實。
