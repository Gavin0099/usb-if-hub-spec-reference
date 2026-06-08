---
title: SS Packet Types
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

# SS Packet Types

> 資料範圍：USB 3.2 Specification Rev 1.0，Section 7.2–8（Link Layer Packets）。
> 本頁是消費端參考摘要，不是封包格式或 protocol behavior 驗證紀錄。

## 頁面目的

本頁回答：

- USB 3.x SuperSpeed 的主要封包類型有哪些。
- SS 封包結構與 USB 2.0 封包的主要差異。
- Hub 相關的封包類型。

本頁不回答：

- 每個封包欄位的 bit-level 格式驗證。
- 封包 routing、flow control、或 retry 機制的 runtime behavior。
- USB-IF 封包合規性或互操作性測試。

## USB 3.x SuperSpeed 主要封包類型

USB 3.x SuperSpeed 使用與 USB 2.0 完全不同的封包格式。主要封包類型（based on USB 3.2 Section 7.2）：

### Link Layer Packets (LLP)

| 封包類型 | 縮寫 | 用途 |
|---|---|---|
| Link Management Packet | LMP | Link 初始化、capability exchange、設定 |
| Transaction Packet | TP | 事務控制（ACK, NRDY, ERDY, STATUS 等） |
| Data Packet | DP | 資料負載傳輸 |
| Isochronous Timestamp Packet | ITP | 等時傳輸的時間戳記 |

### Transaction Packets (TP) 細分

| TP 類型 | 用途 |
|---|---|
| ACK | 確認成功接收 |
| NRDY | 端點尚未就緒（背壓） |
| ERDY | 端點就緒通知（主動喚醒） |
| STATUS | 控制傳輸狀態階段 |
| STALL | 端點停止回應 |
| DEV_NOTIFICATION | 裝置通知 host（U1/U2 policy, function wake 等） |
| PING / PING_RESPONSE | 延遲測量（latency measurement） |

## 與 USB 2.0 封包的主要差異

| 特性 | USB 2.0 | USB 3.x SuperSpeed |
|---|---|---|
| Token/Data/Handshake 結構 | SOF + Token + Data + Handshake | TP + DP（無獨立 Token） |
| Transaction Translator | 需要（HS hub 對 FS/LS 的橋接） | **不需要**（SS 為純 packet-based） |
| 多封包確認 | 每個封包個別 ACK | Link Layer 提供流量控制 |
| 等時傳輸 | SOF timing | ITP（Isochronous Timestamp Packet） |

## Hub 相關的封包

SS hub 在 link layer 扮演封包 routing 的角色：

- Hub 將 downstream transaction packets 路由到對應的 port。
- Hub 聚合 upstream 的 status change interrupt endpoint 封包。
- Hub 不像 USB 2.0 TT hub 那樣需要在 HS/FS 速度域之間進行事務拆分（USB 3.x 無 TT）。

Hub 封包 routing 的 runtime behavior 超出本頁 verified scope。

## 本頁不宣告

- 每個封包欄位的 bit-level 格式驗證。
- 封包 routing、flow control、或 retry 機制的 runtime behavior。
- Link layer state machine 或 LTSSM 行為。
- USB-IF 封包合規性或互操作性測試。
- firmware 封包處理實作的正確性。

→ [SS Transactions](ss_transactions.md) | [SS Signaling](ss_signaling.md) | [Verification Status](../verification_status.md)
