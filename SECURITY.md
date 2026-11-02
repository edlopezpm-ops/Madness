<!-- (kommiBo) Source-reviewed repository notice; no runtime or license grant is implied. -->

# Security reporting and support boundaries

Reviewed 2026-11-01.

## Report privately

Send a minimal description to [aekr@aekr.io](mailto:aekr@aekr.io). Include the repository,
commit, affected path, expected/observed behavior and a synthetic reproduction where
possible. Do not put credentials, real records, private geometry or sensitive attachments
in an initial report or public issue. Ask for an appropriate transfer method if needed.

For this project, relevant reports include a script unexpectedly reading unrelated files, exporting private geometry, or making an outbound request. A report should distinguish
behavior of the repository from a host, dependency or local application setting.

## Scope and response

This experimental repository has no published supported-version matrix or guaranteed
response/remediation SLA. AEKR can assess a report against the identified source version;
this is not a promise that every historical or modified copy is supported. There is no
bug-bounty program or blanket authorization to test other AEKR, GitHub, vendor or customer
systems. Use your own disposable environment and data.

A passing baseline is evidence for its documented checks, not a security certification.
Contain an incident in your environment, rotate any exposed credential with its provider,
and preserve a sanitized record. Follow the [data-handling guide](docs/data-handling.md)
for artifacts and the [privacy notice](PRIVACY.md) for personal-information requests.
