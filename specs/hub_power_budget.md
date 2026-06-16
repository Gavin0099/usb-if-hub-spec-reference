---
title: Hub Power Budget
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Power Budget

> 來源範圍：USB 2.0 Specification Rev 2.0，§11.11。  
> 本頁是 USB 2.0 hub 電源預算規則的 reviewed reference summary——自供電 vs. 匯流排供電操作、每 port 電流限制與 `bHubContrCurrent`。

## 頁面目的

本頁回答：

- 自供電 hub 與匯流排供電 hub 有何不同。
- Hub 可以從 USB 匯流排汲取多少電流，以及為其 port 提供多少電流。
- `bHubContrCurrent` 和 `bMaxPower` 在 hub 電源計算中扮演什麼角色。

## 自供電 vs. 匯流排供電 Hub

| 屬性 | 自供電 Hub | 匯流排供電 Hub |
|---|---|---|
| 電源來源 | 外部（變壓器或內部電源）| USB 匯流排（上行 port 的 VBUS）|
| `bmAttributes bit 6`（config descriptor）| `1` | `0` |
| 每下行 port 最大電流 | 500 mA | 100 mA（或 ganged power 時 500 mA）|
| config descriptor 中的 `bMaxPower` | Hub 匯流排電流消耗 / 2（mA）| Hub 匯流排電流消耗 / 2（mA）|
| 典型 `bMaxPower` | 低（僅 hub controller）| 最高 250（= 500 mA 總計）|

Hub 在 configuration descriptor 的 `bmAttributes bit 6` 中廣告其電源類型。Host 可以此決定 port 電源分配。

## 每 Port 電流限制（§11.11）

### 配置前（Default 狀態）

- USB 設備在 `SET_CONFIGURATION` 前最多從 port 汲取 **100 mA**。
- 這也適用於 host 發出 `SET_CONFIGURATION` 之前的 hub 本身。

### 配置後

- 自供電 hub 每下行 port 最多可提供 **500 mA**。
- 匯流排供電 hub 受限於其總可用匯流排電源；通常每 port **100 mA**。
- Host 根據下行設備 configuration descriptor 中的 `bMaxPower` 分配每 port 電源。

## `bHubContrCurrent`

`bHubContrCurrent` 是 hub class descriptor（非 configuration descriptor）中的欄位：

- 單位：**mA**（直接毫安值，不是 ×2）。
- 含義：hub controller 本身從 VBUS 汲取的最大電流（不含下行設備）。
- 供 host 電源預算計算使用。

自供電 hub 的 `bHubContrCurrent` 可能為 0（hub 從自己的電源汲取，不從 USB 匯流排）。  
匯流排供電 hub 應反映實際 hub controller 消耗量。

## `bMaxPower`（Configuration Descriptor）

Configuration descriptor 中的 `bMaxPower`：

- 單位：**每 LSB 2 mA**（乘以 2 得到 mA）。
- 含義：hub（整個設備）在配置時從 VBUS 汲取的最大電流。
- 自供電 hub：通常低（僅 hub 電子元件）。
- 匯流排供電 hub：`bHubContrCurrent` + （ports × 估計每 port 消耗）的總和。

## 電源預算範例

**匯流排供電 hub，4 個 port：**

```
上行 host port 可用 VBUS 電流：500 mA
Hub controller 消耗（bHubContrCurrent）：50 mA
下行 port 可用：500 - 50 = 450 mA
每 port 可用（4 個 port）：約 112 mA（受 USB 規格限制為 100 mA）
```

**自供電 hub，7 個 port：**

```
外部電源提供：3500 mA（7 × 500 mA）
Hub controller 消耗：100 mA（來自電源）
匯流排消耗（bMaxPower × 2）：例如 10 mA（僅 hub controller 來自 USB）
每 port 可提供：500 mA（來自電源）
```

## 過電流與電源切換的關係

電源預算與 `wHubCharacteristics[4:3]` 中的過電流保護模式相關：

- **全域過電流**（`00`）：hub 監控總電流，超出時切斷所有 port。
- **每 port 過電流**（`01`）：hub 獨立監控每個 port，僅切斷受影響的 port。

電源切換與過電流保護模式詳見 `specs/hub_power_management.md`。

## Governed Linkage

- `specs/hub_descriptor.md`：hub class descriptor 中的 `bHubContrCurrent` 欄位
- `specs/hub_power_management.md`：電源切換模式、`bPwrOn2PwrGood`、過電流
- `specs/standard_descriptors.md`：configuration descriptor 中的 `bMaxPower` 和 `bmAttributes`
- `specs/hub_configuration.md`：情境中的 hub configuration descriptor 結構

## Non-claims

- 本頁不宣告電源預算計算已針對實體 hub 驗證。
- 本頁不宣告 host 電源分配演算法已 implementation-verified。
- 本頁不定義 USB-IF 認證電源要求。
- 本頁不覆蓋 consuming repo 已確認的 project facts。

## Reference Navigation

- specs/usb2.md: USB 2.0 topic index (zh).
- specs/en/hub_power_budget.md: English counterpart topic (en).
