<!-- (kommiBo) Source-reviewed engineering note; optional diagnostic. -->
# Calculate center spacing and the nominal inner gap

The catamaran's `overall_beam` is an outside-to-outside nominal dimension, whereas
`hull_spacing` is the distance between hull centers. Keeping those dimensions
separate prevents moving both hulls too far apart when exploring a wider design.

| Quantity | Expression | Current value |
| --- | --- | ---: |
| Center spacing | overall beam - single hull beam | 4800 mm |
| Port center | -spacing / 2 | -2400 mm |
| Starboard center | spacing / 2 | 2400 mm |
| Midship inner gap | spacing - single hull beam | 3600 mm |
| Midship outer points | centers +/- half beam | Y=-3000, +3000 mm |

The example prints these values and rejects dimensions that would overlap the
nominal midship section. `overall_beam >= 2 * hull_beam` gives a nonnegative
nominal gap; an equality permits touching, not an engineered clearance. The source
does not enforce this condition, so this calculation is a preflight diagnostic.

Expected output includes `center_spacing_mm 4800` and `inner_gap_mm 3600`. The
calculation applies to the seven defining points at the middle station. A B-spline
can have a bound beyond those defining coordinates; use the runtime bounds report
before treating the nominal gap as a measured clearance. No bridge loading,
hydrodynamic interference, or usable deck width is inferred from the calculation.

## Run the complete example

Run from the repository root with Python 3. The example reads local source only.

```shell
python docs/examples/catamaran-spacing.py
```

[Complete example](../examples/catamaran-spacing.py). The script is intended to be run as supplied.

## Source anchors

- [`CatHullSample.py`: `overall_beam`](../../CatHullSample.py#L26).
- [`CatHullSample.py`: `hull_spacing`](../../CatHullSample.py#L36).
- [`CatHullSample.py`: `create_single_hull`](../../CatHullSample.py#L96).
