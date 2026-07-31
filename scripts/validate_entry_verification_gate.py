#!/usr/bin/env python3
"""Validate entry-level verified promotion gate for governed table entries.

Authority ceiling: entry_level_verified_gate_only

This validator does not verify USB semantics. It only enforces that any
entry-level `claim_level: verified` promotion is backed by a narrow, explicit,
reviewable evidence packet.

Current scope:
  - `tables/port_status_bit_matrix.yaml`
    - allowed entries: promoted hub/port status-change bit entries
    - required scope: `bit_name_and_position_only`
  - `tables/hub_descriptor_matrix.yaml`
    - allowed entries: the eight tracked USB 2.0 hub descriptor field entries
    - required scope: `descriptor_field_identity_only`
  - `tables/feature_selector_matrix.yaml`
    - allowed entries: the 25 tracked USB 2.0 feature selector entries
    - required scope: `selector_name_and_value_only`
  - `tables/transaction_translator_matrix.yaml`
    - allowed entries: the 10 tracked USB 2.0 Transaction Translator entries
    - required scopes: per-entry TT type / think-time / request-linkage boundary only
  - `tables/standard_device_request_matrix.yaml`
    - allowed entries: the 12 tracked USB 2.0 standard device request entries
    - required scope: `request_linkage_only`
  - `tables/hub_interrupt_endpoint_matrix.yaml`
    - allowed entries: the 4 tracked USB 2.0 hub interrupt endpoint descriptor fields
    - required scope: `descriptor_field_identity_only`
  - `tables/wHubCharacteristics_bit_matrix.yaml`
    - allowed entries: the 5 verified USB 2.0 wHubCharacteristics bit groups
    - required scope: `bit_group_name_and_value_encoding_identity_only`
  - `tables/escalation_trigger_matrix.yaml`
    - allowed entries: the 10 tracked USB 2.0 escalation triggers
    - required scope: `escalation_trigger_boundary_only`
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
USB2_DEFAULT_MATRICES = [
    ROOT / "tables" / "port_status_bit_matrix.yaml",
    ROOT / "tables" / "hub_descriptor_matrix.yaml",
    ROOT / "tables" / "class_request_matrix.yaml",
    ROOT / "tables" / "feature_selector_matrix.yaml",
    ROOT / "tables" / "transaction_translator_matrix.yaml",
    ROOT / "tables" / "standard_device_request_matrix.yaml",
    ROOT / "tables" / "hub_interrupt_endpoint_matrix.yaml",
    ROOT / "tables" / "wHubCharacteristics_bit_matrix.yaml",
    ROOT / "tables" / "escalation_trigger_matrix.yaml",
]
USB3_DEFAULT_MATRICES = [
    ROOT / "tables" / "ss_hub_descriptor_matrix.yaml",
    ROOT / "tables" / "ss_port_status_bit_matrix.yaml",
    ROOT / "tables" / "ss_feature_selector_matrix.yaml",
    ROOT / "tables" / "ss_hub_class_request_matrix.yaml",
    ROOT / "tables" / "ss_hub_interrupt_endpoint_matrix.yaml",
    ROOT / "tables" / "ss_hub_characteristics_bit_matrix.yaml",
]
DEFAULT_MATRICES = [*USB2_DEFAULT_MATRICES, *USB3_DEFAULT_MATRICES]
DEFAULT_PACKET_DIR = ROOT / "evidence" / "entry_verification_packets"
DEFAULT_PACKET_SCHEMA = ROOT / "contract" / "entry_verification_packet_schema.yaml"
DEFAULT_SOURCE_REGISTRY = ROOT / "evidence" / "source_registry.yaml"

TABLE_RULES = {
    "port_status_bit_matrix": {
        "allowed_entries": {
            "wPortStatus.bit0.PORT_CONNECTION",
            "wPortStatus.bit1.PORT_ENABLE",
            "wPortStatus.bit2.PORT_SUSPEND",
            "wPortStatus.bit3.PORT_OVER_CURRENT",
            "wPortStatus.bit4.PORT_RESET",
            "wPortStatus.bit8.PORT_POWER",
            "wPortStatus.bit9.PORT_LOW_SPEED",
            "wPortStatus.bit10.PORT_HIGH_SPEED",
            "wPortStatus.bit11.PORT_TEST",
            "wPortStatus.bit12.PORT_INDICATOR",
            "wPortChange.bit0.C_PORT_CONNECTION",
            "wPortChange.bit1.C_PORT_ENABLE",
            "wPortChange.bit2.C_PORT_SUSPEND",
            "wPortChange.bit3.C_PORT_OVER_CURRENT",
            "wPortChange.bit4.C_PORT_RESET",
            "wHubStatus.bit0.HUB_LOCAL_POWER",
            "wHubStatus.bit1.HUB_OVER_CURRENT",
            "wHubChange.bit0.C_HUB_LOCAL_POWER",
            "wHubChange.bit1.C_HUB_OVER_CURRENT",
        },
        "required_scope": "bit_name_and_position_only",
        "required_excludes": {
            "timing behavior",
            "state transition behavior",
            "ClearPortFeature behavior",
            "full USB compliance",
        },
    },
    "hub_descriptor_matrix": {
        "allowed_entries": {
            "usb20_hub_desc_bDescLength",
            "usb20_hub_desc_bDescriptorType",
            "usb20_hub_desc_bNbrPorts",
            "usb20_hub_desc_wHubCharacteristics",
            "usb20_hub_desc_bPwrOn2PwrGood",
            "usb20_hub_desc_bHubContrCurrent",
            "usb20_hub_desc_DeviceRemovable",
            "usb20_hub_desc_PortPwrCtrlMask",
        },
        "required_scope": "descriptor_field_identity_only",
        "required_excludes": {
            "descriptor dump validation",
            "device behavior",
            "board-level timing or current guarantee",
            "full USB compliance",
        },
    },
    "class_request_matrix": {
        "allowed_entries": {
            "usb20_get_status_hub",
            "usb20_get_status_port",
            "usb20_set_feature_hub",
            "usb20_set_feature_port",
            "usb20_clear_feature_hub",
            "usb20_clear_feature_port",
            "usb20_clear_tt_buffer",
            "usb20_reset_tt",
            "usb20_get_tt_state",
            "usb20_stop_tt",
            "usb20_get_descriptor_hub",
            "usb20_set_descriptor_hub",
        },
        "required_scope": "request_linkage_only",
        "required_excludes": {
            "timing behavior",
            "state transition behavior",
            "firmware behavior",
            "host-stack interpretation",
            "full USB compliance",
        },
    },
    "feature_selector_matrix": {
        "allowed_entries": {
            "usb20_hub_c_hub_local_power",
            "usb20_hub_c_hub_over_current",
            "usb20_port_connection",
            "usb20_port_enable",
            "usb20_port_suspend",
            "usb20_port_over_current",
            "usb20_port_reset",
            "usb20_port_reserved_5",
            "usb20_port_reserved_6",
            "usb20_port_reserved_7",
            "usb20_port_power",
            "usb20_port_low_speed",
            "usb20_port_high_speed",
            "usb20_port_reserved_11",
            "usb20_port_reserved_12",
            "usb20_port_reserved_13",
            "usb20_port_reserved_14",
            "usb20_port_reserved_15",
            "usb20_c_port_connection",
            "usb20_c_port_enable",
            "usb20_c_port_suspend",
            "usb20_c_port_over_current",
            "usb20_c_port_reset",
            "usb20_port_test",
            "usb20_port_indicator",
        },
        "required_scope": "selector_name_and_value_only",
        "required_excludes": {
            "timing behavior",
            "state transition behavior",
            "selector side effects",
            "host-stack interpretation",
            "full USB compliance",
        },
    },
    "transaction_translator_matrix": {
        "allowed_entries": {
            "usb20_tt_type_single",
            "usb20_tt_type_multiple",
            "usb20_tt_think_time_00",
            "usb20_tt_think_time_01",
            "usb20_tt_think_time_10",
            "usb20_tt_think_time_11",
            "usb20_tt_request_clear_tt_buffer",
            "usb20_tt_request_reset_tt",
            "usb20_tt_request_get_tt_state",
            "usb20_tt_request_stop_tt",
        },
        "entry_rules": {
            "usb20_tt_type_single": {
                "required_scope": "tt_type_boundary_only",
                "required_excludes": {
                    "split-transaction behavior",
                    "timing behavior",
                    "firmware behavior",
                    "full USB compliance",
                    "host-stack interpretation",
                },
            },
            "usb20_tt_type_multiple": {
                "required_scope": "tt_type_boundary_only",
                "required_excludes": {
                    "split-transaction behavior",
                    "timing behavior",
                    "firmware behavior",
                    "full USB compliance",
                    "host-stack interpretation",
                },
            },
            "usb20_tt_think_time_00": {
                "required_scope": "tt_think_time_boundary_only",
                "required_excludes": {
                    "hardware timing behavior",
                    "split-transaction timing",
                    "firmware behavior",
                    "state transition behavior",
                    "full USB compliance",
                },
            },
            "usb20_tt_think_time_01": {
                "required_scope": "tt_think_time_boundary_only",
                "required_excludes": {
                    "hardware timing behavior",
                    "split-transaction timing",
                    "firmware behavior",
                    "state transition behavior",
                    "full USB compliance",
                },
            },
            "usb20_tt_think_time_10": {
                "required_scope": "tt_think_time_boundary_only",
                "required_excludes": {
                    "hardware timing behavior",
                    "split-transaction timing",
                    "firmware behavior",
                    "state transition behavior",
                    "full USB compliance",
                },
            },
            "usb20_tt_think_time_11": {
                "required_scope": "tt_think_time_boundary_only",
                "required_excludes": {
                    "hardware timing behavior",
                    "split-transaction timing",
                    "firmware behavior",
                    "state transition behavior",
                    "full USB compliance",
                },
            },
            "usb20_tt_request_clear_tt_buffer": {
                "required_scope": "request_linkage_boundary_only",
                "required_excludes": {
                    "state transition behavior",
                    "firmware behavior",
                    "full USB compliance",
                    "host-stack interpretation",
                },
            },
            "usb20_tt_request_reset_tt": {
                "required_scope": "request_linkage_boundary_only",
                "required_excludes": {
                    "state transition behavior",
                    "firmware behavior",
                    "full USB compliance",
                    "host-stack interpretation",
                },
            },
            "usb20_tt_request_get_tt_state": {
                "required_scope": "request_linkage_boundary_only",
                "required_excludes": {
                    "state transition behavior",
                    "firmware behavior",
                    "full USB compliance",
                    "host-stack interpretation",
                },
            },
            "usb20_tt_request_stop_tt": {
                "required_scope": "request_linkage_boundary_only",
                "required_excludes": {
                    "state transition behavior",
                    "firmware behavior",
                    "full USB compliance",
                    "host-stack interpretation",
                },
            },
        },
    },
    "standard_device_request_matrix": {
        "allowed_entries": {
            "usb20_std_get_status_device",
            "usb20_std_get_status_interface",
            "usb20_std_get_status_endpoint",
            "usb20_std_clear_feature_device",
            "usb20_std_clear_feature_endpoint",
            "usb20_std_set_feature_device",
            "usb20_std_set_address",
            "usb20_std_get_descriptor",
            "usb20_std_get_configuration",
            "usb20_std_set_configuration",
            "usb20_std_get_interface",
            "usb20_std_set_interface",
        },
        "required_scope": "request_linkage_only",
        "required_excludes": {
            "timing behavior",
            "state transition behavior",
            "firmware behavior",
            "host-stack interpretation",
            "full USB compliance",
        },
    },
    "hub_interrupt_endpoint_matrix": {
        "allowed_entries": {
            "usb20_hub_ep_bEndpointAddress",
            "usb20_hub_ep_bmAttributes",
            "usb20_hub_ep_wMaxPacketSize",
            "usb20_hub_ep_bInterval",
        },
        "required_scope": "descriptor_field_identity_only",
        "required_excludes": {
            "full USB compliance",
        },
    },
    "wHubCharacteristics_bit_matrix": {
        "allowed_entries": {
            "usb20_whc_power_switching",
            "usb20_whc_compound_device",
            "usb20_whc_over_current_mode",
            "usb20_whc_tt_think_time",
            "usb20_whc_port_indicators",
        },
        "required_scope": "bit_group_name_and_value_encoding_identity_only",
        "required_excludes": {
            "firmware descriptor dump correctness",
            "full USB compliance",
        },
    },
    "escalation_trigger_matrix": {
        "allowed_entries": {
            "E-01",
            "E-02",
            "E-03",
            "E-04",
            "E-05",
            "E-06",
            "E-07",
            "E-08",
            "E-09",
            "E-10",
        },
        "required_scope": "escalation_trigger_boundary_only",
        "required_excludes": {
            "firmware behavior",
            "full USB compliance",
        },
    },
    # ── USB 3.x (SuperSpeed) governed tables ──────────────────────────────
    # required_excludes for each ss_* table below is the boundary phrase
    # confirmed present in every evidence packet for that table (verified
    # by grep across evidence/entry_verification_packets/usb3/). Where no
    # single exclude phrase is shared by all entries in a table (ss_hub_
    # interrupt_endpoint_matrix, ss_hub_characteristics_bit_matrix), the set
    # is left empty rather than asserting a boundary the packets don't
    # actually carry in common.
    "ss_hub_descriptor_matrix": {
        "allowed_entries": {
            "usb3_hub_desc_bDescLength",
            "usb3_hub_desc_bDescriptorType",
            "usb3_hub_desc_bNbrPorts",
            "usb3_hub_desc_wHubCharacteristics",
            "usb3_hub_desc_bPwrOn2PwrGood",
            "usb3_hub_desc_bHubContrCurrent",
            "usb3_hub_desc_bHubHdrDecLat",
            "usb3_hub_desc_wHubDelay",
            "usb3_hub_desc_DeviceRemovable",
        },
        "required_scope": "descriptor_field_identity_only",
        "required_excludes": {
            "full USB 3.x compliance",
        },
    },
    "ss_port_status_bit_matrix": {
        "allowed_entries": {
            "ss_wPortStatus.bit0.PORT_CONNECTION",
            "ss_wPortStatus.bit1.PORT_ENABLE",
            "ss_wPortStatus.bit2.PORT_OVER_CURRENT",
            "ss_wPortStatus.bit3.PORT_RESET",
            "ss_wPortStatus.bits85.PORT_LINK_STATE",
            "ss_wPortStatus.bit9.PORT_POWER",
            "ss_wPortStatus.bits1210.PORT_SPEED",
            "ss_wPortStatus.bit13.PORT_U1_ENABLE",
            "ss_wPortStatus.bit14.PORT_U2_ENABLE",
            "ss_wPortChange.bit0.C_PORT_CONNECTION",
            "ss_wPortChange.bit2.C_PORT_OVER_CURRENT",
            "ss_wPortChange.bit3.C_PORT_RESET",
            "ss_wPortChange.bit4.C_BH_PORT_RESET",
            "ss_wPortChange.bit5.C_PORT_LINK_STATE",
            "ss_wPortChange.bit6.C_PORT_CONFIG_ERROR",
        },
        "required_scope": "bit_name_and_position_only",
        "required_excludes": {
            "full USB 3.x compliance",
        },
        "entry_rules": {
            "ss_wPortStatus.bits85.PORT_LINK_STATE": {
                "required_scope": "bit_name_range_and_encoding_identity_only",
                "required_excludes": {"full USB 3.x compliance"},
            },
            "ss_wPortStatus.bits1210.PORT_SPEED": {
                "required_scope": "bit_name_range_and_encoding_identity_only",
                "required_excludes": {"full USB 3.x compliance"},
            },
        },
    },
    "ss_feature_selector_matrix": {
        "allowed_entries": {
            "usb3_port_u1_enable",
            "usb3_port_u2_enable",
            "usb3_port_u1_timeout",
            "usb3_port_u2_timeout",
            "usb3_port_remote_wake_mask",
            "usb3_port_bh_port_reset",
        },
        "required_scope": "selector_name_value_applicability_recipient_identity_only",
        "required_excludes": {
            "firmware compliance",
        },
    },
    "ss_hub_class_request_matrix": {
        "allowed_entries": {
            "usb3_get_status_hub",
            "usb3_get_status_port",
            "usb3_set_feature_hub",
            "usb3_set_feature_port",
            "usb3_clear_feature_hub",
            "usb3_clear_feature_port",
            "usb3_get_descriptor_hub",
            "usb3_set_descriptor_hub",
            "usb3_set_hub_depth",
            "usb3_get_port_err_count",
        },
        "entry_rules": {
            "usb3_get_status_hub": {
                "required_scope": "request_linkage_identity_only",
                "required_excludes": {"full USB 3.x compliance"},
            },
            "usb3_get_status_port": {
                "required_scope": "request_linkage_identity_only",
                "required_excludes": {"full USB 3.x compliance"},
            },
            "usb3_set_feature_hub": {
                "required_scope": "request_linkage_identity_only",
                "required_excludes": {"full USB 3.x compliance"},
            },
            "usb3_set_feature_port": {
                "required_scope": "request_linkage_identity_only",
                "required_excludes": {"full USB 3.x compliance"},
            },
            "usb3_clear_feature_hub": {
                "required_scope": "request_linkage_identity_only",
                "required_excludes": {"full USB 3.x compliance"},
            },
            "usb3_clear_feature_port": {
                "required_scope": "request_linkage_identity_only",
                "required_excludes": {"full USB 3.x compliance"},
            },
            "usb3_get_descriptor_hub": {
                "required_scope": "request_linkage_identity_only",
                "required_excludes": {"full USB 3.x compliance"},
            },
            "usb3_set_descriptor_hub": {
                "required_scope": "request_linkage_identity_only",
                "required_excludes": {"full USB 3.x compliance"},
            },
            "usb3_set_hub_depth": {
                "required_scope": "request_identity_requiredness_only",
                "required_excludes": {"full USB 3.x compliance"},
            },
            "usb3_get_port_err_count": {
                "required_scope": "request_identity_optionality_only",
                "required_excludes": {"full USB 3.x compliance"},
            },
        },
    },
    "ss_hub_interrupt_endpoint_matrix": {
        "allowed_entries": {
            "usb3_ss_hub_ep_bEndpointAddress",
            "usb3_ss_hub_ep_bmAttributes",
            "usb3_ss_hub_ep_wMaxPacketSize",
            "usb3_ss_hub_ep_bInterval",
        },
        "required_scope": "field_identity_constraint_encoding_only",
        "required_excludes": set(),
    },
    "ss_hub_characteristics_bit_matrix": {
        "allowed_entries": {
            "usb3_ss_whc_power_switching",
            "usb3_ss_whc_compound_device",
            "usb3_ss_whc_over_current_mode",
            "usb3_ss_whc_port_indicators",
        },
        "required_scope": "bit_group_name_value_encoding_identity_only",
        "required_excludes": set(),
    },
}

MATRIX_ID_SUFFIX_ALIASES = {
    "hub_descriptor_field_matrix": "hub_descriptor_matrix",
    "hub_characteristics_bit_matrix": "wHubCharacteristics_bit_matrix",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _entry_id(entry: dict[str, Any]) -> str:
    if "trigger_id" in entry:
        return str(entry.get("trigger_id"))
    if "tt_id" in entry:
        return str(entry.get("tt_id"))
    if "selector_id" in entry:
        return str(entry.get("selector_id"))
    if "request_id" in entry:
        return str(entry.get("request_id"))
    if "field_id" in entry:
        return str(entry.get("field_id"))
    if "id" in entry:
        return str(entry.get("id"))
    return f"{entry.get('field')}.bit{entry.get('bit')}.{entry.get('name')}"


def _load_packets(packet_dir: Path) -> dict[str, dict[str, Any]]:
    packets: dict[str, dict[str, Any]] = {}
    if not packet_dir.exists():
        return packets
    for path in sorted(packet_dir.rglob("*.yaml")):
        doc = _load_yaml(path)
        target = doc.get("target") or {}
        entry_id = target.get("entry_id")
        if isinstance(entry_id, str) and entry_id:
            packets[entry_id] = {"path": path, "doc": doc}
    return packets


def _matrix_table_key(matrix_path: Path, matrix: dict[str, Any] | None = None) -> str:
    stem = matrix_path.stem
    if stem in TABLE_RULES:
        return stem

    if matrix is None:
        matrix = _load_yaml(matrix_path)

    matrix_id = str(matrix.get("matrix_id", "")).strip().lower()
    if matrix_id:
        for key in TABLE_RULES:
            suffix = f"_{key}"
            if matrix_id.endswith(suffix):
                return key
            if matrix_id == f"usb20_hub_{key}" or matrix_id == f"usb_hub_{key}":
                return key
            if matrix_id == f"usb20_hub_{suffix}" or matrix_id == f"usb_hub_{suffix}":
                return key

        for alias_suffix, key in MATRIX_ID_SUFFIX_ALIASES.items():
            if matrix_id.endswith(f"_{alias_suffix}") or matrix_id == alias_suffix:
                return key

    return stem


def _entry_gate_rule(rule: dict[str, Any], entry_id: str) -> dict[str, Any]:
    entry_rules = rule.get("entry_rules") or {}
    if entry_id in entry_rules:
        return entry_rules[entry_id]
    return rule


def _registered_source_ids(source_registry_path: Path) -> set[str]:
    registry = _load_yaml(source_registry_path)
    return {
        str(source.get("source_id"))
        for source in (registry.get("sources") or [])
        if isinstance(source, dict) and source.get("source_id")
    }


def _packet_source_errors(
    packet: dict[str, Any],
    loc: str,
    registered_source_ids: set[str],
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    evidence = packet.get("evidence") or {}
    document_ref = evidence.get("document_ref")
    if document_ref is None:
        return errors
    if not isinstance(document_ref, dict):
        return [
            {
                "code": "PACKET_DOCUMENT_REF_INVALID",
                "message": f"{loc}: evidence.document_ref must be an object when present",
            }
        ]

    for source_field in ("primary_source_id", "fallback_source_id"):
        source_id = document_ref.get(source_field)
        if source_id and source_id not in registered_source_ids:
            errors.append(
                {
                    "code": "PACKET_SOURCE_ID_UNREGISTERED",
                    "message": (
                        f"{loc}: evidence.document_ref.{source_field} value "
                        f"{source_id!r} is not registered in the source registry"
                    ),
                }
            )
    return errors


def _packet_schema_errors(
    packet: dict[str, Any],
    loc: str,
) -> list[dict[str, str]]:
    """Apply the executable subset of entry_verification_packet_schema.yaml."""
    schema = _load_yaml(DEFAULT_PACKET_SCHEMA)
    errors: list[dict[str, str]] = []

    def fail(code: str, message: str) -> None:
        errors.append({"code": code, "message": f"{loc}: {message}"})

    for field in schema.get("packet_required_fields") or []:
        if field not in packet:
            fail("PACKET_REQUIRED_FIELD_MISSING", f"packet missing required field '{field}'")

    for container_name, schema_key in (
        ("target", "target_required_fields"),
        ("evidence", "evidence_required_fields"),
        ("verification_scope", "verification_scope_required_fields"),
        ("result", "result_required_fields"),
    ):
        container = packet.get(container_name)
        if not isinstance(container, dict):
            fail("PACKET_REQUIRED_OBJECT_INVALID", f"packet field '{container_name}' must be an object")
            continue
        for field in schema.get(schema_key) or []:
            if field not in container:
                fail(
                    "PACKET_NESTED_REQUIRED_FIELD_MISSING",
                    f"packet {container_name} missing required field '{field}'",
                )

    valid = schema.get("valid_values") or {}
    target = packet.get("target") or {}
    evidence = packet.get("evidence") or {}
    result = packet.get("result") or {}
    checks = (
        ("target.surface", target.get("surface"), valid.get("target_surface") or []),
        ("evidence.spec", evidence.get("spec"), valid.get("spec") or []),
        ("evidence.quoted_surface", evidence.get("quoted_surface"), valid.get("quoted_surface") or []),
        (
            "result.evidence_status",
            result.get("evidence_status"),
            valid.get("result_evidence_status") or [],
        ),
    )
    for field, value, allowed in checks:
        if value not in allowed:
            fail(
                "PACKET_VALUE_OUTSIDE_SCHEMA",
                f"{field} value {value!r} is not in schema valid_values",
            )

    return errors


def _validate_matrix(
    matrix_path: Path,
    packet_dir: Path,
    packets: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    def fail(code: str, message: str) -> None:
        errors.append({"code": code, "message": message})

    matrix = _load_yaml(matrix_path)
    table_key = _matrix_table_key(matrix_path, matrix)
    rule = TABLE_RULES.get(table_key)
    if rule is None:
        fail("MATRIX_NOT_GATED", f"{matrix_path}: no entry verification gate rule is registered")
        return errors

    if matrix.get("claim_level") == "verified":
        fail(
            "TABLE_LEVEL_VERIFIED_NOT_ALLOWED",
            "table-level claim_level=verified is not allowed; only entry-level promotion may be gated",
        )

    entries = matrix.get("entries") or []
    verified_entries = [entry for entry in entries if isinstance(entry, dict) and entry.get("claim_level") == "verified"]

    for idx, entry in enumerate(verified_entries):
        entry_id = _entry_id(entry)
        loc = f"verified_entry[{idx}] {entry_id}"

        if entry_id not in rule["allowed_entries"]:
            fail(
                "VERIFIED_ENTRY_NOT_IN_PILOT_SCOPE",
                f"{loc}: only registered entries {sorted(rule['allowed_entries'])} may be promoted for {table_key}",
            )
            continue

        packet_info = packets.get(entry_id)
        if packet_info is None:
            fail(
                "VERIFIED_ENTRY_MISSING_PACKET",
                f"{loc}: verified promotion requires a matching evidence packet in {packet_dir}",
            )
            continue

        packet = packet_info["doc"]
        errors.extend(_packet_schema_errors(packet, loc))
        result = packet.get("result") or {}
        scope = packet.get("verification_scope") or {}
        target = packet.get("target") or {}
        gate_rule = _entry_gate_rule(rule, entry_id)

        if target.get("surface") != "governed_table_entry" or target.get("table") != table_key:
            fail(
                "PACKET_TARGET_MISMATCH",
                f"{loc}: packet target must be governed_table_entry / {table_key}",
            )

        if result.get("eligible_for_verified") is not True:
            fail(
                "PACKET_NOT_ELIGIBLE",
                f"{loc}: packet result.eligible_for_verified must be true before verified promotion",
            )

        if result.get("evidence_status") != "reviewed":
            fail(
                "PACKET_NOT_REVIEWED",
                f"{loc}: packet result.evidence_status must be 'reviewed' before verified promotion",
            )

        if scope.get("claim") != gate_rule["required_scope"]:
            fail(
                "PACKET_SCOPE_TOO_BROAD",
                f"{loc}: packet verification_scope.claim must be '{gate_rule['required_scope']}'",
            )

        excludes = scope.get("excludes") or []
        if not isinstance(excludes, list):
            fail("PACKET_EXCLUDES_INVALID", f"{loc}: packet verification_scope.excludes must be a list")
        else:
            missing_excludes = sorted(gate_rule["required_excludes"] - set(excludes))
            if missing_excludes:
                fail(
                    "PACKET_EXCLUDES_INCOMPLETE",
                    f"{loc}: packet excludes missing required boundaries: {missing_excludes}",
                )

    return errors


def validate(
    matrix_paths: list[Path],
    packet_dir: Path,
    source_registry_path: Path = DEFAULT_SOURCE_REGISTRY,
) -> tuple[str, list[dict[str, str]]]:
    packets = _load_packets(packet_dir)
    registered_source_ids = _registered_source_ids(source_registry_path)
    errors: list[dict[str, str]] = []
    for packet_info in packets.values():
        errors.extend(
            _packet_source_errors(
                packet_info["doc"],
                f"packet {packet_info['path']}",
                registered_source_ids,
            )
        )
    for matrix_path in matrix_paths:
        errors.extend(
            _validate_matrix(
                matrix_path,
                packet_dir,
                packets,
            )
        )
    return ("FAIL" if errors else "PASS"), errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, action="append")
    parser.add_argument("--packet-dir", type=Path, default=DEFAULT_PACKET_DIR)
    parser.add_argument(
        "--source-registry",
        type=Path,
        default=DEFAULT_SOURCE_REGISTRY,
    )
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    matrix_paths = args.matrix if args.matrix else DEFAULT_MATRICES
    result, errors = validate(matrix_paths, args.packet_dir, args.source_registry)

    for e in errors:
        print(f"[FAIL] {e['code']}: {e['message']}")
    print(f"\nEntry verification gate validation {result}")

    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        receipt = {
            "validator": "validate_entry_verification_gate",
            "matrices": [str(p) for p in matrix_paths],
            "packet_dir": str(args.packet_dir),
            "source_registry": str(args.source_registry),
            "result": result,
            "authority_ceiling": "entry_level_verified_gate_only",
            "errors": errors,
            "table_rules": {
                key: {
                    "allowed_entries": sorted(rule["allowed_entries"]),
                    **(
                        {
                            "required_scope": rule["required_scope"],
                            "required_excludes": sorted(rule["required_excludes"]),
                        }
                        if "required_scope" in rule
                        else {}
                    ),
                    **(
                        {
                            "entry_rules": {
                                entry_id: {
                                    "required_scope": entry_rule["required_scope"],
                                    "required_excludes": sorted(entry_rule["required_excludes"]),
                                }
                                for entry_id, entry_rule in sorted((rule.get("entry_rules") or {}).items())
                            }
                        }
                        if "entry_rules" in rule
                        else {}
                    ),
                }
                for key, rule in TABLE_RULES.items()
            },
        }
        args.receipt_out.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    sys.exit(0 if result == "PASS" else 1)


if __name__ == "__main__":
    main()
