<!-- (kommiBo) Operator-assisted engineering documentation; no certification claim. -->
# Engineering notes and console recipes

These recipes explain the current source, provide small reproducible examples, and
state what their results can establish. They are optional diagnostics under `docs/`;
the repository's generators, validator, workflows, and reference models are unchanged.

The documentation pattern is adapted from
[checktimecardandgivefeedback at 235a70f](https://github.com/edlopezpm-ops/checktimecardandgivefeedback/tree/235a70f1613f9a7c19515b3a579d7539dcff6b47):
record provenance, identify responsibility, keep examples concrete, and distinguish
observed evidence from assumptions. This is attribution of documentation patterns
only. No application, identity, timekeeping, or business facts are imported.

Recipes marked **Python** run without FreeCAD and report analytical or source
evidence. Recipes marked **FreeCAD** need the FreeCAD Python console/runtime; use
a fresh session and review the described document changes before running them.
For the full baseline, see the [existing validation guide](../validation-guide.md).
Successful syntax or analytical checks do not establish a geometry-runtime pass.

- [Inventory dimensions without importing FreeCAD](parameter-inventory.md) — **Python**.
- [Print a reproducible station schedule](station-schedule.md) — **Python**.
- [Check beam, depth, and rocker calculations together](distribution-check.md) — **Python**.
- [Calculate center spacing and the nominal inner gap](catamaran-spacing.md) — **Python**.
- [Inspect the defining points of a transverse section](section-symmetry.md) — **FreeCAD**.
- [Map Python collections to the document tree](object-tree.md) — **FreeCAD**.
- [Locate null and invalid guide shapes by object](shape-diagnostics.md) — **FreeCAD**.
- [Measure curve bounds separately from nominal dimensions](bounds-report.md) — **FreeCAD**.
- [Resolve display labels without assuming internal names](label-lookup.md) — **FreeCAD**.
- [Compare keel and sheer samples with station points](guide-consistency.md) — **FreeCAD**.
- [Locate bridge references and check index validity](bridge-schedule.md) — **Python**.
- [Distinguish Python parameters from editable document properties](recompute-and-edit.md) — **FreeCAD**.
- [Exercise the presentation guard without a GUI](headless-style.md) — **Python**.
