import { readFileSync } from "node:fs";
import { parse as parseYaml } from "yaml";
import { repoPath } from "./repoPaths.js";

export interface GovernedTableRef {
  id: string;
  spec_family: "usb20" | "usb3";
  path: string;
  validator: string;
  state: string;
  verified: number;
  reviewed: number;
  verified_scope?: string;
  reviewed_meaning?: string;
}

export interface ClaimCeiling {
  default: string;
  cannot_establish: string[];
}

export interface GovernedSurfaceManifest {
  manifest_id: string;
  manifest_version: string;
  export_type: string;
  generated_at: string;
  authority_surface: Record<string, unknown>;
  claim_ceiling: ClaimCeiling;
  consumer_usage: {
    intended_for: string[];
    must_not: string[];
  };
  governed_tables: GovernedTableRef[];
}

const MANIFEST_PATH = repoPath("exports", "hub_governed_surface_manifest.yaml");

let cachedManifest: GovernedSurfaceManifest | undefined;

/**
 * Loads and caches exports/hub_governed_surface_manifest.yaml.
 *
 * Per this proposal's non-negotiable design constraint #1, this is the ONLY
 * entry point tools may use to discover which governed tables exist and
 * where they live — no tool reads tables/*.yaml paths that are not listed
 * here.
 */
export function loadManifest(forceReload = false): GovernedSurfaceManifest {
  if (cachedManifest && !forceReload) {
    return cachedManifest;
  }
  const raw = readFileSync(MANIFEST_PATH, "utf-8");
  const parsed = parseYaml(raw) as GovernedSurfaceManifest;
  cachedManifest = parsed;
  return parsed;
}

export function findGovernedTable(tableId: string): GovernedTableRef | undefined {
  return loadManifest().governed_tables.find((t) => t.id === tableId);
}
