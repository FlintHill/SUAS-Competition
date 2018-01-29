# This is the setup file for pip
from setuptools import setup, find_packages
import os, sys
from os import path

setup(
    name = 'UpdatedImageProcessing',

    version = '0.0.1',

    description = 'Image processing algorithm for the SUAS Competition',

    url = 'https://github.com/FlintHill/SUAS-Competition',

    author = 'Zachary Yin',
    author_email = 'zyin@flinthill.org',

    license = 'MIT',

    classifiers = [
        'Development Status :: 3 - Alpha',

        'Programming Language :: Python :: 2.7',

        "Operating System :: OS Independent",
    ],

    packages = find_packages(),

    install_requires = ['numpy'],

    keywords = ['SUAS'],
)
