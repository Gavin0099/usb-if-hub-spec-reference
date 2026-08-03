---
title: USB 3.x LTSSM Behavioral Model Proposal
status: proposal
claim_level: not_governed
authority_surface: usb3_ltssm_behavior
semantic_verification_claimed: false
implementation_truth_claimed: false
---

# USB 3.x LTSSM Behavioral Model Proposal

## Review Status

This document is a design proposal for agent and owner review. It is not a
governed specification page, a verified LTSSM model, or an implementation
contract.

This proposal does not:

- add LTSSM content to `exports/hub_governed_surface_manifest.yaml`;
- release or weaken the active USB 3.x semantic quarantine;
- promote `specs/usb3/ss_ltssm.md` beyond orientation-only status;
- establish firmware, RTL, DV, PHY, xHCI, or silicon behavior as verified;
- authorize implementation changes in a consuming repository.

The current repository remains a USB 2.0 and USB 3.x Hub reference layer. A
future LTSSM surface should be treated as a separate product surface,
preferably in a private repository or an independently governed pack. The
broader name "Link Behavior" should be considered only after an LTSSM pilot
has demonstrated that additional link modules have a stable boundary.

## 1. Problem Statement

ASIC, RTL, DV, firmware, and FAE teams all need LTSSM information, but they do
not need the same representation.

The current Hub reference surface answers questions such as:

- What is the name and encoding of a Hub descriptor field?
- Which request or selector is defined by the Hub specification?
- Which `PORT_LINK_STATE` encoding is exposed at the Hub class boundary?

It intentionally does not answer:

- Why a link entered a particular LTSSM state;
- Which normative condition causes a transition;
- Which timer or ordered set controls a transition;
- Whether an RTL implementation, firmware implementation, or device is correct.

LTSSM therefore should not be added as a normal Hub table. It requires a
behavior-oriented model with a different schema, evidence model, review
process, and consumer contract.

## 2. Decision Requested

Reviewers are asked to decide whether to authorize a separate USB 3.x LTSSM
Behavioral Model workstream with the following default position:

1. Keep the current Hub reference repository bounded to Hub semantics.
2. Preserve `specs/usb3/ss_ltssm.md` as an orientation-only page.
3. Define an independent LTSSM scope contract before creating model data.
4. Pilot one small leaf-state path before attempting broad LTSSM coverage.
5. Select an actual ASIC or DV consumer before claiming cross-department value.
6. Keep Hub-facing, firmware-facing, xHCI-facing, and electrical claims in
   separate layers.

## 3. Proposed Product Boundary

### 3.1 Hub Reference Surface

The existing Hub surface remains responsible for:

- USB 2.0 Hub descriptor, class request, selector, and status references;
- USB 3.x / SuperSpeed Hub descriptor, class request, selector, and status
  references;
- Hub-facing source terminology and escalation triggers;
- identity, encoding, and boundary claims explicitly supported by the existing
  evidence contract.

It must not claim complete LTSSM behavior.

### 3.2 LTSSM Behavioral Model Surface

The proposed LTSSM surface may contain, subject to later scope approval:

- LTSSM state identity and hierarchy;
- transition conditions and exit outcomes;
- link training and recovery paths;
- U0/U1/U2/U3 power-state relationships;
- reset and recovery relationships;
- ordered-set and link-command references;
- timer definitions and applicability;
- mappings from link behavior to observable Hub-facing status;
- department-specific views derived from the core model.

Future link-training, link-power, or recovery modules may be added only through
an explicit scope decision. They are not automatically included by the product
name.

The LTSSM surface must not silently include:

- xHCI host-controller behavior;
- project-specific RTL architecture;
- firmware policy or register-map truth;
- electrical compliance or signal-integrity qualification;
- silicon or hardware validation results;
- USB-IF certification completeness.

## 4. Scope Contract Required Before Implementation

No LTSSM schema or governed transition table should be introduced until the
following decisions are recorded.

### 4.1 Specification and Version Scope

The owner must select and record:

