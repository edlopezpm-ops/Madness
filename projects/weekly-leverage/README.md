# Weekly Leverage

<!-- (kommiBo) A standalone AEKR prompt toolkit; separate from the CAD experiments. -->

Plan once. Make room to live. Six planning prompts for the AI assistant and apps a visitor already uses.

Public entry point: **[aekr.io/weekly-leverage/](https://aekr.io/weekly-leverage/)**. No sign-in is implemented.

## The experience

- Six stages: weekly plan, task definition, app handoff, daily start, rebalance and weekly review.
- Copy a prompt or download a customized UTF-8 `.txt`; download all six starters as a ZIP.
- Optional context: weekly budget, buffer, week date, time zone, apps and a goal/constraint.
- Defaults: 10-hour example budget, 20% unscheduled buffer, up to 50-minute focus blocks followed by 10-minute breaks, one main outcome per day, daily close and weekly review. All supporting time counts inside the available capacity.
- Prompts request missing information together, preserve rest, expose overflow and require approval before external writes. They do not guarantee model compliance or results.

No account, AI API, paid dependency, analytics collector, persistent storage or direct app integration is implemented. Context is held temporarily in the current browser tab. Copying it into an assistant is a separate action governed by that provider. Avoid confidential information. Hosts still process HTTP requests under their own policies.

## Preview and checks

From this directory:

```sh
python3 -m http.server 4783 --bind 127.0.0.1
node --test tests/*.test.mjs
python3 -m unittest discover -s tests -p 'test_*.py'
```

Open `http://127.0.0.1:4783/`. Serve through HTTP: ES modules and the preview JSON are not intended to run via `file://`. The plain text files and ZIP remain usable without JavaScript.

Browser verification should cover all six prompt choices, custom capacity, clipboard success/fallback, customized downloads, reset, mobile layout and keyboard access. The unit tests verify planning-context arithmetic and static package integrity; they do not prove AI planning quality or third-party integration.

## Files and publishing

`index.html`, `style.css`, `app.js`, `planner.mjs`, `favicon.svg`, `social-card.png`, `aekr-mark.png`, `prompts.json`, `prompts/*.txt`, `USE-NOTES.txt` and `weekly-leverage-prompts.zip` are the publishable allowlist. Publish these only; keep tests, Git metadata and operational evidence out of the site artifact.

The canonical public URL carries Open Graph and X `summary_large_image` metadata pointing to `social-card.png`, an original 1200×630 image with the site's visual identity and Built with AEKR branding. Its editable source is `social/social-card.svg`; export that source to the same PNG dimensions when changing the artwork. The SVG source stays outside the deployed allowlist. `aekr-mark.png` is the owner-supplied orbital mark with the green accent changed to the site's rust red; the header logo links directly to `https://aekr.io/`. Social platforms control their own cached previews; deployment verification checks the actual public metadata and image responses.

`prompts.json`, individual prompt files and ZIP copies must agree. The tests check that contract. The ZIP contains the six generic starters and use notes; the single-file browser download includes the visitor's optional context.

This is a subproject of `edlopezpm-ops/Madness`, published as a standalone static application at `https://aekr.io/weekly-leverage/` through Cloudflare Workers Static Assets. GitHub Pages is not used. The new asset-only Worker has no server script, account service, app connector or database binding. Its two routes cover the bare entry path and its slash-delimited subtree; they do not replace the aekr.io homepage or other product routes.

### Deploy and recover

From this directory, with an already authorized Cloudflare CLI session:

```sh
node hosting/build.mjs
npx wrangler@4.157.0 deploy --config hosting/wrangler.jsonc --dry-run
npx wrangler@4.157.0 deploy --config hosting/wrangler.jsonc
```

Use the intended Cloudflare account. Do not add credentials to the repository. The build copies only the 16 public assets into an ignored `hosting/dist/weekly-leverage/` directory and adds the scoped response headers. It refuses unexpected preexisting output files rather than publishing or deleting them. The deployment has no custom GitHub Actions workflow and needs no model API.

The route without a trailing slash redirects to the public slash URL. Share the slash URL, especially with query parameters: Cloudflare's exact bare-path route does not match query strings. `hosting/_headers` applies only to the new static application and sets CSP, HSTS and framing controls. It does not change headers for other aekr.io applications. The scoped `no-transform` cache directive prevents automatic host-side HTML rewriting, including Cloudflare Web Analytics injection, for this tool without changing zone-wide settings.

Record the actual deployed version, routes and live browser/download evidence before claiming publication. On a later update, retain the prior version ID and use the provider rollback command for this Worker only. For the first release, recovery is removal of only the two newly created route IDs from the saved deployment receipt; never delete unrelated routes or change the existing homepage Worker. Keep the source and deployment configuration available for a reviewed corrective release.

This uses the existing vendor-managed hosting path. There is no model billing or new paid-service plan. Cloudflare documents [static asset requests and storage](https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/) separately from billable Worker-script execution; this deployment has no script. Existing account/provider policies still apply.


## Use and permissions

The owner-requested prompt deliverable is intended for visitors to use and adapt for personal or internal business planning. The narrow permission in [USE-NOTES.txt](USE-NOTES.txt) applies to the six prompt texts, not the website source, unrelated Madness material or AEKR marks. The root repository still has no general project license. No third-party product endorsement, compliance certification or guaranteed result is implied.

The article draft supplied as context is not included or published. The toolkit contains original planning instructions informed by its themes; it does not reproduce or attribute an unverified quotation.

Built with **[AEKR](https://aekr.io)**.
