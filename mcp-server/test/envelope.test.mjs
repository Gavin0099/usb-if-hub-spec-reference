import test from "node:test";
import assert from "node:assert/strict";

import {
  buildEnvelope,
  getCannotEstablish,
  summarizeMatches,
} from "../dist/envelope.js";
import { loadManifest } from "../dist/manifest.js";
import { getTable } from "../dist/tableStore.js";
import {
  findHubFieldMatches,
  findVersionComparisonMatches,
  portStatusResultItem,
  reservedUsageResultItem,
} from "../dist/tools.js";

test("wHubCharacteristics lookup does not absorb child bit groups", () => {
  const matches = findHubFieldMatches("wHubCharacteristics", "any");

  assert.equal(matches.length, 2);
  assert.deepEqual(
    new Set(matches.map((entry) => entry.specFamily)),
    new Set(["usb20", "usb3"])
  );
  assert.ok(matches.every((entry) => entry.raw.field_name === "wHubCharacteristics"));

  const envelope = buildEnvelope("wHubCharacteristics", matches, (entry) => ({
    field_name: entry.raw.field_name,
  }));

  assert.equal(envelope.claim_level, "verified");
  assert.equal(envelope.spec_family, null);
  assert.equal(envelope.source, null);
  assert.equal(envelope.result.length, 2);
  assert.ok(
    envelope.result.every(
      (item) =>
        item.source &&
        item.verified_scope &&
        item.source.manifest_version === loadManifest().manifest_version
    )
  );
});

test("mixed verified and reviewed matches use the conservative envelope claim", () => {
  const table = getTable("usb3_ss_hub_characteristics_bit_matrix");
  assert.ok(table);

  const verified = table.entries.find((entry) => entry.claimLevel === "verified");
  const reviewed = table.entries.find((entry) => entry.claimLevel === "reviewed");
  assert.ok(verified);
  assert.ok(reviewed);

  const summary = summarizeMatches([verified, reviewed]);
  assert.equal(summary.claim_level, "reviewed");
  assert.equal(summary.reviewed_meaning, null);
});

test("claim ceiling is loaded from the governed manifest", () => {
  assert.deepEqual(
    getCannotEstablish(),
    loadManifest().claim_ceiling.cannot_establish
  );
});

test("PORT_LINK_STATE exposes range and encoding identity without behavior prose", () => {
  const table = getTable("usb3_ss_hub_port_status_bit_matrix");
  const entry = table.entries.find((candidate) => candidate.raw.name === "PORT_LINK_STATE");

  assert.ok(entry);
  const result = portStatusResultItem(entry);
  assert.equal(result.bit_range, "8:5");
  assert.equal(result.value_encoding["0011"], "U3");
  assert.equal(Object.hasOwn(result, "description"), false);
});

test("check_reserved_usage identifies USB3 reserved boundary entries", () => {
  const table = getTable("usb3_ss_hub_port_status_bit_matrix");
  assert.ok(table);

  const reservedIds = [
    "ss_wPortStatus.bit4.RESERVED",
    "ss_wPortStatus.bit15.RESERVED",
    "ss_wPortChange.bit1.RESERVED",
    "ss_wPortChange.bits157.RESERVED",
  ];
  const entries = reservedIds.map((entryId) => {
    const entry = table.entries.find((candidate) => candidate.entryId === entryId);
    assert.ok(entry, `missing reserved entry ${entryId}`);
    return entry;
  });

  assert.deepEqual(
    entries.map((entry) => reservedUsageResultItem(entry).is_reserved),
    [true, true, true, true]
  );
});

test("compare term_type restricts matching to the requested governed surface", () => {
  const anyMatches = findVersionComparisonMatches("PORT_RESET", "any");
  const selectorMatches = findVersionComparisonMatches("PORT_RESET", "selector");
  const bitMatches = findVersionComparisonMatches("PORT_RESET", "bit");

  assert.ok(anyMatches.length > selectorMatches.length);
  assert.ok(selectorMatches.length > 0);
  assert.ok(bitMatches.length > 0);
  assert.ok(selectorMatches.every((entry) => entry.tableId.includes("feature_selector")));
  assert.ok(bitMatches.every((entry) => entry.tableId.includes("port_status_bit")));
});