- USB 3.2 specification revision;
- whether historical USB 3.0/3.1 differences are included;
- whether USB 3.2 Gen 1x1 is included;
- whether USB 3.2 Gen 2x1 is included;
- whether multi-lane behavior is included;
- whether a state or transition is common across versions or version-specific.

The source registry already contains a registered normative USB 3.2 Revision
1.1 source. Existing Hub evidence linked to that source must not be treated as
LTSSM evidence without a separate review packet. ECN scope and source identity
must be confirmed by the owner before P0 is accepted.

### 4.2 Abstraction Layers

The proposal uses the following separations:

| Layer | Initial meaning | Default mode |
| --- | --- | --- |
| LTSSM core | States, transitions, guards, actions, and source anchors | modeled |
| Link training | Training sequences, ordered sets, receiver detection, negotiation | modeled or referenced_only per item |
| Link power | U0/U1/U2/U3 entry, exit, wake, and timeout relationships | deferred |
| Reset/recovery | Recovery, Hot Reset, Warm Reset relationships | modeled or deferred per item |
| Hub observation | `PORT_LINK_STATE`, speed, change bits, and observation limits | referenced_only |
| xHCI interaction | Host-controller behavior and port management | referenced_only for opaque inputs; semantics excluded |
| Electrical/PHY | Waveform, compliance, equalization, SI, and electrical limits | referenced_only for abstract inputs; semantics excluded |
| Firmware policy | Project-specific register, interrupt, retry, and recovery behavior | excluded |

The allowed modes are `modeled`, `referenced_only`, `excluded`, and `deferred`.
An abstract event such as `receiver_detected` may be referenced without
modeling how PHY produces it. The same event may be referenced across layers,
but it must not receive one undifferentiated claim that covers all layers.

### 4.3 State Coverage

The initial scope should explicitly classify each state as one of:

- core training path;
- power-management path;
- recovery/reset path;
- test or special-mode path;
- excluded or deferred.

The phrase "full LTSSM" must not be used until all of the following are
separately assessed:

- full inventory coverage;
- full structural coverage;
- full semantic coverage;
- full profile coverage.

Inventory completion alone is not sufficient for a full semantic claim.

### 4.4 P0 Execution Record

P0 was executed as a scope and consumer decision on 2026-08-03. The scope
defaults below remain a pilot boundary; they do not claim semantic approval.

```yaml
p0_status: consumer_selected_scope_pending_acceptance
recorded_at: "2026-08-03"
profile:
  candidate: usb32r11_gen1x1
  status: proposed_pending_owner_confirmation
  historical_compatibility: not_claimed
  multi_lane: excluded
layer_modes:
  ltssm_core: modeled
  link_training: modeled_or_referenced_only_per_item
  link_power: deferred
  reset_recovery: modeled_or_deferred_per_item
  hub_observation: referenced_only
  xhci_interaction: referenced_only_for_opaque_inputs_semantics_excluded
  electrical_phy: referenced_only_for_abstract_inputs_semantics_excluded
  firmware_policy: excluded
publication_boundary:
  initial_surface: private_repository_or_private_governed_pack
  public_core: generic_source_derived_model_only_after_separate_approval
  private_consumer_adapter: implementation_and_project_specific_evidence
ambiguity_stop_rule:
  status: defined
  mode: fail_closed
  rule: retain_ambiguous_status_and_block_semantic_promotion
consumer_selection:
  status: selected
  required_type: asic_rtl_or_dv_uvm
  verified_consumer:
    consumer_type: repository
    consumer_identity: usb3-ltssm-consumer-pilot
    path: "../usb3-ltssm-consumer-pilot"
    repository_url: https://github.com/Gavin0099/usb3-ltssm-consumer-pilot
    owner: self-developed pilot
    responsible_team: unassigned
    integration_surface:
      rtl: rtl/usb3_ltssm_pilot.sv
      dv: dv/ltssm_oracle.py
      uvm: dv/uvm/
    current_state: python_dv_regression_pass; p1_structural_model_pass; rtl_smoke_pass; uvm_simulation_not_run
    task: exercise the profile-specific pilot state graph, timeout failure,
      recovery return, ordered-set input, and coarse observation mapping
    acceptance_evidence: contracts/p0_consumer.yaml; dv/test_ltssm_oracle.py
```

