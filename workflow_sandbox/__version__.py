import os
from pathlib import Path

try:
    # Standard library in Python 3.8+
    import importlib.metadata as importlib_metadata
except ImportError:
    # The backport of the Python 3.8 stdlib module
    import importlib_metadata

root = Path(__file__).parent.parent
if (root / '.git').is_dir():
    # Use setuptools_scm when in a git repository
    from setuptools_scm import get_version

    __version__ = get_version(
        root,
        version_scheme="release-branch-semver",
        local_scheme=os.getenv("SCM_LOCAL_SCHEME", "node-and-date"),
    )
else:
    # Get the version at runtime from PEP-0566 metadata using `importlib.metadata`
    # from the standard library or the `importlib_metadata` backport
    try:
        __version__ = importlib_metadata.version(__package__)
    except importlib_metadata.PackageNotFoundError:
        __version__ = None
