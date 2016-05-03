# -*- coding: utf-8 -*-
#
# This file is part of Inspire-Magpie.
# Copyright (c) 2016 CERN
#
# Inspire-Magpie is a free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for
# more details.

"""Configuration.

.. codeauthor:: Jan Stypka <jan.stypka@cern.ch>
.. codeauthor:: Jan Aage Lavik <jan.age.lavik@cern.ch>
"""

from __future__ import absolute_import, print_function

import os
import sys

DATA_DIR = os.path.join(sys.prefix, 'inspire_magpie_data')
LOG_FOLDER = os.path.join(sys.prefix, 'var', 'log', 'keras-results')

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

WORD2VEC_PATH = os.path.join(DATA_DIR, 'word2vec.gensim')
SCALER_PATH = os.path.join(DATA_DIR, 'scaler.pickle')

NO_OF_LABELS = 10000

SUPPORTED_CORPORA = ['keywords', 'categories', 'experiments']
