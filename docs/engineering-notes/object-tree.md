<!-- (kommiBo) Source-reviewed engineering note; optional diagnostic. -->
# Map Python collections to the document tree

A Python list such as `station_curves` is a reference collection, not an extra
FreeCAD object. Use this report to reconcile code-created curves with the tree
before changing an expected object count.

| Model | Transverse curves | Longitudinal curves | Other references | Total |
| --- | ---: | ---: | ---: | ---: |
| Monohull | 13 | 5 | 0 | 18 |
| Catamaran | 30 | 10 | 3 bridges + 1 centerline | 44 |

The example runs each generator once, obtains the document from that execution's
namespace, prints `Name`, `Label`, and `TypeId`, then checks the total against the
current baseline. For the catamaran, `port_hull` and `starboard_hull` each hold 15
station references; the five longitudinal objects for each hull are created in the
function but are not members of the returned list.

Expected output contains exactly 18 and 44 rows respectively, followed by the
reported counts. `Name` is FreeCAD's internal identifier; `Label` is display text
assigned by the scripts. Neither the Python variable name nor a list's length alone
describes every object created. This report is a construction inventory and does
not prove valid geometry, surface continuity, or fabrication readiness.

## Run the complete example

Use a fresh FreeCAD session. Run from the repository root; the example executes
the named generator and creates document objects.

```shell
freecadcmd --safe-mode --console "import runpy; runpy.run_path('docs/examples/object-tree.py')"
```

[Complete example](../examples/object-tree.py). The script is intended to be run as supplied.

## Source anchors

- [`CatHullSample.py`: `create_single_hull`](../../CatHullSample.py#L96).
- [`tests/validate_models.py`: `validate_catamaran`](../../tests/validate_models.py#L17).
- [`tests/validate_models.py`: `validate_monohull`](../../tests/validate_models.py#L30).
