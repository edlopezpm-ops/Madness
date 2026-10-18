# (kommiBo) Optional documentation example; source-backed, bounded evidence.
"""Locate bridge references and check index validity.

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


p = literals("CatHullSample.py")
indexes = p["bridge_station_indexes"]
assert len(indexes) == len(set(indexes)), "duplicate bridge indices"
assert all(type(i) is int and 0 <= i < p["stations"] for i in indexes)
spacing = p["overall_beam"] - p["hull_beam"]
for i in indexes:
    x = p["L"] * i / (p["stations"] - 1)
    start = (x, -spacing / 2, p["deck_z"])
    end = (x, spacing / 2, p["deck_z"])
    print(f"Bridge_Deck_Guide_{i:02d}", start, end, "span_mm", spacing)
