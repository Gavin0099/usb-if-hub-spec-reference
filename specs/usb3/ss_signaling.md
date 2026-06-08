---
title: SS Signaling
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

# SS Signaling

> 資料範圍：USB 3.2 Specification Rev 1.0，Section 6–7（Physical Layer / Link Layer）。
> 本頁是消費端參考摘要，不是電氣/訊號驗證紀錄。
> **重要**：本頁不宣告任何電氣合規性（electrical compliance）或 LTSSM behavior。

## 頁面目的

本頁回答：

- USB 3.x SuperSpeed 的主要訊號特性概述（物理層）。
- Gen 1 / Gen 2 的速度差異。
- LFPS（Low Frequency Periodic Signaling）的用途概述。

本頁不回答：

- 電氣規格（voltage, impedance, eye diagram）的合規性。
- LTSSM 訊號序列的 runtime behavior。
- USB-IF 訊號認證或測試標準。

## USB 3.x SuperSpeed 物理層概述

USB 3.x SuperSpeed 使用**差分序列（differential serial）**訊號傳輸，與 USB 2.0 的差分半雙工不同：

| 特性 | USB 2.0 High-Speed | USB 3.x SuperSpeed Gen 1 | USB 3.x SuperSpeed Gen 2 |
|---|---|---|---|
| 速率 | 480 Mbps | 5 Gbps | 10 Gbps |
| 編碼 | NRZI | 8b/10b | 128b/132b |
| 方向 | 半雙工 | **全雙工**（TX/RX 分離） |
| 物理層 | D+/D- 兩線 | SS TX+/TX- + SS RX+/RX-（四線） |

電氣規格值超出本頁 verified scope。

## LFPS（Low Frequency Periodic Signaling）

LFPS 是 USB 3.x 的低頻週期性訊號，用於：

- **Rx.Detect**：偵測 receiver 是否存在。
- **Polling.LFPS**：link training 啟動階段。
- **U1/U2 Exit**：從低功耗狀態喚醒。
- **U3 Exit（Remote Wake）**：從 Suspend 發起 remote wake。
- **Loopback / Compliance**：測試模式訊號。
- **Warm Reset**：BH reset 時使用 LFPS 序列。

LFPS 的訊號時序、電氣規格、LTSSM 狀態關聯行為超出本頁 verified scope。

## Gen 1 / Gen 2 差異

| 特性 | SuperSpeed Gen 1 | SuperSpeedPlus Gen 2 |
|---|---|---|
| 速率 | 5 Gbps | 10 Gbps per lane |
| 編碼 | 8b/10b | 128b/132b |
| 有效吞吐量 | ~500 MB/s | ~1250 MB/s（per lane） |
| 多通道 | 1x | 1x or 2x（Gen 2×2） |

有效吞吐量為理論值；實際性能超出本頁 verified scope。

## 本頁不宣告

- 電氣規格（voltage, impedance, eye diagram）合規性。
- LFPS 訊號時序或 LTSSM state machine behavior。
- USB-IF 訊號或互操作性認證。
- 實際吞吐量或延遲保證。
- firmware 或 hardware 訊號實作的正確性。

→ [SS Port State Machine](ss_port_state_machine.md) | [SS LPM](ss_lpm.md) | [Verification Status](../verification_status.md)
