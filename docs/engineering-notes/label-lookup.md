<!-- (kommiBo) Source-reviewed engineering note; optional diagnostic. -->
# Resolve display labels without assuming internal names

The scripts set `Label` after Draft creates an object. That display text is the
appropriate lookup key for this repository's named guides; the automatically
allocated `Name` can differ. `getObjectsByLabel` returns a list because labels need
not be unique.

The example resolves the monohull's five guide labels with an explicit exactly-one
check, prints the actual internal names, and verifies that `doc.getObject(name)`
returns the same object. It then demonstrates a missing label through an empty
result. This distinguishes absent geometry from an incorrect assumption that the
label is its internal name.

Expected output contains `Keel_Line`, both sheer labels, both chine labels, and
`missing_matches 0`. A duplicate label stops with a diagnostic instead of silently
choosing the first object. For the catamaran the same approach needs the hull
prefix, for example `Port_Hull_Keel_Line`.

These are lookup checks inside a freshly generated document, not persistent
cross-file identifiers. Renaming a label can affect the validator and diagnostic
scripts even if the shape is unchanged. Do not use this recipe to rename source
objects merely to make a lookup succeed; inspect the generated tree first.

## Run the complete example

Use a fresh FreeCAD session. Run from the repository root; the example executes
the named generator and creates document objects.

```shell
freecadcmd --safe-mode --console "import runpy; runpy.run_path('docs/examples/label-lookup.py')"
```

[Complete example](../examples/label-lookup.py). The script is intended to be run as supplied.

## Source anchors

- [`HullSample.py`: `keel`](../../HullSample.py#L562).
- [`HullSample.py`: `port_sheer`](../../HullSample.py#L583).
- [`tests/validate_models.py`: `validate_monohull`](../../tests/validate_models.py#L30).
