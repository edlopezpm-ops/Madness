# (kommiBo) Optional documentation example; source-backed, bounded evidence.
"""Map Python collections to the document tree.

Requires the FreeCAD runtime; use a fresh session.
See the paired engineering note for expected output and limitations.
"""

import runpy
from pathlib import Path

import FreeCAD as App

ROOT = Path(__file__).resolve().parents[2]


for filename, expected in (("HullSample.py", 18), ("CatHullSample.py", 44)):
    ns = runpy.run_path(str(ROOT / filename))
    doc = ns["doc"]
    print(filename, doc.Name)
    for obj in doc.Objects:
        print(obj.Name, obj.Label, obj.TypeId)
    assert len(doc.Objects) == expected
    print("document_objects", len(doc.Objects))
    if "port_hull" in ns:
        assert len(ns["port_hull"]) == len(ns["starboard_hull"]) == 15
