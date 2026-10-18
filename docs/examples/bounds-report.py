# (kommiBo) Optional documentation example; source-backed, bounded evidence.
"""Measure curve bounds separately from nominal dimensions.

Requires the FreeCAD runtime; use a fresh session.
See the paired engineering note for expected output and limitations.
"""

import runpy
from pathlib import Path

import FreeCAD as App

ROOT = Path(__file__).resolve().parents[2]


doc = runpy.run_path(str(ROOT / "CatHullSample.py"))["doc"]
bounds = {}
for prefix in ("Port_Hull_", "Starboard_Hull_"):
    shapes = [obj.Shape for obj in doc.Objects if obj.Label.startswith(prefix)]
    assert len(shapes) == 20
    box = App.BoundBox()
    for shape in shapes:
        assert not shape.isNull()
        box.add(shape.BoundBox)
    bounds[prefix] = box
    print(prefix, "XYZ_min", (box.XMin, box.YMin, box.ZMin),
          "XYZ_max", (box.XMax, box.YMax, box.ZMax))
gap = bounds["Starboard_Hull_"].YMin - bounds["Port_Hull_"].YMax
print("measured_envelope_gap_mm", gap)
assert gap > 0
print("FreeCAD_version", App.Version())
