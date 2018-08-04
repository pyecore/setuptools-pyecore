"""Setup script for library example."""

if __name__ == '__main__':
    from setuptools import setup, find_packages

    setup(
        name='library',
        version='0.0.1',
        description='Example of use of PyEcore code generator',
        author='Andreas Schmidl',
        author_email='Andreas.Schmidl@gmail.com',
        packages=find_packages(),
        setup_requires=['setuptools-pyecore'],
        install_requires=['pyecore']
    )
