<!-- (kommiBo) Source-reviewed repository notice; no runtime or license grant is implied. -->

# Privacy — Madness

Reviewed 2026-11-01.

## Scope and responsibility

AEKR maintains this project's notices and is the contact for questions at
[aekr@aekr.io](mailto:aekr@aekr.io). This notice covers local FreeCAD monohull and catamaran guide-geometry experiments.
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
