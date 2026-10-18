<!-- (kommiBo) Source-reviewed engineering note; optional diagnostic. -->
# Exercise the presentation guard without a GUI

Geometry construction and presentation are separate concerns in these scripts.
`FreeCAD` supplies documents and vectors, `Draft` constructs curves, and the optional
`FreeCADGui` import supplies view styling and camera operations. Ordinary CPython
can parse the file but cannot create its geometry without the FreeCAD modules.

This standard-library example extracts only the monohull's `style` function as an
AST node. It executes that trusted local function in two synthetic namespaces:
one with `Gui=None`, and one with a non-null GUI sentinel and a fake `ViewObject`.
It never imports FreeCAD or runs a generator.

Expected output is `headless_return_same_object True` and
`synthetic_color (1.0, 0.0, 0.0) width 4`. A headless call returns its input without
requiring `ViewObject`; the synthetic GUI call assigns line color and width. This
isolates the Python branch from the geometry runtime.

The synthetic objects are test doubles used by this documentation example only.
They do not verify a rendered color, camera fitting, a working display server, or
FreeCADGui availability. A GUI import can succeed in some command environments;
the generator separately guards access to the active view at its end.

## Run the complete example

Run from the repository root with Python 3. The example reads local source only.

```shell
python docs/examples/headless-style.py
```

[Complete example](../examples/headless-style.py). The script is intended to be run as supplied.

## Source anchors

- [`HullSample.py`: `style`](../../HullSample.py#L81).
- [`CatHullSample.py`: `style`](../../CatHullSample.py#L54).
