setuptools-pyecore
==================

|Build Status| |Coverage Status| |PyPI Version| |GitHub Version| |License|

.. |Build Status| image:: https://travis-ci.org/pyecore/setuptools-pyecore.svg
   :target: https://travis-ci.org/pyecore/setuptools-pyecore
   :alt: Build Status

.. |Coverage Status| image:: https://coveralls.io/repos/github/pyecore/setuptools-pyecore/badge.svg?branch=master
   :target: https://coveralls.io/github/pyecore/setuptools-pyecore?branch=master
   :alt: Coverage Status

.. |PyPI Version| image:: https://badge.fury.io/py/setuptools-pyecore.svg
   :target: https://pypi.org/project/setuptools-pyecore
   :alt: PyPI Version

.. |GitHub Version| image:: https://badge.fury.io/gh/pyecore%2Fsetuptools-pyecore.svg
   :target: https://github.com/pyecore/setuptools-pyecore/releases
   :alt: GitHub Version

.. |License| image:: https://img.shields.io/github/license/pyecore/setuptools-pyecore.svg
    :target: https://raw.githubusercontent.com/pyecore/setuptools-pyecore/master/LICENSE
    :alt: License

Overview
--------

A ``setuptools`` command for generating Python code from Ecore models.

Installation
------------

``setuptools-pyecore`` can be installed in various ways. To run it the following prerequisites have to be fulfilled:

- Python 3.4+
- setuptools 29.0.0+

After installation, the used Python environment has a new setuptools command called ``pyecore``.

From Source Code
****************

::

    > git clone https://github.com/pyecore/setuptools-pyecore.git
    > cd setuptools-pyecore
    > pip install .

From PyPI
*********

::

    > pip install setuptools-pyecore

From GitHub Releases
********************

::

    > pip install <setuptools-pyecore_wheel>

Usage
-----

Integration
***********

For a smooth user experience it's recommended to pass ``setuptools-pyecore`` using the ``setup_requires`` argument of setup function. Additionally the generated Python code depends on the ``pyecore`` library which should be added to ``install_requires`` argument:

.. code:: python

    setup(
        ...
        setup_requires=['setuptools-pyecore'],
        install_requires=['pyecore']
        ...
    )

Before generating Python code from a given Ecore model ``setuptools`` will automatically check the Python environment and download ``setuptools-pyecore`` from `PyPI <https://pypi.org>`__ if it's missing. During the installation of the project package ``pip`` will install ``pyecore`` into the Python environment.

Configuration
*************

``setuptools-pyecore`` provides two possibilities to configure the pyecore generator.

All options can be passed on the command line after the ``pyecore`` command:

::

    > python setup.py pyecore --auto-register-package

It's also possible to pass several options to ``pyecoregen`` or execute multiple commands at once:

::

    > python setup.py pyecore --auto-register-package --output "default=gen" bdist_wheel

See ``python setup.py pyecore --help`` for available command line options:

::

    > python setup.py pyecore --help
    ...
    Options for 'PyEcoreCommand' command:
      --ecore-models (-e)      specify Ecore models to generate code for
      --output (-o)            specify directories where output is generated
      --user-modules           dotted names of modules with user-provided mixins
                               to import from generated classes
      --auto-register-package  Generate package auto-registration for the PyEcore
                               'global_registry'
    ...

The ``pyecoregen`` documentation explains all `command line options <https://github.com/pyecore/pyecoregen/blob/master/README.rst>`__ in detail.

Apart from passing options on the command line it's also possible to add a dedicated ``[pyecore]`` section to ``setup.cfg``. The following example section contains all available options:

.. code:: ini

    [pyecore]
    # Specify Ecore models to generate code for; default: None
    #ecore-models = <ecore-model> [<ecore-model> ...]
    # Specify directories where output is generated; default: ./
    output = default=gen
    # Dotted names of modules with user-provided mixins to import from generated classes; default: None
    #user-modules = [<model>=<user module>]
    #               [<model>=<user module> ...]
    # Generate package auto-registration for the PyEcore 'global_registry' (yes|no); default: no
    auto-register-package = yes

A reference configuration is provided in the ``resources`` directory.

``pyecoregen`` inherits the log level globally configured for ``setuptools``. To set the verbosity to a certain log level pass the global options ``verbose`` or ``quiet`` straight before the ``pyecore`` command on the command line:

::

    > python setup.py --verbose pyecore

Alternatively, you can add these options to the ``[global]`` section of your ``setup.cfg``:

.. code:: ini

    [global]
    # Run verbosely (yes|no); default: yes
    #verbose = yes
    # Run quietly and turns verbosity off (yes|no); default: no
    quiet = yes

Sample
******

Besides the ``setuptools-pyecore`` source code a sample project called ``library`` is provided in the ``samples`` directory. This sample consists of the Ecore model ``library`` and a setup script. During the execution of ``setuptools-pyecore`` a Python package will be generated into the ``library`` package directory representing the classes from the ``library`` Ecore model.

To generate code out of the Ecore model and build a ``library`` wheel package execute the following command:

::

    > python setup.py pyecore bdist_wheel
