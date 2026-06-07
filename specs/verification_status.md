---
title: Verification Status
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
semantic_verification_claimed: false
---

# Verification Status

> 本頁是靜態的 visibility summary，不是自動生成的 source of truth。  
> 真正受治理的權威來源仍是 YAML tables 與 evidence packets。  
> 只要 table entries 或 packet status 有變動，這頁數字就必須手動同步更新。

## Current Verification Summary

| Area | Tracked entries | Verified | Reviewed | Inferred | Missing |
|---|---:|---:|---:|---:|---:|
| Hub descriptor fields | 8 | 8 | 0 | 0 | 0 |
| Transaction Translator entries | 10 | 10 | 0 | 0 | 0 |
| Escalation triggers | 10 | 10 | 0 | 0 | 0 |
| Class requests | 12 | 12 | 0 | 0 | 0 |
| Feature selectors | 25 | 25 | 0 | 0 | 0 |
| Port status bits | 64 | 19 | 45 | 0 | 0 |
| Hub interrupt endpoint | 4 | 4 | 0 | 0 | 0 |
| Standard device requests | 12 | 12 | 0 | 0 | 0 |
| wHubCharacteristics bit groups | 6 | 5 | 1 | 0 | 0 |
| **Total** | **151** | **105** | **46** | **0** | **0** |

## Evidence Packet Summary

| Artifact type | Count | Status |
|---|---:|---|
| Entry verification packets | 105 | 全部對應到已 promoted 的 verified entries；46 個 reviewed entries 無 evidence packet |

名詞定義：

- **Verified**：已通過 entry-level promotion gate；`claim_level: verified`；scope 有明確邊界。
- **Reviewed**：repo-local review 已完成，surface 已收斂成較清楚的 field role、selector boundary 或 request linkage，但尚未升級為 entry-level verified。
- **Inferred**：已整理但尚未完成 reviewed 或 verified；`claim_level: inferred`。

## Coverage Map

| Area | Current maturity center | Notes |
|---|---|---|
| Hub descriptor fields | verified | 全部 8 個 tracked hub descriptor fields 都已完成 descriptor field identity verified；這不代表 descriptor dumps 或 device behavior 已驗證 |
| Transaction Translator entries | verified | 全部 10 個 tracked TT type、think-time、request-linkage entries 已完成 entry-level verified |
| Escalation triggers | verified | 全部 10 個 tracked E-01 到 E-10 trigger boundaries 已完成 entry-level verified |
| Class requests | verified | 全部 12 個 tracked class requests 都已完成 request-linkage-only verified promotion |
| Feature selectors | verified | 全部 25 個 tracked feature selectors 已完成 selector-name/value scope 的 entry-level verified promotion |
| Port status bits | verified / reviewed | 19 個核心 hub/port status-change bits 已完成 entry-level verified promotion；4 個 high-bit boundary placeholders 為 reviewed；41 個 reserved bit entries 已完成 reviewed namespace boundary |
| Hub interrupt endpoint | verified | 4 個 status change endpoint descriptor 欄位（bEndpointAddress, bmAttributes, wMaxPacketSize, bInterval）已完成 entry-level verified promotion（descriptor field identity scope）|
| Standard device requests | verified | 12 個適用於 hub 的標準 USB 設備請求已完成 entry-level verified promotion（request-linkage identity scope）|
| wHubCharacteristics bit groups | verified / reviewed | 5 個 wHubCharacteristics bit groups（power switching、compound device、OC mode、TT think time、port indicators）已完成 entry-level verified promotion（bit-group name and value-encoding identity scope）；1 個 reserved high-bit boundary 為永久 reviewed |

## Reviewed Surface Inventory

剩餘的 45 個 `reviewed` entries 屬於**永久邊界**，不是未完成的升級缺口。

### 1 筆 wHubCharacteristics reserved high-byte boundary（無語意可驗證，不可升級）

- `usb20_whc_reserved_high`（wHubCharacteristics bits[15:8]，規格定義 reserved，shall be zero）

### 4 筆 Port/Hub status-change high-bit boundary placeholders（無語意可驗證，不可升級）

