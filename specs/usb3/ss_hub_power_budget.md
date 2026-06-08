---
title: SS Hub 電源預算
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

# SS Hub 電源預算

> 來源範圍：USB 3.2 Specification Rev 1.0，§10.14.2 / §11.4。
> 本頁是 USB 3.x SS hub 電源預算規則的 reviewed reference summary——自供電 vs. 匯流排供電操作、每 port 電流限制、`bHubContrCurrent`、以及 USB 3.x 與 USB 2.0 的主要差異。

## 頁面目的

本頁回答：

- USB 3.x SS hub 每 port 最大可提供多少電流。
- 自供電 vs. 匯流排供電 SS hub 的電源規則。
- `bHubContrCurrent`、`bMaxPower`、`bPwrOn2PwrGood` 在 SS hub context 中的角色。

本頁不回答：

- USB Power Delivery（USB PD）協定 —— 這是與 USB hub class 分離的獨立標準。
- USB Battery Charging（BC 1.2）—— 另一獨立標準。
- 任何特定 hub 的實際電源預算是否符合規格。

## 自供電 vs. 匯流排供電 SS Hub

| 屬性 | 自供電 SS Hub | 匯流排供電 SS Hub |
|---|---|---|
| 電源來源 | 外部（變壓器或內部電源）| USB 匯流排（上行 port 的 VBUS）|
| `bmAttributes bit 6`（config descriptor）| `1` | `0` |
| 每下行 port 最大電流 | **900 mA** | **150 mA**（配置後）|
| 配置前（Default 狀態）| 每 port ≤ 150 mA | 每 port ≤ 150 mA |

**USB 3.x 與 USB 2.0 的關鍵差異**：
- USB 2.0 自供電 hub：每 port 最多 **500 mA**
- USB 3.x 自供電 hub：每 port 最多 **900 mA**
- USB 2.0 匯流排供電 hub：每 port 最多 **100 mA**
- USB 3.x 匯流排供電 hub：每 port 最多 **150 mA**（Default/配置前），配置後依 bMaxPower

## 每 Port 電流限制

### 配置前（Default 狀態）

USB 3.x 設備在 `SET_CONFIGURATION` 前從 port 汲取的最大電流：
- **150 mA**（USB 3.x；vs USB 2.0 的 100 mA）

### 配置後

| Hub 類型 | 每 port 最大電流 |
|---|---|
| 自供電 SS hub | **900 mA** |
| 匯流排供電 SS hub | 依 bMaxPower（通常 ≤ 900 mA，受上行 VBUS 限制）|

## `bHubContrCurrent`（SS Hub Descriptor 中）

`bHubContrCurrent` 欄位在 SS Hub Descriptor（type 0x2A）中：

- 單位：**mA**（直接毫安值，不是 ×2）。
- 含義：hub controller 本身從 VBUS 汲取的最大電流（不含下行設備電流）。
- 自供電 SS hub 的 `bHubContrCurrent` 可能為 0 或小值（hub 電子從自己電源取電）。

## `bMaxPower`（Configuration Descriptor 中）

Configuration Descriptor 的 `bMaxPower`：

- 單位：**每 LSB 2 mA**（乘以 2 得到 mA），與 USB 2.0 相同。
- 含義：hub 整個設備在配置時從 VBUS 汲取的最大電流。
- 自供電 SS hub：通常低（僅 hub 電子元件消耗）。
- 匯流排供電 SS hub：hub controller 電流 + 預期下行設備電流之和。

## `bPwrOn2PwrGood`（SS Hub Descriptor 中）

`bPwrOn2PwrGood` 欄位與 USB 2.0 Hub Descriptor 中的同名欄位編碼相同：

- 單位：**每 LSB 2 ms**（乘以 2 得到毫秒）。
- 含義：從 port power-on 到 port power 穩定（可進行 reset）的等待時間。
- Host 在 `SET_FEATURE(PORT_POWER)` 後等待 `bPwrOn2PwrGood × 2ms` 再繼續操作。

## 電源預算範例

**自供電 SS hub，4 個 port（最大配置）：**

```
外部電源可用電流：3600 mA（4 × 900 mA）
Hub controller 消耗（bHubContrCurrent）：100 mA
每 port 最大：900 mA（自供電）
VBUS 匯流排消耗（bMaxPower × 2）：例如 10 mA
```

**匯流排供電 SS hub，4 個 port（受限配置）：**

```
上行 SS port 可用 VBUS 電流：900 mA
Hub controller 消耗：50 mA
下行 port 可用：850 mA
每 port 典型：約 200 mA（受上行限制）
```

## 過電流保護與電源切換

SS hub 的過電流保護模式由 `wHubCharacteristics bits[4:3]` 控制（與 USB 2.0 相同位置）：

| bits[4:3] | 模式 |
|---|---|
| `00` | 全域過電流：hub 監控總電流，超出時切斷所有 port |
| `01` | 每 port 過電流：hub 獨立監控每個 port，僅切斷超出的 port |
| `10` | 無過電流保護（不建議）|

電源切換和 OCP 模式的 bit identity 已透過 `usb3_ss_whc_power_switching` 和 `usb3_ss_whc_over_current_mode` evidence packet 驗證（位元名稱和值 identity only）。

## 與 USB 2.0 的差異

| 面向 | USB 2.0 Hub | USB 3.x SS Hub |
|---|---|---|
| 每 port 最大電流（自供電）| 500 mA | **900 mA** |
| 每 port 最大電流（匯流排供電）| 100 mA | **150 mA**（配置前），依 bMaxPower（配置後）|
| Default 狀態最大電流 | 100 mA | **150 mA** |
| `bHubContrCurrent` 欄位位置 | Hub Descriptor（type 0x29）| SS Hub Descriptor（type 0x2A）|
| 電源預算框架 | §11.11 | §11.4（類似框架，更高電流）|

## Governed Linkage

- `specs/usb3/ss_hub_descriptor.md`：SS hub descriptor 欄位（bHubContrCurrent、bPwrOn2PwrGood）
- `specs/usb3/ss_hub_power.md`：SS hub 電源管理模式（U1/U2/U3 省電）
- `tables/ss_hub_characteristics_bit_matrix.yaml`：power switching 和 OCP mode bit identity — verified
- `specs/usb3/ss_hub_configuration.md`：bmAttributes bit 6（自供電旗標）

## Non-claims

- 本頁不宣告電源預算計算已針對實體 SS hub 驗證。
- 本頁不宣告 host 電源分配演算法已 implementation-verified。
- 本頁不定義 USB-IF 認證電源要求。
- 本頁不涵蓋 USB Power Delivery（USB PD）或 Battery Charging（BC 1.2）標準。
- 本頁不覆蓋 consuming repo 已確認的 project facts。

→ [SS Hub Power Management](ss_hub_power.md) | [SS Hub Descriptor](ss_hub_descriptor.md) | [Verification Status](../verification_status.md)
