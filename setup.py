import os
from setuptools import setup

VERSION_SCHEME = {}
VERSION_SCHEME["version_scheme"] = os.environ.get(
    "SCM_VERSION_SCHEME", "guess-next-dev"
)
VERSION_SCHEME["local_scheme"] = os.environ.get("SCM_LOCAL_SCHEME", "node-and-date")

setup(use_scm_version=VERSION_SCHEME)
