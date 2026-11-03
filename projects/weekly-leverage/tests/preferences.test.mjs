// (kommiBo) Public preference behavior, localized capacity and hostile literal input.
import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import vm from "node:vm";
import {
  chooseLanguage,
  localePrefix,
  message,
  validateBundle,
} from "../i18n.mjs";
import { DEFAULT_CONTEXT, normalizeContext, buildPrompt } from "../planner.mjs";

const bundles = {};
for (const language of ["en", "es", "pt"]) {
  const prefix = localePrefix(language);
  bundles[language] = {
    ui: JSON.parse(
      await readFile(
        new URL("../" + prefix + "ui.json", import.meta.url),
        "utf8",
      ),
    ),
    prompts: JSON.parse(
      await readFile(
        new URL("../" + prefix + "prompts.json", import.meta.url),
        "utf8",
      ),
    ),
  };
}
test("valid saved language wins; otherwise browser language list picks a supported primary language", () => {
  assert.equal(chooseLanguage("es", ["pt-BR"]), "es");
  assert.equal(chooseLanguage("invalid", ["fr-FR", "pt-PT"]), "pt");
  assert.equal(chooseLanguage(null, ["es-MX", "en"]), "es");
  assert.equal(chooseLanguage(null, ["de-DE"]), "en");
  assert.throws(() => localePrefix("../private"));
});
test("all three fixed language bundles are valid; changed filenames and missing stages are rejected", () => {
  for (const bundle of Object.values(bundles))
    assert.equal(validateBundle(bundle), bundle);
  const invalid = structuredClone(bundles.es);
  invalid.prompts[0].file = "../PRIVATE.txt";
  assert.throws(() => validateBundle(invalid));
  assert.throws(() => validateBundle({ ui: {}, prompts: [] }));
});
test("localized custom prompts preserve numerical capacity, dates and user text literally", () => {
  const context = normalizeContext({
    ...DEFAULT_CONTEXT,
    hours: 8,
    buffer: 25,
    week: "2026-11-09",
    context: "<script>throw new Error(1)</script> {planned} $&",
  });
  for (const [language, bundle] of Object.entries(bundles)) {
    const result = buildPrompt(bundle.prompts[0], context, (source, values) =>
      message(bundle.ui, source, values),
    );
    assert.ok(result.includes("360"));
    assert.ok(result.includes("120"));
    assert.ok(result.includes(context.context));
    assert.ok(result.includes("2026-11-09"));
    if (language === "es") assert.match(result, /MI CONTEXTO DE PLANIFICACIÓN/);
    if (language === "pt") assert.match(result, /MEU CONTEXTO DE PLANEJAMENTO/);
  }
  assert.equal(
    message({ "Hello {value}": "Hola {value}" }, "Hello {value}", {
      value: "$& <img> {value}",
    }),
    "Hola $& <img> {value}",
  );
});
test("impossible calendar dates are rejected and leap days remain literal", () => {
  for (const week of ["2026-02-29", "2026-02-31", "2026-13-01", "2026-00-00"])
    assert.throws(() => normalizeContext({ ...DEFAULT_CONTEXT, week }));
  assert.equal(
    normalizeContext({ ...DEFAULT_CONTEXT, week: "2028-02-29" }).week,
    "2028-02-29",
  );
});

const themeSource = await readFile(
  new URL("../theme.js", import.meta.url),
  "utf8",
);
function themePage({ dark = false, saved, blocked = false } = {}) {
  const events = new Map();
  const buttons = {};
  const stored = new Map(
    saved === undefined ? [] : [["weekly-leverage-theme", saved]],
  );
  const writes = [];
  for (const id of ["#theme-toggle", "#system-theme"])
    buttons[id] = {
      dataset: {},
      attrs: {},
      hidden: true,
      setAttribute(k, v) {
        this.attrs[k] = v;
      },
      addEventListener(k, fn) {
        this[k] = fn;
      },
    };
  const root = { dataset: {} };
  const meta = {};
  const system = {
    matches: dark,
    addEventListener(k, fn) {
      this[k] = fn;
    },
  };
  const document = {
    documentElement: root,
    querySelector(s) {
      return s === 'meta[name="theme-color"]' ? meta : buttons[s];
    },
    addEventListener(k, fn) {
      events.set(k, fn);
    },
  };
  const localStorage = {
    getItem(k) {
      if (blocked) throw Error("denied");
      return stored.get(k);
    },
    setItem(k, v) {
      if (blocked) throw Error("denied");
      writes.push([k, v]);
      stored.set(k, v);
    },
    removeItem(k) {
      if (blocked) throw Error("denied");
      writes.push([k, null]);
      stored.delete(k);
    },
  };
  vm.runInNewContext(themeSource, {
    document,
    window: {
      matchMedia() {
        return system;
      },
    },
    localStorage,
  });
  events.get("DOMContentLoaded")();
  return {
    root,
    meta,
    buttons,
    stored,
    writes,
    change(dark) {
      system.matches = dark;
      system.change({ matches: dark });
    },
  };
}
test("first visit follows system changes; an explicit toggle persists only the theme preference", () => {
  const page = themePage({ dark: true });
  assert.equal(page.root.dataset.theme, "dark");
  assert.equal(page.root.dataset.themePreference, "system");
  assert.equal(page.writes.length, 0);
  page.change(false);
  assert.equal(page.root.dataset.theme, "light");
  page.buttons["#theme-toggle"].click();
  assert.equal(page.root.dataset.theme, "dark");
  assert.deepEqual(page.writes, [["weekly-leverage-theme", "dark"]]);
  page.change(false);
  assert.equal(page.root.dataset.theme, "dark");
  page.buttons["#system-theme"].click();
  assert.equal(page.root.dataset.theme, "light");
  assert.equal(page.root.dataset.themePreference, "system");
  assert.equal(page.stored.size, 0);
});
test("saved preference wins on reload; invalid values follow the system", () => {
  assert.equal(
    themePage({ dark: true, saved: "light" }).root.dataset.theme,
    "light",
  );
  assert.equal(
    themePage({ dark: true, saved: "arbitrary" }).root.dataset.theme,
    "dark",
  );
});
test("blocked storage still permits switching and returning to the system", () => {
  const page = themePage({ dark: true, blocked: true });
  page.buttons["#theme-toggle"].click();
  assert.equal(page.root.dataset.theme, "light");
  page.buttons["#system-theme"].click();
  assert.equal(page.root.dataset.theme, "dark");
  assert.equal(page.root.dataset.themePreference, "system");
});
