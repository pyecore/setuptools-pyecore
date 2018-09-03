import collections
import logging
import os
import pathlib
from unittest import mock

import pytest
import setuptools.dist

from setuptools_pyecore.command import PyEcoreCommand


class TestPyEcoreCommand:
    @pytest.fixture(autouse=True)
    def command(self):
        dist = setuptools.dist.Distribution()
        return PyEcoreCommand(dist)

    @pytest.fixture()
    def configured_command(self, tmpdir, command):
        command.ecore_models = None
        command.user_modules = {}

        default_dir = str(tmpdir.mkdir('gen'))
        command.output = collections.defaultdict(lambda: pathlib.Path(default_dir))

        return command

    @pytest.fixture()
    def empty_dir(self, request, tmpdir):
        empty_dir = str(tmpdir.mkdir('empty'))
        self.change_dir(request, empty_dir)

    @pytest.fixture()
    def standalone_dir(self, request):
        self.change_dir(request, 'resources/standalone')

    @pytest.fixture()
    def distributed_dir(self, request):
        self.change_dir(request, 'resources/distributed')

    @staticmethod
    def change_dir(request, path):
        os.chdir('.')
        init_dir = pathlib.Path.cwd()
        local_dir = os.path.dirname(__file__)
        os.chdir(os.path.join(local_dir, path))

        def fin():
            os.chdir(str(init_dir))
        request.addfinalizer(fin)

    def test__finalize_options__default(self, command):
        command.finalize_options()

        assert not command.ecore_models
        assert pathlib.Path(command.output['unknown']) == pathlib.Path('.')
        assert not command.user_modules
        assert command.auto_register_package == 0

    def test__finalize_options__ecore_models__single(self, command):
        command.ecore_models = 'library'
        command.finalize_options()

        assert 'library' in command.ecore_models

    def test__finalize_options__ecore_models__multiple(self, command):
        command.ecore_models = 'a b'
        command.finalize_options()

        assert 'a' in command.ecore_models
        assert 'b' in command.ecore_models

    def test__finalize_options__output__default_dir(self, command):
        command.output = 'default=.'
        command.finalize_options()

        assert pathlib.Path(command.output['unknown']) == pathlib.Path('.')

    def test__finalize_options__output__custom_dir(self, command):
        command.output = 'library=output/library'
        command.finalize_options()

        assert pathlib.Path(command.output['unknown']) == pathlib.Path('.')
        assert pathlib.Path(command.output['library']) == pathlib.Path('output/library')

    def test__finalize_options__output__custom_default_dir(self, command):
        command.output = 'default=output/default'
        command.finalize_options()

        assert pathlib.Path(command.output['unknown']) == pathlib.Path('output/default')

    @mock.patch('distutils.log.warn')
    def test__finalize_options__output__invalid_model(self, mock_warn, command):
        command.output = '=output/default'
        command.finalize_options()

        assert mock_warn.called

    @mock.patch('distutils.log.warn')
    def test__finalize_options__output__invalid_output(self, mock_warn, command):
        command.output = 'default='
        command.finalize_options()

        assert mock_warn.called

    def test__finalize_options__user_modules__single(self, command):
        command.user_modules = 'a=a.pkg.module'
        command.finalize_options()

        assert command.user_modules['a'] == 'a.pkg.module'

    def test__finalize_options__user_modules__multiple(self, command):
        command.user_modules = 'a=a.pkg.module b=b.pkg.module'
        command.finalize_options()

        assert command.user_modules['a'] == 'a.pkg.module'
        assert command.user_modules['b'] == 'b.pkg.module'

    @mock.patch('distutils.log.warn')
    def test__finalize_options__user_modules__invalid_model(self, mock_warn, command):
        command.user_modules = '=a.pkg.module'
        command.finalize_options()

        assert mock_warn.called

    @mock.patch('distutils.log.warn')
    def test__finalize_options__user_modules__invalid_user_module(self, mock_warn, command):
        command.user_modules = 'a='
        command.finalize_options()

        assert mock_warn.called

    test_ids_configure_logging = ['warning', 'info', 'debug', 'undefined']

    test_data_configure_logging = [
        (0, logging.WARNING),
        (1, logging.INFO),
        (2, logging.DEBUG),
        (3, logging.WARNING)
    ]

    @mock.patch('logging.basicConfig')
    @pytest.mark.parametrize('configured_verbosity, expected_log_level',
                             test_data_configure_logging, ids=test_ids_configure_logging)
    def test__configure_logging(self, mock_basic_config, command, configured_verbosity,
                                expected_log_level):
        command.distribution.verbose = configured_verbosity
        command._configure_logging()

        mock_basic_config.assert_called_once_with(format=mock.ANY,
                                                  level=expected_log_level)

    @pytest.mark.usefixtures('empty_dir')
    def test__find_ecore_xmi_files__empty(self, command):
        m = command._find_ecore_xmi_files()

        assert len(m) == 0

    @pytest.mark.usefixtures('standalone_dir')
    def test__find_ecore_xmi_files__single(self, command):
        m = command._find_ecore_xmi_files()

        assert len(m) == 1
        assert m[0] == pathlib.Path('A.ecore')

    @pytest.mark.usefixtures('distributed_dir')
    def test__find_ecore_xmi_files__multiple(self, command):
        m = command._find_ecore_xmi_files()

        assert len(m) == 3
        assert m[0] == pathlib.Path('A.ecore')
        assert m[1] == pathlib.Path('B.ecore')
        assert m[2] == pathlib.Path('C.ecore')

    @mock.patch('pyecore.resources.ResourceSet.get_resource')
    @mock.patch('pyecore.resources.ResourceSet.remove_resource')
    def test__load_ecore_model__successful(self, mock_remove_resource, mock_get_resource, command):
        mock_resource = mock.MagicMock()
        mock_get_resource.return_value = mock_resource
        with command._load_ecore_model(pathlib.Path('standalone/A.ecore')):
            pass

        mock_get_resource.assert_called_once_with('standalone/A.ecore')
        mock_remove_resource.assert_called_once_with(mock_resource)

    @mock.patch('pyecore.resources.ResourceSet.get_resource')
    @mock.patch('pyecore.resources.ResourceSet.remove_resource')
    def test__load_ecore_model__failed(self, mock_remove_resource, mock_get_resource, command):
        mock_get_resource.side_effect = FileNotFoundError()
        with pytest.raises(FileNotFoundError):
            with command._load_ecore_model(pathlib.Path('standalone/A.ecore')):
                pass

        mock_get_resource.assert_called_once_with('standalone/A.ecore')
        assert not mock_remove_resource.called

    @pytest.mark.usefixtures('empty_dir')
    @pytest.mark.usefixtures('configured_command')
    @mock.patch.object(PyEcoreCommand, '_configure_logging')
    def test__run__configure_logging(self, mock_configure_logging, command):
        command.run()

        assert mock_configure_logging.called

    @pytest.mark.usefixtures('empty_dir')
    @pytest.mark.usefixtures('configured_command')
    @mock.patch.object(PyEcoreCommand, '_find_ecore_xmi_files')
    def test__run__find_ecore_xmi_files(self, mock_find_ecore_xmi_files, command):
        command.run()

        assert mock_find_ecore_xmi_files.called

    @pytest.mark.usefixtures('empty_dir')
    @pytest.mark.usefixtures('configured_command')
    @mock.patch('pyecoregen.ecore.EcoreGenerator.generate')
    def test__run__no_model_found(self, mock_generate, command):
        command.run()

        assert mock_generate.call_count == 0

    @pytest.mark.usefixtures('standalone_dir')
    @pytest.mark.usefixtures('configured_command')
    @mock.patch('pyecoregen.ecore.EcoreGenerator.generate')
    def test__run__single_model_found(self, mock_generate, command):
        command.output.default_factory = lambda: pathlib.Path('output/default')
        command.run()

        args, _ = mock_generate.call_args
        assert mock_generate.call_count == 1
        assert args[0].name == 'a'
        assert args[1] == 'output/default'

    @pytest.mark.usefixtures('distributed_dir')
    @pytest.mark.usefixtures('configured_command')
    @mock.patch('pyecoregen.ecore.EcoreGenerator.generate')
    def test__run__multiple_models_found(self, mock_generate, command):
        command.output.default_factory = lambda: pathlib.Path('output/default')
        command.run()

        assert mock_generate.call_count == 3
        args, _ = mock_generate.call_args_list[0]
        assert args[0].name == 'a'
        assert args[1] == 'output/default'
        args, _ = mock_generate.call_args_list[1]
        assert args[0].name == 'b'
        assert args[1] == 'output/default'
        args, _ = mock_generate.call_args_list[2]
        assert args[0].name == 'c'
        assert args[1] == 'output/default'

    @pytest.mark.usefixtures('distributed_dir')
    @pytest.mark.usefixtures('configured_command')
    @mock.patch('pyecoregen.ecore.EcoreGenerator.generate')
    def test__run__ecore_models_defined(self, mock_generate, command):
        command.ecore_models = ['a']
        command.run()

        assert mock_generate.call_count == 1

    @pytest.mark.usefixtures('distributed_dir')
    @pytest.mark.usefixtures('configured_command')
    @mock.patch('pyecoregen.ecore.EcoreGenerator.generate')
    def test__run__ecore_models__not_defined(self, mock_generate, command):
        command.ecore_models = None
        command.run()

        assert mock_generate.call_count == 3

    @pytest.mark.usefixtures('standalone_dir')
    @pytest.mark.usefixtures('configured_command')
    @mock.patch('pyecoregen.ecore.EcoreGenerator')
    def test__run__auto_register_package_defined(self, mock_ecore_generator, command):
        command.auto_register_package = True
        command.run()

        _, kwargs = mock_ecore_generator.call_args
        assert kwargs['auto_register_package'] is True

    @pytest.mark.usefixtures('standalone_dir')
    @pytest.mark.usefixtures('configured_command')
    @mock.patch('pyecoregen.ecore.EcoreGenerator')
    def test__run__auto_register_package_not_defined(self, mock_ecore_generator, command):
        command.run()

        _, kwargs = mock_ecore_generator.call_args
        assert 'auto_register_package' not in kwargs

    @pytest.mark.usefixtures('standalone_dir')
    @pytest.mark.usefixtures('configured_command')
    @mock.patch('pyecoregen.ecore.EcoreGenerator')
    def test__run__user_modules_defined(self, mock_ecore_generator, command):
        command.user_modules['a'] = 'a.pkg.module'
        command.run()

        _, kwargs = mock_ecore_generator.call_args
        assert kwargs['user_module'] == 'a.pkg.module'

    @pytest.mark.usefixtures('standalone_dir')
    @pytest.mark.usefixtures('configured_command')
    @mock.patch('pyecoregen.ecore.EcoreGenerator')
    def test__run__user_modules_not_defined(self, mock_ecore_generator, command):
        command.run()

        _, kwargs = mock_ecore_generator.call_args
        assert 'user_module' not in kwargs