這四筆是刻意設計的命名空間封閉 entries，用於封閉各 status word 的高位元邊界，不代表真實的 USB 2.0 bit 定義：

- `PORT_STATUS_HIGH_BIT_BOUNDARY`（wPortStatus bit 15 命名空間封閉）
- `PORT_CHANGE_HIGH_BIT_BOUNDARY`（wPortChange bit 15 命名空間封閉）
- `HUB_STATUS_HIGH_BIT_BOUNDARY`（wHubStatus bit 15 命名空間封閉）
- `HUB_CHANGE_HIGH_BIT_BOUNDARY`（wHubChange bit 15 命名空間封閉）

### 41 筆 Reserved bit namespace boundaries（語意已封板，不應升 verified）

USB 2.0 §11.24 / Table 11-19 明確定義以下 bit positions 為 reserved（shall be zero）。這些 entries 的 `reviewed` 狀態代表「規格位置已明確，無行為語意可進一步驗證」，不代表驗證缺口：

- wPortStatus reserved：BIT5, BIT6, BIT7, BIT13, BIT14（5 筆）
- wPortChange reserved：BIT5–BIT14（10 筆）
- wHubStatus reserved：BIT2–BIT14（13 筆）
- wHubChange reserved：BIT2–BIT14（13 筆）

**這 45 筆 reviewed entries 是正確的終態。** 將它們升為 verified 不會增加語意覆蓋，因為 reserved bits 沒有行為語意可驗證，boundary placeholder entries 也不是真實 bit 定義。

## Verified Entries

目前共有 105 個 entries 已完成 verified promotion（`claim_level: verified`）：

