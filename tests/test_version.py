"""Unit tests for __version__.py."""

import bgkl_euxfel


def test_package_version():
    """Ensure the package version is defined and not set to the initial
    placeholder."""
    assert hasattr(bgkl_euxfel, "__version__")
    assert bgkl_euxfel.__version__ != "0.0.0"
