from setuptools import setup
from pathlib import Path

if Path("no-local-version").exists():
    VERSION_SCHEME = {"local_scheme": "no-local-version"}
else:
    VERSION_SCHEME = True

setup(use_scm_version=VERSION_SCHEME)
