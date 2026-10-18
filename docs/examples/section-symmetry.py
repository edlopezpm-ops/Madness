# (kommiBo) Optional documentation example; source-backed, bounded evidence.
"""Inspect the defining points of a transverse section.

Requires the FreeCAD runtime; use a fresh session.
See the paired engineering note for expected output and limitations.
"""

import runpy
from pathlib import Path

import FreeCAD as App

ROOT = Path(__file__).resolve().parents[2]


ns = runpy.run_path(str(ROOT / "HullSample.py"))
doc = ns["doc"]
objects = doc.getObjectsByLabel("Station_06")
assert len(objects) == 1
points = list(objects[0].Points)
assert len(points) == 7
for point in points:
    print(tuple(round(v, 6) for v in (point.x, point.y, point.z)))
    assert abs(point.x - 6000.0) < 1e-7
for left, right in zip(points, reversed(points)):
    assert abs(left.y + right.y) < 1e-7
    assert abs(left.z - right.z) < 1e-7
print("defining_points_symmetric", True)
