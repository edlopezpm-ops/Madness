<!-- (kommiBo) Source-reviewed engineering note; optional diagnostic. -->
# Inspect the defining points of a transverse section

Inspect a representative section before judging the entire guide network. The
example generates the monohull, chooses `Station_06`, and reads its Draft `Points`.
It checks the seven-point defining polygon around Y=0 at X=6000 mm.

| Point pair | Absolute Y | Z |
| --- | ---: | ---: |
| 0 and 6 | 1600 | 0 |
| 1 and 5 | 1360 | -280 |
| 2 and 4 | 720 | -980 |
| 3, center | 0 | -1400 |

Expected output is seven `(X, Y, Z)` triples and `defining_points_symmetric True`.
The script checks reflected pairs with a numerical tolerance and verifies a shared
X coordinate. A mismatch is localized to the defining points, label lookup, or
generator rather than inferred from a camera angle.

`Points` belongs to the Draft document object; it is not a list of sampled vertices
on every position of the mathematical spline. Symmetry of this polygon is useful
design evidence, but the separate `Shape.isValid()` and bounds checks concern the
kernel result. The section remains open across its top: seven points do not create
a watertight hull or a displacement volume.

## Run the complete example

Use a fresh FreeCAD session. Run from the repository root; the example executes
the named generator and creates document objects.

```shell
freecadcmd --safe-mode --console "import runpy; runpy.run_path('docs/examples/section-symmetry.py')"
```

[Complete example](../examples/section-symmetry.py). The script is intended to be run as supplied.

## Source anchors

- [`HullSample.py`: `station_curves`](../../HullSample.py#L261).
- [`HullSample.py`: `stations`](../../HullSample.py#L73).
