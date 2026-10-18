<!-- (kommiBo) Source-reviewed engineering note; optional diagnostic. -->
# Round-trip a selected guide through a temporary BREP

Export a single known guide when investigating interchange rather than exporting
the entire visible document indiscriminately. The example chooses the monohull's
`Keel_Line`, writes its shape to a temporary BREP, reads it into a new `Part.Shape`,
and compares length and X extent within 1e-6 mm.

| Item | Selection or check |
| --- | --- |
| Source object | exactly one `Keel_Line` label |
| Output | `keel.brep` inside a temporary directory |
| Round-trip checks | non-null, valid, matching edge length and X extent |

Expected output is a positive file size and `brep_roundtrip True`. The temporary
directory is removed at the end of the example, including on assertion failure.
No committed model or user-selected file is overwritten. To retain an engineering
artifact, adapt the destination deliberately and record the source revision and
FreeCAD version beside it.

BREP carries the selected topological shape; this recipe does not assert that the
Draft object's Python behavior, label, presentation, or parameter relationships
survive. A guide edge exported successfully remains an edge. This is not a solid,
STEP assembly, fabrication drawing, or engineering approval. The source does not
currently provide an exporter; this example is an optional console diagnostic.

## Run the complete example

Use a fresh FreeCAD session. Run from the repository root; the example executes
the named generator and creates document objects.

```shell
freecadcmd --safe-mode --console "import runpy; runpy.run_path('docs/examples/brep-roundtrip.py')"
```

[Complete example](../examples/brep-roundtrip.py). The script is intended to be run as supplied.

## Source anchors

- [`HullSample.py`: `keel`](../../HullSample.py#L562).
- [`tests/validate_models.py`: `validate_monohull`](../../tests/validate_models.py#L30).
