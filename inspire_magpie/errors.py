# -*- coding: utf-8 -*-
#
# This file is part of Inspire-Magpie.
# Copyright (c) 2016 CERN
#
# Inspire-Magpie is a free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for
# more details.

"""Custom exceptions.

.. codeauthor:: Jan Aage Lavik <jan.age.lavik@cern.ch>
"""

from __future__ import absolute_import, print_function


class InspireMagpieException(Exception):
    """Base exception for Inspire-Magpie."""


class WordDoesNotExist(InspireMagpieException):
    """Raised when word representation is not found in corpus."""
