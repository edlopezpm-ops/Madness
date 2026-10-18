<!-- (kommiBo) Source-reviewed engineering note; optional diagnostic. -->
# Distinguish Python parameters from editable document properties

The source parameters are ordinary Python numbers. Reassigning `L` in a returned
namespace does not rebuild already-created curves or install parametric links in
the document. Editing a Draft object's `Points`, by contrast, changes a document
property and requires recompute to update its shape.

The example generates a monohull in a clean session, records the middle station's
points, changes only the returned dictionary's `L`, and verifies unchanged points.
It then shifts every defining point of that one curve by +100 mm in Z, recomputes,
checks the point property, and restores the original points in a `finally` block.

Expected output is `namespace_edit_moved_points False` followed by
`restored_points True`. This is a local synthetic edit demonstration; it does not
rewrite `HullSample.py` or save a document. The longitudinal guides remain unchanged
during the temporary section edit, illustrating that these separately constructed
curves have no automatic station-to-guide dependency.

Use source edits plus a reviewed regeneration when changing the whole model.
Recompute evaluates dirty document objects; it does not rerun arbitrary Python
construction logic. Do not treat this example's temporary displacement as a new
design or assume restoring points clears the document's modified indicator.

## Run the complete example

Use a fresh FreeCAD session. Run from the repository root; the example executes
the named generator and creates document objects.

```shell
freecadcmd --safe-mode --console "import runpy; runpy.run_path('docs/examples/recompute-and-edit.py')"
```

[Complete example](../examples/recompute-and-edit.py). The script is intended to be run as supplied.

## Source anchors

- [`HullSample.py`: `L`](../../HullSample.py#L49).
- [`HullSample.py`: `station_curves`](../../HullSample.py#L261).
