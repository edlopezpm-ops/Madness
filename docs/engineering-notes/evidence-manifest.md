<!-- (kommiBo) Source-reviewed engineering note; optional diagnostic. -->
# Record a source fingerprint without claiming a geometry pass

A useful validation note identifies exactly which source and validator it refers
to. This standard-library example prints a JSON manifest containing the checkout
HEAD and SHA-256 digests of both generators and the validator. It labels its own
evidence as source inspection, with runtime validation explicitly not executed.

| Field | Purpose |
| --- | --- |
| `head` | commit identity, when a Git checkout is available |
| `files` | byte-level source and validator fingerprints |
| `geometry_validation` | explicit `not_run_by_this_example` boundary |
| `working_tree_note` | HEAD alone does not prove a clean checkout |

Expected output is one parseable JSON object with three 64-character hex digests.
The command does not modify the checkout or install FreeCAD. A digest changes if
the file bytes change, including encoding or line endings; that is intentional
provenance, not evidence of a geometric regression.

To accompany a real geometry run, retain this manifest and the command exit status,
FreeCAD version, complete validator output, and worktree status from that same
run. The baseline command is documented in the existing validation guide. Do not
replace a failed or unavailable FreeCAD run with this successful manifest output:
source identity, syntax validity, geometry validity, and engineering suitability
answer different questions.

## Run the complete example

Run from the repository root with Python 3. The example reads local source only.

```shell
python docs/examples/evidence-manifest.py
```

[Complete example](../examples/evidence-manifest.py). The script is intended to be run as supplied.

## Source anchors

- [`tests/validate_models.py`: `main`](../../tests/validate_models.py#L44).
- [`HullSample.py`: `L`](../../HullSample.py#L49).
- [`CatHullSample.py`: `L`](../../CatHullSample.py#L19).