| Entry | Field | Bit | Verified Scope |
|---|---|---|---|
| bDescLength | `wHubDescriptor.bDescLength` | - | descriptor field identity only |
| bDescriptorType | `wHubDescriptor.bDescriptorType` | - | descriptor field identity only |
| bNbrPorts | `wHubDescriptor.bNbrPorts` | - | descriptor field identity only |
| wHubCharacteristics | `wHubDescriptor.wHubCharacteristics` | - | descriptor field identity only |
| bPwrOn2PwrGood | `wHubDescriptor.bPwrOn2PwrGood` | - | descriptor field identity only |
| bHubContrCurrent | `wHubDescriptor.bHubContrCurrent` | - | descriptor field identity only |
| DeviceRemovable | `wHubDescriptor.DeviceRemovable` | - | descriptor field identity only |
| PortPwrCtrlMask | `wHubDescriptor.PortPwrCtrlMask` | - | descriptor field identity only |
| PORT_CONNECTION | `wPortStatus` | bit 0 | bit name and bit position only |
| PORT_ENABLE | `wPortStatus` | bit 1 | bit name and bit position only |
| PORT_SUSPEND | `wPortStatus` | bit 2 | bit name and bit position only |
| PORT_OVER_CURRENT | `wPortStatus` | bit 3 | bit name and bit position only |
| PORT_RESET | `wPortStatus` | bit 4 | bit name and bit position only |
| PORT_POWER | `wPortStatus` | bit 8 | bit name and bit position only |
| PORT_LOW_SPEED | `wPortStatus` | bit 9 | bit name and bit position only |
| PORT_HIGH_SPEED | `wPortStatus` | bit 10 | bit name and bit position only |
| PORT_TEST | `wPortStatus` | bit 11 | bit name and bit position only |
| PORT_INDICATOR | `wPortStatus` | bit 12 | bit name and bit position only |
| C_PORT_CONNECTION | `wPortChange` | bit 0 | bit name and bit position only |
| C_PORT_ENABLE | `wPortChange` | bit 1 | bit name and bit position only |
| C_PORT_SUSPEND | `wPortChange` | bit 2 | bit name and bit position only |
| C_PORT_OVER_CURRENT | `wPortChange` | bit 3 | bit name and bit position only |
| C_PORT_RESET | `wPortChange` | bit 4 | bit name and bit position only |
| HUB_LOCAL_POWER | `wHubStatus` | bit 0 | bit name and bit position only |
| HUB_OVER_CURRENT | `wHubStatus` | bit 1 | bit name and bit position only |
| C_HUB_LOCAL_POWER | `wHubChange` | bit 0 | bit name and bit position only |
| C_HUB_OVER_CURRENT | `wHubChange` | bit 1 | bit name and bit position only |
| usb20_get_status_hub | `GET_STATUS` hub recipient | - | request linkage only |
| usb20_get_status_port | `GET_STATUS` port recipient | - | request linkage only |
| usb20_set_feature_hub | `SET_FEATURE` hub recipient | - | request linkage only |
| usb20_set_feature_port | `SET_FEATURE` port recipient | - | request linkage only |
| usb20_clear_feature_hub | `CLEAR_FEATURE` hub recipient | - | request linkage only |
| usb20_clear_feature_port | `CLEAR_FEATURE` port recipient | - | request linkage only |
| usb20_clear_tt_buffer | `CLEAR_TT_BUFFER` TT-capable hub recipient | - | request linkage only |
| usb20_reset_tt | `RESET_TT` TT-capable hub recipient | - | request linkage only |
| usb20_get_tt_state | `GET_TT_STATE` TT-capable hub recipient | - | request linkage only |
| usb20_stop_tt | `STOP_TT` TT-capable hub recipient | - | request linkage only |
| usb20_get_descriptor_hub | `GET_DESCRIPTOR` hub recipient | - | request linkage only |
| usb20_set_descriptor_hub | `SET_DESCRIPTOR` hub recipient | - | request linkage only |
| usb20_std_get_status_device | `GET_STATUS` device recipient | - | request linkage only |
| usb20_std_get_status_interface | `GET_STATUS` interface recipient | - | request linkage only |
| usb20_std_get_status_endpoint | `GET_STATUS` endpoint recipient | - | request linkage only |
| usb20_std_clear_feature_device | `CLEAR_FEATURE` device recipient | - | request linkage only |
| usb20_std_clear_feature_endpoint | `CLEAR_FEATURE` endpoint recipient | - | request linkage only |
| usb20_std_set_feature_device | `SET_FEATURE` device recipient | - | request linkage only |
| usb20_std_set_address | `SET_ADDRESS` device recipient | - | request linkage only |
| usb20_std_get_descriptor | `GET_DESCRIPTOR` device recipient | - | request linkage only |
| usb20_std_get_configuration | `GET_CONFIGURATION` device recipient | - | request linkage only |
| usb20_std_set_configuration | `SET_CONFIGURATION` device recipient | - | request linkage only |
| usb20_std_get_interface | `GET_INTERFACE` interface recipient | - | request linkage only |
| usb20_std_set_interface | `SET_INTERFACE` interface recipient | - | request linkage only |
| usb20_hub_ep_bEndpointAddress | `bEndpointAddress` hub status-change EP | - | descriptor field identity only |
| usb20_hub_ep_bmAttributes | `bmAttributes` hub status-change EP | - | descriptor field identity only |
| usb20_hub_ep_wMaxPacketSize | `wMaxPacketSize` hub status-change EP | - | descriptor field identity only |
| usb20_hub_ep_bInterval | `bInterval` hub status-change EP | - | descriptor field identity only |
| usb20_whc_power_switching | `wHubCharacteristics` | bits[1:0] | bit-group name and value-encoding identity only |
| usb20_whc_compound_device | `wHubCharacteristics` | bit[2] | bit-group name and value-encoding identity only |
| usb20_whc_over_current_mode | `wHubCharacteristics` | bits[4:3] | bit-group name and value-encoding identity only |
| usb20_whc_tt_think_time | `wHubCharacteristics` | bits[6:5] | bit-group name and value-encoding identity only |
| usb20_whc_port_indicators | `wHubCharacteristics` | bit[7] | bit-group name and value-encoding identity only |
| usb20_tt_type_single | `wHubCharacteristics` | - | TT type boundary only |
| usb20_tt_type_multiple | `wHubCharacteristics` | - | TT type boundary only |
| usb20_tt_think_time_00 | `wHubCharacteristics` | 00 | TT think-time boundary only |
| usb20_tt_think_time_01 | `wHubCharacteristics` | 01 | TT think-time boundary only |
| usb20_tt_think_time_10 | `wHubCharacteristics` | 10 | TT think-time boundary only |
| usb20_tt_think_time_11 | `wHubCharacteristics` | 11 | TT think-time boundary only |
| usb20_tt_request_clear_tt_buffer | `hub_class_request` | - | TT request-linkage boundary only |
| usb20_tt_request_reset_tt | `hub_class_request` | - | TT request-linkage boundary only |
| usb20_tt_request_get_tt_state | `hub_class_request` | - | TT request-linkage boundary only |
| usb20_tt_request_stop_tt | `hub_class_request` | - | TT request-linkage boundary only |
| E-01 | `Escalation trigger` | - | escalation trigger boundary only |
| E-02 | `Escalation trigger` | - | escalation trigger boundary only |
| E-03 | `Escalation trigger` | - | escalation trigger boundary only |
| E-04 | `Escalation trigger` | - | escalation trigger boundary only |
| E-05 | `Escalation trigger` | - | escalation trigger boundary only |
| E-06 | `Escalation trigger` | - | escalation trigger boundary only |
| E-07 | `Escalation trigger` | - | escalation trigger boundary only |
| E-08 | `Escalation trigger` | - | escalation trigger boundary only |
| E-09 | `Escalation trigger` | - | escalation trigger boundary only |
| E-10 | `Escalation trigger` | - | escalation trigger boundary only |

