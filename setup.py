from setuptools import setup

from sheetsync.version import __version__

with open('README.rst') as fh:
    long_description = fh.read()

with open('requirements.txt') as fh:
    requirements = [line.strip() for line in fh.readlines()]

setup(
    name='SheetSync',
    version=__version__,
    description="Synchronize rows of data with a google spreadsheet",
    long_description=long_description,
    author='Mark Brenig-Jones',
    author_email='markbrenigjones@gmail.com',
    url='https://github.com/mbrenig/SheetSync/',
    packages=['sheetsync'],
    platforms='any',
    install_requires=requirements,
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        ],
)
