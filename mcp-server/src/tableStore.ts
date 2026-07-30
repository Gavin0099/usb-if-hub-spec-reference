import { readFileSync } from "node:fs";
import { parse as parseYaml } from "yaml";
import { repoPath } from "./repoPaths.js";
import { loadManifest, type GovernedTableRef } from "./manifest.js";

export interface NormalizedEntry {
  tableId: string;
  specFamily: "usb20" | "usb3";
  entryId: string;
  /** Lowercased, alnum-only search candidates derived from this entry. */
  searchKeys: string[];
  claimLevel?: string;
  evidenceStatus?: string;
  sectionAnchor?: string;
  notes?: string;
  reviewedMeaning?: string;
  /** Repo-relative evidence packet path, if declared inline on this entry. */
  inlineVerificationPacket?: string;
  raw: Record<string, unknown>;
}

function normalizeKey(value: unknown): string | undefined {
  if (typeof value === "string" && value.trim().length > 0) {
    return value.trim().toLowerCase().replace(/[^a-z0-9]+/g, "");
  }
  if (typeof value === "number") {
    return String(value);
  }
  return undefined;
}

/** Depth-first search for the first `verification_packet` key anywhere in the entry. */
function findVerificationPacketDeep(obj: unknown, depth = 0): string | undefined {
  if (depth > 4 || obj === null || typeof obj !== "object") {
    return undefined;
  }
  const record = obj as Record<string, unknown>;
  if (typeof record["verification_packet"] === "string") {
    return record["verification_packet"];
  }
  for (const value of Object.values(record)) {
    if (value && typeof value === "object") {
      const found = findVerificationPacketDeep(value, depth + 1);
      if (found) return found;
    }
  }
  return undefined;
}

function computeEntryId(raw: Record<string, unknown>): string {
  if (typeof raw["field_id"] === "string") return raw["field_id"];
  if (typeof raw["id"] === "string") return raw["id"];
  if (typeof raw["selector_id"] === "string") return raw["selector_id"];
  if (typeof raw["request_id"] === "string") return raw["request_id"];
  if (
    typeof raw["field"] === "string" &&
    raw["bit"] !== undefined &&
    typeof raw["name"] === "string"
  ) {
    return `${raw["field"]}.bit${raw["bit"]}.${raw["name"]}`;
  }
  // Last resort: stable-ish fallback so lookups never crash. This should not
  // occur for any of the 13 table shapes this tool set actually reads.
  return JSON.stringify(raw).slice(0, 64);
}

function computeSearchKeys(entryId: string, raw: Record<string, unknown>): string[] {
  const candidates: unknown[] = [
    entryId,
    raw["field_name"],
    raw["selector_name"],
    raw["request_name"],
    raw["name"],
    raw["semantic_group"],
    raw["field"],
    raw["bit_range"],
    raw["selector_value"],
    raw["selector_value_hex"],
    raw["request_family"],
  ];
  const keys = new Set<string>();
  for (const c of candidates) {
    const k = normalizeKey(c);
    if (k) keys.add(k);
  }
  return [...keys];
}

function sectionAnchorOf(raw: Record<string, unknown>): string | undefined {
  if (typeof raw["section_anchor"] === "string") return raw["section_anchor"];
  const refs = raw["section_refs"];
  if (Array.isArray(refs) && refs.length > 0) {
    const first = refs[0] as Record<string, unknown>;
    if (first?.["spec"] && first?.["section"]) {
      return `${first["spec"]} §${first["section"]}`;
    }
  }
  return undefined;
}

function normalizeEntry(
  tableId: string,
  specFamily: "usb20" | "usb3",
  raw: Record<string, unknown>
): NormalizedEntry {
  const entryId = computeEntryId(raw);
  return {
    tableId,
    specFamily,
    entryId,
    searchKeys: computeSearchKeys(entryId, raw),
    claimLevel: typeof raw["claim_level"] === "string" ? raw["claim_level"] : undefined,
    evidenceStatus:
      typeof raw["evidence_status"] === "string" ? raw["evidence_status"] : undefined,
    sectionAnchor: sectionAnchorOf(raw),
    notes: typeof raw["notes"] === "string" ? raw["notes"] : undefined,
    reviewedMeaning:
      typeof raw["reviewed_meaning"] === "string" ? raw["reviewed_meaning"] : undefined,
    inlineVerificationPacket: findVerificationPacketDeep(raw),
    raw,
  };
}

interface LoadedTable {
  ref: GovernedTableRef;
  entries: NormalizedEntry[];
}

let cachedTables: Map<string, LoadedTable> | undefined;

export function loadGovernedTables(forceReload = false): Map<string, LoadedTable> {
  if (cachedTables && !forceReload) {
    return cachedTables;
  }
  const manifest = loadManifest(forceReload);
  const tables = new Map<string, LoadedTable>();

  for (const ref of manifest.governed_tables) {
    const raw = parseYaml(readFileSync(repoPath(ref.path), "utf-8")) as Record<string, unknown>;
    const rawEntries = Array.isArray(raw["entries"]) ? (raw["entries"] as unknown[]) : [];
    const entries = rawEntries.map((e) =>
      normalizeEntry(ref.id, ref.spec_family, e as Record<string, unknown>)
    );
    tables.set(ref.id, { ref, entries });
  }

  cachedTables = tables;
  return tables;
}

export function getTable(tableId: string): LoadedTable | undefined {
  return loadGovernedTables().get(tableId);
}

/** Searches one or more tables for entries matching a free-text query against searchKeys. */
export function searchTables(tableIds: string[], query: string): NormalizedEntry[] {
  const key = normalizeKey(query);
  if (!key) return [];
  const results: NormalizedEntry[] = [];
  for (const tableId of tableIds) {
    const table = getTable(tableId);
    if (!table) continue;
    for (const entry of table.entries) {
      if (entry.searchKeys.includes(key)) {
        results.push(entry);
      }
    }
  }
  return results;
}

export function specFamilyMatches(
  entrySpecFamily: "usb20" | "usb3",
  requested: string | undefined
): boolean {
  if (!requested || requested === "any") return true;
  return entrySpecFamily === requested;
}
