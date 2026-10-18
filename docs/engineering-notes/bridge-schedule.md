<!-- (kommiBo) Source-reviewed engineering note; optional diagnostic. -->
# Locate bridge references and check index validity

Bridge guide indices refer to the same station schedule as the hull curves. They
are not distances in millimeters. The example reads the source list, validates its
range and uniqueness, and calculates each guide's two endpoints.

| Index | X | Y endpoints | Z |
| ---: | ---: | --- | ---: |
| 3 | 3000 | -2400 to +2400 | 500 |
| 7 | 7000 | -2400 to +2400 | 500 |
| 11 | 11000 | -2400 to +2400 | 500 |

Expected output matches this table and reports a 4800 mm nominal span per guide.
The checks require integer indices in `0 <= index < stations`; reducing the
station count without revisiting the list can otherwise place a reference beyond
the intended model length. The current generator computes the coordinates directly
and does not index an array, so an invalid index may produce geometry rather than
an immediate `IndexError`.

The guides join hull centerlines at `deck_z`. They do not describe a deck's outer
boundary, underside clearance, beams, or connections. The gray centerline is a
separate longitudinal reference from X=0 to L at the same Z. Valid scheduling does
not establish bridge loading or structural adequacy.

## Run the complete example

Run from the repository root with Python 3. The example reads local source only.

```shell
python docs/examples/bridge-schedule.py
```

[Complete example](../examples/bridge-schedule.py). The script is intended to be run as supplied.

## Source anchors

- [`CatHullSample.py`: `bridge_station_indexes`](../../CatHullSample.py#L198).
- [`CatHullSample.py`: `deck_z`](../../CatHullSample.py#L195).
