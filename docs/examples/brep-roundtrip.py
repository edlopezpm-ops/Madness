# (kommiBo) Optional documentation example; source-backed, bounded evidence.
"""Round-trip a selected guide through a temporary BREP.

Requires the FreeCAD runtime; use a fresh session.
See the paired engineering note for expected output and limitations.
"""

import runpy
from pathlib import Path

import FreeCAD as App

ROOT = Path(__file__).resolve().parents[2]

from tempfile import TemporaryDirectory
import Part

doc = runpy.run_path(str(ROOT / "HullSample.py"))["doc"]
matches = doc.getObjectsByLabel("Keel_Line")
assert len(matches) == 1
source = matches[0].Shape
assert not source.isNull() and source.isValid()
with TemporaryDirectory(prefix="madness-keel-") as directory:
    path = Path(directory) / "keel.brep"
    source.exportBrep(str(path))
    restored = Part.Shape()
    restored.read(str(path))
    assert path.stat().st_size > 0
    assert not restored.isNull() and restored.isValid()
    assert abs(restored.Length - source.Length) < 1e-6
    assert abs(restored.BoundBox.XLength - source.BoundBox.XLength) < 1e-6
    print("temporary_brep_bytes", path.stat().st_size)
print("brep_roundtrip", True)
