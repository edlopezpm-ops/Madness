<!-- (kommiBo) Source-reviewed repository notice; no runtime or license grant is implied. -->

# Privacy — Madness

Reviewed 2026-11-01.

## Scope and responsibility

AEKR maintains this project's notices and is the contact for questions at
[aekr@aekr.io](mailto:aekr@aekr.io). This notice covers local FreeCAD monohull and catamaran guide-geometry experiments
and the separate Weekly Leverage prompt toolkit described below.
It does not claim a new legal entity or apply the aekr.io website's analytics,
questionnaire, browser-data email service or retention periods to this repository.

## What the reviewed source does

`HullSample.py` and `CatHullSample.py` construct FreeCAD documents in the local
process. Their reviewed source does not implement an analytics collector, account
service or model API call. The geometry validator also runs locally in FreeCAD.

Saving or exporting a document is a separate local action. CAD files, screenshots,
console traces and FreeCAD preferences can expose labels, dimensions, usernames or
paths. FreeCAD and installed add-ons have their own settings; this notice does not
certify their network behavior or the contents of every user-created model.

Source evidence: [monohull generator](HullSample.py), [catamaran generator](CatHullSample.py), [geometry validator](tests/validate_models.py). This is a source review, not a guarantee about every
dependency, host, historical artifact or future deployment.

<!-- (kommiBo) Browser-local planning and separately controlled optional statistics. -->
## Weekly Leverage subproject

[Weekly Leverage](projects/weekly-leverage/README.md) is a separate prompt toolkit with static assets
and two optional statistics routes.
Its customizer holds optional planning context temporarily in the current browser tab and
uses it to prepare text for copying or download. It implements no account, cookie, model API call
or calendar/task connector. Planning entries are never persisted or sent by the toolkit.
The customizer fetches fixed bundled UI/prompt JSON from this same subproject. Public files use
normal HTTP caching; loaded language bundles are reused in memory.

Optional language and manual theme preferences persist under `weekly-leverage-language` and
`weekly-leverage-theme`. A separate `weekly-leverage-analytics-v1` key stores the statistics choice,
policy and a 30-day expiry. Denied storage leaves display choices in the current tab and keeps
optional statistics off. Clearing browser storage removes remembered choices.

The [optional statistics module](projects/weekly-leverage/usage.js) requires explicit Weekly-only
permission and enabled, current service configuration before attempting one view per visible
document. It has no visitor identifier, event queue or retries. GPC/DNT, refusal, expiry,
withdrawal and storage failures stop prospective events. A view contains policy/consent/version
metadata, language, a coarse device category and a referrer category; the
[Worker](projects/weekly-leverage/hosting/worker.mjs) adds the hosting edge's country code or
`unknown`. These application payloads exclude raw IP addresses, full referrers, raw browser
strings, planning entries and prompt text.

The fixed same-origin routes are `GET /weekly-leverage/api/metrics/config` and
`POST /weekly-leverage/api/metrics`. Requests omit credentials; the Worker delegates only
configuration and recording to the named Console service. These statements describe the
reviewed source, not evidence of current hosted activation or storage retention. The footer
links to AEKR master policies without loading the main site's collection, consent or
policy-dialog scripts; those links and other products' choices do not authorize Weekly statistics.

Copying the result into an AI assistant is a separate disclosure to the provider chosen
by the visitor. External connectors, if available there, require their own authorization.
Use anonymized task labels and avoid confidential data. Customized downloaded files include
the entered context and remain in the visitor's download location until they remove them.
The generic ZIP contains no visitor context. Hosting providers process page and download
requests under their own policies; browser-local processing is not a zero-log claim.

## Hosting, requests and retention

GitHub processes repository visits and collaboration activity under its
[privacy statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).
If you serve a local copy over HTTP, that server can log requests. Downloading runtimes
or dependencies contacts their providers. Those operations are distinct from collection
implemented by the project itself. No repository-wide anonymous-visitor or zero-log
guarantee is made here.

Public issues, commits and attachments can be retained in history, forks, caches and
clones. Do not submit secrets, personal records or confidential data. For questions,
corrections, access or removal requests about project-held information, contact AEKR;
use [SECURITY.md](SECURITY.md) for a vulnerability report. Requests are considered under
applicable requirements; this notice promises neither a specific legal outcome nor
deletion of copies controlled by other parties. Local files have the retention described
in the [data-handling guide](docs/data-handling.md).
