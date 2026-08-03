import { z } from "zod";
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { getTable, specFamilyMatches, type NormalizedEntry } from "./tableStore.js";
import {
  buildEnvelope,
  entryEnvelopeMetadata,
  getCannotEstablish,
  summarizeMatches,
} from "./envelope.js";
import { findGovernedTable, loadManifest } from "./manifest.js";
import { getDriftStatus } from "./fingerprint.js";

const SPEC_FAMILY_ENUM = ["usb20", "usb3", "any"] as const;
const TERM_TYPE_ENUM = ["field", "bit", "selector", "request", "any"] as const;
type TermType = (typeof TERM_TYPE_ENUM)[number];

function normStr(v: unknown): string {
  return typeof v === "string" ? v.trim().toLowerCase() : "";
}

function textResult(payload: unknown) {
  return {
    content: [{ type: "text" as const, text: JSON.stringify(payload, null, 2) }],
  };
}

function entriesOf(tableId: string): NormalizedEntry[] {
  return getTable(tableId)?.entries ?? [];
}

/** Common result-item shape: identity/position/encoding fields only, plus provenance pointers. */
function baseResultItem(entry: NormalizedEntry): Record<string, unknown> {
  return {
    ...entryEnvelopeMetadata(entry),
    evidence_status: entry.evidenceStatus ?? null,
    section_anchor: entry.sectionAnchor ?? null,
    notes: entry.notes ?? null,
  };
}

// ── Tool 1 — lookup_hub_field ──────────────────────────────────────────────

const HUB_FIELD_TABLES = [
  "usb20_hub_descriptor_field_matrix",
  "usb3_ss_hub_descriptor_field_matrix",
  "usb20_hub_characteristics_bit_matrix",
  "usb3_ss_hub_characteristics_bit_matrix",
  "usb20_hub_interrupt_endpoint_matrix",
  "usb3_ss_hub_interrupt_endpoint_matrix",
];

export function findHubFieldMatches(
  fieldName: string,
  specFamily: (typeof SPEC_FAMILY_ENUM)[number] = "any"
): NormalizedEntry[] {
  const q = normStr(fieldName);
  return HUB_FIELD_TABLES.flatMap((tableId) =>
    entriesOf(tableId).filter((entry) => {
      if (!specFamilyMatches(entry.specFamily, specFamily)) return false;
      const raw = entry.raw;
      // raw.field is a parent/container field on bit-group entries. Including
      // it makes a query for wHubCharacteristics return every child bit group
      // and incorrectly merges their claim boundaries with the descriptor
      // field itself.
      const candidates = [
        raw["field_name"],
        raw["semantic_group"],
        entry.entryId,
      ].map(normStr);
      return candidates.includes(q);
    })
  );
}

function registerLookupHubField(server: McpServer) {
  server.registerTool(
    "lookup_hub_field",
    {
      description:
        "Look up a USB hub descriptor field, wHubCharacteristics bit group, or hub interrupt endpoint field by name. Returns identity/position/encoding only. Does not return firmware behavior.",
      inputSchema: {
        field_name: z.string().describe("Field name, e.g. bDescLength, wHubCharacteristics, PORT_INDICATOR bit group"),
        spec_family: z.enum(SPEC_FAMILY_ENUM).default("any"),
      },
    },
    async ({ field_name, spec_family }) => {
      const matches = findHubFieldMatches(field_name, spec_family);

      const envelope = buildEnvelope(field_name, matches, (entry) => ({
        ...baseResultItem(entry),
        field_name: entry.raw["field_name"] ?? entry.raw["semantic_group"] ?? null,
        offset: entry.raw["offset"] ?? null,
        size: entry.raw["size"] ?? null,
        bit_range: entry.raw["bit_range"] ?? null,
        role: entry.raw["role"] ?? null,
        value_encoding: entry.raw["value_encoding"] ?? null,
      }));
      return textResult(envelope);
    }
  );
}

// ── Tool 2 — lookup_feature_selector ───────────────────────────────────────

const FEATURE_SELECTOR_TABLES = ["usb_hub_feature_selector_matrix", "usb3_ss_feature_selector_matrix"];

