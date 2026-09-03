# FreeCAD Hull Experiments

Learning scripts that generate monohull and catamaran guide geometry with FreeCAD's Python APIs.

## Status

The models are visual experiments, not certified naval architecture, fabrication, or safety designs. Both scripts create guide curves in millimeters and can run interactively or through the headless FreeCAD command runtime.

## Run

Requirements: FreeCAD 1.1.3.

Open either script in the FreeCAD Python console, or run it from the repository root:

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

No license file is present, so this repository grants no general permission to copy, modify, distribute, or reuse the work. Professionalization did not add or change licensing terms.

## Governance

Changes follow the AEKR engineering workflow: bounded scope, deterministic geometry validation, pull-request review, and revert-PR recovery. The PR author and reviewer are distinct technical actors under one HOC authority; the reviewer approves and merges the exact validated head. This separation is an operational control, not an independent audit.

---

Built with the **[AI Engineering Knowledge Repo (AEKR)](https://aekr.io)** workflow.
