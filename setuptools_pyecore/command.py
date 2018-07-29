"""Implements the setuptools command 'pyecore'."""
import shlex

import setuptools


class PyEcoreCommand(setuptools.Command):
    """A setuptools command for generating Python code from PyEcore models.

    <Long description.>

    :cvar description: Description of ecore command
    :cvar user_options: Options which can be passed by the user
    :cvar boolean_options: Subset of user options which are binary
    :cvar negative_opt: Dictionary of user options which exclude each other
    """

    description = 'generate Python code from PyEcore models'

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
        """Sets default values for all the options that this command supports.
        Note that these defaults may be overridden by other commands, by the
        setup script, by config files, or by the command-line.
        """
        self.ecore_models = None
        self.output = {}
        self.user_modules = {}
        self.auto_register_package = 0

    def finalize_options(self):
        """Sets final values for all the options that this command supports.
        This is always called as late as possible, ie. after any option
        assignments from the command-line or from other commands have been
        done.
        """
        # parse ecore-models option
        if self.ecore_models:
            self.ecore_models = shlex.split(self.ecore_models, comments=True)

        # parse output option
        if self.output:
            tokens = shlex.split(self.output, comments=True)
            self.output = dict(t.split('=', 1) for t in tokens)
        # if default directory isn't specified set base directory as default
        if 'default' not in self.output:
            self.output['default'] = '.'

        # parse user-modules option
        if self.user_modules:
            tokens = shlex.split(self.user_modules, comments=True)
            self.user_modules = dict(t.split('=', 1) for t in tokens)

    def run(self):
        """Performs all tasks necessary to generate Python packages
        representing the classes from Ecore models. This process is controlled
        by the user options passed on the command line or set internally to
        default values.
        """
        pass
