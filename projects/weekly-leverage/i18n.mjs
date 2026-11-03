// (kommiBo) Fixed local language routes and literal, non-HTML message formatting.
export const LANGUAGES = Object.freeze(["en", "es", "pt"]);

export function chooseLanguage(saved, languages = []) {
  if (LANGUAGES.includes(saved)) return saved;
  for (const language of languages) {
    const primary = String(language).toLowerCase().split("-")[0];
    if (LANGUAGES.includes(primary)) return primary;
  }
  return "en";
}

export function localePrefix(language) {
  if (!LANGUAGES.includes(language)) throw new Error("Unsupported language");
  return language === "en" ? "" : `locales/${language}/`;
}

export function message(dictionary, source, values = {}) {
  const normalized = source.replace(/\s+/g, " ").trim();
  const template = Object.hasOwn(dictionary, normalized)
    ? dictionary[normalized]
    : normalized;
  return template.replace(/\{(\w+)\}/g, (placeholder, key) =>
    Object.hasOwn(values, key) ? String(values[key]) : placeholder,
  );
}

export function validateBundle(bundle) {
  const ids = ["plan", "tasks", "apps", "daily", "reset", "review"];
  const files = [
    "01-plan-my-week.txt",
    "02-define-the-tasks.txt",
    "03-move-it-to-my-apps.txt",
    "04-start-the-day.txt",
    "05-rebalance-a-disrupted-week.txt",
    "06-close-and-repeat.txt",
  ];
  if (
    !bundle.ui ||
    typeof bundle.ui !== "object" ||
    Array.isArray(bundle.ui) ||
    !Object.values(bundle.ui).every(
      (value) => typeof value === "string" && value.trim(),
    ) ||
    !Array.isArray(bundle.prompts) ||
    bundle.prompts.length !== ids.length ||
    !bundle.prompts.every(
      (prompt, index) =>
        prompt.id === ids[index] &&
        prompt.file === files[index] &&
        ["title", "tag", "minutes", "description", "text"].every(
          (key) => typeof prompt[key] === "string" && prompt[key].trim(),
        ),
    )
  )
    throw new Error("Invalid local language bundle");
  return bundle;
}
