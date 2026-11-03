// (kommiBo) Local prompts, fixed language assets and optional display preferences only.
import {
  DEFAULT_CONTEXT,
  normalizeContext,
  capacity,
  buildPrompt,
} from "./planner.mjs";
import {
  chooseLanguage,
  localePrefix,
  message,
  validateBundle,
} from "./i18n.mjs";

const form = document.querySelector("#context-form");
const output = document.querySelector("#prompt-output");
const status = document.querySelector("#prompt-status");
const copyButton = document.querySelector("#copy-prompt");
const downloadButton = document.querySelector("#download-prompt");
const languageToggle = document.querySelector("#language-toggle");
const languageOptions = document.querySelector("#language-options");
const choices = [...document.querySelectorAll("[data-prompt]")];
const bundles = new Map();
let language = "en";
let bundle = { ui: {}, prompts: [] };
let selected = "plan";
let context = { ...DEFAULT_CONTEXT };
let languageRequest = 0;

// Capture the original text nodes once. Forms, focus and visitor values are never replaced.
const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
const staticText = [];
const excluded =
  "script,style,noscript,textarea,#preferences,#prompt-tag,#prompt-title,#prompt-time,#prompt-description,#capacity-note,#prompt-status";
while (walker.nextNode()) {
  const node = walker.currentNode;
  if (node.nodeValue.trim() && !node.parentElement.closest(excluded))
    staticText.push({ node, original: node.nodeValue });
}
const attributes = [];
for (const element of document.querySelectorAll("[aria-label],[placeholder]")) {
  if (element.closest("#preferences")) continue;
  for (const name of ["aria-label", "placeholder"])
    if (element.hasAttribute(name))
      attributes.push({ element, name, original: element.getAttribute(name) });
}
const downloads = [...document.querySelectorAll('a[href^="prompts/"]')].map(
  (element) => ({ element, original: element.getAttribute("href") }),
);
const t = (source, values) => message(bundle.ui, source, values);

function translatePage() {
  document.documentElement.lang = language === "pt" ? "pt-BR" : language;
  document.title = t("Weekly Leverage — Built with AEKR");
  for (const { node, original } of staticText)
    node.nodeValue = original.replace(original.trim(), t(original));
  for (const { element, name, original } of attributes)
    element.setAttribute(name, t(original));
  for (const { element, original } of downloads)
    element.setAttribute("href", localePrefix(language) + original);
  languageToggle.textContent = language.toUpperCase();
  languageToggle.setAttribute(
    "aria-label",
    t("Choose language") + " (" + language.toUpperCase() + ")",
  );
  for (const button of document.querySelectorAll("[data-language]")) {
    const active = button.dataset.language === language;
    button.hidden = active;
    button.setAttribute("aria-pressed", String(active));
  }
  document
    .querySelector('#language-options [role="group"]')
    .setAttribute("aria-label", t("Language options"));
  document
    .querySelector("#system-theme")
    .setAttribute("aria-label", t("Use system theme"));
  document.querySelector("#system-theme").title = t("Use system theme");
  const theme = document.querySelector("#theme-toggle");
  theme.dataset.darkLabel = t("Switch to dark mode");
  theme.dataset.lightLabel = t("Switch to light mode");
  document.dispatchEvent(new Event("weekly-language-change"));
}

function render() {
  const prompt = bundle.prompts.find((item) => item.id === selected);
  if (!prompt) return;
  document.querySelector("#prompt-tag").textContent = prompt.tag;
  document.querySelector("#prompt-title").textContent = prompt.title;
  document.querySelector("#prompt-time").textContent = prompt.minutes;
  document.querySelector("#prompt-description").textContent =
    prompt.description;
  output.value = buildPrompt(prompt, context, t);
  output.scrollTop = 0;
  const budget = capacity(context);
  const hours = (minutes) =>
    new Intl.NumberFormat(language, { maximumFractionDigits: 2 }).format(
      minutes / 60,
    );
  document.querySelector("#capacity-note").textContent = t(
    "Up to {planned} hours planned + {buffer} hours of buffer.",
    {
      planned: hours(budget.plannedMinutes),
      buffer: hours(budget.bufferMinutes),
    },
  );
  for (const button of choices) {
    const active = button.dataset.prompt === selected;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  }
  copyButton.disabled = false;
  downloadButton.disabled = false;
}

function readFields() {
  return Object.fromEntries(
    [...form.querySelectorAll("[name]")].map((field) => [
      field.name,
      field.value,
    ]),
  );
}

function updateContext() {
  if (!form.reportValidity()) return false;
  try {
    context = normalizeContext(readFields());
    render();
    return true;
  } catch (error) {
    status.textContent = t(error.message);
    return false;
  }
}

