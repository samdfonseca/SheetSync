from setuptools import setup
from setuptools.command.test import test as TestCommand
import os
import sys


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

with open(os.path.join('sheetsync','version.py')) as fh:
    exec(fh.read())

with open('README.rst') as fh:
    long_description = fh.read()

with open('requirements.txt') as fh:
    requirements = map(str.strip, fh.readlines())

setup(
    name='sheetsync3',
    version=__version__,
    description="Synchronize rows of data with a google spreadsheet",
    long_description=long_description,
    author='Sam Fonseca',
    author_email='samfonseca@utexas.edu',
    url='https://github.com/samdfonseca/SheetSync3/',
    packages=['sheetsync'],
    platforms='any',
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        ],
)
