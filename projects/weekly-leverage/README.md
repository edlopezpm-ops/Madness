# Weekly Leverage

<!-- (kommiBo) Public AEKR planning prompts, separate from the CAD experiments. -->

Plan once. Make room to live. Six planning prompts for the AI assistant and apps a visitor already uses.

Public entry point: **[aekr.io/weekly-leverage/](https://aekr.io/weekly-leverage/)**.

## The experience

- The compact language button opens floating EN/ES/PT squares without a surrounding panel; the active language is omitted from the alternatives. English, Spanish and Brazilian Portuguese cover the page, six prompts, optional planning context, statuses and UTF-8 text downloads. Browser language supplies the initial default; a successful manual choice can be remembered.
- Light and dark palettes retain the editorial typography, ivory surfaces and rust accent. The first visit follows `prefers-color-scheme`; a manual override is remembered. The floating “Auto” action (labelled “Use system theme”) beside the language choices removes that override and resumes live system changes.
- Body copy, descriptions, form labels/values, controls, prompt output and supporting text are an additional 10% larger than the prior release. Headings, the six prompt titles, display titles and header wordmark retain their prior sizes at every breakpoint. Geometry is not scaled with a page zoom.
- Copy a prompt or download its customized `.txt`; individual starter prompts are available in every language without JavaScript. No full-kit download or source-repository link is exposed in the page. Historical source notes/archive remain repository material and are excluded from publication.
- Optional context: work budget, buffer, week date, time zone, apps and a goal/constraint. Changing language retains those fields and the selected stage. Failed or superseded language loads do not replace the current prompt.

Defaults: 10-hour example budget, 20% unscheduled buffer, focus blocks up to 50 minutes followed by 10-minute breaks, one main outcome per day, daily close and weekly review. All supporting time counts inside available capacity. Prompts request missing information, expose overflow, protect rest and require approval before external writes. They cannot guarantee model compliance or an outcome.

## Data, preferences and policies

There is no application account, model API, app connector or cookie. Optional Weekly-only aggregate statistics require an explicit choice in the footer. Planning entries remain in the current tab until the visitor copies or downloads them. No plan content enters browser storage.

Two optional display preferences persist: `weekly-leverage-language` and `weekly-leverage-theme`. The separately controlled `weekly-leverage-analytics-v1` key contains only an optional statistics choice, policy and expiry. They are separate from other AEKR products' preference keys. Denied storage does not block the tool; choices then last only in the tab. Clearing browser storage removes remembered choices. No service worker, visitor ID or event queue is implemented. Optional measurement is best effort, without retries.

Public UI/prompt JSON uses normal HTTP cache semantics; successfully loaded language bundles are also reused in memory. A failed request can be retried and a slow response cannot overwrite a newer language choice. These caches hold the supplied public assets, not visitor planning entries.

The footer links to the master [AEKR terms](https://aekr.io/terms.html), [privacy policy](https://aekr.io/privacy.html) and [cookie policy](https://aekr.io/cookies.html). It does not embed the master site's scripts or activate its optional measurement. The in-page FAQ explains this tool's narrower current behavior and the prompt-use permission. The dated statistics increment below records its separately authorized scope, reviewed data flow and explicit source-specific choice; policy links alone never enable it.

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

The customizer fetches only fixed same-origin language assets; the separate optional module can call the two closed metrics routes after permission. Context is bounded, validated and written through text/value APIs; it is never inserted as HTML, interpreted as code, sent to a server or used as a filename/URL. External new-tab links carry `noopener noreferrer`. The form remains disabled without the customizer and CSP forbids form submission. There is no upload, arbitrary proxy, public authentication or database access. Only the two optional metrics routes delegate to the bounded Console service.

`hosting/build.mjs` publishes exactly 33 public files: HTML/CSS, five JS modules/scripts, two PNGs, and three sets of UI JSON, prompt JSON and six TXT files. It adds native response headers as the 34th artifact file. Tests, notes, historical archives, editable social-card SVG, Git and provider state stay out. The builder refuses unexpected preexisting output, symlinked source/output paths and altered prompt-manifest filenames. When changing the allowlist, inspect and archive the prior generated output outside the release instead of silently deleting it.

The headers apply only to `/weekly-leverage/*`: self-only scripts/images/fonts/connections, no framing/media/workers/form submission, HSTS, MIME-sniffing protection, no-referrer, opener isolation and limited browser permissions. `Cache-Control: public, max-age=300, no-transform` enables bounded public caching and prevents the host's automatic analytics injection for this tool. The homepage, global zone settings and other product routes are unchanged.

From an already authorized Cloudflare CLI session:

```sh
node hosting/build.mjs
npx wrangler@4.157.0 deploy --config hosting/wrangler.jsonc --dry-run
npx wrangler@4.157.0 deploy --config hosting/wrangler.jsonc
```

Use the intended account; never add credentials to the repository. The Worker executes only the two optional metrics endpoints; other requests retain native asset behavior. Its only application binding is the named WeeklyLeverageMetrics service, never a database or secret. Its two routes cover the bare entry and slash-delimited subtree. Share the slash URL, especially with query parameters: the exact bare-path route does not match query strings. GitHub Pages is not used and no GitHub Actions workflow is introduced.

Record the exact source/merge, deployed version, current route IDs and anonymous HTTP/browser evidence. Wrangler may renew this Worker's own route IDs on an update; retain their new values and verify unrelated routes remain byte-identical. Recovery uses a revert PR for source and a saved prior version for this Worker only. Do not redeploy the homepage Worker or remove sibling routes.

The existing vendor-managed static-assets path is retained, without a new paid-service plan or model billing. Cloudflare documents [static asset requests/storage](https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/) separately from Worker-script execution. Provider/account policies still apply.

The Open Graph/X image at `social-card.png` is the owner-supplied 1731×909 PNG, preserved byte-for-byte. Its metadata URL includes a content-fingerprint query so social crawlers receive a new image URL when the artwork changes. Dimensions and alternative text describe that image. `social/social-card.svg` is historical artwork, excluded from publication. The header and browser favicon use the same owner-supplied, rust-accented `aekr-mark.png`. The transparent footer signature follows the accreatio layout while using this page's colors. Instagram and X link to AEKR's `__aekr` profiles.

## Use and permissions

Visitors may use and adapt the six prompt texts for personal or internal business planning, as described in source [USE-NOTES.txt](USE-NOTES.txt). This permission covers those texts, not unrelated Madness material, website source or AEKR marks. The repository has no general project license. No third-party endorsement, compliance certification or guaranteed result is implied.

The supplied article draft is not published. The toolkit contains original planning instructions and does not reproduce an unverified quotation.

Built with **[AEKR](https://aekr.io)**.


## Optional Weekly-only statistics — 2026-11-03

Ed requested a visit counter and free available metrics in the existing private
AEKR Console. The smallest coherent change reuses its Activity, authentication,
source control, aggregate D1 store and native service binding. This prospective
product-improvement increment supersedes the earlier no-collector statement
only after explicit Weekly-only permission. It adds no cookie, visitor identifier,
third-party SDK, model API, operational upload, new dependency or paid plan.
The supplied social image and floating language/theme behavior are unchanged.

The footer discloses and controls one best-effort view per visible document,
with independent UTC-day/language/coarse country/device/referrer-category totals.
No full referrer, raw IP/browser string, planning entry or prompt text is sent or
stored. Repeat documents can count again; these are consented page views, not
unique people, sessions or complete traffic. There is no historical backfill.
GPC/DNT, refusal, expiry, blocked storage and withdrawal stop prospective events.
Requests omit credentials. A Weekly-specific choice, policy and expiry are saved
locally for 30 days; no other product's prior opt-in grants this new purpose.

Only `/weekly-leverage/api/metrics/config` and `/weekly-leverage/api/metrics`
execute the bounded Worker. Static assets retain native serving and headers.
The named Console service grants only config/record operations, never a database
handle, owner session or secret. Its source starts paused pending separate review
and activation; existing global/source/event/purpose/category gates remain
authoritative. A fixed limiter and atomic 1,000/day accepted-view cap bound work.
The Console-only daily purge retains 30 UTC days. Existing account metering still
applies: no unlimited zero-charge guarantee is made.

Delivery order is additive schema, reviewed Console service, reviewed source
activation, then this Worker. Never lift global pause to enable only Weekly.
Rollback pauses only this source and restores the recorded Weekly/Console Worker
versions while preserving additive tables and receipts. No public aekr-web Worker,
other product, authentication, DNS, zone or Build-trigger edit is part of delivery.
A source push/merge must first prove it cannot auto-deploy an excluded Worker.

Verification includes real SQLite atomic cap/pause/version/failure/retention
cases in the Console repository, native request and choice regressions here,
local named-service integration, EN/ES/PT and 320px dark browser checks, existing
planner/package/hosting tests and separate exact-diff review. Tests and local
preview do not establish hosted activation, provider deployment or HOC acceptance.

Local checkpoint: 27 Node cases and eight Python cases pass. Official Wrangler
dry runs for the kit and Console pass; a fresh bundle-bound local workerd/D1
run verifies the actual named service, five equal synthetic marginals and closed
privacy/private/static boundaries. SQLite Promise-all arrivals test serialized
batch transactions at the cap; no production D1 load claim is made. Source hashes
and complete output live in the external increment receipt. Browser review,
separate source review and hosted/Git delivery remain separately evidenced.
