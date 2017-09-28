# This is the setup file for pip
from setuptools import setup, find_packages
import os, sys
from os import path

setup(
    name = 'SyntheticDataset2',

    version = '0.0.1',

    description = 'The updated Synthetic Dataset for the SUAS Competition',

    url = 'https://github.com/FlintHill/SUAS-Competition',

    author = 'John Moxley & Zachary Yin',
    author_email = 'vtolpegin@flinthill.org',

    license = 'MIT',

    classifiers = [
        'Development Status :: 3 - Alpha',

        'Programming Language :: Python :: 2.7',

        "Operating System :: OS Independent",
    ],

    packages = find_packages(),

    install_requires = ['numpy', 'pillow'],

    keywords = ['SUAS'],
)
