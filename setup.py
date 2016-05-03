# -*- coding: utf-8 -*-
#
# This file is part of Inspire-Magpie.
# Copyright (c) 2016 CERN
#
# Inspire-Magpie is a free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for
# more details.

"""Setup for Inspire-Magpie.

.. codeauthor:: Jan Stypka <jan.stypka@cern.ch>
.. codeauthor:: Eamonn Maguire <eamonnmag@gmail.com>
.. codeauthor:: Jan Aage Lavik <jan.age.lavik@cern.ch>
"""

from __future__ import absolute_import, print_function

import os

from codecs import open
from setuptools import setup, find_packages


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('inspire_magpie', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

readme = open('README.md').read()

setup(
    name='inspire-magpie',
    version=version,
    description='Magpie wrapper for Inspire',
    long_description=readme,
    url='https://github.com/inspirehep/inspire-magpie',
    author='CERN',
    author_email='admin@inspirehep.net',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Text Processing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
    ],
    keywords='automatic keyword keyphrase extraction text classification inspire hep',
    packages=find_packages(),
    install_requires=[
        'magpie',
        'flask',
        'gensim',
        'h5py',
    ],
    include_package_data=True,
    data_files=[('inspire_magpie_data', [
        'data/scaler.pickle',
        'data/word2vec.gensim',
        'data/word2vec.gensim.syn0.npy',
    ]), ('inspire_magpie_data/experiments', [
        'data/experiments/model.pickle',
    ]), ('inspire_magpie_data/keywords', [
        'data/keywords/model.pickle',
    ]), ('inspire_magpie_data/categories', [
        'data/categories/model.pickle',
    ])],
)
