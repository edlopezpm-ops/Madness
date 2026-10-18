# (kommiBo) Optional documentation example; source-backed, bounded evidence.
"""Resolve display labels without assuming internal names.

Requires the FreeCAD runtime; use a fresh session.
See the paired engineering note for expected output and limitations.
"""

import runpy
from pathlib import Path

import FreeCAD as App

ROOT = Path(__file__).resolve().parents[2]


doc = runpy.run_path(str(ROOT / "HullSample.py"))["doc"]
labels = ("Keel_Line", "Port_Sheer_Line", "Starboard_Sheer_Line",
          "Port_Chine_Guide", "Starboard_Chine_Guide")
for label in labels:
    matches = doc.getObjectsByLabel(label)
    assert len(matches) == 1, (label, [obj.Name for obj in matches])
    obj = matches[0]
    assert doc.getObject(obj.Name) is obj
    print("label", label, "internal_name", obj.Name, "type", obj.TypeId)
missing = doc.getObjectsByLabel("Example_Intentionally_Missing")
print("missing_matches", len(missing))
assert not missing
