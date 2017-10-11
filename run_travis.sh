#!/usr/bin/env bash

sh ./install_external.sh

nosetests --with-coverage tests/unit_tests
