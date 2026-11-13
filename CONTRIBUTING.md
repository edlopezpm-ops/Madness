<!-- (kommiBo) Project-specific contribution and reproduction guidance. -->

# Contributing to Madness

Start with the [README](README.md), [use boundaries](TERMS.md) and
[licensing inventory](docs/licensing.md). The root [license scope](LICENSE) identifies
the files available under the standard [MIT License](LICENSES/MIT.txt). This guide
does not expand that scope, add conditions to MIT, or create a contributor agreement
or promise of support. Submit only material you are entitled to share. For restricted
material or an unclear permission, contact [aekr@aekr.io](mailto:aekr@aekr.io) before
sharing it. Use [SECURITY.md](SECURITY.md) for a private vulnerability report.

## Reproduce a CAD change

Use FreeCAD 1.1.3 and run from the repository root in a disposable session:

```sh
freecadcmd --safe-mode --console "import runpy; runpy.run_path('tests/validate_models.py', run_name='__main__')"
```

The [validator](tests/validate_models.py) runs both hull generators and checks object
counts, station counts, named geometry, shape validity and the monohull length.
The [CI workflow](.github/workflows/python-app.yml) verifies the pinned Linux AppImage
before executing the same validator. Standard Python cannot substitute for FreeCAD's
modules. Record an unavailable runtime as untested, not as a passing geometry check.

For a geometry report, include the script, parameter change, FreeCAD version, OS,
fresh-session steps, failing assertion or traceback, and expected versus actual shape.
Use screenshots to supplement the reproducible parameters, not replace them.
Geometry checks establish no vessel safety, buoyancy or fabrication approval.

## Keep Weekly Leverage changes separate

The planning toolkit has its own [source and operation notes](projects/weekly-leverage/README.md).
From its directory, run both existing suites:

```sh
cd projects/weekly-leverage
node --test tests/*.test.mjs
python3 -B -m unittest discover -s tests -p 'test_*.py'
```

For a browser issue, include language, viewport, browser, reproduction steps and whether
storage was blocked. Use fictional planning inputs. Keep translated prompt text, JSON,
starter files and permission statements aligned. Report test results separately from
hosted behavior: CAD CI alone does not validate this subproject, and a source PR is not
a deployment authorization.

## Submit a bounded pull request

Describe the concrete problem, affected files, resulting behavior and validation
actually performed, including failures or missing runtime checks. Separate unrelated
changes. For documentation-only edits, check relative links, commands and claims
against the repository; do not claim runtime evidence from prose checks.

Do not include credentials, personal records or generated temporary artifacts.
Preserve copyright and dependency notices, and explain any proposed permission change
explicitly. Keep review and acceptance separate from implementation. A reviewed merge
is not proof of deployment or real-world suitability. Recover a bad merged change
through a reviewed revert rather than rewriting shared history.
