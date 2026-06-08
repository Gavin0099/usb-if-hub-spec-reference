---
title: SS Hub 無 Transaction Translator
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

# SS Hub 無 Transaction Translator

> 資料範圍：USB 3.2 Specification Rev 1.0，§10、§11（Hub Class）；USB 2.0 Specification，§11.14（Transaction Translator）。
> 本頁說明 SuperSpeed hub 為何不使用 Transaction Translator（TT），並對比 USB 2.0 TT 的架構差異。

## 頁面目的

本頁回答：

- USB 2.0 Transaction Translator 的存在原因及其架構角色。
- SuperSpeed hub 不需要 TT 的原因。
- SS hub 省去 TT 後，描述符欄位的具體差異。

本頁不回答：

- TT 的 runtime transaction timing 或 Split Transaction 詳細流程。
- xHCI 如何管理 SS hub 下的 TT-less device enumeration。
- USB-IF TT 合規性測試。
- FS/LS 裝置連接 SS hub 的行為（SS hub 不支援 FS/LS 直接連接）。

## USB 2.0 Transaction Translator 的角色

USB 2.0 hub 在連接 High-Speed（HS）上游 host 與 Full-Speed / Low-Speed（FS/LS）下游裝置時，需要 Transaction Translator（TT）進行速度域橋接：

| 功能 | 說明 |
|---|---|
| 速度域轉換 | HS host 與 FS/LS device 無法直接通訊；TT 做速度橋接 |
| Split Transaction | Host 發出 SSPLIT/CSPLIT Token；TT 在 FS/LS 速度域完成傳輸後回報 |
| TT Think Time | `wHubCharacteristics[6:5]` 記錄 TT 完成一次 FS 傳輸所需的最大 HS microframe 數 |

USB 2.0 Hub Descriptor（type 0x29）包含 TT Think Time 欄位，`bDeviceProtocol` 以 `0x01`（Single TT）或 `0x02`（Multiple TT）標識 TT 類型。

## SuperSpeed Hub 不含 TT

SuperSpeed（USB 3.x）hub 的所有下游端口均以 SuperSpeed 運作，不存在速度域轉換需求：

| 特性 | USB 2.0 Hub（HS-capable） | USB 3.x SS Hub |
|---|---|---|
| 下游端口速度 | HS + FS/LS（混合） | SS only |
| TT 需求 | 是（FS/LS 裝置需要 TT） | **否** |
| Split Transaction | 需要（SSPLIT/CSPLIT Token） | **不存在** |
| TT Think Time 欄位 | `wHubCharacteristics[6:5]` 有效 | **無此欄位**（SS Hub Descriptor 不含 TT） |
| `bDeviceProtocol` | `0x01` / `0x02`（Single/Multiple TT） | **`0x03`**（SS hub，無 TT） |

## 描述符差異

### `bDeviceProtocol`（Device Descriptor）

| 值 | 說明 |
|---|---|
| `0x00` | Root hub 或 Full-Speed-only hub |
| `0x01` | USB 2.0 hub，Single Transaction Translator |
| `0x02` | USB 2.0 hub，Multiple Transaction Translators |
| `0x03` | **USB 3.x SuperSpeed hub（無 TT）** |

### Hub Descriptor 類型

| 規格 | Descriptor Type | TT Think Time 欄位 |
|---|---|---|
| USB 2.0 | `0x29` | `wHubCharacteristics[6:5]`：有效 |
| USB 3.x | **`0x2A`** | **不存在**（SS Hub Descriptor 無 TT 欄位） |

### `wHubCharacteristics` 位元佈局差異

| 位元 | USB 2.0 Hub | USB 3.x SS Hub |
|---|---|---|
| `[1:0]` | Power Switching Mode | Power Switching Mode（相同） |
| `[2]` | Compound Device | Compound Device（相同） |
| `[4:3]` | Over-current Protection Mode | Over-current Protection Mode（相同） |
| `[6:5]` | **TT Think Time** | **Reserved**（SS hub 無 TT Think Time） |
| `[7]` | Port Indicators | **Reserved**（USB 3.x hub 此位移位） |
| `[5]` | Reserved | **Port Indicators**（USB 3.x hub 移至 bit[5]） |

## 不宣告

- 本頁不宣告 TT 的 runtime transaction timing 已驗證。
- 本頁不宣告 xHCI 對 TT-less hub 的處理行為已驗證。
- 本頁不宣告 USB-IF TT 測試合規性。
- 本頁不宣告 FS/LS 裝置連接 SS hub 的行為（SS hub 不支援 FS/LS 直接連接）。
- 本頁不覆蓋 consuming repo 的確認專案事實。

## Governed Linkage

- `tables/ss_hub_characteristics_bit_matrix.yaml`：`usb3_ss_whc_port_indicators`（bit[5]）、`usb3_ss_whc_reserved_high`（TT Think Time bits 不存在）— verified
- [SS Hub Descriptor](ss_hub_descriptor.md)：`bDeviceProtocol = 0x03`，SS Hub Descriptor type 0x2A
- [SS Hub Characteristics](ss_hub_characteristics.md)：`wHubCharacteristics` 位元佈局（USB3 vs USB2）
- [SS Transactions](ss_transactions.md)：Split Transaction 在 SS 環境下不存在

→ [SS Hub Characteristics](ss_hub_characteristics.md) | [SS Transactions](ss_transactions.md) | [SS Hub Descriptor](ss_hub_descriptor.md) | [Verification Status](../verification_status.md)