| C_HUB_LOCAL_POWER | `feature_selector_matrix` | 0 | selector name and value only |
| C_HUB_OVER_CURRENT | `feature_selector_matrix` | 1 | selector name and value only |
| PORT_CONNECTION | `feature_selector_matrix` | 0 | selector name and value only |
| PORT_ENABLE | `feature_selector_matrix` | 1 | selector name and value only |
| PORT_SUSPEND | `feature_selector_matrix` | 2 | selector name and value only |
| PORT_OVER_CURRENT | `feature_selector_matrix` | 3 | selector name and value only |
| PORT_RESET | `feature_selector_matrix` | 4 | selector name and value only |
| reserved | `feature_selector_matrix` | 5 | selector name and value only |
| reserved | `feature_selector_matrix` | 6 | selector name and value only |
| reserved | `feature_selector_matrix` | 7 | selector name and value only |
| PORT_POWER | `feature_selector_matrix` | 8 | selector name and value only |
| PORT_LOW_SPEED | `feature_selector_matrix` | 9 | selector name and value only |
| PORT_HIGH_SPEED | `feature_selector_matrix` | 10 | selector name and value only |
| reserved | `feature_selector_matrix` | 11 | selector name and value only |
| reserved | `feature_selector_matrix` | 12 | selector name and value only |
| reserved | `feature_selector_matrix` | 13 | selector name and value only |
| reserved | `feature_selector_matrix` | 14 | selector name and value only |
| reserved | `feature_selector_matrix` | 15 | selector name and value only |
| C_PORT_CONNECTION | `feature_selector_matrix` | 16 | selector name and value only |
| C_PORT_ENABLE | `feature_selector_matrix` | 17 | selector name and value only |
| C_PORT_SUSPEND | `feature_selector_matrix` | 18 | selector name and value only |
| C_PORT_OVER_CURRENT | `feature_selector_matrix` | 19 | selector name and value only |
| C_PORT_RESET | `feature_selector_matrix` | 20 | selector name and value only |
| PORT_TEST | `feature_selector_matrix` | 21 | selector name and value only |
| PORT_INDICATOR | `feature_selector_matrix` | 22 | selector name and value only |

所有 verified entries 的 verified scope 都明確限制在各表列欄位中指定的範圍（selector name/value、bit name 和 bit position）。

以下內容對所有 entries 都仍然在 verified scope 之外：

- Timing behavior
- State transition behavior
- `SET_FEATURE` behavior
- `CLEAR_FEATURE` behavior
- Error recovery conditions
- Host-stack interpretation
- Full USB 2.0 compliance

