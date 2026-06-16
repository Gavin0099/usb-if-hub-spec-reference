---
title: Hub Interrupt Endpoint
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Interrupt Endpoint（Status Change Endpoint）

> 來源範圍：USB 2.0 Specification Rev 2.0，§11.13 / §11.15.1。  
> 本頁是 hub status change endpoint 的 reviewed reference summary；不是 firmware 或 driver 行為驗證。

## 頁面目的

本頁回答：

- Hub 為何需要一個 interrupt IN endpoint。
- Status change endpoint 的 descriptor 欄位（bEndpointAddress、bmAttributes、wMaxPacketSize、bInterval）代表什麼。
- wMaxPacketSize 的最小大小如何由 port 數計算。
- bInterval 在 FS 與 HS hub 之間的編碼差異。

本頁不回答：

- Host driver 的 interrupt 輪詢實作細節。
- Hub firmware 如何管理 status change bit 的 latching。
- Interrupt endpoint 是否在特定設備上已完成驗證。

## Status Change Endpoint 概述

Hub 必須實作一個 **interrupt IN endpoint**，稱為 status change endpoint（§11.13）。  
每當 hub 或任一 port 的 status 發生變化，hub 會透過此 endpoint 通知 host。

Host 透過 interrupt polling 週期性取得 status change 通知，格式如下：

- bit 0：hub 自身的 status 是否有變化（對應 `wHubStatus.C_*` bits）
- bit N（N ≥ 1）：port N 的 status 是否有變化（對應 `wPortChange` bits）

## Endpoint Descriptor 欄位

下表根據 `tables/hub_interrupt_endpoint_matrix.yaml` 整理：

| 欄位 | 規範要求 | 備註 |
|---|---|---|
| `bEndpointAddress` | bit 7=1（IN），bits\[3:0\]由實作決定 | endpoint number 常為 1 |
| `bmAttributes` | bits\[1:0\]=`0b11`（Interrupt 傳輸） | FS/LS hub bits\[7:2\]=0 |
| `wMaxPacketSize` | ≥ `ceil((bNbrPorts + 1) / 8)` bytes | 見下方計算說明 |
| `bInterval` | FS/LS: 1–255 ms；HS: 2^(n-1) × 125 µs（n=1–16） | 見下方速度差異說明 |

### `wMaxPacketSize` 計算

status change bitmap 需要：
- 1 bit for hub status change（bit 0）
- 1 bit per downstream port（bit N for port N）

因此需要至少 `ceil((bNbrPorts + 1) / 8)` bytes。

| `bNbrPorts` | 最小 `wMaxPacketSize` |
|---:|---:|
| 1–7 | 1 byte |
| 8–15 | 2 bytes |
| 16–23 | 3 bytes |
| 24–31 | 4 bytes |

實務上大多數 hub 的 port 數 ≤ 7，所以 1 byte 最常見。

### `bInterval` 速度差異

| Hub 速度 | `bInterval` 編碼 | 最小建議輪詢間隔 |
|---|---|---|
| Full-speed (FS) | 直接以 ms 表示，範圍 1–255 | 取決於 host 實作 |
| Low-speed (LS) | 同 FS | 同 FS |
| High-speed (HS) | 2^(bInterval-1) × 125 µs，bInterval 範圍 1–16 | 由 bInterval 決定 |

例：HS hub bInterval=6 表示輪詢間隔 = 2^(6-1) × 125 µs = 4000 µs = 4 ms。

## Status Change Bitmap 格式

Host 收到的 interrupt IN data 是一個 bitmap：

```
bit 0   : hub 本身的 status change（wHubStatus C_HUB_LOCAL_POWER 或 C_HUB_OVER_CURRENT）
bit 1   : port 1 的 status change（wPortChange 中任一 bit set）
bit 2   : port 2 的 status change
...
bit N   : port N 的 status change
```

Host 收到非零 bitmap 後，對相應的 port 或 hub 發送 `GET_STATUS` 請求（§11.24.2.6）以取得詳細狀態。

## Governed Linkage

- `tables/hub_interrupt_endpoint_matrix.yaml`：endpoint descriptor 欄位的 governed reviewed surface
- `specs/port_status_bits.md`：wPortChange 與 wHubChange bits 的定義
- `specs/hub_class_requests.md`：`GET_STATUS` hub/port 請求 family

## Non-claims

- 本頁不宣告任何 hub 的 interrupt endpoint 實作已經過驗證。
- 本頁不描述 host driver 的 interrupt 輪詢行為或 latency 保證。
- 本頁不覆蓋 consuming repo 已確認的 project facts。

## Reference Navigation

- specs/usb2.md: USB 2.0 topic index (zh).
- specs/en/hub_interrupt_endpoint.md: English counterpart topic (en).
