# Get the version at runtime from PEP-0566 metadata using `importlib.metadata`
# from the standard library or the `importlib_metadata` backport

try:
    # Standard library in Python 3.8+
    import importlib.metadata as importlib_metadata
except ImportError:
    # The backport of the Python 3.8 stdlib module
    import importlib_metadata

try:
    __version__ = importlib_metadata.version(__name__)
except importlib_metadata.PackageNotFoundError:
    # package is not installed
    pass
