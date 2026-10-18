<!-- (kommiBo) Source-reviewed engineering note; optional diagnostic. -->
# Track documents created by repeated generator runs

Both generators call `App.newDocument` at module execution time. They do not
search for or close an earlier document with the same requested name. Re-running
one in an interactive session can therefore leave multiple models open and make
the currently active tree a poor proxy for the execution you intended to inspect.

The example runs the monohull twice and retains each returned `doc`. It compares
the document inventory before and after each run, prints the allocated names,
and requires two distinct document handles with 18 objects each. It does not
assume the suffix FreeCAD chooses for the second name.

Expected output reports one added document per run and two different names. Use
the `doc` returned from the relevant `runpy.run_path` namespace for subsequent
lookups. Inspect and close unwanted experimental documents manually after saving
any work that matters; this example deliberately performs no automatic cleanup.

This recipe explains session custody rather than idempotence: repeating the
script creates a new document and is not an in-place model update. A screenshot
of one valid-looking tree cannot prove that a different retained document was
validated. Do not infer persistent identity from `ActiveDocument`, whose value
changes as documents are opened, generated, or selected.

## Run the complete example

Use a fresh FreeCAD session. Run from the repository root; the example executes
the named generator and creates document objects.

```shell
freecadcmd --safe-mode --console "import runpy; runpy.run_path('docs/examples/repeat-run-custody.py')"
```

[Complete example](../examples/repeat-run-custody.py). The script is intended to be run as supplied.

## Source anchors

- [`HullSample.py`: `doc`](../../HullSample.py#L32).
- [`CatHullSample.py`: `doc`](../../CatHullSample.py#L11).
