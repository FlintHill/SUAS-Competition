# This is the setup file for pip
from setuptools import setup, find_packages
import os, sys
from os import path

setup(
    name = 'ImgProcessingCLI',

    version = '0.0.1',

    description = 'Image Processing for SUAS Competition',

    url = 'https://github.com/FlintHill/SUAS-Competition',

    author = 'Peter Husisian',
    author_email = 'phusisian@flinthill.org',

    license = 'MIT',

    classifiers = [
        'Development Status :: 3 - Alpha',

        'Programming Language :: Python :: 2.7',

        "Operating System :: OS Independent",
    ],

    packages = find_packages(),

    install_requires = [],

    keywords = ['SUAS'],
)
