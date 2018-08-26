"""Implementation of the setuptools command 'pyecore'."""
import collections
import contextlib
import logging
import pathlib
import shlex

import pyecore.resources
import pyecoregen.ecore
import setuptools


class PyEcoreCommand(setuptools.Command):
    """A setuptools command for generating Python code from Ecore models.

    An extra command for setuptools to generate static Python classes from Ecore models. The pyecore
    command wraps pyecoregen - the real Python code generator for Ecore models. It searches for
    Ecore models starting from the base directory and generates a Python package for each found
    Ecore model.

    :cvar _ECORE_FILE_EXT: File extension of Ecore XMI file
    :cvar description: Description of ecore command
    :cvar user_options: Options which can be passed by the user
    :cvar boolean_options: Subset of user options which are binary
    """

    _ECORE_FILE_EXT = 'ecore'

    description = 'generate Python code from Ecore models'

    user_options = [
        ('ecore-models=', 'e', 'specify Ecore models to generate code for'),
        ('output=', 'o', 'specify directories where output is generated'),
        ('user-modules=', None, 'dotted names of modules with user-provided mixins to import from '
                                'generated classes'),
        ('auto-register-package', None, 'Generate package auto-registration for the PyEcore '
                                        '\'global_registry\''),
    ]

    boolean_options = ['auto-register-package']

    def initialize_options(self):
        """Set default values for all the options that this command supports. Note that these
        defaults may be overridden by other commands, by the setup script, by config files, or by
        the command-line.
        """
        self.ecore_models = None
        self.output = ''
        self.user_modules = ''
        self.auto_register_package = 0

    def finalize_options(self):
        """Set final values for all the options that this command supports. This is always called
        as late as possible, ie. after any option assignments from the command-line or from other
        commands have been done.
        """
        base_path = pathlib.Path('.')

        # parse ecore-models option
        if self.ecore_models:
            self.ecore_models = shlex.split(self.ecore_models, comments=True)

        # parse output option
        tokens = shlex.split(self.output, comments=True)
        self.output = collections.defaultdict(lambda: base_path)
        for t in tokens:
            model, output = t.split('=', 1)
            output_path = pathlib.Path(output).relative_to(base_path)
            if model == 'default':
                self.output.default_factory = lambda: output_path
            else:
                self.output[model] = output_path

        # parse user-modules option
        tokens = shlex.split(self.user_modules, comments=True)
        self.user_modules = {}
        for t in tokens:
            model, user_module = t.split('=', 1)
            user_module_path = pathlib.Path(user_module).relative_to(base_path)
            self.user_modules[model] = user_module_path

    def _configure_logging(self):
        """Configure logging using global verbosity level of distutils."""
        loglevel_map = collections.defaultdict(lambda: logging.WARNING)
        loglevel_map.update({
            0: logging.WARNING,
            1: logging.INFO,
            2: logging.DEBUG
        })
        logging.basicConfig(
            format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
            level=loglevel_map[self.distribution.verbose]
        )

    def _find_ecore_xmi_files(self, base_path=pathlib.Path('.')):
        """Search for all Ecore XMI files starting from base directory and returns a list of them.

        :param base_path: base path to search for Ecore XMI files
        :return: a list of all found Ecore XMI files
        """
        pattern = '*.{}'.format(self._ECORE_FILE_EXT)
        return sorted(base_path.rglob(pattern))

    @staticmethod
    @contextlib.contextmanager
    def _load_ecore_model(ecore_model_path):
        """Load a single Ecore model from a Ecore XMI file and return the root package.

        :param ecore_model_path: path to Ecore XMI file
        :return: root package of the Ecore model
        """
        rset = pyecore.resources.ResourceSet()
        try:
            resource = rset.get_resource(ecore_model_path.as_posix())
            yield resource.contents[0]
        finally:
            rset.remove_resource(resource)

    def run(self):
        """Perform all tasks necessary to generate Python packages representing the classes from
        Ecore models. This process is controlled by the user options passed on the command line or
        set internally to default values.
        """
        self._configure_logging()

        # find Ecore XMI files
        ecore_xmi_files = self._find_ecore_xmi_files()

        # load each Ecore model
        for ecore_xmi_file in ecore_xmi_files:
            with self._load_ecore_model(ecore_xmi_file) as resource:
                # if user passed Ecore models skip models aren't in list
                if self.ecore_models and resource.name not in self.ecore_models:
                    continue

                # configure EcoreGenerator
                kwargs = {}
                if self.auto_register_package:
                    kwargs['auto_register_package'] = True
                if resource.name in self.user_modules:
                    kwargs['user_module'] = self.user_modules[resource.name].as_posix()

                #  generate Python classes
                pyecoregen.ecore.EcoreGenerator(**kwargs).generate(
                    resource,
                    self.output[resource.name].as_posix()
                )
