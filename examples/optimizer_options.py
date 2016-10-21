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
	parser.add_option('-o', '--output_file', dest='output_file', help="relative path to output file")
	parser.add_option('-d', '--image_directory', dest='img_directory', help="relative path to image directory")
	parser.add_option('-m', '--mode', dest="mode", help="task to optimize")

	global __Options__

	(__Options__, args) = parser.parse_args()

	return (__Options__, args)
