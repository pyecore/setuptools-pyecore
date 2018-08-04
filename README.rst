setuptools-pyecore
==================

|Build Status| |Coverage Status| |License|

.. |Build Status| image:: https://travis-ci.com/ferraith/setuptools-pyecore.svg
   :target: https://travis-ci.com/ferraith/setuptools-pyecore
   :alt: Build Status

.. |Coverage Status| image:: https://coveralls.io/repos/github/ferraith/setuptools-pyecore/badge.svg?branch=master
   :target: https://coveralls.io/github/ferraith/setuptools-pyecore?branch=master
   :alt: Coverage Status

.. |License| image:: https://img.shields.io/github/license/ferraith/setuptools-pyecore.svg
    :target: https://raw.githubusercontent.com/ferraith/setuptools-pyecore/master/LICENSE
    :alt: License

Overview
--------

A ``setuptools`` command for generating Python code from Ecore models.

Installation
------------

``setuptools-pyecore`` can be installed in various ways. To run it the following prerequisites have to be fulfilled:

- Python 3.6+
- setuptools 29.0.0+

After installation, the used Python environment has a new setuptools command called ``pyecore``.

From Source Code
****************

::

    > git clone https://github.com/ferraith/setuptools-pyecore.git
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
