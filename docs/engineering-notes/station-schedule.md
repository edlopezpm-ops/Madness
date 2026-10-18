<!-- (kommiBo) Source-reviewed engineering note; optional diagnostic. -->
# Print a reproducible station schedule

Use a station schedule when matching a visible transverse curve to its longitudinal
location. Both generators use `x = L * i / (stations - 1)` with inclusive endpoints.
The example reads the source literals and prints index, normalized position, and X
in millimeters without constructing curves.

| Model | Index range | Increment | Middle station |
| --- | --- | ---: | --- |
| Monohull | 0..12 | 1000 mm | index 6 at X=6000 |
| Catamaran | 0..14 | 1000 mm | index 7 at X=7000 |

Expected output starts at X=0 and ends at each model's `L`. The assertions check
both endpoints and strict increasing order. The section label is formatted with
two digits; index 6 becomes `Station_06` on the monohull and
`Port_Hull_Station_06` or `Starboard_Hull_Station_06` on the catamaran.

The current odd station counts include the exact midpoint. An even count would not;
do not label the nearest section as the midpoint without calculating its position.
Increasing `stations` changes the number of generated objects and requires review
of the baseline validator. This example is a sampling calculation, not evidence
that lofts, surfaces, or solids exist: both generators create open guide curves.

## Run the complete example

Run from the repository root with Python 3. The example reads local source only.

```shell
python docs/examples/station-schedule.py
```

[Complete example](../examples/station-schedule.py). The script is intended to be run as supplied.

## Source anchors

- [`HullSample.py`: `stations`](../../HullSample.py#L73).
- [`CatHullSample.py`: `create_single_hull`](../../CatHullSample.py#L96).
