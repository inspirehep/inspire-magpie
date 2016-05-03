# -*- coding: utf-8 -*-
#
# This file is part of Inspire-Magpie.
# Copyright (c) 2016 CERN
#
# Inspire-Magpie is a free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for
# more details.

"""WSGI app.

.. codeauthor:: Jan Aage Lavik <jan.age.lavik@cern.ch>
"""

from __future__ import absolute_import, print_function

import logging

from inspire_magpie import application

# Enable logging for wsgi server
if not application.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    application.logger.addHandler(stream_handler)
    wsgi_logger = logging.getLogger('wsgi.errors')
    wsgi_logger.addHandler(stream_handler)

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5051, debug=True)
