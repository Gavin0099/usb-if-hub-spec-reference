---
title: Hub 類別請求
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub 類別請求

> 來源：USB 2.0 規格書 Revision 2.0，第 11.24.2 節
> 用途：僅供語意參考層使用。不可用於覆蓋已確認的專案事實。

## 請求摘要

| bRequest | 值 | 傳輸方向 | 說明 |
|----------|---|---------|------|
| GET_STATUS | 0x00 | 裝置→主機 | 取得 Hub 或連接埠狀態 |
| CLEAR_FEATURE | 0x01 | 主機→裝置 | 清除 Hub 或連接埠功能旗標 |
| SET_FEATURE | 0x03 | 主機→裝置 | 設定 Hub 或連接埠功能旗標 |
| GET_DESCRIPTOR | 0x06 | 裝置→主機 | 取得 Hub 描述符 |
| SET_DESCRIPTOR | 0x07 | 主機→裝置 | 設定 Hub 描述符 |
| CLEAR_TT_BUFFER | 0x08 | 主機→裝置 | 清除 TT 緩衝區 |
| RESET_TT | 0x09 | 主機→裝置 | 重置 TT |
| GET_TT_STATE | 0x0A | 裝置→主機 | 取得 TT 狀態 |
| STOP_TT | 0x0B | 主機→裝置 | 停止 TT |

## Hub 功能選擇器（Feature Selectors）

| 功能 | Selector 值 | 接收對象 |
|-----|-------------|---------|
| C_HUB_LOCAL_POWER | 0 | Hub |
| C_HUB_OVER_CURRENT | 1 | Hub |
| PORT_CONNECTION | 0 | 連接埠 |
| PORT_ENABLE | 1 | 連接埠 |
| PORT_SUSPEND | 2 | 連接埠 |
| PORT_OVER_CURRENT | 3 | 連接埠 |
| PORT_RESET | 4 | 連接埠 |
| PORT_POWER | 8 | 連接埠 |
| PORT_LOW_SPEED | 9 | 連接埠 |
| C_PORT_CONNECTION | 16 | 連接埠 |
| C_PORT_ENABLE | 17 | 連接埠 |
| C_PORT_SUSPEND | 18 | 連接埠 |
| C_PORT_OVER_CURRENT | 19 | 連接埠 |
| C_PORT_RESET | 20 | 連接埠 |
| PORT_TEST | 21 | 連接埠 |
| PORT_INDICATOR | 22 | 連接埠 |

## GET_DESCRIPTOR（Hub 描述符）

- bmRequestType: 1010 0000b（0xA0）
- bRequest: GET_DESCRIPTOR（0x06）
- wValue: 0x2900（Hub 描述符型別）
- wIndex: 0x0000
- wLength: 描述符長度

## 廠商命令邊界

USB-IF Hub 類別請求的 selector 值上限為 22（PORT_INDICATOR）。
超出本表的請求碼或 selector 均為廠商自訂，必須在專案的
廠商命令協議規格中記錄。

## 標準衝突說明

- 所有 USB Hub 依規格須支援 Hub 型別（0x29）的 GET_DESCRIPTOR。
  若專案不支援，須標記為 Standards Compliance Risk。
- CLEAR_TT_BUFFER 與 RESET_TT 僅適用於含內嵌 TT 的 Hub。
  不含 TT 的全速專用 Hub 控制器可省略這兩個請求。

---

## 請求家族說明

> **claim_level: inferred** — 內容依 USB 2.0 規格書 §11.24.2 推論。
> **semantic_verification_claimed: false** — 位元層級行為與時序未經驗證。
> **來源參考：** usb20_spec（規範性 — 本頁未直接驗證）。

### GET_STATUS

**用途：** 回傳 Hub 或指定連接埠的狀態資訊，包含目前狀態位元與變更指示位元。

**傳輸方向：** 裝置→主機。

**目標：** Hub（wIndex=0）或特定連接埠（wIndex=1 起始的連接埠號）。

**回應：** 4 位元組 — 2 位元組狀態欄位 + 2 位元組變更欄位。Hub 目標：wHubStatus + wHubChange。連接埠目標：wPortStatus + wPortChange。

**治理表格連結：**
- `class_request_matrix`：GET_STATUS（usb20_get_status_hub、usb20_get_status_port）
- `port_status_bit_matrix`：目標為連接埠時，wPortStatus/wPortChange 的位元定義

**非聲明項目：** 本節不驗證回應位元佈局、時序或錯誤行為。位元層級語意須進行 PDF 章節審查（Phase 6）。

---

### CLEAR_FEATURE

**用途：** 清除功能旗標 — 通常用於重置 Hub 或連接埠的變更指示位元。

**傳輸方向：** 主機→裝置，無資料階段。

**目標：** Hub（功能選擇器作用於 Hub）或連接埠（功能選擇器作用於指定連接埠號）。

**功能選擇器：** 透過 wValue 傳入。Hub 選擇器包含 C_HUB_LOCAL_POWER 與 C_HUB_OVER_CURRENT。連接埠變更選擇器包含 C_PORT_CONNECTION、C_PORT_ENABLE、C_PORT_SUSPEND、C_PORT_OVER_CURRENT 與 C_PORT_RESET。

**治理表格連結：**
- `class_request_matrix`：CLEAR_FEATURE（usb20_clear_feature_hub、usb20_clear_feature_port）
- `feature_selector_matrix`：有效 selector 值及各 selector 的接收對象限制

