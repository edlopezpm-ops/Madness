# (kommiBo) Optional documentation example; source-backed, bounded evidence.
"""Check beam, depth, and rocker calculations together.

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

import math

for name, beam_floor, depth_floor, rocker_floor in (
    ("HullSample.py", .12, .45, .75),
    ("CatHullSample.py", .10, .40, .70),
):
    p = literals(name)
    beam = p.get("B", p.get("hull_beam"))

    def sample(t):
        fullness = 1 - (2 * t - 1) ** 2
        width = beam * (beam_floor + (1 - beam_floor) * fullness)
        depth = p["D"] * (depth_floor + (1 - depth_floor) * fullness)
        keel = -depth * (rocker_floor + (1 - rocker_floor) * (1 - abs(2 * t - 1)))
        return width, depth, keel

    print(name)
    for t in (0, .25, .5, .75, 1):
        row = sample(t)
        assert all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(row, sample(1 - t)))
        print(p["L"] * t, tuple(round(v, 3) for v in row))
