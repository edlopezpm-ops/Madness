# (kommiBo) Optional documentation example; source-backed, bounded evidence.
"""Exercise the presentation guard without a GUI.

Uses standard-library Python; does not validate FreeCAD geometry.
See the paired engineering note for expected output and limitations.
"""

import ast
from pathlib import Path
from types import SimpleNamespace

root = Path(__file__).resolve().parents[2]
tree = ast.parse((root / "HullSample.py").read_text(encoding="utf-8"))
style_node = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "style")
module = ast.Module(body=[style_node], type_ignores=[])
namespace = {"Gui": None}
exec(compile(module, "HullSample.py:style", "exec"), namespace)
plain = object()
assert namespace["style"](plain) is plain
print("headless_return_same_object", True)
namespace["Gui"] = object()
visual = SimpleNamespace(ViewObject=SimpleNamespace())
assert namespace["style"](visual, (1.0, 0.0, 0.0), 4) is visual
assert visual.ViewObject.LineColor == (1.0, 0.0, 0.0)
assert visual.ViewObject.LineWidth == 4
print("synthetic_color", visual.ViewObject.LineColor, "width", visual.ViewObject.LineWidth)
