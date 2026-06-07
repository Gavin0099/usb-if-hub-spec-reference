# Release Notes — Hub Governed Surface Export Contract

> **Release tag**: EXPORT-CONTRACT-1.0  
> **Date**: 2026-06-07  
> **Status**: Stable checkpoint

---

## What This Release Covers

This release marks the completion of the hub governed surface export contract — the point at which the repo transitions from "spec reference with internal governance" to "externally consumable governed surface with documented CI integration."

---

## Governed Surface State at Release

### USB 2.0 — Governed Reference Surface Freeze

| Metric | Value |
|---|---|
| State | Freeze |
| Tracked entries | 151 |
| Verified entries | 105 |
| Reviewed entries | 46 |
| Evidence packets | 105 |
| Reviewed meaning | Reserved bits and boundary-only placeholders (no promotion pending) |
| Pending semantic promotion | 0 |

Verified scope: selector-name/value, descriptor field identity, bit name and position, request-linkage identity, bit-group name and value-encoding identity.

### USB 3.x / SuperSpeed Hub — Matrix-Level Closeout

| Metric | Value |
|---|---|
| State | Matrix-level closeout |
| Tracked entries | 38 |
| Verified entries | 34 |
| Reviewed entries | 4 |
| Evidence packets | 34 |
| Reviewed meaning | Reserved boundary entries only (no promotion pending) |
| Pending semantic promotion | 0 |

Three governed matrices: SS hub descriptor (9/9 verified), SS hub class requests (10/10 verified), SS port status/change bits (15/19 verified, 4 reserved boundary reviewed).

Verified scopes per matrix:
- Descriptor fields: `descriptor_field_identity_only`
- Class requests: `request_linkage_identity_only` / `request_identity_requiredness_only` / `request_identity_optionality_only`
- Port status single-bit: `bit_name_and_position_only`
- PORT_LINK_STATE, PORT_SPEED: `bit_name_range_and_encoding_identity_only`

### Governed Tables

| Table | Spec family | State | Verified | Reviewed |
|---|---|---|---:|---:|
| hub_descriptor_matrix | usb20 | freeze | 8 | 0 |
| transaction_translator_matrix | usb20 | freeze | 10 | 0 |
| escalation_trigger_matrix | usb20 | freeze | 10 | 0 |
| class_request_matrix | usb20 | freeze | 12 | 0 |
| feature_selector_matrix | usb20 | freeze | 25 | 0 |
| port_status_bit_matrix | usb20 | freeze | 19 | 45 |
| hub_interrupt_endpoint_matrix | usb20 | freeze | 4 | 0 |
| standard_device_request_matrix | usb20 | freeze | 12 | 0 |
| wHubCharacteristics_bit_matrix | usb20 | freeze | 5 | 1 |
| ss_hub_descriptor_matrix | usb3 | matrix_level_closeout | 9 | 0 |
| ss_hub_class_request_matrix | usb3 | matrix_level_closeout | 10 | 0 |
| ss_port_status_bit_matrix | usb3 | matrix_level_closeout | 15 | 4 |
| **Total** | | | **139** | **50** |

---

## Export Contract Components

| Component | Path | Role |
|---|---|---|
| Unified manifest | `exports/hub_governed_surface_manifest.yaml` | Governed truth index for all 12 tables |
| Fingerprint baseline | `evidence/table_fingerprint_baseline.jsonl` | Content-hash baseline for drift detection |
| Consumer contract | `docs/CONSUMER_INTEGRATION_CONTRACT.md` | Allowed/forbidden usage, failure interpretation |
| Manifest validator | `scripts/validate_hub_governed_surface_manifest.py` | Summary ↔ table entry cross-check gate |
| Fingerprint probe | `scripts/probe_table_fingerprint.py` | Table content drift gate |
| Consumer smoke | `scripts/smoke_consumer_integration_fixtures.py` | Smoke-tested contract behavior |

All six components are publicly linked from README → index → verification_status → contract → manifest.

---

## Consuming Repo Usage

### Entry point

```
exports/hub_governed_surface_manifest.yaml
```

Do not read individual YAML tables directly as a primary source of truth. The manifest is the stable contract surface.

### Two-step CI gate

```bash
# Step 1 — manifest structural integrity
python scripts/validate_hub_governed_surface_manifest.py

# Step 2 — table content drift detection
python scripts/probe_table_fingerprint.py \
  --mode check \
  --manifest exports/hub_governed_surface_manifest.yaml \
  --baseline-in evidence/table_fingerprint_baseline.jsonl
```

Both steps must PASS before treating the governed surface as stable.

### Allowed usage

- Table drift detection in CI
- Selector / request / bit identity reference
- Reserved boundary guard
- USB 2.0 / USB 3.x spec family separation via `spec_family` field
- Verified scope lookup per entry
- Reviewed meaning lookup per entry

### Re-baseline after an authorized table change

```bash
python scripts/probe_table_fingerprint.py \
  --mode baseline \
  --manifest exports/hub_governed_surface_manifest.yaml \
  --baseline-out evidence/table_fingerprint_baseline.jsonl

python scripts/probe_table_fingerprint.py \
  --mode compact \
  --baseline-in evidence/table_fingerprint_baseline.jsonl \
  --baseline-out evidence/table_fingerprint_baseline.jsonl
```

Then commit the updated baseline.

---

## Non-Claims (Fixed Boundaries)

This export contract does **not** establish:

- Firmware compliance truth or firmware implementation correctness
- LTSSM runtime state transition behavior (PORT_LINK_STATE verified scope is bit range and encoding table identity only)
- xHCI port state management or xHCI enumeration behavior
- SuperSpeed hub firmware compliance
- Electrical, timing, or interoperability compliance
- USB-IF certification completeness
- USB 3.x reference surface depth equivalent to USB 2.0 (USB 3.x covers three governed matrices; USB 2.0 has 28 topic pairs of wiki reference)
- The ability to override confirmed project facts in consuming repositories
- Any page-level or table-level compliance proof

---

## Public Navigation Chain

```
README.md
└─ Governed Surface Status
└─ Consumer Integration section
   └─ specs/en/index.md (Consumer Integration Contract feature card)
      └─ specs/en/verification_status.md (Export Contract Surface section)
         └─ docs/CONSUMER_INTEGRATION_CONTRACT.md
            └─ exports/hub_governed_surface_manifest.yaml
               └─ evidence/table_fingerprint_baseline.jsonl
```

---

## Phases Included in This Release

| Phase | Description |
|---|---|
| USB3-0 through USB3-4 | USB 3.x scope boundary, wiki scaffold, governed matrix scaffold, verified pilots (3A/3B/3C), closeout hygiene |
| EXPORT-1 | Unified hub governed surface manifest (12 tables) + fingerprint baseline |
| EXPORT-2 | Consumer integration contract documentation |
| CONSUMER-SMOKE-1 | Consumer integration contract smoke fixture (3 cases) |
| DOC-LINK-1 | Public navigation visibility sync (README, homepage, verification_status) |
