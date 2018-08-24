import logging
import os
import pathlib
import unittest.mock

import pytest
import setuptools.dist

from setuptools_pyecore.command import PyEcoreCommand


@pytest.fixture(scope='module', autouse=True)
def ch_resources_dir(request):
    os.chdir('.')
    init_dir = pathlib.Path.cwd()
    local_dir = os.path.dirname(__file__)
    os.chdir(os.path.join(local_dir, 'resources'))

    def fin():
        os.chdir(str(init_dir))
    request.addfinalizer(fin)


class TestPyEcoreCommand:
    @pytest.fixture(autouse=True)
    def command(self):
        dist = setuptools.dist.Distribution()
        return PyEcoreCommand(dist)

    def test_finalize_options_default(self, command):
        command.finalize_options()

        assert not command.ecore_models
        assert pathlib.Path(command.output['unknown']) == pathlib.Path('.')
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

        assert pathlib.Path(command.output['unknown']) == pathlib.Path('.')

    def test_finalize_options_custom_output_dir(self, command):
        command.output = 'library=output/library'
        command.finalize_options()

        assert pathlib.Path(command.output['unknown']) == pathlib.Path('.')
        assert pathlib.Path(command.output['library']) == pathlib.Path('output/library')

    def test_finalize_options_custom_default_output_dir(self, command):
        command.output = 'default=output/default'
        command.finalize_options()

        assert pathlib.Path(command.output['unknown']) == pathlib.Path('output/default')

    def test_finalize_options_user_modules_single(self, command):
        command.user_modules = 'a=input/a.pkg.module'
        command.finalize_options()

        assert pathlib.Path(command.user_modules['a']) == pathlib.Path('input/a.pkg.module')

    def test_finalize_options_user_modules_multiple(self, command):
        command.user_modules = 'a=input/a.pkg.module b=input/b.pkg.module'
        command.finalize_options()

        assert pathlib.Path(command.user_modules['a']) == pathlib.Path('input/a.pkg.module')
        assert pathlib.Path(command.user_modules['b']) == pathlib.Path('input/b.pkg.module')

    test_ids_configure_logging = ['warning', 'info', 'debug', 'undefined']

    test_data_configure_logging = [
        (0, logging.WARNING),
        (1, logging.INFO),
        (2, logging.DEBUG),
        (3, logging.WARNING)
    ]

    @unittest.mock.patch('logging.basicConfig')
    @pytest.mark.parametrize('configured_verbosity, expected_log_level',
                             test_data_configure_logging, ids=test_ids_configure_logging)
    def test_configure_logging(self, mock_basic_config, command, configured_verbosity,
                               expected_log_level):
        command.distribution.verbose = configured_verbosity
        command._configure_logging()

        mock_basic_config.assert_called_once_with(format=unittest.mock.ANY,
                                                  level=expected_log_level)

    def test_find_ecore_xmi_files_empty(self, tmpdir, command):
        model_dir = tmpdir.mkdir('model')
        m = command._find_ecore_xmi_files(pathlib.Path(str(model_dir)))

        assert len(m) == 0

    def test_find_ecore_xmi_files_standalone(self, command):
        base_path = pathlib.Path('standalone')
        m = command._find_ecore_xmi_files(base_path)

        assert len(m) == 1
        assert m[0] == base_path / 'A.ecore'

    def test_find_ecore_xmi_files_distributed(self, command):
        base_path = pathlib.Path('distributed')
        m = command._find_ecore_xmi_files(base_path)

        assert len(m) == 3

        assert m[0] == base_path / 'A.ecore'
        assert m[1] == base_path / 'B.ecore'
        assert m[2] == base_path / 'C.ecore'
