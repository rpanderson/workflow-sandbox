# workflow-sandbox

[![Build Status](https://api.cirrus-ci.com/github/rpanderson/workflow-sandbox.svg)](https://cirrus-ci.com/rpanderson/workflow-sandbox)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![License](https://img.shields.io/pypi/l/workflow-sandbox.svg)](https://github.com/rpanderson/workflow-sandbox/raw/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/workflow-sandbox.svg)](https://pypi.org/project/workflow-sandbox)
[![Python Version](https://img.shields.io/pypi/pyversions/workflow-sandbox.svg)](https://python.org)

Dummy project used to test GitHub actions and Cirrus CI for building and publishing releases of Python packages.

This will be a (dummy) Python package on test PyPI in its own right, with package name `workflow-sandbox` and module name `workflow_sandbox`.

## Practices

- This dummy project *loosely* adopts the [release flow](https://releaseflow.org) branching model/strategy. (Loosley as I'm not going to always use feature branches.)
- Versioning is introspected using the excellent [`setuptools_scm`](https://github.com/pypa/setuptools_scm), using the `release-branch-semver` [version scheme](https://github.com/pypa/setuptools_scm#version-number-construction).
- When a release candidate was identified ([a574270](https://github.com/rpanderson/workflow-sandbox/commit/a5742702fcf6530da3080ad1d4a3eabb4fd78013), C below):
  * A new branch `maintenance/0.2.x` was created, to service the minor release `0.2`.
  * The commit was tagged `v0.2.0rc1`, the first release candidate of this version.
  * Subsequent untagged commits are versioned (with local scheme `no-local-version`): 
  * On `master` as `0.3.0devN`, e.g. `0.3.0dev1` ([ee03672](https://github.com/rpanderson/workflow-sandbox/commit/ee03672fa0cdf96f4e400586a1629d0e3908a48e), E below);
  * On `maintenance/0.2.x` as `0.2.0rc2.dev1` ([6006a6f](https://github.com/rpanderson/workflow-sandbox/commit/6006a6f5ca5922d9b4f352c2a37f23008eb4d597), D below).
* In this example, the release candidate was deemed satisfactory and a dummy commit was used to create [6006a6f](https://github.com/rpanderson/workflow-sandbox/commit/6006a6f5ca5922d9b4f352c2a37f23008eb4d597) (F below) so that it could be uniquely tagged as `v0.2.0`.

In pictures, this looks like:
```
       D -- F [maintenance/0.2.x]
      /     ^ [v0.2.0]
B -- C---E [master]
     ^
[v0.2.0rc1]
```

*Update:* See #13 for a discussion of why this was necessary and a better alternative (tag C/D with both v0.2.0rc1 and v0.2.0).

Actual releases, e.g. `0.2.0` and bugfix releases `0.2.1`, `0.2.2`, etc. will be tagged on `maintenance/0.2.x` alone. This branch will contain no development, but cherry pick bug-fixes from master.

## Roadmap

### GitHub Actions

- [x] Create release using `actions/create_release`.
- [ ] Publish release on GitHub using `actions/upload-release-asset` with the `body` above extracted from the appropriate release notes based on git tags, similar to [napari/napari#1138](https://github.com/napari/napari/pull/1138).
- [x] Using `pypa/gh-action-pypi-publish`:
  - All tagged releases (including candidates) are published on PyPI and TestPyPI automatically.
  - All untagged pushes to `master` and `maintenance/*` branches are published on TestPyPI automatically with an appropriate `dev` version suffix.
- [x] Investigate triggering off creation vs branch push events (see rpanderson/workflow-sandbox#8).
- [ ] Automated documentation build and push to `gh-pages` branch.

### CirrusCI

- [x] Formatting using `black`.
- [x] Linting using `flake8`.

### Acknowledgements

Much of this is guided by the practices of other development communities, and many helpful conversations with [@chrisjbillington](https://github.com/chrisjbillington) and [@philipstarkey](https://github.com/philipstarkey).
