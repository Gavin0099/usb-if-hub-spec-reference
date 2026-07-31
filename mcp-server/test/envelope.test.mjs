import test from "node:test";
import assert from "node:assert/strict";

import {
  buildEnvelope,
  getCannotEstablish,
  summarizeMatches,
} from "../dist/envelope.js";
import { loadManifest } from "../dist/manifest.js";
import { getTable } from "../dist/tableStore.js";
import { findHubFieldMatches } from "../dist/tools.js";

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
