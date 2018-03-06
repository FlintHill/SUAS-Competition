# This is the setup file for pip
from setuptools import setup, find_packages
import os, sys
from os import path

setup(
    name = 'VectorFieldSDASimulator',

    version = '0.0.1',

    description = 'New vector field SDA testing program for SUAS Competition',

    url = 'https://github.com/FlintHill/SUAS-Competition',

    author = 'Yudong Li',
    author_email = 'a1923172548@gmail.com',

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
