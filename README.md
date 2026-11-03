# FreeCAD Hull Experiments

Local Python experiments that generate monohull and catamaran guide geometry through FreeCAD's APIs.

<!-- (kommiBo) Owner-authorized standalone weekly planning subproject. -->
## Subprojects

- **[Weekly Leverage](projects/weekly-leverage/README.md)**: a standalone HTML toolkit with six downloadable prompts for planning a realistic week with your own AI and apps. Built with AEKR. The CAD experiments below remain separate.

## Status

The models are visual experiments, not certified naval architecture, fabrication, or safety designs. Both scripts create guide curves in millimeters and can run interactively or through the headless FreeCAD command runtime.

## Run

Requirements: FreeCAD 1.1.3.

<!-- (kommiBo) Repeated runs create separate documents rather than updating one model. -->
Use a fresh disposable FreeCAD session for the commands below. Both scripts create a new
document when executed; rerunning one does not update an earlier model in place. In an
interactive session, keep the `doc` from the intended run and save your own work before
manually closing experiments. See [repeat-run custody](docs/engineering-notes/repeat-run-custody.md)
and the [use boundaries](TERMS.md).

Open either script in that session's Python console, or run it from the repository root:

```bash
freecadcmd --safe-mode --console "import runpy; runpy.run_path('CatHullSample.py')"
freecadcmd --safe-mode --console "import runpy; runpy.run_path('HullSample.py')"
```

## Validate

```bash
freecadcmd --safe-mode --console "import runpy; runpy.run_path('tests/validate_models.py', run_name='__main__')"
```

The validator executes both generators and verifies their object counts, expected named geometry, valid shapes, and model dimensions. CI verifies and extracts the official Linux x86-64 FreeCAD 1.1.3 AppImage before running that same validator.

## License

No project license has been selected. GitHub’s platform terms permit viewing and forking; broader project reuse requires appropriate permission. The separate AEKR provenance notice does not license the project material.

## Governance

Changes follow the AEKR engineering workflow: bounded scope, deterministic geometry validation, pull-request review, and revert-PR recovery. The PR author and reviewer are distinct technical actors under one HOC authority; the reviewer approves and merges the exact validated head. This separation is an operational control, not an independent audit.

<!-- (kommiBo) Source-backed documentation navigation. -->
## Engineering recipes

See the [engineering notes](docs/engineering-notes/README.md) for reproducible examples, source references and validation limits.

<!-- (kommiBo) Project-specific behavior, privacy and permission boundaries. -->
## Privacy, use and permissions

The generators build guide curves in a local FreeCAD process. Their validation does
not establish buoyancy, stability or fabrication safety. Saving or sharing CAD files
requires a separate review of document labels, properties and export metadata.

- [Privacy notice](PRIVACY.md): project processing, hosting and requests.
- [Use and service boundaries](TERMS.md): intended use and license precedence.
- [Licensing inventory](docs/licensing.md): project, dependency and AEKR provenance scopes.
- [Data handling](docs/data-handling.md): local artifacts and publication checks.
- [Security reporting](SECURITY.md): private reports and support limits.

---

Built with the **[AI Engineering Knowledge Racking (AEKR)](https://aekr.io)** workflow.