function registerLookupFeatureSelector(server: McpServer) {
  server.registerTool(
    "lookup_feature_selector",
    {
      description:
        "Look up a USB hub feature selector by name or value (e.g. PORT_RESET, PORT_U1_TIMEOUT). Returns selector name, value, applicable recipient, and spec family. Does not confirm host or firmware runtime behavior when the feature is set.",
      inputSchema: {
        selector_name: z.string().optional(),
        selector_value: z.number().int().optional(),
        spec_family: z.enum(SPEC_FAMILY_ENUM).default("any"),
      },
    },
    async ({ selector_name, selector_value, spec_family }) => {
      const nameQ = normStr(selector_name);
      const matches = FEATURE_SELECTOR_TABLES.flatMap((tableId) =>
        entriesOf(tableId).filter((entry) => {
          if (!specFamilyMatches(entry.specFamily, spec_family)) return false;
          const raw = entry.raw;
          const nameMatch = nameQ.length > 0 && normStr(raw["selector_name"]) === nameQ;
          const valueMatch = selector_value !== undefined && raw["selector_value"] === selector_value;
          return nameMatch || valueMatch;
        })
      );

      const echo = selector_name ?? (selector_value !== undefined ? String(selector_value) : "");
      const envelope = buildEnvelope(echo, matches, (entry) => ({
        ...baseResultItem(entry),
        selector_name: entry.raw["selector_name"] ?? null,
        selector_value: entry.raw["selector_value"] ?? null,
        selector_value_hex: entry.raw["selector_value_hex"] ?? null,
        applies_to: entry.raw["applies_to"] ?? entry.raw["recipient"] ?? null,
        request_usage: entry.raw["request_usage"] ?? null,
      }));
      return textResult(envelope);
    }
  );
}

// ── Tool 3 — lookup_port_status_bit ────────────────────────────────────────

const PORT_STATUS_BIT_TABLES = ["usb20_hub_port_status_bit_matrix", "usb3_ss_hub_port_status_bit_matrix"];

export function portStatusResultItem(entry: NormalizedEntry): Record<string, unknown> {
  return {
    ...baseResultItem(entry),
    field: entry.raw["field"] ?? null,
    bit: entry.raw["bit"] ?? null,
    bit_range: entry.raw["bit_range"] ?? null,
    name: entry.raw["name"] ?? null,
    status: entry.raw["status"] ?? null,
    value_encoding: entry.raw["value_encoding"] ?? null,
  };
}

function registerLookupPortStatusBit(server: McpServer) {
  server.registerTool(
    "lookup_port_status_bit",
    {
      description:
        "Look up a hub/port status or change bit by name (e.g. C_PORT_CONNECTION, PORT_LINK_STATE). Returns bit name, position, and encoding identity only. For PORT_LINK_STATE and PORT_SPEED specifically, verified_scope covers bit range and encoding table identity only — LTSSM state transitions are never verified by this tool.",
      inputSchema: {
        bit_name: z.string(),
        spec_family: z.enum(SPEC_FAMILY_ENUM).default("any"),
      },
    },
    async ({ bit_name, spec_family }) => {
      const q = normStr(bit_name);
      const matches = PORT_STATUS_BIT_TABLES.flatMap((tableId) =>
        entriesOf(tableId).filter((entry) => {
          if (!specFamilyMatches(entry.specFamily, spec_family)) return false;
          return normStr(entry.raw["name"]) === q;
        })
      );

      const envelope = buildEnvelope(bit_name, matches, portStatusResultItem);
      return textResult(envelope);
    }
  );
}

// ── Tool 4 — lookup_class_request ──────────────────────────────────────────

const CLASS_REQUEST_TABLES = [
  "usb_hub_class_request_matrix",
  "usb3_ss_hub_class_request_matrix",
  "usb20_standard_device_request_matrix",
];

function registerLookupClassRequest(server: McpServer) {
  server.registerTool(
    "lookup_class_request",
    {
      description:
        "Look up a USB hub class request or standard device request by name (e.g. SET_HUB_DEPTH, GET_PORT_ERR_COUNT). Returns bRequest, bmRequestType, recipient, and required/optional identity. Does not confirm host driver call sequence or timing.",
      inputSchema: {
        request_name: z.string(),
        spec_family: z.enum(SPEC_FAMILY_ENUM).default("any"),
      },
    },
    async ({ request_name, spec_family }) => {
      const q = normStr(request_name);
      const matches = CLASS_REQUEST_TABLES.flatMap((tableId) =>
        entriesOf(tableId).filter((entry) => {
          if (!specFamilyMatches(entry.specFamily, spec_family)) return false;
          const raw = entry.raw;
          return normStr(raw["request_name"]) === q || normStr(entry.entryId) === q;
        })
      );

      const envelope = buildEnvelope(request_name, matches, (entry) => ({
        ...baseResultItem(entry),
        request_name: entry.raw["request_name"] ?? null,
        recipient: entry.raw["recipient"] ?? null,
        setup: entry.raw["setup"] ?? null,
        bRequest_hex: entry.raw["bRequest_hex"] ?? null,
      }));
      return textResult(envelope);
    }
  );
}

// ── Tool 5 — compare_usb_versions ──────────────────────────────────────────

const ALL_TERM_TABLES = [
  ...HUB_FIELD_TABLES,
  ...FEATURE_SELECTOR_TABLES,
  ...PORT_STATUS_BIT_TABLES,
  ...CLASS_REQUEST_TABLES,
];

