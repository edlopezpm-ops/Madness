# (kommiBo) Optional documentation example; source-backed, bounded evidence.
"""Calculate center spacing and the nominal inner gap.

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
assert p["hull_beam"] > 0
spacing = p["overall_beam"] - p["hull_beam"]
gap = spacing - p["hull_beam"]
assert gap >= 0, "nominal midship hulls overlap"
centers = (-spacing / 2, spacing / 2)
print("center_spacing_mm", spacing)
print("centers_y_mm", centers)
print("inner_gap_mm", gap)
print("outer_control_y_mm", (centers[0] - p["hull_beam"] / 2,
                             centers[1] + p["hull_beam"] / 2))
