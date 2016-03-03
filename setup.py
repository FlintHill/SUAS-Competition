# This is the setup file for pip
from setuptools import setup, find_packages
import os
import sys
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'DESCRIPTION.rst')) as f:
    description_file = f.read()

req = open('requirements.txt')
requirements = req.readlines()
req.close()

setup(
    name = 'SUASImageParser',

    version = '0.0.1',

    description = '',
    long_description = description_file,

    url = 'https://github.com/FlintHill/SUAS-Competition',

    author = 'Vale Tolpegin',
    author_email = 'valetolpegin@gmail.com',

    license = 'MIT',

    classifiers = [
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',

        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',

        'License :: OSI Approved :: MIT License',

        "Programming Language :: Python :: 2.7",

        "Operating System :: OS Independent",
    ],

    packages = find_packages(),

    platforms=["any"],
    install_requires = requirements,

    keywords = [ 'image processing', 'suas' ],
)
