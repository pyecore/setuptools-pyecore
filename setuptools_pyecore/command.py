"""Implements the setuptools command 'pyecore'."""
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

    user_options = []

    boolean_options = []

    negative_opt = {}

    def initialize_options(self):
        """Sets default values for all the options that this command supports.
        Note that these defaults may be overridden by other commands, by the
        setup script, by config files, or by the command-line.
        """
        pass

    def finalize_options(self):
        """Sets final values for all the options that this command supports.
        This is always called as late as possible, ie. after any option
        assignments from the command-line or from other commands have been
        done.
        """
        pass

    def run(self):
        """Performs all tasks necessary to generate Python packages
        representing the classes from Ecore models. This process is controlled
        by the user options passed on the command line or set internally to
        default values.
        """
        pass
