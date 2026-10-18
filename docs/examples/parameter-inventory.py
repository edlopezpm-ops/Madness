# (kommiBo) Optional documentation example; source-backed, bounded evidence.
"""Inventory dimensions without importing FreeCAD.

Uses standard-library Python; does not validate FreeCAD geometry.
See the paired engineering note for expected output and limitations.
"""

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def literals(relative_path):
    tree = ast.parse((ROOT / relative_path).read_text(encoding="utf-8"))
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name):
                try:
                    values[target.id] = ast.literal_eval(node.value)
                except (ValueError, TypeError):
                    pass
    return values


for name in ("HullSample.py", "CatHullSample.py"):
    values = literals(name)
    keys = ("L", "B", "hull_beam", "overall_beam", "D", "stations")
    print(name, {key: values[key] for key in keys if key in values})
    assert values["L"] > 0 and values["D"] > 0
    assert isinstance(values["stations"], int) and values["stations"] >= 2
    print("length_m", values["L"] / 1000.0)
