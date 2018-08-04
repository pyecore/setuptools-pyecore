import pathlib

import pytest
import setuptools.dist

from setuptools_pyecore.command import PyEcoreCommand


class TestPyEcoreCommand:
    @pytest.fixture(autouse=True)
    def command(self):
        dist = setuptools.dist.Distribution()
        return PyEcoreCommand(dist)

    def test_finalize_options_default(self, command):
        command.finalize_options()

        assert command.ecore_models is None
        assert pathlib.Path(command.output['default']) == pathlib.Path('.')
        assert not command.user_modules
        assert command.auto_register_package == 0

    def test_finalize_options_ecore_models_single(self, command):
        command.ecore_models = 'library'
        command.finalize_options()

        assert 'library' in command.ecore_models

    def test_finalize_options_ecore_models_multiple(self, command):
        command.ecore_models = 'a b'
        command.finalize_options()

        assert 'a' in command.ecore_models
        assert 'b' in command.ecore_models

    def test_finalize_options_default_output_dir(self, command):
        command.output = 'default=.'
        command.finalize_options()

        assert pathlib.Path(command.output['default']) == pathlib.Path('.')

    def test_finalize_options_custom_output_dir(self, command):
        command.output = 'library=output/library'
        command.finalize_options()

        assert pathlib.Path(command.output['default']) == pathlib.Path('.')
        assert pathlib.Path(command.output['library']) == pathlib.Path('output/library')

    def test_finalize_options_custom_default_output_dir(self, command):
        command.output = 'default=output/default'
        command.finalize_options()

        assert pathlib.Path(command.output['default']) == pathlib.Path('output/default')

    def test_finalize_options_user_modules_single(self, command):
        command.user_modules = 'a=input/a.pkg.module'
        command.finalize_options()

        assert pathlib.Path(command.user_modules['a']) == pathlib.Path('input/a.pkg.module')

    def test_finalize_options_user_modules_multiple(self, command):
        command.user_modules = 'a=input/a.pkg.module b=input/b.pkg.module'
        command.finalize_options()

        assert pathlib.Path(command.user_modules['a']) == pathlib.Path('input/a.pkg.module')
        assert pathlib.Path(command.user_modules['b']) == pathlib.Path('input/b.pkg.module')
