# (kommiBo) Optional documentation example; source-backed, bounded evidence.
"""Save and reopen a generated document in temporary custody.

Requires the FreeCAD runtime; use a fresh session.
See the paired engineering note for expected output and limitations.
"""

import runpy
from pathlib import Path

import FreeCAD as App

ROOT = Path(__file__).resolve().parents[2]

from tempfile import TemporaryDirectory

doc = runpy.run_path(str(ROOT / "CatHullSample.py"))["doc"]
expected = sorted((obj.Name, obj.Label) for obj in doc.Objects)
with TemporaryDirectory(prefix="madness-document-") as directory:
    path = Path(directory) / "catamaran-example.FCStd"
    doc.saveAs(str(path))
    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(path))
    try:
        reopened.recompute()
        assert sorted((obj.Name, obj.Label) for obj in reopened.Objects) == expected
        assert len(reopened.Objects) == 44
        assert all(not obj.Shape.isNull() and obj.Shape.isValid() for obj in reopened.Objects)
        print("roundtrip_objects", len(reopened.Objects))
    finally:
        App.closeDocument(reopened.Name)
print("fcstd_roundtrip", True)
