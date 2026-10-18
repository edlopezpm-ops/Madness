<!-- (kommiBo) Source-reviewed engineering note; optional diagnostic. -->
# Check beam, depth, and rocker calculations together

Before interpreting a curve, inspect the three distributions that generate its
control points. The monohull's beam floor is 12% of `B`; its depth floor is 45%
of `D`. The catamaran uses 10% and 40%. These nonzero endpoints are explicit in
the expressions; the monohull beam docstring's statement about zero endpoints
does not describe the implemented formula.

| Model | End beam | End depth | End keel Z | Midpoint keel Z |
| --- | ---: | ---: | ---: | ---: |
| Monohull | 384 | 630 | -472.5 | -1400 |
| Each catamaran hull | 120 | 480 | -336 | -1200 |

The example mirrors the source expressions using source-read dimensions. It prints
X=0, L/4, L/2, 3L/4, L and asserts longitudinal symmetry at those samples. Negative
Z is downward in these models; `depth_at` is a positive scale while `z_keel` is a
signed coordinate. The monohull's `App.Units.Quantity(1).Value` is a neutral scalar
in this calculation, not a conversion from meters.

Expected output matches the endpoint and midpoint table to floating-point tolerance.
This is a documented analytical reconstruction, not execution of `beam_at` or the
FreeCAD spline kernel. A future formula change must be reflected here deliberately;
validity and bounds of the interpolated curves still need FreeCAD validation.

## Run the complete example

Run from the repository root with Python 3. The example reads local source only.

```shell
python docs/examples/distribution-check.py
```

[Complete example](../examples/distribution-check.py). The script is intended to be run as supplied.

## Source anchors

- [`HullSample.py`: `beam_at`](../../HullSample.py#L121).
- [`HullSample.py`: `depth_at`](../../HullSample.py#L175).
- [`HullSample.py`: `z_keel`](../../HullSample.py#L211).
- [`CatHullSample.py`: `beam_at`](../../CatHullSample.py#L65).