The initial repository search found no qualifying existing consumer:

- `pcie_g5_contract` is a PCIe LTSSM contract/template, not a USB 3.x
  ASIC/DV consumer;
- `verilog-domain-contract` is a protocol-agnostic RTL governance pack, not
  an active USB RTL project;
- `usb-logic-trace-correlator` is a USB packet/trace tool, not an LTSSM
  RTL/DV/UVM consumer, and its worktree is dirty;
- `USB-Hub-Firmware-Architecture-Contract` is a firmware consumer and cannot
  substitute for the required first ASIC/RTL or DV/UVM consumer;
- remote `Gavin0099/asic-dv-evidence-contract` exists but is empty and has no
  consumer surface.

The self-developed `usb3-ltssm-consumer-pilot` resolves the consumer-selection
blocker. Its P1 structural validator passes, its Python DV regression passes
six focused checks, and its Icarus RTL smoke passes nine checks. UVM runtime
evidence remains pending because no UVM library is installed in the current
environment.

P0 remains pending only for explicit acceptance of the pilot profile, layer
modes, publication boundary, and ambiguity stop rule. The selected consumer
is now sufficient to begin a separately labeled P1 structural model pilot; no
semantic promotion or full-scope claim is authorized.

## 5. Proposed Machine-Readable Model

The following is a design sketch, not a final schema. The pilot should use
separate entities rather than one general LTSSM record:

```text
profiles.yaml
states.yaml
conditions.yaml
transitions.yaml
timers.yaml
ordered_sets.yaml
observations.yaml
```

Each entity carries its own evidence status. A single record-level
`claim_level` must not imply that every relationship inside the record has the
same evidence strength.

### 5.1 Profile Record

Revision is not the only applicability dimension. The pilot should select one
explicit profile and defer historical and multi-lane comparisons.

```yaml
profile_id: usb32r11_gen1x1
base_spec:
  document_ref: usb32_spec
  revision: "1.1"
speed_profile: gen1
lane_count: 1
historical_compatibility: not_claimed
ecn_set: []
```

### 5.2 State Record

Transition truth is owned by transition records. State records do not repeat
entry or exit conditions.

```yaml
state_id: polling_active
spec_label: Polling.Active
state_group: polling
parent_state: polling
applicability:
  profile_refs:
    - usb32r11_gen1x1
source_anchors:
  - document_ref: usb32_spec
    revision: "1.1"
    locator_type: section
    section: "7.5"
    extraction_scope: state_identity
semantic_status: unreviewed
evidence_refs: []
```

### 5.3 Condition/Event Record

Conditions must be typed rather than treated as opaque strings. The model may
reference an input from an excluded layer without modeling that layer's
internal behavior.

```yaml
condition_id: receiver_detected
condition_kind: external_event
origin_layer: phy
boundary_mode: referenced_only
meaning: opaque_input_to_ltssm
source_anchors:
  - document_ref: usb32_spec
    revision: "1.1"
    locator_type: section
    section: "7.5"
    extraction_scope: trigger_definition
semantic_status: unreviewed
evidence_refs: []
```

Allowed initial `condition_kind` values are:

```text
external_event | predicate | timer_expiry | ordered_set_received |
link_command | capability_check | counter_threshold
```

### 5.4 Transition Record

Transitions are the single source of truth for graph edges, triggers, and
outcomes.

```yaml
transition_id: polling_active_to_polling_configuration
from_state: polling_active
to_state: polling_configuration
trigger_refs:
  - ts2_sequence_satisfied
timer_refs:
  - t_polling_active
applicability:
  profile_refs:
    - usb32r11_gen1x1
source_anchors:
  - document_ref: usb32_spec
    revision: "1.1"
    locator_type: section
    section: "7.5"
    extraction_scope: transition_guard
semantic_status: unreviewed
evidence_refs: []
ambiguity: null
```

### 5.5 Timer Record

Timer data must not collapse normative limits, typical values, implementation
tolerances, and firmware timeouts into one scalar. The lifecycle must be
explicit even when the pilot has not yet verified the numerical value.

