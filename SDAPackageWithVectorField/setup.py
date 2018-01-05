# This is the setup file for pip
from setuptools import setup, find_packages
import os, sys
from os import path

setup(
    name = 'SDAWtihVectorField',

    version = '0.0.2',

    description = 'Object detection and Avoidance for SUAS Competition',

    url = 'https://github.com/FlintHill/SUAS-Competition',

    author = 'Vale Tolpegin',
    author_email = 'vtolpegin@flinthill.org',

    license = 'MIT',

    classifiers = [
        'Development Status :: 1 - experiment',

        'Programming Language :: Python :: 2.7',

        "Operating System :: OS Independent",
    ],

    packages = find_packages(),

    install_requires = ['numpy', 'matplotlib'],

    keywords = ['SUAS'],
)