function tablesForTermType(termType: TermType): string[] {
  switch (termType) {
    case "field":
      return HUB_FIELD_TABLES;
    case "bit":
      return PORT_STATUS_BIT_TABLES;
    case "selector":
      return FEATURE_SELECTOR_TABLES;
    case "request":
      return CLASS_REQUEST_TABLES;
    default:
      return ALL_TERM_TABLES;
  }
}

export function findVersionComparisonMatches(
  term: string,
  termType: TermType = "any"
): NormalizedEntry[] {
  const q = normStr(term).replace(/[^a-z0-9]+/g, "");
  return tablesForTermType(termType).flatMap((tableId) =>
    entriesOf(tableId).filter((entry) => entry.searchKeys.includes(q))
  );
}

function registerCompareUsbVersions(server: McpServer) {
  server.registerTool(
    "compare_usb_versions",
    {
      description:
        "Compare a field, bit, selector, or request name across USB 2.0 and USB 3.x governed tables. Returns both entries (or 'not_governed_in_this_family' for the missing side) side by side. Never infers that identical naming implies identical runtime behavior.",
      inputSchema: {
        term: z.string(),
        term_type: z.enum(TERM_TYPE_ENUM).default("any"),
      },
    },
    async ({ term, term_type }) => {
      const matches = findVersionComparisonMatches(term, term_type);

      const usb20 = matches.filter((m) => m.specFamily === "usb20");
      const usb3 = matches.filter((m) => m.specFamily === "usb3");
      const { driftStatus } = getDriftStatus();
      const summary = summarizeMatches(matches);

      const toItem = (entry: NormalizedEntry) => ({
        ...baseResultItem(entry),
        raw_identity: {
          field_name: entry.raw["field_name"] ?? null,
          selector_name: entry.raw["selector_name"] ?? null,
          request_name: entry.raw["request_name"] ?? null,
          name: entry.raw["name"] ?? null,
        },
      });

      const envelope = {
        resultType: "complete" as const,
        query_echo: term,
        match_found: matches.length > 0,
        result: [
          {
            usb20: usb20.length > 0 ? usb20.map(toItem) : "not_governed_in_this_family",
            usb3: usb3.length > 0 ? usb3.map(toItem) : "not_governed_in_this_family",
          },
        ],
        ...summary,
        cannot_establish: getCannotEstablish(),
        drift_status: driftStatus,
        non_claim: "Identical naming across usb20/usb3 does not imply identical runtime behavior.",
      };
      return textResult(envelope);
    }
  );
}

// ── Tool 6 — get_verified_evidence ─────────────────────────────────────────

function registerGetVerifiedEvidence(server: McpServer) {
  server.registerTool(
    "get_verified_evidence",
    {
      description:
        "Given a governed table entry id, return its evidence_packet_id and source table pointer from the manifest. Does not fetch or reinterpret PDF content; the caller must treat this as a citation pointer only.",
      inputSchema: {
        table_id: z.string(),
        entry_id: z.string(),
      },
    },
    async ({ table_id, entry_id }) => {
      const table = getTable(table_id);
      const entry = table?.entries.find((e) => e.entryId === entry_id);
      const matches = entry ? [entry] : [];

      const envelope = buildEnvelope(`${table_id}:${entry_id}`, matches, (e) => ({
        ...baseResultItem(e),
      }));
      if (!entry) {
        (envelope as unknown as Record<string, unknown>)["note"] = findGovernedTable(table_id)
          ? "entry_id not found in this table"
          : "table_id not present in exports/hub_governed_surface_manifest.yaml";
      }
      return textResult(envelope);
    }
  );
}

// ── Tool 7 — check_reserved_usage ───────────────────────────────────────────

export function reservedUsageResultItem(entry: NormalizedEntry): Record<string, unknown> {
  const rawStatus = entry.raw["status"];
  const statusReserved = typeof rawStatus === "string" && rawStatus.toLowerCase() === "reserved";
  const descriptiveText = [entry.reviewedMeaning, entry.notes, entry.raw["description"]]
    .filter((value): value is string => typeof value === "string")
    .join(" ");

  return {
    ...baseResultItem(entry),
    is_reserved:
      entry.claimLevel === "reviewed" &&
      (statusReserved || /reserved/i.test(descriptiveText)),
    reviewed_meaning: entry.reviewedMeaning ?? null,
  };
}