```yaml
timer_id: t_polling_active
constraint_kind: maximum_duration
starts_on:
  event_ref: enter_polling_active
stops_on:
  - event_ref: exit_polling_active
expires_as:
  condition_ref: polling_active_timeout
value:
  scalar: null
  min: null
  max: null
  unit: null
applicability:
  profile_refs:
    - usb32r11_gen1x1
source_anchors:
  - document_ref: usb32_spec
    revision: "1.1"
    locator_type: section
    section: "7.5"
    extraction_scope: timer_constraint
semantic_status: unreviewed
evidence_refs: []
```

The `null` values are intentional. No timer value should be filled from memory,
a secondary summary, or an implementation constant without a reviewed source
anchor. The pilot must nevertheless select at least one timer for semantic
review, so the timer lifecycle is exercised rather than merely described.

### 5.6 Observation Mapping Record

Hub-facing observations are a separate relation. A Hub encoding must not imply
that a fine-grained LTSSM substate is externally visible one-to-one.

```yaml
observation_id: polling_group_to_port_link_state
state_group_ref: polling
surface:
  type: hub_port_status
  field: PORT_LINK_STATE
  encoding: 0x7
mapping_kind: coarse
observability:
  exact_substate_visible: false
limitations:
  - multiple_ltssm_substates_share_the_same_hub_encoding
source_anchors:
  - document_ref: usb32_spec
    revision: "1.1"
    locator_type: section
    section: "10"
    extraction_scope: hub_observation_mapping
semantic_status: unreviewed
evidence_refs: []
```

Allowed initial `mapping_kind` values are `exact`, `coarse`, `conditional`,
`derived`, `implementation_dependent`, and `not_observable`.

### 5.7 Ambiguity Record

Ambiguity is a first-class blocking state. When the source is unclear, the
model retains alternatives and does not promote either interpretation.

```yaml
ambiguity:
  alternatives:
    - interpretation_a
    - interpretation_b
  blocking: true
  owner_decision: null
  evidence_refs: []
```

The default rule is fail-closed: keep `semantic_status: ambiguous`, stop
semantic promotion, and escalate to a qualified reviewer or owner decision.

Source anchors should identify more than a section when possible:

```yaml
source_anchors:
  - document_ref: usb32_spec
    revision: "1.1"
    locator_type: table_row
    section: "7.5"
    table: "state transition table"
    row: "Polling.Active -> Polling.Configuration"
    extraction_scope: transition_guard
    evidence_packet_ref: ev-ltssm-pilot-001
```

## 6. Pilot Scope

The first pilot should be deliberately narrow and profile-specific:

```text
profile: usb32r11_gen1x1
Rx.Detect -> Polling.Active -> U0
U0 -> Recovery.Active -> Polling.Active -> U0
```

The pilot must include enough branches to exercise the model, not only the
happy path:

- one leaf-state success path;
- one timer-expiry or training-failure path;
- one recovery-return path;
- one ordered-set condition;
- one PHY `referenced_only` event;
- one coarse Hub observation mapping;
- one explicitly excluded branch.

The pilot should include one semantic packet containing independent review
decisions for each pilot transition, rather than requiring one packet per
transition. A qualified ASIC or DV reviewer must participate in the packet.

The pilot should not yet include:

- all compliance and loopback behavior;
- complete electrical behavior;
- xHCI port-management semantics;
- project-specific RTL or firmware decisions;
- a claim of complete LTSSM coverage;
- a shared cross-pack framework.

## 7. Evidence and Claim Dimensions

Evidence is multidimensional. The following dimensions must not be interpreted
as a single maturity ladder or as substitutes for one another:

```yaml
evidence_status:
  source_traceability: anchored
  structural_consistency: pass
  semantic_review: unreviewed
  consumer_validation: none
  implementation_evidence: external_only
```

For example, a model may pass semantic review before a consumer adopts it. A
consumer may experiment with an unreviewed pilot without proving semantic
correctness. Runtime evidence may demonstrate an implementation behavior
without proving that the reference model's normative interpretation is right.

### E0 - Source Traceability

Each state, transition, condition, timer, ordered-set, and observation record
has a source document, revision, precise locator, and extraction scope.

