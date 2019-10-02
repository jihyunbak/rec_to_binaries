#!/usr/bin/env python3

from setuptools import find_packages, setup

INSTALL_REQUIRES = ['numpy >= 1.11', 'pandas']
TESTS_REQUIRE = ['pytest >= 2.7.1']

setup(
    name='rec_to_binaries',
    version='0.1.0.dev0',
    license='MIT',
    description=('Covert SpikeGadgets rec files to binaries'),
    author='Eric Denovellis',
    author_email='Eric.Denovellis@ucsf.edu',
    url='https://github.com/edeno/rec_to_binaries',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
)