function registerCheckReservedUsage(server: McpServer) {
  server.registerTool(
    "check_reserved_usage",
    {
      description:
        "Check whether a given bit position, byte range, or field is marked as a reserved boundary placeholder in the governed tables, as a guard against assuming semantic meaning for reserved bits.",
      inputSchema: {
        identifier: z.string().describe("Bit name, byte offset, or field name to check"),
        spec_family: z.enum(SPEC_FAMILY_ENUM).default("any"),
      },
    },
    async ({ identifier, spec_family }) => {
      const q = normStr(identifier).replace(/[^a-z0-9]+/g, "");
      const matches = ALL_TERM_TABLES.flatMap((tableId) =>
        entriesOf(tableId).filter((entry) => {
          if (!specFamilyMatches(entry.specFamily, spec_family)) return false;
          return entry.searchKeys.includes(q);
        })
      );

      const envelope = buildEnvelope(identifier, matches, reservedUsageResultItem);
      return textResult(envelope);
    }
  );
}

// ── Tool 8 — escalate_spec_conflict ────────────────────────────────────────

function registerEscalateSpecConflict(server: McpServer) {
  server.registerTool(
    "escalate_spec_conflict",
    {
      description:
        "Format a three-column (standard fact / project fact / observed fact) comparison table for a named field/bit/selector/request. The 'standard fact' column is populated from this repo's governed lookup tools. The 'project fact' and 'observed fact' columns are taken verbatim from caller input and are NOT verified or endorsed by this server. This tool never outputs a resolution or recommendation — only the comparison table plus a fixed disclaimer.",
      inputSchema: {
        term: z.string(),
        project_fact: z.string().describe("Caller-supplied, verbatim, unverified"),
        observed_fact: z.string().optional().describe("Caller-supplied, verbatim, unverified"),
      },
    },
    async ({ term, project_fact, observed_fact }) => {
      const q = normStr(term).replace(/[^a-z0-9]+/g, "");
      const matches = ALL_TERM_TABLES.flatMap((tableId) =>
        entriesOf(tableId).filter((entry) => entry.searchKeys.includes(q))
      );
      const { driftStatus } = getDriftStatus();

      const standardFact =
        matches.length > 0
          ? matches.map((entry) => ({
              ...baseResultItem(entry),
              raw_identity: {
                field_name: entry.raw["field_name"] ?? null,
                selector_name: entry.raw["selector_name"] ?? null,
                request_name: entry.raw["request_name"] ?? null,
                name: entry.raw["name"] ?? null,
              },
            }))
          : "not_governed";

      const payload = {
        resultType: "complete" as const,
        query_echo: term,
        match_found: matches.length > 0,
        result: [
          {
            term,
            standard_fact: standardFact,
            project_fact: { value: project_fact, verified: false, source: "caller_supplied" },
            observed_fact: observed_fact
              ? { value: observed_fact, verified: false, source: "caller_supplied" }
              : null,
          },
        ],
        claim_level: matches.length > 0 ? ("reviewed" as const) : ("not_governed" as const),
        verified_scope: null,
        reviewed_meaning: null,
        spec_family: null,
        source: null,
        evidence_packet_id: null,
        cannot_establish: getCannotEstablish(),
        drift_status: driftStatus,
        disclaimer:
          "This tool does not resolve standard/project/observed fact conflicts. Per AGENTS.md, conflict resolution belongs to the consuming repo's escalation process. project_fact and observed_fact are unverified caller input, not endorsed by this server.",
      };
      return textResult(payload);
    }
  );
}

// ── Tool 9 — get_governed_surface_status ───────────────────────────────────

function registerGetGovernedSurfaceStatus(server: McpServer) {
  server.registerTool(
    "get_governed_surface_status",
    {
      description:
        "Return the current governed surface summary: table counts, verified/reviewed counts per spec family, manifest version, and the last table-fingerprint drift check result. Use this before treating any other tool's output as current if drift_status is not 'clean'.",
      inputSchema: {},
    },
    async () => {
      const manifest = loadManifest();
      const { driftStatus, checkedAt } = getDriftStatus();
      const payload = {
        resultType: "complete" as const,
        manifest_id: manifest.manifest_id,
        manifest_version: manifest.manifest_version,
        generated_at: manifest.generated_at,
        authority_surface: manifest.authority_surface,
        claim_ceiling: manifest.claim_ceiling,
        governed_table_count: manifest.governed_tables.length,
        drift_status: driftStatus,
        drift_last_checked_at: checkedAt,
      };
      return textResult(payload);
    },
    // ttlMs / cacheScope per mcp_tool_schema.md Tool 9. These are advisory
    // caching hints for CacheableResult-aware clients; this SDK version does
    // not enforce them server-side, so the freshness guarantee is provided
    // by fingerprint.ts's own CHECK_INTERVAL_MS instead.
  );
}

export function registerAllTools(server: McpServer): void {
  registerLookupHubField(server);
  registerLookupFeatureSelector(server);
  registerLookupPortStatusBit(server);
  registerLookupClassRequest(server);
  registerCompareUsbVersions(server);
  registerGetVerifiedEvidence(server);
  registerCheckReservedUsage(server);
  registerEscalateSpecConflict(server);
  registerGetGovernedSurfaceStatus(server);
}
