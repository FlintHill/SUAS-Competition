# -*- coding: utf-8 -*-
#
# Copyright 2016 Vale Tolpegin
# Distributed under the terms of the MIT License.

# -- Modules ------------------------------------------------------------------

from optparse import OptionParser


# -- global options -----------------------------------------------------------

global __Options__


# -- getOption ===-------------------------------------------------------------

def getOption(string):
	"""
	Fetches an option by name
	"""

	return getattr(__Options__, string)


# -- parseOptions -------------------------------------------------------------

def parseOptions():
	"""
	Completes command line argument parsing
	"""
	parser = OptionParser(usage='usage: %prog [options]', version='0.0.1')
	parser.add_option('-i', '--image', dest='image', help="relative path to image")

	global __Options__

	(__Options__, args) = parser.parse_args()

	return (__Options__, args)
