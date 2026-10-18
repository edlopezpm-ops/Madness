# (kommiBo) Optional documentation example; source-backed, bounded evidence.
"""Print a reproducible station schedule.

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
    p = literals(name)
    count = p["stations"]
    assert count >= 2
    positions = [p["L"] * i / (count - 1) for i in range(count)]
    assert positions[0] == 0 and positions[-1] == p["L"]
    assert all(a < b for a, b in zip(positions, positions[1:]))
    print(name)
    for i, x in enumerate(positions):
        print(f"{i:02d} t={i / (count - 1):.6f} x_mm={x:.3f}")
