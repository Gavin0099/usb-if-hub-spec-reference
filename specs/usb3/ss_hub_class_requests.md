---
title: SS Hub Class Requests
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

# SS Hub Class Requests

> 資料範圍：USB 3.2 Specification Rev 1.0，Section 10.14.2（Hub Class Requests for SuperSpeed）。  
> 本頁是消費端參考摘要，不是逐請求 PDF 驗證紀錄。

## 頁面目的

本頁回答：

- USB 3.x SS hub 新增的兩個 hub class requests：`SET_HUB_DEPTH` 和 `GET_PORT_ERR_COUNT`。
- 哪些 USB 2.0 hub requests 在 SS hub 中不適用。
- SS hub 專用的 feature selectors（U1/U2/BH reset 相關）。

本頁不回答：

- xHCI host controller 如何驅動這些請求的內部實作。
- 每個請求是否已在特定 firmware 中驗證為正確實作。

## SS 新增 Hub Class Requests

### SET_HUB_DEPTH（0x0C）

| 欄位 | 值 |
|---|---|
| bmRequestType | 0x20（class, device, host-to-device） |
| bRequest | 0x0C |
| wValue | Hub depth（0 = root hub 或直接連接 root hub 的 hub，最大 5） |
| wIndex | 0 |
| wLength | 0 |

**用途**：通知 hub 其在 SS bus topology 中的層次深度。xHCI 在配置 hub 時必須先發送此請求。SS hub 最多支援 5 層（root hub = 0，最後一層 hub = 5）。**SS hub 必須支援此請求（mandatory）。**

### GET_PORT_ERR_COUNT（0x0D）

| 欄位 | 值 |
|---|---|
| bmRequestType | 0xA0（class, device, device-to-host） |
| bRequest | 0x0D |
| wValue | 0 |
| wIndex | 端口號碼 |
| wLength | 2 |

**用途**：讀取指定端口的 link error count（16-bit），讀取後重置為 0。可用於診斷鏈路品質問題。**SS hub 可選支援此請求（optional）。**

## 不適用於 SS Hub 的請求

以下 USB 2.0 hub class requests 在 SS hub 中不適用，原因是 SS hub 不含 TT（Transaction Translator）：

| 請求 | bRequest | 不適用原因 |
|---|---|---|
| CLEAR_TT_BUFFER | 0x08 | SS hub 無 TT |
| RESET_TT | 0x09 | SS hub 無 TT |
| GET_TT_STATE | 0x0A | SS hub 無 TT |
| STOP_TT | 0x0B | SS hub 無 TT |

SET_FEATURE PORT_SUSPEND / CLEAR_FEATURE PORT_SUSPEND 亦不適用：SS hub 以 U1/U2 policy 取代 suspend。

## SS 專用 Feature Selectors

以下 feature selectors 為 USB 3.x SS hub 新增或重新定義，與 USB 2.0 不同：

| Selector 名稱 | 值 | 說明 |
|---|---|---|
| PORT_U1_TIMEOUT | 0x23 | 設定 U1 entry timeout（host 觸發） |
| PORT_U2_TIMEOUT | 0x24 | 設定 U2 entry timeout（host 觸發） |
| PORT_BH_PORT_RESET | 0x1C | 觸發 Warm Reset（BH Port Reset） |
| C_PORT_LINK_STATE | 0x19 | 清除 C_PORT_LINK_STATE change bit |
| C_PORT_CONFIG_ERROR | 0x1E | 清除 C_PORT_CONFIG_ERROR change bit |

## 與 USB 2.0 共用的請求

以下請求 SS hub 與 USB 2.0 hub 共用，語意大致相容：

| 請求 | 說明 |
|---|---|
| GET_STATUS（hub/port） | 取得 hub 或端口狀態（SS 端口狀態 layout 不同，見 SS Port Status Bits 頁面） |
| SET_FEATURE / CLEAR_FEATURE（hub/port） | 設定或清除功能（SS 有新增 selectors） |
| GET_DESCRIPTOR / SET_DESCRIPTOR | 取得或設定 hub descriptor（SS 使用 0x2A descriptor） |

## Non-claims

- 不宣告 SET_HUB_DEPTH 的 hub depth 計算方式已在任何 firmware 中驗證為正確。
- 不宣告 xHCI 與 SS hub 之間的完整 request 交互序列。
- 不宣告 U1/U2 timeout policy 的最佳實踐或合規要求。
