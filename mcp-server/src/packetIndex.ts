import { readdirSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { parse as parseYaml } from "yaml";
import { repoPath, toRepoRelative } from "./repoPaths.js";

export interface PacketIndexEntry {
  /** Repo-relative path, e.g. evidence/entry_verification_packets/usb3/ss_hub_descriptor_usb3_bLength.yaml */
  packetPath: string;
  table: string;
  entryId: string;
  verificationScopeClaim?: string;
}

const PACKET_DIR = repoPath("evidence", "entry_verification_packets");

function walkYamlFiles(dir: string, out: string[]): void {
  for (const name of readdirSync(dir)) {
    const full = path.join(dir, name);
    const st = statSync(full);
    if (st.isDirectory()) {
      walkYamlFiles(full, out);
    } else if (name.endsWith(".yaml") || name.endsWith(".yml")) {
      out.push(full);
    }
  }
}

let cachedIndex: Map<string, PacketIndexEntry> | undefined;

/**
 * Builds an index of entry_id -> evidence packet pointer by recursively
 * scanning evidence/entry_verification_packets/**\/*.yaml and reading each
 * packet's own self-declared `target.entry_id` / `target.table` fields.
 *
 * This intentionally does NOT guess packet filenames from entry_id naming
 * conventions (those conventions differ per table group and guessing would
 * risk pointing to a nonexistent or wrong file). Every pointer this index
 * returns is backed by a real file that was actually read and parsed.
 */
export function loadPacketIndex(forceReload = false): Map<string, PacketIndexEntry> {
  if (cachedIndex && !forceReload) {
    return cachedIndex;
  }
  const files: string[] = [];
  walkYamlFiles(PACKET_DIR, files);

  const index = new Map<string, PacketIndexEntry>();
  for (const file of files) {
    let parsed: unknown;
    try {
      parsed = parseYaml(readFileSync(file, "utf-8"));
    } catch {
      continue; // Skip unparseable files rather than fail server startup.
    }
    const target = (parsed as Record<string, unknown> | null)?.["target"] as
      | Record<string, unknown>
      | undefined;
    const entryId = target?.["entry_id"];
    const table = target?.["table"];
    if (typeof entryId !== "string" || typeof table !== "string") {
      continue;
    }
    const verificationScope = (parsed as Record<string, unknown>)["verification_scope"] as
      | Record<string, unknown>
      | undefined;
    const claim = verificationScope?.["claim"];

    index.set(entryId, {
      packetPath: toRepoRelative(file),
      table,
      entryId,
      verificationScopeClaim: typeof claim === "string" ? claim : undefined,
    });
  }

  cachedIndex = index;
  return index;
}

export function lookupPacketByEntryId(entryId: string): PacketIndexEntry | undefined {
  return loadPacketIndex().get(entryId);
}
