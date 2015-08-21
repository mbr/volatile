#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='temp',
    version='0.1.dev1',
    description='A small extension for the tempfile module.',
    long_description=read('README.rst'),
    author='Marc Brinkmann',
    author_email='git@marcbrinkmann.de',
    url='https://github.com/mbr/temp',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    modules=['temp.py'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ])