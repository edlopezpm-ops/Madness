<!-- (kommiBo) Source-reviewed engineering note; optional diagnostic. -->
# Save and reopen a generated document in temporary custody

An `.FCStd` round-trip tests document persistence separately from source execution.
The example creates a fresh catamaran document, captures object names and labels,
saves it in a temporary directory, closes that newly created document, then reopens
the saved file and checks the same inventory and valid shapes.

Expected output is `roundtrip_objects 44` and `fcstd_roundtrip True`. The opened
temporary document is closed in a `finally` block before the directory is removed.
Use a clean FreeCAD session: the recipe intentionally closes the document it just
generated, and is not intended to manage a user's previously edited model.

| Evidence | What it establishes |
| --- | --- |
| Successful save/reopen | this document persists in the current runtime |
| Same names and labels | tree inventory survived this round-trip |
| All checked shapes valid | current kernel accepts the restored geometry |

The recipe does not compare binary file bytes: FreeCAD documents can contain
metadata and serialization differences. It does not compare all properties,
presentation, or every curve numerically either. Keep the source generator and
its normal geometry validator as separate evidence. Nothing in this example
updates a committed reference model or creates a durable release artifact.

## Run the complete example

Use a fresh FreeCAD session. Run from the repository root; the example executes
the named generator and creates document objects.

```shell
freecadcmd --safe-mode --console "import runpy; runpy.run_path('docs/examples/document-roundtrip.py')"
```

[Complete example](../examples/document-roundtrip.py). The script is intended to be run as supplied.

## Source anchors

- [`CatHullSample.py`: `doc`](../../CatHullSample.py#L11).
- [`tests/validate_models.py`: `validate_catamaran`](../../tests/validate_models.py#L17).
