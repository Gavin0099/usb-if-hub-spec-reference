> **Last Updated**: 2026-06-02
> **Owner**: USB-IF Hub Spec Reference
> **Freshness**: Sprint (14d)

# PLAN

[x] Phase 1 : Initialize governance baseline
- Adopt `ai-governance-framework` v1.2.0
- Create `contract.yaml`, `AGENTS.md`, `AGENTS.base.md`
- Install git hooks

[x] Phase 2 (partial) : Populate USB-IF spec reference tables
- [x] Hub class request matrix (`tables/class_request_matrix.yaml`) — 12 entries, 9/9 families, coverage complete
- [x] Feature selector matrix (`tables/feature_selector_matrix.yaml`) — 25 entries, port namespace `0–22` complete
- [x] Port status bit matrix (`tables/port_status_bit_matrix.yaml`) — scaffold established, `wHub*` / `wPort*` entry surface active
- [x] Hub descriptor field definitions page drafted and deepened
- [x] Transaction Translator rules summary page drafted
- [x] Standard Escalation trigger table (`specs/escalation_table.md`) drafted and localized
- [x] Core spec pages remain `inferred` / `review_required` until PDF-backed verification exists
- Claim ceiling: `inferred` / `review_required`. No PDF section-level verification performed.

[x] Phase 2A : Specs wiki frontmatter bootstrap
- Added YAML frontmatter to all spec pages
- Fields include `title`, `claim_level: inferred`, `status: review_required`, `semantic_verification_claimed: false`
- Wiki frontmatter validation established
- Claim ceiling: `wiki_frontmatter_structural_consistency_only`

[x] Phase 2B : Wiki consistency probe (observation-only)
- `probe_wiki_consistency.py`: regex token-search, governed table names vs specs page content
- Fixture smoke gate established
- Real-table advisory coverage has since been improved to practical 100% on current core pages after deepening work
- Claim ceiling: `wiki_table_token_consistency_observation_only`
- Capability: wiki/table lexical consistency is observable; semantic correctness is not yet proven

[x] Phase 4 : Machine-readable consumer access contract
- Export manifest (`exports/usb20_hub_class_request_manifest.yaml`) listing governed tables
- Validators: `validate_class_request_matrix`, `validate_feature_selector_matrix`, `validate_port_status_bit_matrix`, `validate_usb20_hub_class_request_manifest`
- All validators remain structural only
- Claim: `consumer_discovered_governed_table_access_gaps_closed`
- Claim ceiling: `machine_readable_namespace_and_access_contract_only`

[x] Phase 5B : Table fingerprint baseline and drift observability
- `probe_table_fingerprint.py`: `--mode baseline` / `--mode check`
- `evidence/table_fingerprint_baseline.jsonl` recorded for 3 governed tables
- Drift receipt recorded with PASS / no drift at baseline checkpoint
- Smoke tests established
- Claim ceiling: `table_content_fingerprint_drift_only`

[x] Phase 5C : Traceability surface sync
- Update consuming repo `TRACEABILITY_MATRIX` with manifest path + receipt links
- Explicit non-claims section in traceability entry
- Consuming repo commit: `USB-Hub-Firmware-Architecture-Contract 0e08179`

[x] Phase 6 : USB 2.0 Core Reference Deepening
- [x] Phase 6A — `specs/port_status_bits.md` deepened into LLM-readable reference summary
- [x] Phase 6B — `specs/hub_descriptor.md` and `specs/en/hub_descriptor.md` deepened (`d189cda`)
- [x] Phase 6C — `specs/hub_class_requests.md` and `specs/en/hub_class_requests.md` setup-field detail pass completed (`0907113`)
- [x] Minimal bilingual glossary added and linked (`292928c`)
- Core outcome: existing USB 2.0 hub pages are now reviewable, consumer-usable, and bounded by explicit non-claims
- Claim ceiling remains `inferred` / `review_required`

[x] Phase 7A : Section Anchor Schema
- Add `contract/section_anchor_schema.yaml`
- Add `governance/SECTION_ANCHOR_SCHEMA.md`
- `section_refs` established as evidence metadata only
- `section_refs` does not upgrade `claim_level`
- Legacy scalar `section_anchor` remains compatible

[x] Phase 7B : Port Status Section Anchor Pilot
- Attach `section_refs` to selected `tables/port_status_bit_matrix.yaml` entries (`72269bf`)
- Pilot entries: `PORT_CONNECTION`, `PORT_ENABLE`, `C_PORT_CONNECTION`, `C_PORT_ENABLE`
- Result: entry-level anchors can be attached without promoting `claim_level` or `evidence_status`

[x] Phase 7C : Wiki Section-Ref Usage Note
- Add wiki-side `section_refs` usage note to `specs/port_status_bits.md` and `specs/en/port_status_bits.md` (`7dd0588`)
- Clarify that wiki claim-block anchor metadata is allowed without verified promotion

[ ] Phase 8 (future) : PDF-backed entry-level verification pilot
- Select a very small number of bounded USB 2.0 entries for human-reviewable PDF comparison
- Use `section_refs` as attachment metadata, not as automatic promotion logic
- Allow only entry-level or claim-block-level verification, not page-level blanket promotion
- Prerequisite: USB 2.0 Rev 2.0 PDF access plus explicit review workflow

[ ] Phase 3 (deferred) : Wire cross-repo reference
- Register as referenced spec source in `USB-Hub-Firmware-Architecture-Contract`
- Define allowed usage boundary: clarify semantics only, never override confirmed project facts
- Depends on traceability surface expectations in consuming repos
