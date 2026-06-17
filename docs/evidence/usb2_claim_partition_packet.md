# USB2 Claim Partition Evidence Packet

Date: 2026-06-17  
Status: Closed  
Scope: USB2 governed entry claim partition evidence chain

## Purpose

This packet records the evidence chain for the current USB2 governed entry
surface after entry-level verification gates, reviewed-boundary locks, and the
claim partition guard were added.

It binds the validators and generated receipt paths so future work does not
blur USB2 content verification with matrix bookkeeping or navigation hardening.

## Inputs

- Entry verification validator: `scripts/validate_entry_verification_gate.py`
- Entry gate coverage validator: `scripts/validate_entry_gate_coverage.py`
- Reviewed boundary lock validator: `scripts/validate_reviewed_boundary_lock.py`
- Claim partition validator: `scripts/validate_usb2_claim_partition.py`
- Entry verification packet directory: `evidence/entry_verification_packets/`

## Validation Commands

```powershell
python -X utf8 scripts/validate_entry_verification_gate.py `
  --receipt-out evidence/validation_receipt_entry_verification_gate.json

python -X utf8 scripts/validate_entry_gate_coverage.py `
  --receipt-out evidence/validation_receipt_entry_gate_coverage.json

python -X utf8 scripts/validate_reviewed_boundary_lock.py `
  --receipt-out evidence/validation_receipt_reviewed_boundary_lock.json

python -X utf8 scripts/validate_usb2_claim_partition.py `
  --receipt-out evidence/validation_receipt_usb2_claim_partition.json
```

## Receipt Contract

The evidence chain expects these reproducible receipt paths:

- `evidence/validation_receipt_entry_verification_gate.json`
- `evidence/validation_receipt_entry_gate_coverage.json`
- `evidence/validation_receipt_reviewed_boundary_lock.json`
- `evidence/validation_receipt_usb2_claim_partition.json`
- Advisory mirror: `ci-receipts/usb2_claim_partition.json`

The receipts are validation outputs. They are not new governed matrices, not
USB-IF source material, and not evidence packets for additional verified entry
promotions.

## Current Partition

The current governed USB2 surface is partitioned as:

| Bucket | Count | Guard |
|---|---:|---|
| tracked | 151 | `validate_reference_surface_statistics.py` |
| verified | 105 | `validate_entry_verification_gate.py` and `validate_entry_gate_coverage.py` |
| reviewed | 46 | `validate_reviewed_boundary_lock.py` |
| inferred | 0 | `validate_usb2_claim_partition.py` |
| missing | 0 | `validate_usb2_claim_partition.py` |
| entry verification packets | 105 | `validate_entry_verification_gate.py` |
| locked reviewed boundaries | 46 | `validate_reviewed_boundary_lock.py` |

## Enforced Scope

This packet binds:

- Verified entries to entry-level verification packets and gate allowlists.
- Reviewed entries to permanent boundary-only entries.
- Entry verification packets to verified entries only.
- The current `151 = 105 verified + 46 reviewed + 0 inferred + 0 missing`
  partition.

## Explicit Non-Claims

This packet does not claim:

- USB behavior correctness.
- USB 2.0 behavior completeness.
- Firmware implementation correctness.
- Host stack behavior coverage.
- New verified entries.
- New USB spec semantics.
- Runtime timing, state transition, reset sequence, or TT scheduling behavior.
- That reviewed boundary entries are eligible for verified promotion.

## Closure Statement

The USB2 claim partition evidence chain is closed as guard evidence only.

The validated chain is:

`entry gate -> reviewed boundary lock -> claim partition -> evidence packet`

Future verified uplift must be opened as a separate content verification slice
with its own source evidence, entry verification packet, and claim ceiling.
