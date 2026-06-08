---
title: SS Hub Interrupt Endpoint
claim_level: inferred
spec_family: usb3
status: review_required
last_reviewed: "2026-06-08"
usb_versions:
  - usb_3_2
source_refs:
  - usb32_spec
semantic_verification_claimed: false
---

# SS Hub Interrupt Endpoint

> 資料範圍：USB 3.2 Specification Rev 1.0，Section 10.15.1（SuperSpeed Hub Interrupt Endpoint Descriptor）。
> 本頁是消費端參考摘要，不是逐欄位 PDF 驗證紀錄。
> 治理矩陣：`tables/ss_hub_interrupt_endpoint_matrix.yaml`（4 個欄位，全部 verified）。

## 頁面目的

本頁回答：

- USB 3.x SS hub 的 status-change（interrupt）endpoint descriptor 有哪些欄位。
- `bInterval` 在 SuperSpeed hub 中的編碼方式（與 USB 2.0 的差異）。
- `wMaxPacketSize` 的最小值計算方式。

本頁不回答：

- Host 如何實際排程 interrupt polling。
- firmware 如何指定 endpoint 號碼或 bInterval 值。
- 真實 polling latency 保證。

## SS Hub Interrupt Endpoint 欄位摘要

| 欄位 | 限制 / 編碼 | Claim level |
|---|---|---|
| `bEndpointAddress` | bit7=1（IN 方向）；bits[3:0]=endpoint 號碼（firmware 定義） | **verified** |
| `bmAttributes` | bits[1:0]=0b11（Interrupt transfer type） | **verified** |
| `wMaxPacketSize` | ceil((bNbrPorts + 1) / 8) bytes 最小值 | **verified** |
| `bInterval` | 2^(bInterval-1) × 125 μs；bInterval 範圍 1–16 | **verified** |

Source: USB 3.2 Specification §10.15.1。

## bEndpointAddress

- **bit 7 必須為 1**（IN 方向；hub 回報 status change 給 host）。
- **bits[3:0]**：endpoint 號碼，由 hub firmware 定義，常見值為 1。
- 方向限制（IN）是 spec 要求；endpoint 號碼的實際分配是 firmware 行為，超出本頁 verified scope。

## bmAttributes

- **bits[1:0] = 0b11**：Interrupt transfer type。
- SS hub status-change endpoint 必須為 Interrupt endpoint。
- USB 3.x interrupt endpoint 的 burst 或 stream 行為超出本頁 verified scope。

## wMaxPacketSize

最小值計算：

```
wMaxPacketSize ≥ ceil((bNbrPorts + 1) / 8) bytes
```

其中 +1 代表 hub 本身的 status bit（hub device status change bit）。

| 下游 ports 數量 | 最小 wMaxPacketSize |
|---|---|
| 1–7 ports | 1 byte |
| 8–15 ports | 2 bytes |
| 16–23 ports | 3 bytes |

## bInterval（超速端點的 microframe 編碼）

| 模式 | 編碼 | 範圍 |
|---|---|---|
| SuperSpeed | 2^(bInterval-1) × 125 μs | bInterval 1–16 |

> **USB 3.x SS 與 USB 2.0 High-Speed 使用相同的 bInterval 編碼**（microframe-based，2^(n-1) × 125 μs）。
> USB 2.0 Full-Speed / Low-Speed 的直接 ms 編碼（1–255 ms）**不適用**於 SuperSpeed hub。

常見 bInterval 值對照：

| bInterval | 輪詢週期 |
|---|---|
| 1 | 125 μs |
| 4 | 1 ms |
| 8 | 16 ms |
| 12 | 256 ms |

## Verified Gate 說明

本治理矩陣（`tables/ss_hub_interrupt_endpoint_matrix.yaml`）的 verified gate 狀態：**PARTIAL（allowlist，全 4 筆已完成 verified promotion）**。

Verified scope：field identity 和 constraint encoding only。

Evidence packets: `evidence/entry_verification_packets/usb3/ss_iep_*.yaml`（4 筆）。

## 本頁不宣告

- Host 實際 interrupt polling 排程或 latency 保證。
- firmware endpoint address assignment 或 bInterval 選擇的正確性。
- USB 3.x interrupt endpoint burst 或 stream 行為。
- polling behavior 的 runtime 驗證。

→ [Verification Status](../verification_status.md)
