---
title: 術語表
claim_level: inferred
status: review_required
last_reviewed: "2026-06-02"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# 術語表

> 本頁固定本 repo 的中英文術語寫法，用途是降低文件與 LLM 回答漂移，不代表額外的 USB 2.0 section-level verification。

## 使用原則

- 規格欄位名、request 名、bit 名保留原文：例如 `GET_STATUS`、`CLEAR_FEATURE`、`wHubCharacteristics`、`PORT_CONNECTION`。
- 第一次出現可採「中文 + 原文」；之後固定使用同一寫法。
- 若中文翻譯會降低技術精度，優先保留英文專有名詞。

## 核心術語

| 建議寫法 | 英文原文 | 使用說明 |
|---|---|---|
| Hub 類別請求 | Hub Class Requests | 用於 `specs/hub_class_requests.md` 一類頁面標題。 |
| Hub 描述符 | Hub Descriptor | 用於 class-specific hub descriptor。 |
| 連接埠狀態位元 | Port Status Bits | 用於 `wPortStatus` / `wPortChange` 的位元摘要頁。 |
| 升級觸發表 | Escalation Table | 對 consuming repo 的 Standard Escalation Mode 觸發條件摘要。 |
| 術語表 | Glossary | 用於固定本 repo 術語。 |

## 不建議硬翻的術語

| 建議寫法 | 不建議寫法 | 原因 |
|---|---|---|
| Transaction Translator（TT） | 交易轉換器 | 直譯可理解，但在 USB Hub 脈絡下容易失去專有名詞辨識度。 |
| TT Think Time | TT 思考時間 | 技術上是既有欄位名稱，硬翻容易誤導。 |
| Port Indicator | 連接埠指示燈 / 指示器 | 若上下文需要可補中文說明，但欄位名本身保留原文較穩定。 |

## request 與欄位術語

| 建議寫法 | 英文原文 | 使用說明 |
|---|---|---|
| 功能選擇器 | Feature Selector | 可作為正文翻譯；欄位名仍保留 `feature_selector`。 |
| 描述符類型 | Descriptor Type | 正文可翻，欄位值與 request 名保留原文。 |
| 變更位元 | Change Bit | 指 `wPortChange` / `wHubChange` 中的 latched event bits。 |
| 保留位元 | Reserved Bit | 指規格保留、不可任意重用的 bits。 |
| 裝置到主機 | Device-to-Host | `bmRequestType` 方向摘要可翻成中文。 |
| 主機到裝置 | Host-to-Device | `bmRequestType` 方向摘要可翻成中文。 |

## 速度相關術語

| 建議寫法 | 英文原文 | 使用說明 |
|---|---|---|
| 低速 | Low-speed | 可直接翻。 |
| 全速 | Full-speed | 可直接翻。 |
| 高速 | High-speed | 可直接翻。 |
| 速度組合判讀 | Combined speed decoding | 用於 `PORT_LOW_SPEED` / `PORT_HIGH_SPEED` 的合併解讀。 |

## descriptor 相關術語

| 建議寫法 | 英文原文 | 使用說明 |
|---|---|---|
| downstream port 數量 | downstream port count | 與 `bNbrPorts` 對應；保留 `downstream port` 可避免歧義。 |
| 可移除 bitmap | removable bitmap | 對 `DeviceRemovable` 的高層摘要。 |
| 電源切換模式 | Power Switching Mode | 可作正文翻譯。 |
| 過電流保護模式 | Over-current Protection Mode | 可作正文翻譯。 |

## 邊界提醒

- 本頁只固定術語，不建立新的規格真值。
- 本頁不把中文翻譯升級成 verified authority。
- consuming repo 若遇到 project fact 與本 repo 術語摘要衝突，仍應進入 Standard Escalation Mode。
