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

## HOC review note — 2026-10-09

At the HOC's request, this note records Friday's maintenance review in repository history. The date uses America/New_York.

Automated baseline validation passed at [`dc80fc51e3d0`](https://github.com/edlopezpm-ops/Madness/commit/dc80fc51e3d076b2659f7a14a02a5751d92d2f8d). The enabled documentation maintenance rules returned `NO_ACTION`: no eligible change was found.

The FreeCAD check exercised the hull generators and their geometry assertions; it did not establish buoyancy or fabrication suitability.

<details>
<summary>67 test · Friday lab 🤖</summary>

(kommiBo) HOC-requested, one-off contribution-count experiment for 2026-10-09 (America/New_York). These are jokes, not additional test cases or engineering review evidence. Operator-assisted delivery; the scheduled maintenance rules are unchanged.

- 01. 🛥️ The catamaran insists on two sides to every story. — kommiBo 🤖
- 02. 📉 Negative Z: the hull is keeping things down to earth. — kommiBo 🤖
- 03. 〰️ The B-spline prefers a smooth exit on Friday. — kommiBo 🤖
- 04. 📏 Twelve thousand millimeters of weekend ambition. — kommiBo 🤖
- 05. 🧭 The keel has a centerline and a clear sense of direction. — kommiBo 🤖
- 06. 🌊 Geometry passed; the bathtub has not peer-reviewed it. — kommiBo 🤖
- 07. 🏁 All aboard the documentation-only cruise. — kommiBo 🤖

</details>
