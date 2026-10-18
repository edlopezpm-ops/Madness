# (kommiBo) Optional documentation example; source-backed, bounded evidence.
"""Track documents created by repeated generator runs.

Requires the FreeCAD runtime; use a fresh session.
See the paired engineering note for expected output and limitations.
"""

import runpy
from pathlib import Path

import FreeCAD as App

ROOT = Path(__file__).resolve().parents[2]


before = set(App.listDocuments())
first = runpy.run_path(str(ROOT / "HullSample.py"))["doc"]
after_first = set(App.listDocuments())
second = runpy.run_path(str(ROOT / "HullSample.py"))["doc"]
after_second = set(App.listDocuments())
assert first.Name != second.Name
assert len(first.Objects) == len(second.Objects) == 18
assert after_first - before == {first.Name}
assert after_second - after_first == {second.Name}
print("first_document", first.Name, "objects", len(first.Objects))
print("second_document", second.Name, "objects", len(second.Objects))
print("added_first", sorted(after_first - before))
print("added_second", sorted(after_second - after_first))
