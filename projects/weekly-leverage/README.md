# Weekly Leverage

<!-- (kommiBo) Public AEKR planning prompts, separate from the CAD experiments. -->

Plan once. Make room to live. Six planning prompts for the AI assistant and apps a visitor already uses.

Public entry point: **[aekr.io/weekly-leverage/](https://aekr.io/weekly-leverage/)**.

## The experience

- English, Spanish and Brazilian Portuguese cover the page, six prompts, optional planning context, statuses and UTF-8 text downloads. Browser language supplies the initial default; a successful manual choice can be remembered.
- Light and dark palettes retain the editorial typography, ivory surfaces and rust accent. The first visit follows `prefers-color-scheme`; a manual override is remembered. “Use system theme” in the language/preferences panel removes that override and resumes live system changes.
- Type sizes are 10% larger than the original page, including responsive headings and form controls. Geometry is not scaled with a page zoom.
- Copy a prompt or download its customized `.txt`; individual starter prompts are available in every language without JavaScript. No full-kit download or source-repository link is exposed in the page. Historical source notes/archive remain repository material and are excluded from publication.
- Optional context: work budget, buffer, week date, time zone, apps and a goal/constraint. Changing language retains those fields and the selected stage. Failed or superseded language loads do not replace the current prompt.

Defaults: 10-hour example budget, 20% unscheduled buffer, focus blocks up to 50 minutes followed by 10-minute breaks, one main outcome per day, daily close and weekly review. All supporting time counts inside available capacity. Prompts request missing information, expose overflow, protect rest and require approval before external writes. They cannot guarantee model compliance or an outcome.

## Data, preferences and policies

There is no application account, model API, app connector, analytics collector, cookie, consent banner or collection endpoint. Planning entries remain in the current tab until the visitor copies or downloads them. No plan content enters browser storage.

Only two optional display preferences persist: `weekly-leverage-language` and `weekly-leverage-theme`. They are separate from other AEKR products' preference keys. Denied storage does not block the tool; choices then last only in the tab. Clearing browser storage removes remembered choices. No service worker, visitor ID, event queue or background submission is implemented.

Public UI/prompt JSON uses normal HTTP cache semantics; successfully loaded language bundles are also reused in memory. A failed request can be retried and a slow response cannot overwrite a newer language choice. These caches hold the supplied public assets, not visitor planning entries.

The footer links to the master [AEKR terms](https://aekr.io/terms.html), [privacy policy](https://aekr.io/privacy.html) and [cookie policy](https://aekr.io/cookies.html). It does not embed the master site's scripts or activate its optional measurement. The in-page FAQ explains this tool's narrower current behavior and the prompt-use permission. Adding collection later requires a separate authorized release, reviewed data flow, accurate disclosures and applicable choices before activation; policy links alone never enable it.

Hosts process HTTP requests under their own policies. Pasting a prompt into an assistant is a separate disclosure governed by that provider. Avoid secrets and confidential records. Customized downloaded files contain the visitor's context.

## Source and checks

From this directory:

```sh
python3 -m http.server 4783 --bind 127.0.0.1
node --test tests/*.test.mjs
python3 -B -m unittest discover -s tests -p 'test_*.py'
```

Open `http://127.0.0.1:4783/`. ES modules need HTTP. `app.js` owns the customizer and atomic language handoff; `i18n.mjs` owns fixed language selection/paths and literal formatting; `planner.mjs` owns context validation and capacity. `theme.js` applies the initial preference before the stylesheet, then handles theme controls and system changes. No third-party runtime library is required.

English uses root `ui.json`, `prompts.json` and `prompts/*.txt`; translations use the corresponding `locales/es/` and `locales/pt/` paths. UI keys/placeholders and prompt identities, filenames and numerical defaults must agree. Each starter TXT must be byte-identical to its JSON text. Keep translated permission/privacy statements aligned with actual behavior.

Checks cover localized capacity and literal user text, impossible/leap dates, bundle validation, saved/system/blocked-storage theme behavior, all three text sets, translated visible/accessibility copy, social metadata, footer policy destinations and the publication boundary. Browser evidence additionally covers responsive light/dark layouts, system-default fixtures, blocked storage, failed/retried/delayed language loads, in-memory cache reuse, focus, clipboard and downloaded text under native CSP. Tests do not certify AI planning quality or third-party integration.

## Security and publication

Only fixed same-origin language asset paths are fetched. Context is bounded, validated and written through text/value APIs; it is never inserted as HTML, interpreted as code, sent to a server or used as a filename/URL. External new-tab links carry `noopener noreferrer`. The form remains disabled without the customizer and CSP forbids form submission. No upload, arbitrary proxy, authentication, database or application API exists.

`hosting/build.mjs` publishes exactly 32 public files: HTML/CSS, four JS modules/scripts, two PNGs, and three sets of UI JSON, prompt JSON and six TXT files. It adds native response headers as the 33rd artifact file. Tests, notes, historical archives, editable social-card SVG, Git and provider state stay out. The builder refuses unexpected preexisting output, symlinked source/output paths and altered prompt-manifest filenames. When changing the allowlist, inspect and archive the prior generated output outside the release instead of silently deleting it.

The headers apply only to `/weekly-leverage/*`: self-only scripts/images/fonts/connections, no framing/media/workers/form submission, HSTS, MIME-sniffing protection, no-referrer, opener isolation and limited browser permissions. `Cache-Control: public, max-age=300, no-transform` enables bounded public caching and prevents the host's automatic analytics injection for this tool. The homepage, global zone settings and other product routes are unchanged.

From an already authorized Cloudflare CLI session:

```sh
node hosting/build.mjs
npx wrangler@4.157.0 deploy --config hosting/wrangler.jsonc --dry-run
npx wrangler@4.157.0 deploy --config hosting/wrangler.jsonc
```

Use the intended account; never add credentials to the repository. The asset-only Worker has no application server script or bindings. Its two routes cover the bare entry and slash-delimited subtree. Share the slash URL, especially with query parameters: the exact bare-path route does not match query strings. GitHub Pages is not used and no GitHub Actions workflow is introduced.

Record the exact source/merge, deployed version, current route IDs and anonymous HTTP/browser evidence. Wrangler may renew this Worker's own route IDs on an update; retain their new values and verify unrelated routes remain byte-identical. Recovery uses a revert PR for source and a saved prior version for this Worker only. Do not redeploy the homepage Worker or remove sibling routes.

The existing vendor-managed static-assets path is retained, without a new paid-service plan or model billing. Cloudflare documents [static asset requests/storage](https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/) separately from Worker-script execution. Provider/account policies still apply.

The existing 1200×630 Open Graph/X image remains at `social-card.png`; editable source is `social/social-card.svg`. The header and browser favicon use the same owner-supplied, rust-accented `aekr-mark.png`. The transparent footer signature follows the accreatio layout while using this page's colors. Instagram and X link to AEKR's `__aekr` profiles.

## Use and permissions

Visitors may use and adapt the six prompt texts for personal or internal business planning, as described in source [USE-NOTES.txt](USE-NOTES.txt). This permission covers those texts, not unrelated Madness material, website source or AEKR marks. The repository has no general project license. No third-party endorsement, compliance certification or guaranteed result is implied.

The supplied article draft is not published. The toolkit contains original planning instructions and does not reproduce an unverified quotation.

Built with **[AEKR](https://aekr.io)**.
