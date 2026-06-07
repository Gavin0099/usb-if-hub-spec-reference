# Consumer Integration Contract

> **Status**: Active  
> **Established**: 2026-06-07  
> **Supersedes**: `docs/phase4_consumer_access_closeout.md` (Phase 4 partial contract)  
> **Claim ceiling**: governed_matrix_identity_and_boundary_reference_only

---

## Entry Point

The canonical entry point for consuming repo integration is:

```
exports/hub_governed_surface_manifest.yaml
```

This manifest is the **governed truth index** for this repository. It covers:
- 9 USB 2.0 freeze tables (151 tracked / 105 verified / 46 reviewed)
- 3 USB 3.x matrix-level closeout tables (38 tracked / 34 verified / 4 reviewed)
- 12 governed tables total

Consuming repos should **not** read individual YAML tables directly as a primary source of truth. The manifest is the stable contract surface; individual tables are its implementation.

---

## Two-Step Integration Check

Before using any governed surface output, a consuming repo CI should run both checks in sequence:

### Step 1 — Manifest Structural Integrity

```
python scripts/validate_hub_governed_surface_manifest.py
```

Expected output:
```
PASS: hub_governed_surface_manifest validation
  manifest_id: hub_governed_surface_manifest
  governed_tables: 12 (usb20=9, usb3=3)
  usb20: state=freeze tracked=151 verified=105 reviewed=46
  usb3: state=matrix_level_closeout tracked=38 verified=34 reviewed=4
```

### Step 2 — Table Content Drift Detection

```
python scripts/probe_table_fingerprint.py \
  --mode check \
  --manifest exports/hub_governed_surface_manifest.yaml \
  --baseline-in evidence/table_fingerprint_baseline.jsonl
```

Expected output:
```
Table fingerprint check PASSED: 12 table(s), 0 drift
```

Both checks must PASS before treating any governed surface output as stable.

---

## Allowed Usage

The following uses are within the claim ceiling of this contract:

| Use | Description |
|---|---|
| **Table drift detection** | Detect whether any governed YAML table has changed since the last known-good baseline |
| **Selector / request / bit identity reference** | Look up selector name + value, request bRequest + bmRequestType, bit name + bit position — as named in the governed matrices |
| **Reserved boundary guard** | Confirm that a bit position or field range is marked as reserved in the spec; use as a guard against assuming semantic meaning for reserved bits |
| **USB 2.0 / USB 3.x family separation** | Distinguish which entries belong to USB 2.0 vs USB 3.x governed surface using `spec_family` field |
| **Verified scope lookup** | Read `verified_scope` per table entry to understand exactly what identity claim has been made |
| **Reviewed meaning lookup** | Read `reviewed_meaning` per table entry to confirm whether remaining reviewed entries are permanent boundaries or pending promotion |

---

## Forbidden Usage

The following uses **exceed the claim ceiling** and must not be inferred from this contract:

| Forbidden Use | Why |
|---|---|
| **Firmware compliance truth** | Verified entries confirm identity/position only, not that firmware correctly implements the feature |
| **LTSSM runtime behavior verification** | `PORT_LINK_STATE` and `PORT_SPEED` verified scope covers bit range and encoding table identity only; LTSSM state transitions are not verified |
| **xHCI port state management** | xHCI interaction, hub depth assignment, and enumeration behavior are explicitly outside all USB 3.x verified scopes |
| **Electrical, timing, or interoperability compliance** | No timing, signal quality, or USB-IF interoperability claims are made |
| **USB-IF certification completeness** | This reference does not constitute or approximate USB-IF certification evidence |
| **Treating reviewed entries as implementation truth** | Reviewed entries define boundaries and names, not verified implementation behavior |
| **Overriding consuming repo project facts** | If a consuming repo has confirmed project-specific behavior, this reference cannot override it |

---

## Failure Interpretation

### Failure mode 1: Manifest validator FAIL

```
FAIL: hub_governed_surface_manifest validation
  R8: usb20 verified sum mismatch: ...
```

**Meaning**: The export contract is broken. A governed table's verified/reviewed count was changed without updating the manifest's `authority_surface` summary, OR an entry was modified that breaks structural invariants.

**Required action**: Do not use the governed surface output. Investigate which table changed and whether it was an authorized change. Update the manifest summary if the change was intentional.

### Failure mode 2: Fingerprint drift FAIL

```
Table fingerprint check DRIFT_DETECTED: 1 drift, 0 error(s)
  [drift] usb20_hub_port_status_bit_matrix: sha256:abc... -> sha256:def...
```

**Meaning**: A governed table's content has changed since the last recorded baseline. This does not mean the change was unauthorized — it may be an intentional update that was not reflected in the baseline.

**Required action**: Review the table diff. If the change is authorized (e.g., a new phase just landed), re-run the baseline and compact:
```
python scripts/probe_table_fingerprint.py \
  --mode baseline \
  --manifest exports/hub_governed_surface_manifest.yaml \
  --baseline-out evidence/table_fingerprint_baseline.jsonl

python scripts/probe_table_fingerprint.py \
  --mode compact \
  --baseline-in evidence/table_fingerprint_baseline.jsonl \
  --baseline-out evidence/table_fingerprint_baseline.jsonl
```
Then commit the updated baseline. If the change is unexpected, investigate and revert.

---

## Governance Layer Model

This contract operates at layers L1–L3 of the five-layer governance model defined in `docs/local_governance_freeze_point.md`:

| Layer | Status | Description |
|---|---|---|
| L1 — script exists | ✓ | Validator scripts present in `scripts/` |
| L2 — contract declared | ✓ | This document + `exports/hub_governed_surface_manifest.yaml` |
| L3 — CI runs | ✓ Advisory | Validators can run in consuming repo CI as advisory gates |
| L4 — framework invokes | ✗ | ai-governance-framework runtime invocation unconfirmed; not required |
| L5 — consumer enforces | ✗ | Consumer-side enforcement decision belongs to the consuming repo |

**L3 advisory CI is sufficient for this contract.** The consuming repo decides whether to make these checks blocking gates.

---

## What This Contract Does Not Establish

- USB 2.0 hub behavior is fully verified
- Any page-level or table-level compliance is confirmed
- PORT_LINK_STATE runtime behavior or LTSSM transitions are verified
- xHCI enumeration behavior is verified
- The governed surface is equivalent to USB-IF certification
- USB 3.x reference depth is equivalent to USB 2.0 reference depth (USB 3.x covers three governed matrices only, not a 28-topic-pair wiki surface)
- Consuming repo firmware behavior can be derived solely from this reference
