"""Setup script for setuptools-pyecore."""
import sys

import setuptools

# need to guard script here due to reentrance while testing multiprocessing:
if __name__ == '__main__':
    needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
    pytest_runner_opt = ['pytest-runner~=4.0,<5dev'] if needs_pytest else []

    setuptools.setup(
        name='setuptools-pyecore',
        version='0.1.1',
        packages=setuptools.find_packages(),
        entry_points={
            'distutils.commands': [
                'pyecore = setuptools_pyecore.command:PyEcoreCommand'
            ]
        },
        python_requires='>=3.4',
        install_requires=['pyecore', 'pyecoregen'],
        tests_require=['pytest'],
        setup_requires=pytest_runner_opt,
        url='https://github.com/pyecore/setuptools-pyecore',
        license='BSD 3-Clause',
        author='Andreas Schmidl',
        author_email='Andreas.Schmidl@gmail.com',
        description='Setuptools command for generating Python code from '
                    'PyEcore models.',
        long_description=open('README.rst').read(),
        platforms=['any'],
        keywords='setuptools model metamodel EMF Ecore code generator',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6'
        ]
    )
