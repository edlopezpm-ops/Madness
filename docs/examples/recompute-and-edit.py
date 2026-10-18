# (kommiBo) Optional documentation example; source-backed, bounded evidence.
"""Distinguish Python parameters from editable document properties.

Requires the FreeCAD runtime; use a fresh session.
See the paired engineering note for expected output and limitations.
"""

import runpy
from pathlib import Path

import FreeCAD as App

ROOT = Path(__file__).resolve().parents[2]


ns = runpy.run_path(str(ROOT / "HullSample.py"))
doc = ns["doc"]
matches = doc.getObjectsByLabel("Station_06")
assert len(matches) == 1
station = matches[0]
original = [App.Vector(p.x, p.y, p.z) for p in station.Points]
ns["L"] = 15000
assert all(a.sub(b).Length < 1e-7 for a, b in zip(original, station.Points))
print("namespace_edit_moved_points", False)
try:
    station.Points = [App.Vector(p.x, p.y, p.z + 100) for p in original]
    doc.recompute()
    assert all(abs(new.z - old.z - 100) < 1e-7 for old, new in zip(original, station.Points))
finally:
    station.Points = original
    doc.recompute()
assert all(a.sub(b).Length < 1e-7 for a, b in zip(original, station.Points))
print("restored_points", True)
