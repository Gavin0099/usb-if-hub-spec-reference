---
title: SuperSpeed Hub Descriptor
claim_level: inferred
spec_family: usb3
status: review_required
last_reviewed: "2026-06-07"
usb_versions:
  - usb_3_2
source_refs:
  - usb32_spec
semantic_verification_claimed: false
---

# SuperSpeed Hub Descriptor

> 資料範圍：USB 3.2 Specification Rev 1.0，Section 10.14.2.1。  
> 本頁是消費端參考摘要，不是逐欄位 PDF 驗證紀錄。

## 頁面目的

本頁回答：

- SuperSpeed hub descriptor 的欄位有哪些，以及與 USB 2.0 hub descriptor 的差異。
- `wHubCharacteristics` 在 USB 3.x 下的位元定義（無 TT Think Time 欄位）。
- `bHubDecLat` 與 `wHubDelay` 新增欄位的用途。

本頁不回答：

- 是否某個 firmware descriptor dump 已逐位元驗證。
- 是否某個 SS hub 實作在此處視為正確。

## 欄位總覽

| Offset | 欄位 | 大小 | 說明 |
|---|---|---|---|
| 0 | bLength | 1B | Descriptor 總長度（最小 12B，不含 DeviceRemovable 時） |
| 1 | bDescriptorType | 1B | **0x2A**（SuperSpeed Hub Descriptor，USB 2.0 為 0x29） |
| 2 | bNbrPorts | 1B | 下游端口數量，最大 15 |
| 3 | wHubCharacteristics | 2B | Hub 特性位元欄位（見下表） |
| 5 | bPwrOn2PwrGood | 1B | 電源接通到穩定的等待時間，單位 2ms |
| 6 | bHubContrCurrent | 1B | Hub controller 最大消耗電流（mA） |
| 7 | bHubDecLat | 1B | Hub packet header decode latency，單位 0.1μs（root hub 填 0） |
| 8 | wHubDelay | 2B | Hub 增加的平均延遲（ns），用於 U1/U2 exit latency 計算 |
| 10 | DeviceRemovable | 可變長度 | 每個端口 1 bit，bit N=1 表示端口 N+1 不可拆除 |

## wHubCharacteristics 位元定義（USB 3.x）

| 位元 | 欄位 | 說明 |
|---|---|---|
| bits[1:0] | Logical Power Switching Mode | 00b=整體切換，01b=單口切換，10b/11b=不支援切換 |
| bit[2] | Compound Device | 0=獨立裝置，1=複合裝置 |
| bits[4:3] | Over-Current Protection Mode | 00b=整體保護，01b=單口保護，10b/11b=不提供保護 |
| bit[5] | Port Indicators Supported | 0=不支援，1=支援 PORT_INDICATOR feature |
| bits[15:6] | Reserved | 必須為 0 |

## 與 USB 2.0 hub descriptor 的差異

| 差異點 | USB 2.0（0x29） | USB 3.x（0x2A） |
|---|---|---|
| bDescriptorType | 0x29 | **0x2A** |
| TT Think Time（wHubCharacteristics bits[9:8]） | 有（8/16/24/32 FS bit times） | **無**（SS hub 無 TT） |
| Port Indicators bit | bit[7] | **bit[5]** |
| PortPwrCtrlMask 欄位 | 有（USB 2.0 semantics: all 0xFF） | **無** |
| bHubDecLat | 無 | **新增**：封包 header decode latency |
| wHubDelay | 無 | **新增**：U1/U2 exit latency 計算用 |

## bHubDecLat 與 wHubDelay 用途說明

- **bHubDecLat**：hub 解碼 packet header 所需的延遲，單位 0.1μs。用於系統計算整體 U1/U2 exit latency budget。Root hub 填 0。
- **wHubDelay**：hub 增加的平均傳播延遲（ns）。xHCI 使用此值計算 U1/U2 entry 的允許延遲預算。典型值：200–400 ns。

## Non-claims

- 不宣告此頁覆蓋所有 SS hub descriptor 欄位的完整語意驗證。
- 不宣告 bHubDecLat / wHubDelay 的具體數值是否已在 firmware 中正確實作。
- 不宣告 USB 3.x hub descriptor 的電氣或互通性符合規範。
