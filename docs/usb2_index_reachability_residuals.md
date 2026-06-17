# USB2-INDEX-3R Residual Reachability Report

Date: 2026-06-17  
Scope: Non-core USB 2.0 topic reachability hardening (post USB2-INDEX-3)

## Enforced Invariants After USB2-INDEX-3

The following invariants are now enforced by `scripts/validate_usb2_topic_pair_reachability.py` and wired into advisory CI:

- USB2 index (zh/en) includes matching non-core topic pairs.
- Each non-core topic page links to the USB2 index in its own language.
- Each non-core topic page links to its zh/en counterpart.

Validator scope in this slice is topology-level only (links and pair presence), not semantic correctness.

### validator inputs / outputs

- Script: `scripts/validate_usb2_topic_pair_reachability.py`
- Checked non-core topics: 24
- Command result: PASS

## Non-core topic set covered by this hardening

Both language versions are updated in `specs/` and `specs/en/`:

- `escalation_table`
- `glossary`
- `hs_detection`
- `hub_compound_device`
- `hub_configuration`
- `hub_device_class`
- `hub_enumeration`
- `hub_interrupt_endpoint`
- `hub_power_budget`
- `hub_power_management`
- `port_indicators`
- `port_state_machine`
- `split_transaction_packets`
- `standard_descriptors`
- `standard_device_requests`
- `transaction_translator`
- `usb_device_states`
- `usb_packet_types`
- `usb_signaling`
- `usb_test_modes`
- `usb_transactions`
- `usb_transfer_types`
- `verification_status`
- `version_source_map`

## What is explicitly NOT covered

- Non-core topic to topic semantic cross-link mesh.
- USB 2.0 behavior claims, runtime behavior claims, or timing/sequence claims.
- Descriptor/request/status semantic verification.
- Verification count promotion (`verified` / `reviewed` semantics).
- Any change to matrix/YAML governance content or evidence packets.

## Statistical and claim boundaries

`tracked` / `verified` / `reviewed` / `inferred` / `missing` / `evidence packets` remain unchanged from pre-existing baseline:

- tracked: 151
- verified: 105
- reviewed: 46
- inferred: 0
- missing: 0
- evidence packets: 105

This slice is therefore a navigation/buildability hardening slice only.

## Evidence

- `python -X utf8 scripts/validate_usb2_topic_pair_reachability.py`
- `python -X utf8 scripts/validate_usb2_reference_navigation.py`
- `python -X utf8 scripts/validate_usb2_topic_cross_references.py`
- `python -X utf8 scripts/validate_wiki_frontmatter.py --dir specs/`
- `python -X utf8 scripts/validate_reference_surface_statistics.py`
- `npm.cmd run build`

## Residual risk

- Link topology is enforced, but semantic review mesh for non-core topics is intentionally not enforced.
- Build/validator PASS confirms structure and path integrity only; it does not confirm spec interpretation correctness.
- Verification coverage remains non-increased by this change; no claim on coverage completeness is implied.

## Not claimable in this session

- "USB2 topic relationships are fully validated."
- "USB2 reference graph is complete."
- "verified coverage is improved."
- "USB 2.0 is behaviorally complete in this repo."