**非聲明項目：** 本節不驗證哪些 selector 為必要或選擇性，或對不支援 selector 的錯誤行為。

---

### SET_FEATURE

**用途：** 在 Hub 或連接埠上設定或啟用功能（例如觸發 PORT_RESET 或啟用 PORT_POWER）。

**傳輸方向：** 主機→裝置，無資料階段。

**目標：** 依功能選擇器決定作用於 Hub 或連接埠。

**功能選擇器：** 透過 wValue 傳入。連接埠功能包含 PORT_CONNECTION、PORT_ENABLE、PORT_SUSPEND、PORT_OVER_CURRENT、PORT_RESET、PORT_POWER、PORT_LOW_SPEED、PORT_TEST 與 PORT_INDICATOR。

**治理表格連結：**
- `class_request_matrix`：SET_FEATURE（usb20_set_feature_hub、usb20_set_feature_port）
- `feature_selector_matrix`：有效 selector 值及各 selector 的接收對象限制

**非聲明項目：** 本節不驗證功能啟用時序、副作用或必要回應行為。

---

### GET_DESCRIPTOR（Hub 類別）

**用途：** 取得 Hub 類別描述符，包含連接埠數量、電源特性與過電流保護模式等 Hub 特定組態資訊。

**傳輸方向：** 裝置→主機。

**目標：** Hub 裝置。

**背景說明：** 此為 Hub 類別專用的 GET_DESCRIPTOR（bmRequestType type=class，wValue 高位元組=0x29 Hub 描述符型別），透過 bmRequestType 的請求型別欄位與標準 USB GET_DESCRIPTOR 區分。

**治理表格連結：**
- `class_request_matrix`：GET_DESCRIPTOR（usb20_get_descriptor_hub，request_context: hub_class_specific）

**非聲明項目：** Hub 描述符欄位佈局及必要/選擇性欄位須進行 PDF 章節審查。wValue 與 wLength 編碼在表格中為 spec_defined。

---

### SET_DESCRIPTOR（Hub 類別）

**用途：** 選擇性寫入或更新 Hub 描述符。依 USB 2.0 規格書，實作支援並非強制。

**傳輸方向：** 主機→裝置。

**目標：** Hub 裝置。

**背景說明：** Hub 類別專用情境。Hub 可對此請求回傳 STALL 而不違反規格。勿與標準 USB SET_DESCRIPTOR 混淆。

**治理表格連結：**
- `class_request_matrix`：SET_DESCRIPTOR（usb20_set_descriptor_hub，request_context: hub_class_specific）

**非聲明項目：** SET_DESCRIPTOR 的必要支援條件與有效負載結構為 spec_defined，本節未驗證。

---

### CLEAR_TT_BUFFER

**用途：** 指示 Hub 的內嵌 Transaction Translator 丟棄特定端點/裝置組合的緩衝交易。用於從分割交易錯誤中恢復。

**傳輸方向：** 主機→裝置，無資料階段。

**目標：** TT 連接埠情境 — TT 連接埠號透過 wIndex 傳入。

**適用條件：** 僅適用於含內嵌 Transaction Translator 的高速 Hub。全速 Hub 及不含 TT 的 Hub 不得接收此請求。

**治理表格連結：**
- `class_request_matrix`：CLEAR_TT_BUFFER（usb20_clear_tt_buffer，applies_to: hub_with_tt_only）

**非聲明項目：** wValue 與 wIndex 欄位編碼在表格項目中為 spec_defined。TT 緩衝區語意須進行 PDF 章節審查。

---

### RESET_TT

**用途：** 重置 Transaction Translator，中止所有待處理的分割交易。用於錯誤恢復序列。

**傳輸方向：** 主機→裝置，無資料階段。

**目標：** wIndex 中指定的 TT 連接埠號。

**適用條件：** 僅適用於含內嵌 TT 的高速 Hub。

**治理表格連結：**
- `class_request_matrix`：RESET_TT（usb20_reset_tt，applies_to: hub_with_tt_only）

**非聲明項目：** TT 連接埠情境編碼及重置前的交易完成要求為 spec_defined，本節未驗證。

---

### GET_TT_STATE

**用途：** 從 Transaction Translator 取得診斷狀態資訊，用於 TT 診斷或錯誤分析工具。

**傳輸方向：** 裝置→主機。

**目標：** TT 連接埠情境 — wIndex 攜帶 TT 連接埠/情境識別碼。

**適用條件：** 僅適用於含內嵌 TT 的高速 Hub。

**治理表格連結：**
- `class_request_matrix`：GET_TT_STATE（usb20_get_tt_state，applies_to: hub_with_tt_only）

**非聲明項目：** wLength（TT 狀態資料有效負載大小）及狀態資料格式在表格項目中為 spec_defined，本節未驗證。

---

### STOP_TT

**用途：** 停止 Transaction Translator 在指定 TT 連接埠上處理分割交易，作為 RESET_TT 的受控停機對應操作。

**傳輸方向：** 主機→裝置，無資料階段。

**目標：** wIndex 中的 TT 連接埠號。

**適用條件：** 僅適用於含內嵌 TT 的高速 Hub。

**治理表格連結：**
- `class_request_matrix`：STOP_TT（usb20_stop_tt，applies_to: hub_with_tt_only）

**非聲明項目：** TT 連接埠情境編碼為 spec_defined，本節未驗證。