async function loadBundle(next) {
  if (!bundles.has(next)) {
    const prefix = localePrefix(next);
    const request = (async () => {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 15000);
      try {
        const responses = await Promise.all(
          ["ui.json", "prompts.json"].map((file) =>
            fetch(new URL(prefix + file, import.meta.url), {
              signal: controller.signal,
              credentials: "omit",
            }),
          ),
        );
        if (responses.some((response) => !response.ok))
          throw new Error("Local language unavailable");
        const [ui, prompts] = await Promise.all(
          responses.map((response) => response.json()),
        );
        return validateBundle({ ui, prompts });
      } finally {
        clearTimeout(timeout);
      }
    })();
    bundles.set(next, request);
    request.catch(() => bundles.delete(next)); // Failed requests can be retried; no data is queued.
  }
  return bundles.get(next);
}

function closeLanguages() {
  languageOptions.hidden = true;
  languageToggle.setAttribute("aria-expanded", "false");
}
async function changeLanguage(next, remember = true) {
  if (bundle.prompts.length && !form.reportValidity()) return;
  const request = ++languageRequest;
  try {
    const loaded = await loadBundle(next);
    if (request !== languageRequest) return;
    // Apply current fields only at successful handoff; a failed load leaves everything intact.
    context = normalizeContext(readFields());
    bundle = loaded;
    language = next;
    translatePage();
    document.querySelector("#context-fields").disabled = false;
    render();
    status.textContent = t(
      "Ready. You can use the defaults or add context above.",
    );
    if (remember)
      try {
        localStorage.setItem("weekly-leverage-language", language);
      } catch {
        /* This tab still works. */
      }
    closeLanguages();
    if (remember) languageToggle.focus();
  } catch {
    if (request !== languageRequest) return;
    status.textContent = t(
      bundle.prompts.length
        ? "This language could not load. Your current prompt and context are unchanged. Try again or use a starter download."
        : "The preview could not load. Download the plain-text starter prompts below; they work without the customizer.",
    );
  }
}

languageToggle.addEventListener("click", () => {
  languageOptions.hidden = !languageOptions.hidden;
  languageToggle.setAttribute("aria-expanded", String(!languageOptions.hidden));
});
for (const button of document.querySelectorAll("[data-language]"))
  button.addEventListener("click", () =>
    changeLanguage(button.dataset.language),
  );
document.addEventListener("click", (event) => {
  if (!event.target.closest("#preferences")) closeLanguages();
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !languageOptions.hidden) {
    closeLanguages();
    languageToggle.focus();
  }
});
document.querySelector("#system-theme").addEventListener("click", () => {
  closeLanguages();
  languageToggle.focus();
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  if (updateContext())
    status.textContent = t("Prompt updated. Read it, then copy or download.");
});
for (const button of choices)
  button.addEventListener("click", () => {
    if (!updateContext()) return;
    selected = button.dataset.prompt;
    render();
    status.textContent = t("{title} is ready with your context.", {
      title: bundle.prompts.find((item) => item.id === selected).title,
    });
  });
copyButton.addEventListener("click", async () => {
  if (!updateContext()) return;
  try {
    if (!navigator.clipboard?.writeText)
      throw new Error("Clipboard unavailable");
    await navigator.clipboard.writeText(output.value);
    status.textContent = t(
      "Copied. Paste it into the AI assistant you choose.",
    );
  } catch {
    output.focus();
    output.select();
    status.textContent = t(
      "Automatic copy is unavailable. The prompt is selected: press Ctrl+C or ⌘C, or download the .txt.",
    );
  }
});
downloadButton.addEventListener("click", () => {
  if (!updateContext()) return;
  const prompt = bundle.prompts.find((item) => item.id === selected);
  const url = URL.createObjectURL(
    new Blob([output.value], { type: "text/plain;charset=utf-8" }),
  );
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = prompt.file;
  document.body.append(anchor);
  anchor.click();
  anchor.remove();
  setTimeout(() => URL.revokeObjectURL(url), 30000);
  status.textContent = t(
    "Download requested. This file includes the context you entered; review it before sharing.",
  );
});
document.querySelector("#reset-context").addEventListener("click", () => {
  form.reset();
  context = { ...DEFAULT_CONTEXT };
  render();
  status.textContent = t("Context reset to the starter values in this tab.");
});
let saved;
try {
  saved = localStorage.getItem("weekly-leverage-language");
} catch {
  /* Browser language is the default. */
}
await changeLanguage(chooseLanguage(saved, navigator.languages), false);
languageToggle.disabled = false;
