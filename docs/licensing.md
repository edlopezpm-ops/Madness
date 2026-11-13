<!-- (kommiBo) Source-reviewed repository notice; no runtime or license grant is implied. -->

# Licensing and provenance inventory

Reviewed 2026-11-12.

The root [license scope](../LICENSE) now grants standard [MIT permissions](../LICENSES/MIT.txt) for its exact list of educational source and associated documentation. It is the sole authoritative path list. Unlisted material receives no new license; existing permissions remain intact.

| Component | Evidence and licensing boundary |
|---|---|
| Listed CAD source and paired documentation | Standard MIT for the exact paths in the root [scope notice](../LICENSE); preserve the copyright and permission notice in copies or substantial portions. |
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
| 2026-11-12 | Earlier inventory update | Added reuse guidance and traceable history without a new grant. |
| 2026-11-12 | Owner-authorized [scoped MIT grant](../LICENSE) | Makes the exact listed source and documentation available under MIT; preserves previous permissions and third-party notices. |

## Which permission applies to a proposed reuse?

| Proposed action | Applicable boundary |
|---|---|
| View or fork this public repository on GitHub | GitHub's platform terms permit these platform actions; the root MIT grant separately covers its listed material. |
| Copy or adapt the six Weekly Leverage prompts for personal/internal business planning | Follow the scoped [prompt permission](../projects/weekly-leverage/USE-NOTES.txt); it does not extend to website code or hull scripts. |
| Use, modify or redistribute material covered by the root scope notice | Follow the standard MIT notice condition; commercial use needs no separate approval under this grant. |
| Reuse Weekly Leverage website source, artwork or other unlisted material beyond existing permissions | Request the missing permission and identify the exact files and revision. |
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
