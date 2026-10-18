# (kommiBo) Optional documentation example; source-backed, bounded evidence.
"""Compare keel and sheer samples with station points.

Requires the FreeCAD runtime; use a fresh session.
See the paired engineering note for expected output and limitations.
"""

import runpy
from pathlib import Path

import FreeCAD as App

ROOT = Path(__file__).resolve().parents[2]


doc = runpy.run_path(str(ROOT / "CatHullSample.py"))["doc"]
stations = sorted((obj for obj in doc.Objects if obj.Label.startswith("Port_Hull_Station_")),
                  key=lambda obj: int(obj.Label.rsplit("_", 1)[1]))
assert len(stations) == 15
for label, point_index in (("Port_Hull_Port_Sheer_Line", 0),
                           ("Port_Hull_Keel_Line", 3),
                           ("Port_Hull_Starboard_Sheer_Line", 6)):
    matches = doc.getObjectsByLabel(label)
    assert len(matches) == 1
    samples = matches[0].Points
    assert len(samples) == len(stations)
    for station, guide_point in zip(stations, samples):
        assert station.Points[point_index].sub(guide_point).Length < 1e-7
    print(label, "matching_samples", len(samples))
