<!-- (kommiBo) Operator-assisted maintenance; source-reviewed documentation. -->
# Hull geometry: validation and diagnosis

Run from the repository root:

```shell
freecadcmd --safe-mode --console "import runpy; runpy.run_path('tests/validate_models.py', run_name='__main__')"
```

Run with FreeCAD 1.1.3, matching [the active workflow](../.github/workflows/python-app.yml). Ordinary CPython does not provide `FreeCAD` or its geometry runtime.

The [validator](../tests/validate_models.py) executes both generators. These are assertions in the current source, not permanent geometry requirements:

| Model | Checked behavior |
| --- | --- |
| Catamaran | 44 objects; 15 stations per hull; a labeled centerline; every shape non-null and valid. |
| Monohull | 18 objects; 13 station curves; a labeled keel; non-null valid shapes; keel length within 1 mm of 12,000 mm. |

For an object-count failure, compare the generator's changed construction steps with the expected objects. For a missing-label failure, check labels separately from Python variable names. For invalid geometry, inspect the generated shapes before changing expected counts. An intentional parameter change needs corresponding validator changes and visual inspection; weakening an assertion solely to make CI green hides a regression.

A download or SHA-256 failure occurs before geometry execution. Read the workflow's pinned filename and digest, and do not disable checksum verification. The legacy package workflow only prints a retirement notice and is not geometry evidence.

Passing these checks proves the selected geometric invariants, not buoyancy, stability, manufacturability, or certified engineering suitability.

See [change and recovery guidance](change-recovery.md) before merging a correction.
