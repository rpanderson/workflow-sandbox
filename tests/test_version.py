from pkg_resources import get_distribution
import workflow_sandbox


def test_version():
    """Check version against `pkg_resources` from `setuptools`.
    """
    assert workflow_sandbox.__version__ == get_distribution('workflow_sandbox').version
