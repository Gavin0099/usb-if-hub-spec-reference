---
title: 詞彙表
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# 詞彙表

> 本頁用來標準化本 repo 術語，降低文件與 LLM 的 drift。它不新增 USB 2.0 的段落級驗證。

## 使用規則

- 請保留規格欄位名、請求名與位元名稱原文，例如 `GET_STATUS`、`CLEAR_FEATURE`、`wHubCharacteristics`、`PORT_CONNECTION`。
- 首次提及可使用中英對照，之後請固定使用同一術語。
- 若翻譯會降低技術精確度，保留原始英文字面表達。

## 核心術語

| 首選術語 | 備註 |
|---|---|
| Hub Class Requests | 對應 `specs/hub_class_requests.md` 的請求族頁面。 |
| Hub Descriptor | 對應 class-specific hub descriptor。 |
| Port Status Bits | 對應 `wPortStatus` / `wPortChange` 的摘要頁。 |
| Escalation Table | 對應 consuming repo 的 Standard Escalation Mode 觸發彙整。 |
| Glossary | 對應本 repo 的術語標準化頁。 |

## 建議保留英文的術語

| 首選術語 | 原因 |
|---|---|
| Transaction Translator (TT) | 這是穩定的 USB Hub 術語，翻譯常降低可識別性。 |
| TT Think Time | 作為欄位/群組名稱時建議保留英文。 |
| Port Indicator | 欄位名稱以英文為準，正文可補充中文解釋。 |

## 請求與欄位術語

| 首選術語 | 說明 |
|---|---|
| Feature Selector | 說明文可本地化，但欄位名稱與識別子仍保留 `feature_selector`。 |
| Descriptor Type | 作為請求欄位用語可本地化，request 名稱與字面值保留原文。 |
| Change Bit | 指 `wPortChange` / `wHubChange` 中的 latch event bits。 |
| Reserved Bit | 指規格保留位元，不能任意當作一般可用位元。 |
| Device-to-Host | 可用於 `bmRequestType` 方向摘要。 |
| Host-to-Device | 可用於 `bmRequestType` 方向摘要。 |

## 速度術語

| 首選術語 | 說明 |
|---|---|
| Low-speed | 可直接使用。 |
| Full-speed | 可直接使用。 |
| High-speed | 可直接使用。 |
| Combined speed decoding | 指 `PORT_LOW_SPEED` 與 `PORT_HIGH_SPEED` 的組合解讀。 |

## 描述符術語

| 首選術語 | 說明 |
|---|---|
| downstream port count | 用於描述 `bNbrPorts`。 |
| removable bitmap | `DeviceRemovable` 的高階描述。 |
| Power Switching Mode | descriptor 正文中的穩定用語。 |
| Over-current Protection Mode | descriptor 正文中的穩定用語。 |

## 邊界提醒

- 本頁只做術語標準化，不建立新的規格真值權威。
- 本頁不把術語選擇升級為 verified 或欄位驗證。
- 若 consuming repo 發現與 project fact 衝突，本頁內容不應覆蓋已確認事實，仍走 Standard Escalation Mode。