## USB 3.x Governed Surface Statistics

> USB 3.x entries 與 evidence packets 獨立追蹤，**不計入** USB 2.0 151/105/46 freeze 統計。

| Area | Tracked entries | Verified | Reviewed | Inferred | Missing |
|---|---:|---:|---:|---:|---:|
| SS hub descriptor fields | 9 | 9 | 0 | 0 | 0 |
| SS hub class requests | 10 | 10 | 0 | 0 | 0 |
| SS port status bits | 19 | 15 | 4 | 0 | 0 |
| **USB 3.x Total** | **38** | **34** | **4** | **0** | **0** |

| Artifact type | Count | Status |
|---|---:|---|
| USB 3.x evidence packets | 34 | `evidence/entry_verification_packets/usb3/`；9 筆對應 SS hub descriptor (USB3-3A)，10 筆對應 SS hub class requests (USB3-3B)，15 筆對應 SS port status bits (USB3-3C) |

SS port status bit matrix 已完成 USB3-3C pilot：15 個 defined entries 升為 verified（bit name and position/range identity only）；4 個 reserved boundary entries 維持 reviewed（永久邊界）。

## What This Page Does Not Claim

本頁不宣告：

- USB 2.0 hub behavior 已全面 verified。
- 任何 page-level 或 table-level verification 已完成。
- `PORT_ENABLE` state machine、`SET_FEATURE`、`CLEAR_FEATURE` 或 error recovery behavior 已驗證。
- Reviewed entries 可以直接當 implementation truth 使用。
- Reviewed coverage 等同於 verified coverage。
- 本 reference 可以覆蓋 consuming repositories 中已確認的 project facts。
- 這些靜態數字已與 YAML tables 自動同步，並可作為 source of truth。

## USB 3.x Governed Matrix Closeout State（獨立於 USB 2.0 統計）

以下統計**與 USB 2.0 的 151/105/46 完全獨立**，不加入 USB 2.0 總數。

| Table | Tracked | Verified | Reviewed | State |
|---|---:|---:|---:|---|
| SS port status bits | 19 | 15 | 4 | **CLOSED**（15/19 defined verified；4 reserved boundary，永久邊界） |
| SS hub class requests | 10 | 10 | 0 | **CLOSED**（10/10 verified） |
| SS hub descriptor fields | 9 | 9 | 0 | **CLOSED**（9/9 verified） |
| **USB 3.x total** | **38** | **34** | **4** | matrix-level closeout |

USB 3.x 三張 matrices 均已達 matrix-level closeout。34 個 entries 已完成 entry-level verified promotion；4 個 reserved boundary entries 維持 reviewed（永久邊界，無語意可驗證）。

### USB 3.x Governed Matrix Closeout Details

目前 USB 3.x governed matrix surface 已進入穩定狀態（Phase USB3-3C 完成後）：

- **三張 matrix 的 defined entries 全部完成 entry-level verified promotion**：SS hub descriptor 9/9、SS hub class requests 10/10、SS port status/change bits 15/19。
- **剩餘 4 個 reviewed entries 均為 reserved boundary**，不是未完成的升級缺口：wPortStatus bit4、bit15；wPortChange bit1、bits[15:7]。
- **不存在任何 defined USB 3.x matrix entry 仍在 pending semantic promotion**。

### USB 3.x Non-Claims（固定邊界）

以下內容對所有 USB 3.x entries 均在 verified scope 之外，**無論現在或未來**：

- 不宣告 LTSSM runtime state transition behavior 已驗證。
- 不宣告 xHCI port state management 或 xHCI enumeration behavior 已驗證。
- 不宣告 SuperSpeed hub firmware compliance truth。
- 不宣告電氣、時序、或互操作性合規（electrical / timing / interoperability）。
- 不宣告 USB-IF certification completeness。
- `PORT_LINK_STATE` verified scope **僅限** bit range [8:5] 與 12-value encoding table identity；不涵蓋 LTSSM transition behavior 或 U-state 語意。
- `PORT_SPEED` verified scope **僅限** bit range [12:10] 與 6-value encoding table identity；不涵蓋 speed detection hardware 或 link training outcome。
- USB 3.x reference surface 僅涵蓋目前三張 governed matrix；**不是完整的 USB 3.x spec coverage**，也不等同於 USB 2.0 的 28 topic pairs reference surface。
- USB 3.x entries 不算入 USB 2.0 evidence packet count（USB 2.0 維持 105 packets）。

