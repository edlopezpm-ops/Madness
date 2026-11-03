// (kommiBo) Browser-local prompt preview, clipboard and text download.
import {
  DEFAULT_CONTEXT,
  normalizeContext,
  capacity,
  formatHours,
  buildPrompt,
} from "./planner.mjs";

const form = document.querySelector("#context-form");
const output = document.querySelector("#prompt-output");
const status = document.querySelector("#prompt-status");
const copyButton = document.querySelector("#copy-prompt");
const downloadButton = document.querySelector("#download-prompt");
const choices = [...document.querySelectorAll("[data-prompt]")];
let prompts = [];
let selected = "plan";
let context = { ...DEFAULT_CONTEXT };

function render() {
  const prompt = prompts.find((item) => item.id === selected);
  if (!prompt) return;
  document.querySelector("#prompt-tag").textContent = prompt.tag;
  document.querySelector("#prompt-title").textContent = prompt.title;
  document.querySelector("#prompt-time").textContent = prompt.minutes;
  document.querySelector("#prompt-description").textContent =
    prompt.description;
  output.value = buildPrompt(prompt, context);
  output.scrollTop = 0;
  const budget = capacity(context);
  document.querySelector("#capacity-note").textContent =
    `Up to ${formatHours(budget.plannedMinutes)} hours planned + ${formatHours(budget.bufferMinutes)} hours of buffer.`;
  for (const button of choices) {
    const active = button.dataset.prompt === selected;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  }
  copyButton.disabled = false;
  downloadButton.disabled = false;
}

function updateContext() {
  if (!form.reportValidity()) return false;
  try {
    context = normalizeContext(Object.fromEntries(new FormData(form)));
    render();
    return true;
  } catch (error) {
    status.textContent = error.message;
    return false;
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  if (updateContext())
    status.textContent = "Prompt updated. Read it, then copy or download.";
});

for (const button of choices) {
  button.addEventListener("click", () => {
    // Apply the currently visible form before switching, so context never silently goes stale.
    if (!updateContext()) return;
    selected = button.dataset.prompt;
    render();
    status.textContent = `${prompts.find((item) => item.id === selected).title} is ready with your context.`;
  });
}

copyButton.addEventListener("click", async () => {
  if (!updateContext()) return;
  try {
    if (!navigator.clipboard?.writeText)
      throw new Error("Clipboard unavailable");
    await navigator.clipboard.writeText(output.value);
    status.textContent = "Copied. Paste it into the AI assistant you choose.";
  } catch {
    output.focus();
    output.select();
    status.textContent =
      "Automatic copy is unavailable. The prompt is selected: press Ctrl+C or ⌘C, or download the .txt.";
  }
});

downloadButton.addEventListener("click", () => {
  if (!updateContext()) return;
  const prompt = prompts.find((item) => item.id === selected);
  const blob = new Blob([output.value], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = prompt.file;
  document.body.append(anchor);
  anchor.click();
  anchor.remove();
  setTimeout(() => URL.revokeObjectURL(url), 30000);
  status.textContent =
    "Download requested. This file includes the context you entered; review it before sharing.";
});

document.querySelector("#reset-context").addEventListener("click", () => {
  form.reset();
  context = { ...DEFAULT_CONTEXT };
  render();
  status.textContent = "Context reset to the starter values in this tab.";
});

try {
  const response = await fetch(new URL("./prompts.json", import.meta.url));
  if (!response.ok) throw new Error("Prompt file could not be loaded");
  prompts = await response.json();
  document.querySelector("#context-fields").disabled = false;
  render();
  status.textContent = "Ready. You can use the defaults or add context above.";
} catch {
  status.textContent =
    "The preview could not load. Download the plain-text starter files or ZIP below; they work without the customizer.";
}
