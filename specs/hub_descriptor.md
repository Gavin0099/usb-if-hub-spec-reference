---
title: Hub 描述符欄位
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub 描述符欄位

> 來源：USB 2.0 規格書 Revision 2.0，第 11.23.2.1 節
> 用途：僅供語意參考層使用。不可用於覆蓋已確認的專案事實。

## Hub 描述符格式

Hub 描述符由 GET_DESCRIPTOR 請求（Descriptor Type = 0x29，Hub）回傳。

| 偏移 | 欄位 | 大小（位元組）| 說明 |
|------|------|-------------|------|
| 0 | bDescLength | 1 | 此描述符的位元組總數 |
| 1 | bDescriptorType | 1 | Hub 描述符型別（0x29） |
| 2 | bNbrPorts | 1 | 下行連接埠數量 |
| 3 | wHubCharacteristics | 2 | Hub 特性（見下表） |
| 5 | bPwrOn2PwrGood | 1 | 電源開啟至穩定所需時間（單位：2ms） |
| 6 | bHubContrCurrent | 1 | Hub 控制器最大電流需求（mA） |
| 7 | DeviceRemovable | 可變 | 指示各連接埠是否連接不可拔除裝置 |
| 7+x | PortPwrCtrlMask | 可變 | 保留（設定為 0xFF） |

## wHubCharacteristics 位元定義

| 位元 | 欄位 | 數值說明 |
|------|------|---------|
| 1:0 | Logical Power Switching Mode | 00=群組切換, 01=個別連接埠, 10-11=保留 |
| 2 | Compound Device | 0=非複合裝置, 1=複合裝置 |
| 4:3 | Over-current Protection Mode | 00=全域, 01=個別連接埠, 10-11=無過電流保護 |
| 6:5 | TT Think Time | 00=8 FS 位元時間, 01=16, 10=24, 11=32 |
| 7 | Port Indicators Supported | 0=不支援, 1=支援 |
| 15:8 | 保留 | 0 |

## 標準衝突說明

- `bNbrPorts` 為標準欄位。若韌體使用的連接埠數與此欄位不符，
  須觸發 Standard Escalation Mode。
- `bPwrOn2PwrGood` 時序為專案特定值，不可用通用數值覆蓋。
- `wHubCharacteristics[1:0]` 電源切換模式，必須與專案已確認的
  電源切換事實相符。若有衝突 → 觸發升級。
