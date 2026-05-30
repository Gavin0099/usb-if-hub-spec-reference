# Agent Contract — USB Hub Specification Authority

## Required Reads Before Any Spec Table Edit

An agent must read, in order:

1. `contract/authority_levels.yaml`
2. `contract/version_scope.yaml`
3. `contract/claim_rules.yaml`
4. `contract/evidence_requirements.yaml`

## Must-Do Workflow

1. Identify the USB version scope first.
2. Classify each source by authority level before using it.
3. Attach evidence fields for each new or changed entry.
4. Downgrade claim level when section anchors are missing.
5. Preserve the repo boundary: clarification only, never project-fact override.

## Must-Not Rules

- Do not promote community or mirror sources to normative authority.
- Do not treat USB 2.1 as an independent base spec unless officially registered.
- Do not treat USB4 topology behavior as equivalent to USB 2.0/3.x hub class behavior without section-level evidence.
- Do not add descriptor/request/status/TT claims without source authority and extraction status.
- Do not convert uncertain interpretation into a normative claim.

## Entry Completeness Requirement

Every new table or matrix entry must include:

- source document title
- source URL
- authority level
- USB version scope
- section reference or explicit `section_unknown`
- extraction status
- claim level
