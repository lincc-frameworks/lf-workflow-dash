import lf_workflow_dash


def test_version():
    """Check to see that we can get the package version"""
    assert lf_workflow_dash.__version__ is not None
