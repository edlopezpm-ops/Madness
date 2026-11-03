# Weekly Leverage

<!-- (kommiBo) A standalone AEKR prompt toolkit; separate from the CAD experiments. -->

Plan once. Make room to live. Six planning prompts for the AI assistant and apps a visitor already uses.

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
node --test tests/planner.test.mjs
python3 -m unittest discover -s tests -p 'test_*.py'
```

Open `http://127.0.0.1:4783/`. Serve through HTTP: ES modules and the preview JSON are not intended to run via `file://`. The plain text files and ZIP remain usable without JavaScript.

Browser verification should cover all six prompt choices, custom capacity, clipboard success/fallback, customized downloads, reset, mobile layout and keyboard access. The unit tests verify planning-context arithmetic and static package integrity; they do not prove AI planning quality or third-party integration.

## Files and publishing

`index.html`, `style.css`, `app.js`, `planner.mjs`, `favicon.svg`, `prompts.json`, `prompts/*.txt`, `USE-NOTES.txt` and `weekly-leverage-prompts.zip` are the publishable allowlist. Publish these only; keep tests, Git metadata and operational evidence out of the site artifact.

`prompts.json`, individual prompt files and ZIP copies must agree. The tests check that contract. The ZIP contains the six generic starters and use notes; the single-file browser download includes the visitor's optional context.

This is a subproject of `edlopezpm-ops/Madness`. Its public hosting URL must be confirmed after an actual deployment. GitHub Pages always uses an internal Actions workflow, including branch-based publication; a previous no-Actions instruction must be resolved before enabling Pages. No custom workflow is included here.

## Use and permissions

The owner-requested prompt deliverable is intended for visitors to use and adapt for personal or internal business planning. The narrow permission in [USE-NOTES.txt](USE-NOTES.txt) applies to the six prompt texts, not the website source, unrelated Madness material or AEKR marks. The root repository still has no general project license. No third-party product endorsement, compliance certification or guaranteed result is implied.

The article draft supplied as context is not included or published. The toolkit contains original planning instructions informed by its themes; it does not reproduce or attribute an unverified quotation.

Built with **[AEKR](https://aekr.io)**.
