import pytest
import setuptools.dist

from setuptools_pyecore.command import PyEcoreCommand


class TestPyEcoreCommand:
    @pytest.fixture(autouse=True)
    def command(self):
        dist = setuptools.dist.Distribution()
        return PyEcoreCommand(dist)

    def test_dummy(self):
        assert True
