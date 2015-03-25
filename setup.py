#!/usr/bin/env python

from setuptools import setup, find_packages


requires = ['boto']

setup_options = dict(
    name='canary',
    version='0.01',
    description='Universal Command Line Environment for AWS.',
    author='Nate McCourtney',
    author_email='nathan@luminal.io',
    scripts=['bin/canary'],
    packages=find_packages('.', exclude=['tests*']),
    package_dir={'': 'lib'},
    package_data={'': ['conf/*.json']},
    install_requires=requires,
    )

setup(**setup_options)