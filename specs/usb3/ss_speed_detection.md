---
title: SS Speed Detection
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

# SS Speed Detection

> 資料範圍：USB 3.2 Specification Rev 1.0，§6（Physical Layer）；USB 2.0 Specification，§7.1（Electrical）。
> 本頁是 SuperSpeed speed detection 機制的參考摘要，說明 LFPS 與 TSEQ 的角色，並對比 USB 2.0 HS Chirp。
> 本頁不宣告 LTSSM 行為已驗證、PHY 電氣規格已驗證、或 firmware compliance。

## 頁面目的

本頁回答：

- USB 3.x SuperSpeed 速度偵測的主要機制（LFPS、TSEQ）在 reference level 的差異。
- SS speed detection 與 USB 2.0 HS Chirp 的對比。

本頁不回答：

- LTSSM（Link Training and Status State Machine）完整狀態機行為。
- PHY 層電氣規格或 SS 眼圖要求。
- xHCI 如何管理 link training 序列。
- USB-IF 電氣或互操作性合規性測試。

## USB 2.0 HS 速度偵測（背景對比）

USB 2.0 高速偵測使用 **Chirp** 序列（在 USB reset 後進行）：

| 步驟 | 說明 |
|---|---|
| Chirp K | 裝置在 reset 後透過 D+/D- 差動線對發出 Chirp K |
| Chirp K/J 序列 | Host 以 Chirp K/J/K/J/K/J 回應確認 HS 能力 |
| HS 模式確認 | 雙方進入 High-Speed 模式（480 Mbps） |
| 回落 | 若 Chirp 交換未完成，裝置回落到 Full-Speed（12 Mbps） |

USB 2.0 Chirp 使用 D+/D-（USB 2.0 差動對）；速度偵測不需要獨立的 SS 物理層。

## USB 3.x SS 速度偵測

USB 3.x SuperSpeed 使用獨立的 SS 差動對（TX+/TX-/RX+/RX-），速度偵測機制不使用 Chirp：

### LFPS（Low-Frequency Periodic Signaling）

LFPS 是 SS link 在建立連線、電源狀態轉換、或喚醒時使用的低頻脈衝訊號：

| 特性 | 說明 |
|---|---|
| 頻率 | 10–50 MHz（遠低於 SS 5 Gbps 資料訊號） |
| 主要用途 | Link 狀態偵測（Polling 階段）；U1/U2/U3 → U0 喚醒觸發 |
| 實體媒介 | SS 差動對（TX+/TX-）；不使用 USB 2.0 D+/D- |
| Runtime scope | LFPS 的 runtime timing 與 LTSSM 狀態轉換超出本頁 verified scope |

LFPS 是 SS link training 起始與電源管理的基礎訊號機制，是 SS 與 USB 2.0 Chirp 在功能角色上的對應替換。

### TSEQ（Training Sequence EQ）

TSEQ 是 SS link training 中發送的均衡訓練序列：

| 特性 | 說明 |
|---|---|
| 格式 | 重複的 TSEQ ordered set（由 LTSSM Polling.RxEQ 狀態發送） |
| 用途 | 接收端均衡器訓練（equalizer training）；使接收端取得最佳訊號取樣點 |
| 訓練流程概要 | LFPS → TSEQ → TS1 → TS2 → U0（link training 完成） |
| Runtime scope | 完整 LTSSM 訓練流程超出本頁 verified scope |

TSEQ 電氣參數與詳細時序超出本頁 verified scope。

## SS vs USB 2.0 HS Speed Detection 比較

| 特性 | USB 2.0 HS | USB 3.x SS |
|---|---|---|
| 偵測機制 | Chirp K / Chirp K+J 交換 | LFPS + TSEQ（link training 序列） |
| 實體媒介 | D+/D-（USB 2.0 差動對） | TX+/TX-/RX+/RX-（SS 差動對，獨立） |
| 協商方式 | 差動驅動 + J/K 電壓 pattern | LTSSM Polling.LFPS → Polling.RxEQ → U0 |
| 回落機制 | 未完成 Chirp → Full-Speed（12 Mbps） | 未完成 SS link training → SS link 無法建立 |
| Hub 角色 | TT 速度橋接（HS 上行 / FS/LS 下行） | 無速度橋接；hub routing 只處理 SS |
| LTSSM | 不適用 | LTSSM 管理 link state；行為超出本頁 verified scope |

## 不宣告

- 本頁不宣告 LTSSM 狀態機行為已驗證。
- 本頁不宣告 LFPS 的 runtime timing 已驗證。
- 本頁不宣告 TSEQ 的電氣參數已驗證。
- 本頁不宣告 xHCI link training 行為已驗證。
- 本頁不宣告 USB-IF 電氣合規性測試結果。
- 本頁不宣告 SS link training 完整流程已被 firmware 實作驗證。
- 本頁不覆蓋 consuming repo 的確認專案事實。

→ [SS Signaling](ss_signaling.md) | [SS LPM](ss_lpm.md) | [SS No Transaction Translator](ss_no_transaction_translator.md) | [Verification Status](../verification_status.md)
