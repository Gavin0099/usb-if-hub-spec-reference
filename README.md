# USB-IF Hub Spec Reference

Read-only spec reference layer for USB hub class firmware development.

## Purpose

This repository provides controlled reference content from the USB 2.0 hub class specification
for consumption by firmware governance contracts.

It does **not** govern firmware behavior. It clarifies standard semantics only.

## Contents

| Document | Spec Section | Description |
|----------|-------------|-------------|
| [specs/hub_descriptor.md](specs/hub_descriptor.md) | 11.23.2.1 | Hub descriptor field definitions |
| [specs/port_status_bits.md](specs/port_status_bits.md) | 11.24.2.7 | Port status and change bit definitions |
| [specs/hub_class_requests.md](specs/hub_class_requests.md) | 11.24.2 | Hub class request semantics |
| [specs/transaction_translator.md](specs/transaction_translator.md) | 11.17–11.18 | TT rules summary |
| [specs/escalation_table.md](specs/escalation_table.md) | — | Standard Escalation trigger table for consuming repos |

## Usage Boundary

This repo may be used to **clarify semantics**. It may **not** be used to override
confirmed project facts in consuming firmware repos.

When a conflict is detected between this spec and a confirmed project fact, the consuming
repo's **Standard Escalation Mode** (AGENTS.md Section 10) must be activated.

## Governance

Adopted from [ai-governance-framework](https://github.com/Gavin0099/ai-governance-framework) v1.2.0.

## Source

USB 2.0 Specification, Revision 2.0 (April 27, 2000) — USB Implementers Forum.
