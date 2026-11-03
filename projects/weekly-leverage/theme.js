// (kommiBo) Only an explicit visual preference is stored; system theme is the default.
(() => {
  const root = document.documentElement;
  const key = "weekly-leverage-theme";
  const system = window.matchMedia("(prefers-color-scheme: dark)");
  let saved;
  try {
    saved = localStorage.getItem(key);
  } catch {
    /* Storage is optional. */
  }
  let manual = saved === "dark" || saved === "light";
  let theme = manual ? saved : system.matches ? "dark" : "light";

  function apply() {
    root.dataset.theme = theme;
    root.dataset.themePreference = manual ? theme : "system";
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = theme === "dark" ? "#181b17" : "#f4f0e7";
    const automatic = document.querySelector("#system-theme");
    if (automatic) automatic.hidden = !manual;
    const button = document.querySelector("#theme-toggle");
    if (button) {
      button.hidden = false;
      button.setAttribute("aria-pressed", String(theme === "dark"));
      button.setAttribute(
        "aria-label",
        theme === "dark"
          ? button.dataset.lightLabel || "Switch to light mode"
          : button.dataset.darkLabel || "Switch to dark mode",
      );
    }
  }
  apply();
  system.addEventListener("change", (event) => {
    if (!manual) {
      theme = event.matches ? "dark" : "light";
      apply();
    }
  });
  document.addEventListener("weekly-language-change", apply);
  document.addEventListener(
    "DOMContentLoaded",
    () => {
      document.querySelector("#theme-toggle").addEventListener("click", () => {
        theme = theme === "dark" ? "light" : "dark";
        manual = true;
        try {
          localStorage.setItem(key, theme);
        } catch {
          /* Current-tab toggle still works. */
        }
        apply();
      });
      document.querySelector("#system-theme").addEventListener("click", () => {
        manual = false;
        theme = system.matches ? "dark" : "light";
        try {
          localStorage.removeItem(key);
        } catch {
          /* Current-tab default still works. */
        }
        apply();
      });
      apply();
    },
    { once: true },
  );
})();
