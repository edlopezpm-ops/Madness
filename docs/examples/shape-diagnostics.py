# (kommiBo) Optional documentation example; source-backed, bounded evidence.
"""Locate null and invalid guide shapes by object.

Requires the FreeCAD runtime; use a fresh session.
See the paired engineering note for expected output and limitations.
"""

import runpy
from pathlib import Path

import FreeCAD as App

ROOT = Path(__file__).resolve().parents[2]


doc = runpy.run_path(str(ROOT / "CatHullSample.py"))["doc"]
doc.recompute()
failures = []
for obj in doc.Objects:
    if not hasattr(obj, "Shape"):
        failures.append((obj.Name, "missing Shape"))
        continue
    null = obj.Shape.isNull()
    valid = not null and obj.Shape.isValid()
    print(obj.Name, obj.Label, "null", null, "valid", valid,
          "solids", len(obj.Shape.Solids))
    if not valid:
        failures.append((obj.Name, obj.Label))
print("failures", failures)
assert not failures
