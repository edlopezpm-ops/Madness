<!-- (kommiBo) Source-reviewed engineering note; optional diagnostic. -->
# Inventory dimensions without importing FreeCAD

Read the two generators before selecting a model. The literal inventory example uses
Python's AST; it never imports or executes either generator. Values are millimeters,
except `stations`, which is an integer count. This is useful on a workstation that has
Python but no FreeCAD runtime.

| Input | Monohull | Catamaran | Geometric role |
| --- | ---: | ---: | --- |
| `L` | 12000 | 14000 | Longitudinal extent in X |
| `B` / `hull_beam` | 3200 | 1200 | Maximum width of one hull |
| `D` | 1400 | 1200 | Depth scale, not a verified draft |
| `stations` | 13 | 15 | Transverse section count per hull |
| `overall_beam` | absent | 6000 | Nominal outside beam |

Expected output contains two dictionaries matching this table. `L / 1000` prints
12.0 and 14.0 meters; it does not change the model's working unit. The extractor
intentionally ignores expressions such as `hull_spacing = overall_beam - hull_beam`.
It reports direct assignments only, so a later expression-based parameter requires
review rather than silently being evaluated. Compare the printed values with the
source before recording them in a design note.

This inventory cannot establish that a B-spline has the requested bounds. It also
does not validate numeric domains: the station formula requires at least two stations
and positive dimensions. The geometry validator remains a separate runtime check.

## Run the complete example

Run from the repository root with Python 3. The example reads local source only.

```shell
python docs/examples/parameter-inventory.py
```

[Complete example](../examples/parameter-inventory.py). The script is intended to be run as supplied.

## Source anchors

- [`HullSample.py`: `L`](../../HullSample.py#L49).
- [`CatHullSample.py`: `L`](../../CatHullSample.py#L19).
- [`tests/validate_models.py`: `validate_monohull`](../../tests/validate_models.py#L30).
