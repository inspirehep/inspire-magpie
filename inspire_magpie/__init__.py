# -*- coding: utf-8 -*-
#
# This file is part of Inspire-Magpie.
# Copyright (c) 2016 CERN
#
# Inspire-Magpie is a free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for
# more details.

"""Custom exceptions.

.. codeauthor:: Jan Stypka <jan.stypka@cern.ch>
.. codeauthor:: Jan Aage Lavik <jan.age.lavik@cern.ch>
"""

from __future__ import absolute_import, print_function

from flask import Flask

from .api import get_cached_model
from .config import SUPPORTED_CORPORA
from .rest import blueprint as rest_blueprint
from .ui import blueprint as ui_blueprint


application = Flask('magpie', static_url_path='')
application.register_blueprint(rest_blueprint)
application.register_blueprint(ui_blueprint)

if not application.debug:
    application.logger.info("Preloading corpus..")
    # Preload data
    for corpus in SUPPORTED_CORPORA:
        get_cached_model(corpus)
    application.logger.info("DONE.")

__all__ = ('application',)