This proves traceability only.

### E1 - Structural Consistency

Automated validation checks:

- every state and condition reference resolves;
- every transition source and target resolves;
- timer and ordered-set references resolve;
- required source anchors exist;
- profile applicability is valid;
- observation mappings declare precision and limitations;
- excluded layers are not represented as silently modeled behavior.

This proves model consistency only.

### E2 - Semantic Review

An appropriately qualified reviewer checks, per entity or relation:

- transition interpretation;
- condition meaning and boundary mode;
- timer classification and lifecycle;
- ordered-set applicability;
- version/profile differences;
- observation precision;
- abstraction-layer boundaries;
- unresolved ambiguity.

An entity cannot be promoted while a blocking ambiguity remains unresolved.

### E3 - Consumer Validation

An actual consumer checks whether the model supports a real task:

- ASIC: state mapping or RTL design review;
- DV: assertion, negative-case, or coverage mapping;
- firmware: status/register/interrupt mapping;
- FAE: trace symptom and diagnostic mapping.

Consumer validation is independent of semantic review and does not prove
implementation correctness.

### E4 - Implementation Evidence

RTL simulation, DV results, hardware traces, protocol analyzer output, silicon
validation, and firmware runtime tests belong to consuming projects. They are
external evidence unless independently supplied and governed under a separate
contract. E4 does not upgrade E2 automatically.

## 8. Consumer Selection

The already selected `USB-Hub-Firmware-Architecture-Contract` is suitable for
the Hub-facing firmware boundary, but it is not evidence of ASIC or DV
consumption.

The first non-Hub consumer must be an ASIC/RTL or DV/UVM consumer. Firmware may
be a later mapping consumer, but it cannot substitute for the first ASIC/DV
trial. The consumer need not be a Git repository; it may be an internal
workspace, testbench, regression system, or debug tool.

The consumer selection record should include:

```yaml
consumer_type: repository | workspace | testbench | debug_tool
consumer_identity: null
owner: null
responsible_team: null
integration_surface: null
current_state: null
task: null
acceptance_evidence: null
```

The selected consumer must contain one of:

- ASIC RTL state-machine design;
- USB 3.x link DV/UVM tests;
- protocol-analyzer or link-debug automation.

The concrete task must state what the LTSSM model is expected to improve.

No consumer repository should be modified during selection or scope review.

## 9. Proposed Phases and Gates

| Phase | Deliverable | Required gate | Claim ceiling |
| --- | --- | --- | --- |
| P0 | Scope decision | Owner accepts profile, layers, exclusions, and publication boundary | Proposal only |
| P1 | Pilot entity model | Structural validator passes | Traceable model only |
| P2 | Semantic review packet | Qualified reviewer accepts entity-level decisions and ambiguity status | Pilot semantic claims only |
| P3 | ASIC/DV consumer trial | Real task produces reviewable evidence | Consumer validation only |
| P4 | Module expansion | New power, reset, or training scope reviewed independently | Module-level claims only |
| P5 | Derived department views | Projection and source consistency checks pass | Derived views only |
| P6 | Full-scope decision | Inventory, structure, semantics, profiles, timers, and exclusions are all assessed | Full claim only if separately approved |

No phase may promote a claim merely because a Markdown page, diagram, or YAML
file exists. Evidence dimensions remain independently reportable at every
phase.

## 10. Review Questions for Other Agents

Reviewers should answer these questions explicitly:

1. Is a separate LTSSM product surface justified before a broader Link Behavior product?
2. Should it live in a new private repository or an independently governed pack?
3. Is USB 3.2 Revision 1.1 the correct initial authority source, including ECN scope?
4. Should Gen 1x1, Gen 2x1, and multi-lane behavior be separate profiles?
5. Which leaf states and transitions belong in the first pilot?
6. Which timer lifecycle should be exercised, and which value must be semantically reviewed?
7. Are ordered sets part of the core model or a separate training entity?
8. Which xHCI and electrical/PHY semantics remain excluded while abstract inputs are referenced?
9. Which actual ASIC/RTL or DV/UVM consumer can act as the first non-firmware consumer?
10. What evidence is sufficient to promote each entity or relation from unreviewed to reviewed?
11. What fields are required for DV assertions and coverage generation?
12. What fields are required for firmware status and interrupt mapping?
13. What evidence would falsify the proposed model or expose a missing distinction?
14. What is the fail-closed stop condition if the source specification is ambiguous?

