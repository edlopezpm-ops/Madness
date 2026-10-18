<!-- (kommiBo) Source-reviewed engineering note; optional diagnostic. -->
# Compare keel and sheer samples with station points

The longitudinal keel and sheer guides are built from samples at each station.
This recipe checks the relationship between those document objects rather than
only counting them. It uses the catamaran's port hull and compares all 15 stations.

| Station point index | Longitudinal object | Relationship |
| --- | --- | --- |
| 0 | Port hull port sheer | same X/Y/Z sample |
| 3 | Port hull keel | same X/Y/Z sample |
| 6 | Port hull starboard sheer | same X/Y/Z sample |

Expected output is three rows, each reporting 15 matching samples. The script
uses Draft's `Points` property, sorts stations by their numeric label suffix, and
checks vector distances within 1e-7 mm. If the point count differs it fails before
attempting a misleading pairwise comparison.

Do not extend this equality test to the chine guides. Their points use lateral
factor 0.50 and depth factor 0.65, whereas the station's neighboring points use
0.40 and 0.70. They are independent visual guides. Equality at sample positions
also does not force identical spline tangents, shared topology, a watertight shell,
or matching geometry everywhere between stations.

## Run the complete example

Use a fresh FreeCAD session. Run from the repository root; the example executes
the named generator and creates document objects.

```shell
freecadcmd --safe-mode --console "import runpy; runpy.run_path('docs/examples/guide-consistency.py')"
```

[Complete example](../examples/guide-consistency.py). The script is intended to be run as supplied.

## Source anchors

- [`CatHullSample.py`: `create_single_hull`](../../CatHullSample.py#L96).
