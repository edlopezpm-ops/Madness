<!-- (kommiBo) Source-reviewed repository notice; no runtime or license grant is implied. -->

# Licensing and provenance inventory

Reviewed 2026-11-12.

No root project license has been selected. There is no general grant to reuse the project scripts, explanations or generated reference material.

| Component | Evidence and licensing boundary |
|---|---|
| Hull scripts and engineering notes | No root project license; public visibility is not an open-source grant. |
| Weekly Leverage prompt texts | Owner-requested downloadable planning deliverable; personal/internal business use and adaptation permitted only for the six prompt texts under [the scoped use notes](../projects/weekly-leverage/USE-NOTES.txt). Website source and unrelated material are not included in that permission. |
| `FreeCAD`, `Draft`, `Part`, optional `FreeCADGui` | Imports from an external FreeCAD installation; its distribution carries its own licenses and third-party notices. |
| User-saved CAD or exported geometry | Review source ownership and embedded metadata independently; do not infer a new license from a file extension. |

## AEKR provenance has a bounded scope

The [AEKR banner notice](../assets/AEKR-BANNER-LICENSE.txt) is copied unchanged from
the AEKR project-branding scaffold. It records the MIT provenance of that upstream
scaffold and any AEKR banner copied from it. Upstream references inside that verbatim
notice describe the toolkit, not a requirement to add its handbook here. It is not a
license for unrelated project code, data, personal material or third-party marks.

The AEKR footer names the workflow used. It neither transfers copyright to AEKR nor
imports the toolkit's CC BY handbook license into this repository. Where no banner
image is present, retaining its provenance notice does not claim that an image is bundled.

## Recorded license and permission changes

This history distinguishes a changed permission from an update to its documentation.
The linked commits identify the material being described; this inventory is not a new grant.

| Date | Source change | Effect on permissions |
|---|---|---|
| 2026-11-01 | [Licensing inventory added](https://github.com/edlopezpm-ops/Madness/commit/d5ce62e7ef5b6adedad22e38e83b688dd19d3c81) | Documented the absent root license and external-runtime boundaries; no general license was added. |
| 2026-11-03 | [Weekly Leverage introduced](https://github.com/edlopezpm-ops/Madness/commit/92b169c8c791bcba54a7e02ea4f9322cb3a0d98d) | Added the narrow prompt-text permission in `USE-NOTES.txt`; the rest of the repository remained without a general license. |
| 2026-11-12 | This inventory update | Adds reuse guidance and traceable history; preserves the existing permissions. |

## Which permission applies to a proposed reuse?

| Proposed action | Applicable boundary |
|---|---|
| View or fork this public repository on GitHub | GitHub's platform terms permit these platform actions; this is not a general project license. |
| Copy or adapt the six Weekly Leverage prompts for personal/internal business planning | Follow the scoped [prompt permission](../projects/weekly-leverage/USE-NOTES.txt); it does not extend to website code or hull scripts. |
| Redistribute or adapt hull scripts, website source or reference geometry beyond applicable rights | Request the missing permission and identify the exact files and revision. |
| Bundle FreeCAD or an add-on with a project copy | Review that distribution's own notices and requirements separately. |

For a permission request, send [aekr@aekr.io](mailto:aekr@aekr.io) the repository,
commit or release, relevant paths, and intended use or distribution. Omit confidential
source data. A request is not approval; retain any actual written permission with the
revision and files it covers. A future license change needs an explicit scope and must
preserve third-party notices and permissions already granted.

## Before redistributing

Check the actual files and installed dependency versions, preserve their applicable
notices, and obtain any missing permissions. A package name, a public repository,
a passing test or a software bill of materials is not itself a grant. This is a bounded
source inventory, not an exhaustive dependency-license or ownership certification.
The [use notes](../TERMS.md) cannot override a license grant.

Reference: [GitHub's repository licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).