## Export Contract Surface

Hub governed surface 現在已有完整的 machine-readable export contract，供 consuming repo CI 使用。

| 元件 | 路徑 | 角色 |
|---|---|---|
| Unified manifest | `exports/hub_governed_surface_manifest.yaml` | Governed truth index：12 張 tables 的 authority surface、claim ceiling、consumer usage contract |
| Fingerprint baseline | `evidence/table_fingerprint_baseline.jsonl` | 12 張 governed tables 的 content-hash baseline，用於 CI drift detection |
| Consumer contract | `docs/CONSUMER_INTEGRATION_CONTRACT.md` | Allowed / forbidden usage、failure interpretation、governance layer model |
| Manifest validator | `scripts/validate_hub_governed_surface_manifest.py` | manifest summary 與實際 table entries 的一致性 gate（R1–R8） |
| Fingerprint probe | `scripts/probe_table_fingerprint.py --mode check` | Table content drift gate（exit 1 + 指名 drifted table） |
| Consumer smoke | `scripts/smoke_consumer_integration_fixtures.py` | Smoke-tested：manifest PASS、no-drift PASS、drift FAIL with table attribution |

**Consuming repo 兩步 CI gate：**

```
步驟 1  python scripts/validate_hub_governed_surface_manifest.py
        → PASS: 12 tables, usb20 freeze, usb3 matrix_level_closeout

步驟 2  python scripts/probe_table_fingerprint.py --mode check \
          --manifest exports/hub_governed_surface_manifest.yaml \
          --baseline-in evidence/table_fingerprint_baseline.jsonl
        → PASS: 12 tables, 0 drift
```

**Export contract non-claims：**
- 不代表 firmware compliance truth
- 不代表 LTSSM / xHCI runtime behavior verified
- 不代表 USB-IF certification
- 不可取代 consuming repo 已確認的 project facts

## Reference Surface Maintenance Rule

當 verification maturity 或 tracked entry counts 有變化時，以下 visible surfaces 必須一起檢查：

- `specs/index.md`：zh-TW homepage 的 tracked / maturity summary
- `specs/en/index.md`：English homepage 的 tracked / maturity summary
- `specs/verification_status.md`：zh-TW verification summary、coverage map、verified entries、non-claims
- `specs/en/verification_status.md`：English verification summary、coverage map、verified entries、non-claims
- Core spec pages：受影響 entry family 的 `Non-claims` 與 `Governed Linkage` sections

維護規則：

- 單純 wording update 不得改變 YAML source-of-truth semantics。
- 任何新的或 promoted verified entries，都必須同步更新 verification status pages 與 homepage summaries。
- 若某個 surface 從 inferred 轉成 reviewed，本頁與 coverage map 的 maturity breakdown 也必須一起更新。
- Evidence packet count 變動時，evidence packet summary 也必須同步更新。
- 新增 `section_refs` metadata，不得自動宣告頁面或 entry 已 verified。

## Static Numbers Note

本頁的 entry counts 與 packet statuses 都是人工維護的靜態 summary。

只要下列任一來源有變化，本頁都必須手動更新：

- `tables/port_status_bit_matrix.yaml` 中任一 entry 的 `claim_level`
- `tables/escalation_trigger_matrix.yaml`、`tables/hub_descriptor_matrix.yaml`、`tables/transaction_translator_matrix.yaml`、`tables/class_request_matrix.yaml`、`tables/feature_selector_matrix.yaml` 中 entries 的 `evidence_status` / `claim_level`
- `evidence/entry_verification_packets/` 中新增或修改的 packets

真正的 source of truth 是 governed YAML tables；本頁只是 visibility summary。
