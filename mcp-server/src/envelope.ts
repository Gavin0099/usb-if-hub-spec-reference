import { findGovernedTable, loadManifest } from "./manifest.js";
import type { NormalizedEntry } from "./tableStore.js";
import { getDriftStatus } from "./fingerprint.js";
import { lookupPacketByEntryId } from "./packetIndex.js";

export type EnvelopeClaimLevel = "verified" | "reviewed" | "not_governed";

export interface EnvelopeSource {
  table_id: string;
  path: string;
  validator: string;
  manifest_version: string;
}

export interface EnvelopeResultItem {
  [key: string]: unknown;
}

export interface Envelope {
  resultType: "complete";
  query_echo: string;
  match_found: boolean;
  result: EnvelopeResultItem[];
  claim_level: EnvelopeClaimLevel;
  verified_scope: string | null;
  reviewed_meaning: string | null;
  spec_family: "usb20" | "usb3" | null;
  source: EnvelopeSource | null;
  evidence_packet_id: string | null;
  cannot_establish: readonly string[];
  drift_status: "clean" | "drift_detected" | "unknown";
}

export function resolveEvidencePacketId(entry: NormalizedEntry): string | null {
  if (entry.inlineVerificationPacket) return entry.inlineVerificationPacket;
  const fromIndex = lookupPacketByEntryId(entry.entryId);
  return fromIndex?.packetPath ?? null;
}

export function getCannotEstablish(): readonly string[] {
  return [...loadManifest().claim_ceiling.cannot_establish];
}

function singleSharedValue<T>(values: T[]): T | null {
  if (values.length === 0) return null;
  const first = values[0];
  return values.every((value) => value === first) ? first : null;
}

export function entryEnvelopeMetadata(entry: NormalizedEntry): Record<string, unknown> {
  const manifest = loadManifest();
  const tableRef = findGovernedTable(entry.tableId);
  const claimLevel = entry.claimLevel === "verified" ? "verified" : "reviewed";

  return {
    table_id: entry.tableId,
    entry_id: entry.entryId,
    spec_family: entry.specFamily,
    claim_level: claimLevel,
    verified_scope: tableRef?.verified_scope ?? null,
    reviewed_meaning:
      claimLevel === "reviewed"
        ? (entry.reviewedMeaning ?? tableRef?.reviewed_meaning ?? null)
        : null,
    source: tableRef
      ? {
          table_id: tableRef.id,
          path: tableRef.path,
          validator: tableRef.validator,
          manifest_version: manifest.manifest_version,
        }
      : null,
    evidence_packet_id: resolveEvidencePacketId(entry),
  };
}

export function summarizeMatches(
  matches: NormalizedEntry[]
): Pick<
  Envelope,
  | "claim_level"
  | "verified_scope"
  | "reviewed_meaning"
  | "spec_family"
  | "source"
  | "evidence_packet_id"
> {
  if (matches.length === 0) {
    return {
      claim_level: "not_governed",
      verified_scope: null,
      reviewed_meaning: null,
      spec_family: null,
      source: null,
      evidence_packet_id: null,
    };
  }

  const metadata = matches.map((entry) => entryEnvelopeMetadata(entry));
  const allVerified = metadata.every((item) => item["claim_level"] === "verified");
  const allReviewed = metadata.every((item) => item["claim_level"] === "reviewed");
  const tableIds = matches.map((entry) => entry.tableId);
  const sharedTableId = singleSharedValue(tableIds);

  return {
    // A mixed verified/reviewed set is reviewed at the envelope level. The
    // envelope must never borrow the strongest claim from one result.
    claim_level: allVerified ? "verified" : "reviewed",
    verified_scope: singleSharedValue(
      metadata.map((item) => item["verified_scope"] as string | null)
    ),
    reviewed_meaning: allReviewed
      ? singleSharedValue(
          metadata.map((item) => item["reviewed_meaning"] as string | null)
        )
      : null,
    spec_family: singleSharedValue(matches.map((entry) => entry.specFamily)),
    source:
      sharedTableId !== null
        ? (metadata[0]["source"] as EnvelopeSource | null)
        : null,
    evidence_packet_id: singleSharedValue(
      metadata.map((item) => item["evidence_packet_id"] as string | null)
    ),
  };
}

/** Builds the shared response envelope required by every lookup tool. */
export function buildEnvelope(
  queryEcho: string,
  matches: NormalizedEntry[],
  toResultItem: (entry: NormalizedEntry) => EnvelopeResultItem
): Envelope {
  const { driftStatus } = getDriftStatus();
  const cannotEstablish = getCannotEstablish();

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
      cannot_establish: cannotEstablish,
      drift_status: driftStatus,
    };
  }

  const summary = summarizeMatches(matches);

  return {
    resultType: "complete",
    query_echo: queryEcho,
    match_found: true,
    result: matches.map((entry) => ({
      ...toResultItem(entry),
      ...entryEnvelopeMetadata(entry),
    })),
    ...summary,
    cannot_establish: cannotEstablish,
    drift_status: driftStatus,
  };
}
