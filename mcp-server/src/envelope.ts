import { findGovernedTable } from "./manifest.js";
import type { NormalizedEntry } from "./tableStore.js";
import { getDriftStatus } from "./fingerprint.js";
import { lookupPacketByEntryId } from "./packetIndex.js";

/** Verbatim from exports/hub_governed_surface_manifest.yaml#/claim_ceiling/cannot_establish. */
export const CANNOT_ESTABLISH = [
  "firmware_behavior",
  "project_specific_truth",
  "observed_device_behavior",
  "vendor_specific_behavior",
  "LTSSM_runtime_behavior",
  "xHCI_port_management",
  "electrical_or_timing_compliance",
  "USB_IF_certification_completeness",
] as const;

export interface EnvelopeResultItem {
  [key: string]: unknown;
}

export interface Envelope {
  resultType: "complete";
  query_echo: string;
  match_found: boolean;
  result: EnvelopeResultItem[];
  claim_level: "verified" | "reviewed" | "not_governed";
  verified_scope: string | null;
  reviewed_meaning: string | null;
  spec_family: "usb20" | "usb3" | null;
  source: {
    table_id: string;
    path: string;
    validator: string;
    manifest_version: string;
  } | null;
  evidence_packet_id: string | null;
  cannot_establish: readonly string[];
  drift_status: "clean" | "drift_detected" | "unknown";
}

export function resolveEvidencePacketId(entry: NormalizedEntry): string | null {
  if (entry.inlineVerificationPacket) return entry.inlineVerificationPacket;
  const fromIndex = lookupPacketByEntryId(entry.entryId);
  return fromIndex?.packetPath ?? null;
}

/**
 * Builds the shared response envelope required by every tool. When multiple
 * entries match, claim_level/verified_scope/reviewed_meaning/source reflect
 * the FIRST matched entry only (each result item also carries its own
 * table_id/entry_id so callers can distinguish per-item provenance when
 * result.length > 1).
 */
export function buildEnvelope(
  queryEcho: string,
  matches: NormalizedEntry[],
  toResultItem: (entry: NormalizedEntry) => EnvelopeResultItem
): Envelope {
  const { driftStatus } = getDriftStatus();

  if (matches.length === 0) {
    return {
      resultType: "complete",
      query_echo: queryEcho,
      match_found: false,
      result: [],
      claim_level: "not_governed",
      verified_scope: null,
      reviewed_meaning: null,
      spec_family: null,
      source: null,
      evidence_packet_id: null,
      cannot_establish: CANNOT_ESTABLISH,
      drift_status: driftStatus,
    };
  }

  const primary = matches[0];
  const tableRef = findGovernedTable(primary.tableId);
  const claimLevel = primary.claimLevel === "verified" ? "verified" : "reviewed";

  return {
    resultType: "complete",
    query_echo: queryEcho,
    match_found: true,
    result: matches.map(toResultItem),
    claim_level: claimLevel,
    verified_scope: tableRef?.verified_scope ?? null,
    reviewed_meaning:
      claimLevel === "reviewed"
        ? (primary.reviewedMeaning ?? tableRef?.reviewed_meaning ?? null)
        : null,
    spec_family: primary.specFamily,
    source: tableRef
      ? {
          table_id: tableRef.id,
          path: tableRef.path,
          validator: tableRef.validator,
          manifest_version: "0.3",
        }
      : null,
    evidence_packet_id: resolveEvidencePacketId(primary),
    cannot_establish: CANNOT_ESTABLISH,
    drift_status: driftStatus,
  };
}
