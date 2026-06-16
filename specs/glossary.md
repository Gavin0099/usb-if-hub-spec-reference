---
title: Glossary
claim_level: inferred
status: review_required
last_reviewed: "2026-06-08"
usb_versions:
  - usb_2_0
  - usb_3_2
source_refs:
  - usb20_spec
  - usb32_spec
semantic_verification_claimed: false
---

# Glossary

> 本頁用來統一本 repo 的術語使用方式，以降低文件與 LLM 回答的 drift。  
> 它不會新增 USB 2.0 的 section-level verification。

## Usage Rules

- 規格中的 field names、request names 與 bit names 盡量保留原始形式，例如 `GET_STATUS`、`CLEAR_FEATURE`、`wHubCharacteristics`、`PORT_CONNECTION`。
- 第一次出現時可同時給中英文說明；之後應固定使用同一個術語。
- 如果翻譯會降低技術精準度，就保留原始英文術語。

## Core Terms

| Preferred Term | Notes |
|---|---|
| Hub Class Requests | 用於 `specs/hub_class_requests.md` 這類 request-family 頁面。 |
| Hub Descriptor | 用於 class-specific hub descriptor。 |
| Port Status Bits | 用於 `wPortStatus` / `wPortChange` 的摘要頁。 |
| Escalation Table | 用於 Standard Escalation Mode 的 trigger summaries。 |
| Glossary | 用於 repo-level 術語正規化。 |

## Terms Kept in English

| Preferred Term | Reason |
|---|---|
| Transaction Translator (TT) | 這是穩定的 USB hub 術語；直接翻譯通常會降低辨識度。 |
| TT Think Time | 這已被視為固定的 field/group 名稱。 |
| Port Indicator | 保留英文欄位名通常更清楚；必要時可在正文補本地說明。 |

## Request and Field Terms

| Preferred Term | Notes |
|---|---|
| Feature Selector | 正文可視情況翻成「功能選擇值」，但 field identifier 仍維持 `feature_selector`。 |
| Descriptor Type | 可作為一般敘述用語；request 名稱與 literal values 保持不變。 |
| Change Bit | 指 `wPortChange` / `wHubChange` 中 latched event bits。 |
| Reserved Bit | 指規格保留、不可隨意重用的位元。 |
| Device-to-Host | 可安全用於 `bmRequestType` direction summaries。 |
| Host-to-Device | 可安全用於 `bmRequestType` direction summaries。 |

## Speed Terms

| Preferred Term | Notes |
|---|---|
| Low-speed | 可直接使用。 |
| Full-speed | 可直接使用。 |
| High-speed | 可直接使用。 |
| Combined speed decoding | 用於描述 `PORT_LOW_SPEED` 與 `PORT_HIGH_SPEED` 的聯合解讀方式。 |

## Descriptor Terms

| Preferred Term | Notes |
|---|---|
| downstream port count | 用於描述 `bNbrPorts`。 |
| removable bitmap | `DeviceRemovable` 的高層摘要說法。 |
| Power Switching Mode | 可安全用於 descriptor prose。 |
| Over-current Protection Mode | 可安全用於 descriptor prose。 |

## USB 3.x / SuperSpeed 術語

| 偏好用語 | 說明 |
|---|---|
| SS / SuperSpeed | USB 3.x 速率，指 Gen 1 5Gbps 或 Gen 2 10Gbps 的 SuperSpeed 模式。 |
| SSP / SuperSpeed Plus | USB 3.2 Gen 2 10Gbps 或 Gen 2×2 20Gbps；USB 3.1/3.2 的高速變體。 |
| BOS（Binary Device Object Store） | USB 3.x 必需的描述符（type 0x0F）；由 GET_DESCRIPTOR(BOS) 取得；包含 Device Capability Descriptor。 |
| LPM（Link Power Management） | SS 鏈路電源管理；包含 U1/U2 自動轉換（短暫待機）與 U3 暫停（Suspend）。 |
| U0 / U1 / U2 / U3 | SS 鏈路電源狀態：U0 = Active、U1 = Idle（短延遲）、U2 = Idle（較長延遲）、U3 = Suspend。 |
| LFPS（Low-Frequency Periodic Signaling） | SS link 電源狀態轉換與喚醒的低頻脈衝訊號；由 LTSSM 管理，runtime timing 超出本 repo verified scope。 |
| TSEQ（Training Sequence EQ） | SS link training 的均衡訓練 ordered set；LTSSM Polling.RxEQ 階段使用；詳細 timing 超出本 repo verified scope。 |
| ITP（Isochronous Timestamp Packet） | SS 等時傳輸的同步時間戳記封包，取代 USB 2.0 SOF（Start of Frame）。 |
| NRDY / ERDY | SS 端點流量控制封包：NRDY = 端點未就緒（Not Ready）；ERDY = 端點主動通知就緒（Endpoint Ready）。 |
| SET_HUB_DEPTH | SS-only hub 請求；在 SET_CONFIGURATION 後強制發送，設定 hub 在 SS 路由樹中的深度。 |

## Boundary Reminder

- 本頁只統一用語，不建立新的 spec truth。
- 本頁不會把術語選擇升級成 verified authority。
- 若 consuming repo 發現 project facts 與本 repo 的 terminology summary 衝突，仍應套用 Standard Escalation Mode。

## Reference Navigation

- specs/usb2.md: USB 2.0 topic index (zh).
- specs/en/glossary.md: English counterpart topic (en).
