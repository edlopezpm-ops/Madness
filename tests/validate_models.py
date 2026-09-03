from __future__ import annotations

import runpy
from pathlib import Path

import FreeCAD as App


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_catamaran() -> None:
    namespace = runpy.run_path(str(ROOT / "CatHullSample.py"), run_name="__aekr_validation__")
    document = App.getDocument("Draft_Catamaran_Hull_Lines")
    require(len(document.Objects) == 44, "catamaran object count drifted")
    require(len(namespace["port_hull"]) == 15, "port hull station count drifted")
    require(len(namespace["starboard_hull"]) == 15, "starboard hull station count drifted")
    require(document.getObjectsByLabel("Catamaran_Centerline_Reference"), "centerline is missing")
    require(
        all(not obj.Shape.isNull() and obj.Shape.isValid() for obj in document.Objects),
        "catamaran contains invalid geometry",
    )


def validate_monohull() -> None:
    namespace = runpy.run_path(str(ROOT / "HullSample.py"), run_name="__aekr_validation__")
    document = App.getDocument("Draft_Hull_Only")
    require(len(document.Objects) == 18, "monohull object count drifted")
    require(len(namespace["station_curves"]) == 13, "monohull station count drifted")
    require(document.getObjectsByLabel("Keel_Line"), "keel line is missing")
    require(
        all(not obj.Shape.isNull() and obj.Shape.isValid() for obj in document.Objects),
        "monohull contains invalid geometry",
    )
    bounds = document.getObjectsByLabel("Keel_Line")[0].Shape.BoundBox
    require(abs(bounds.XLength - 12000.0) < 1.0, "monohull length drifted")


def main() -> None:
    validate_catamaran()
    validate_monohull()
    print("FreeCAD geometry validation: PASS")


if __name__ == "__main__":
    main()
