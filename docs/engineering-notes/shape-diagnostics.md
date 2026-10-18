<!-- (kommiBo) Source-reviewed engineering note; optional diagnostic. -->
# Locate null and invalid guide shapes by object

When the baseline says a model contains invalid geometry, identify the failing
object before altering a distribution or relaxing an assertion. The example prints
each catamaran object's internal name, label, null state, and validity.

| Observation | Interpretation | Next inspection |
| --- | --- | --- |
| `isNull()` true | no usable topological shape | object properties and recompute |
| non-null, `isValid()` false | kernel validity failed | defining points and nearby curves |
| valid, zero solids | normal for these guide curves | do not demand a solid from this generator |

Expected output is 44 non-null, valid objects and an empty `failures` list under
the unchanged baseline. The assertions mirror the important shape checks in the
repository validator, while the per-object rows add diagnostic context. A missing
`Shape` is handled as a distinct failure instead of causing an unexplained attribute
error.

A valid edge does not imply fairness, tangency between independently generated
curves, a closed shell, or positive enclosed volume. Bridge references are curves
too. Preserve the current baseline failure as evidence; change model inputs only
after identifying which object and coordinate set failed.

## Run the complete example

Use a fresh FreeCAD session. Run from the repository root; the example executes
the named generator and creates document objects.

```shell
freecadcmd --safe-mode --console "import runpy; runpy.run_path('docs/examples/shape-diagnostics.py')"
```

[Complete example](../examples/shape-diagnostics.py). The script is intended to be run as supplied.

## Source anchors

- [`tests/validate_models.py`: `validate_catamaran`](../../tests/validate_models.py#L17).
- [`CatHullSample.py`: `create_single_hull`](../../CatHullSample.py#L96).
