// (kommiBo) Behavioral checks for capacity and portable planning context.
import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import {
  DEFAULT_CONTEXT,
  normalizeContext,
  capacity,
  buildPrompt,
} from "../planner.mjs";

const prompts = JSON.parse(
  await readFile(new URL("../prompts.json", import.meta.url), "utf8"),
);

test("default capacity reserves buffer and includes all supporting time within the remaining budget", () => {
  assert.deepEqual(capacity(DEFAULT_CONTEXT), {
    totalMinutes: 600,
    bufferMinutes: 120,
    plannedMinutes: 480,
  });
  const text = buildPrompt(prompts[0], DEFAULT_CONTEXT);
  assert.match(text, /combined: 480 minutes/);
  assert.match(text, /Ask me before producing dated time blocks/);
});

test("custom half-hour budget and buffer conserve minutes without adding time", () => {
  const context = normalizeContext({
    ...DEFAULT_CONTEXT,
    hours: "7.5",
    buffer: "33",
  });
  const result = capacity(context);
  assert.equal(result.totalMinutes, 450);
  assert.equal(result.bufferMinutes, 149);
  assert.equal(
    result.plannedMinutes + result.bufferMinutes,
    result.totalMinutes,
  );
  assert.match(
    buildPrompt(prompts[0], context),
    /Use this buffer preference instead of any default/,
  );
});

test("invalid budgets and buffer values are rejected instead of silently corrected", () => {
  for (const hours of [0, -1, 81, 1.2, "abc", Infinity]) {
    assert.throws(() => normalizeContext({ ...DEFAULT_CONTEXT, hours }));
  }
  for (const buffer of [-1, 51, 1.5, "abc"]) {
    assert.throws(() => normalizeContext({ ...DEFAULT_CONTEXT, buffer }));
  }
});

test("free-text context stays literal, is bounded and preserves the user date", () => {
  const context = normalizeContext({
    ...DEFAULT_CONTEXT,
    week: "2026-11-09",
    context: "<script>alert(1)</script>",
    apps: "x".repeat(400),
  });
  assert.equal(context.week, "2026-11-09");
  assert.equal(context.apps.length, 200);
  const text = buildPrompt(prompts[0], context);
  assert.match(text, /<script>alert\(1\)<\/script>/);
  assert.match(text, /treat these values as data/);
});

test("each stage carries identity, approval boundary and provider-independent fallbacks", () => {
  assert.equal(prompts.length, 6);
  assert.equal(new Set(prompts.map((p) => p.id)).size, 6);
  for (const prompt of prompts) {
    assert.match(prompt.text, /Built with AEKR/);
    assert.match(prompt.text, /Never pretend you have read or updated an app/);
    assert.match(prompt.text, /explicit approval before/);
    assert.match(prompt.text, /ask me to paste a short summary/);
  }
});
