> **最後更新**: 2026-06-01
> **Owner**: USB-IF Hub Spec Reference
> **Freshness**: Sprint (14d)

# PLAN

[x] Phase 1 : Initialize governance baseline
- Adopt ai-governance-framework v1.2.0
- Create contract.yaml, AGENTS.md, AGENTS.base.md
- Install git hooks

[x] Phase 2 (partial) : Populate USB-IF spec reference tables
- [x] Hub class request matrix (class_request_matrix.yaml) — 12 entries, 9/9 families, coverage complete
- [x] Feature selector matrix (feature_selector_matrix.yaml) — 25 entries, port namespace 0–22 complete
- [x] Port status bit matrix (port_status_bit_matrix.yaml) — 16 entries, wHub*/wPort* bits 0–15, draft
- [ ] Hub descriptor field definitions (USB 2.0 spec 11.23) — not started
- [ ] Transaction Translator rules summary — not started
- [ ] Standard Escalation trigger table — not started
- Claim ceiling: inferred / review_required. No PDF section-level verification performed.

[x] Phase 2A : Specs wiki frontmatter bootstrap
- Added YAML frontmatter to all 6 specs/*.md pages
- Fields: title, claim_level: inferred, status: review_required, semantic_verification_claimed: false
- Wiki frontmatter validator: 6/6 PASS
- Claim ceiling: wiki_frontmatter_structural_consistency_only

[x] Phase 2B : Wiki consistency probe (observation-only)
- probe_wiki_consistency.py: regex token-search, governed table names vs specs page content
- Fixture smoke: 3/3 PASS (consistent, partial_coverage, empty_table)
- Real-table advisory results: class_request 100% · port_status 40% · feature_selector 88.9%
- Advisory findings are expected — specs pages are stubs; not blocking, not semantic incorrectness
- CI: fixture-smoke gate + 3 advisory steps wired
- Claim ceiling: wiki_table_token_consistency_observation_only
- Capability: "wiki/table lexical consistency is observable" — semantic correctness NOT proven
- Next trigger: advisory findings reviewed by consuming repo AND content expansion requested

[x] Phase 4 : Machine-readable consumer access contract
- Export manifest (exports/usb20_hub_class_request_manifest.yaml) listing governed tables
- Validators: validate_class_request_matrix, validate_feature_selector_matrix,
  validate_port_status_bit_matrix, validate_usb20_hub_class_request_manifest
- All validators: structural rules only. Smoke tests: 4/4 PASS each.
- Claim: consumer_discovered_governed_table_access_gaps_closed
- Claim ceiling: machine_readable_namespace_and_access_contract_only

[x] Phase 5B : Table fingerprint baseline and drift observability
- probe_table_fingerprint.py: --mode baseline / --mode check
- evidence/table_fingerprint_baseline.jsonl: 3 governed tables, recorded 2026-06-01
- evidence/validation_receipt_table_fingerprint_drift.json: 0 drift, PASS
- Smoke tests: 3/3 PASS (no_drift, hash_changed, baseline_fresh)
- CI: fixture-smoke gate includes fingerprint smoke; advisory job runs drift check
- Claim ceiling: table_content_fingerprint_drift_only

[x] Phase 5C : Traceability surface sync
- Update consuming repo TRACEABILITY_MATRIX with manifest path + receipt links
- Explicit non-claims section in traceability entry
- consuming repo commit: USB-Hub-Firmware-Architecture-Contract `0e08179`

[ ] Phase 6 (future) : PDF bit-level verification
- Verify port_status_bit_matrix entries against USB 2.0 spec 11.24.2.7
- Add section_anchor fields; upgrade claim_level inferred → verified
- Prerequisite: USB 2.0 Rev 2.0 PDF access

[ ] Phase 3 (deferred) : Wire cross-repo reference
- Register as referenced spec source in USB-Hub-Firmware-Architecture-Contract
- Define allowed usage boundary (clarify semantics only — no behavior override)
- Depends on Phase 5C traceability sync completion