## 11. Publication and Proprietary Boundary

The initial LTSSM pilot should preferably live in a private repository or
private governed pack. Publication status is a separate decision from semantic
status.

### Public/Core Surface

The public surface may contain, after separate approval:

- generic source-derived state and transition identities;
- generic profile and applicability metadata;
- generic evidence and source-anchor metadata;
- explicitly reviewed non-claims and observation limitations.

It must not contain proprietary project implementation details merely because
they were useful during consumer validation.

### Private Consumer Adapter

The following should remain in the consuming project or a controlled private
adapter unless separately approved:

- RTL signal mappings;
- internal register and interrupt mappings;
- silicon traces and lab captures;
- project-specific workarounds and retry policy;
- customer-specific behavior;
- implementation or compliance results.

Publication approval does not promote semantic claims, and semantic review does
not authorize publication of proprietary evidence.

## 12. Full-Scope Claim Conditions

The term "full" must be qualified. The following claims are distinct:

- `full_inventory_coverage`: all in-scope states and transitions are listed;
- `full_structural_coverage`: all references, profiles, and graph constraints pass;
- `full_semantic_coverage`: every in-scope entity or relation has qualified review;
- `full_profile_coverage`: every approved profile has applicable evidence;
- `full_ltssm_semantic_coverage`: all of the above, with timers classified,
  ambiguities resolved or explicitly excluded, and observation precision reviewed.

No full semantic claim is allowed while any in-scope transition, timer,
profile, or observation mapping remains unresolved or carries a blocking
ambiguity.

## 13. Non-Claims

This proposal does not claim:

- that the current `ss_ltssm.md` is a complete or normative LTSSM model;
- that any current USB 3.x Hub matrix verifies LTSSM behavior;
- that the USB 3.2 specification alone verifies RTL, firmware, or silicon;
- that an LTSSM model can replace PHY, electrical, xHCI, or project contracts;
- that a consumer repository has adopted this proposal;
- that a full LTSSM scope has been approved;
- that any implementation, runtime, compliance, or interoperability result exists.

## 14. Recommended Next Action

The next authorized action should be a review-only decision on this proposal.
If the proposal is accepted, execute `P0` only: record one profile, define the
layer modes and publication boundary, select an actual ASIC/RTL or DV/UVM
consumer, and define the ambiguity stop rule. Do not create transition data,
modify the current Hub manifest, or release the current USB 3.x quarantine as
part of that decision.

## 15. Cross-Repository Integration Boundary

The spec reference repository is the source-side reference provider. The
`usb3-ltssm-consumer-pilot` repository is the implementation-side consumer.
Neither repository may silently become the authority of the other.

The consumer must pin a committed spec-repository revision before claiming
that it consumes this proposal. The pin must identify:

- the spec repository URL and immutable commit;
- the proposal path and proposal content hash;
- the selected profile and proposal status;
- `boundary_mode: specification_reference_only`;
- an explicit statement that the reference is not implementation authority;
- the source anchor and evidence boundary used by the consumer task.

The communication protocol is:

1. The spec repository publishes a committed proposal revision or an approved
  source/reference update.
2. The consumer opens a change that updates its lock file and records the
  affected profile, source anchors, and expected impact.
3. Consumer structural validation checks the immutable commit, content hash,
  profile, and boundary declarations before the consumer change is accepted.
4. A semantic ambiguity or source conflict is reported back as a review
  request; consumer RTL, DV, or runtime evidence must not silently rewrite
  the reference interpretation.
5. Consumer implementation evidence remains in the consumer repository and
  does not promote this proposal to a governed or normative model.

An invalid, dirty, missing, or hash-mismatched lock is a blocking integration
condition. A pending lock may describe work in progress, but it cannot be used
as evidence that the consumer has adopted a stable spec revision.
