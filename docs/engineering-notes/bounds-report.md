<!-- (kommiBo) Source-reviewed engineering note; optional diagnostic. -->
# Measure curve bounds separately from nominal dimensions

The numerical dimensions describe the defining points. A B-spline's extrema may
occur between those points, so measure its kernel bounding box before treating a
nominal value as a physical envelope. The report covers each hull independently
and includes its station and longitudinal curves.

| Measurement | Meaning | Expected baseline observation |
| --- | --- | --- |
| X min/max | guide length extent | near 0 / 14000 mm |
| Y min/max | measured lateral extent | port negative, starboard positive |
| Z min/max | measured vertical extent | includes the downward keel |

The example excludes bridges and the centerline by requiring the `Port_Hull_` or
`Starboard_Hull_` label prefix. It reports the inner gap as starboard YMin minus
port YMax. Compare this measured result with the nominal 3600 mm point-based gap;
the script deliberately does not assert their equality.

Expected output has one union bound per hull and a positive measured gap under
the current geometry. A negative gap would mean overlapping axis-aligned envelopes,
not necessarily a topological intersection. An envelope also contains empty space;
it cannot establish deck clearance, collision-free operation, or hydrodynamic
separation. Record the FreeCAD version with the values when comparing a change.

## Run the complete example

Use a fresh FreeCAD session. Run from the repository root; the example executes
the named generator and creates document objects.

```shell
freecadcmd --safe-mode --console "import runpy; runpy.run_path('docs/examples/bounds-report.py')"
```

[Complete example](../examples/bounds-report.py). The script is intended to be run as supplied.

## Source anchors

- [`CatHullSample.py`: `create_single_hull`](../../CatHullSample.py#L96).
- [`CatHullSample.py`: `hull_spacing`](../../CatHullSample.py#L36).
