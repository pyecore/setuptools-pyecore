"""Setup script for setuptools-pyecore."""
import sys

import setuptools

# need to guard script here due to reentrance while testing multiprocessing:
if __name__ == '__main__':
    setuptools.setup(
        name='setuptools-pyecore',
        version='0.0.1',
        packages=setuptools.find_packages(),
        entry_points={
            'distutils.commands': [
                'pyecore = setuptools_pyecore.command:PyEcoreCommand'
            ]
        },
        python_requires='>=3.3',
        tests_require=['pytest'],
        setup_requires=['pyecoregen'],
        url='https://github.com/ferraith/setuptools-pyecore',
        license='BSD 3-Clause',
        author='Andreas Schmidl',
        author_email='Andreas.Schmidl@gmail.com',
        description='Setuptools command for generating Python code from '
                    'PyEcore models.',
        long_description=open('README.rst').read(),
        platforms=['any'],
        keywords='setuptools model metamodel EMF Ecore code generator',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6'
        ]
    )
