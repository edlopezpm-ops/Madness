# (kommiBo) Optional documentation example; source-backed, bounded evidence.
"""Record a source fingerprint without claiming a geometry pass.

Uses standard-library Python; does not validate FreeCAD geometry.
See the paired engineering note for expected output and limitations.
"""

import hashlib
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
names = ("HullSample.py", "CatHullSample.py", "tests/validate_models.py")
result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, text=True,
                        capture_output=True, check=False)
manifest = {
    "head": result.stdout.strip() if result.returncode == 0 else None,
    "files": {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names},
    "evidence_kind": "source_fingerprint",
    "geometry_validation": "not_run_by_this_example",
    "working_tree_note": "HEAD does not establish worktree cleanliness",
}
assert all(len(value) == 64 for value in manifest["files"].values())
print(json.dumps(manifest, indent=2, sort_keys=True))
