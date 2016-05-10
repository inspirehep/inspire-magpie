# -*- coding: utf-8 -*-
#
# This file is part of Inspire-Magpie.
# Copyright (c) 2016 CERN
#
# Inspire-Magpie is a free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for
# more details.

"""UI Blueprint.

.. codeauthor:: Eamonn Maguire <eamonnmag@gmail.com>
.. codeauthor:: Jan Stypka <jan.stypka@cern.ch>
.. codeauthor:: Jan Aage Lavik <jan.age.lavik@cern.ch>
"""

from __future__ import absolute_import, print_function

from flask import Blueprint, render_template, redirect, request, url_for

from .api import get_word_vector, predict_labels

blueprint = Blueprint(
    'ui',
    __name__,
    template_folder="templates",
    static_folder="static"
)

headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}


@blueprint.route('/', methods=['POST', 'GET'])
def extractor():
    if request.method == 'POST':
        text = request.form.get('text', '')
        corpus = request.form.get('corpus', 'keywords')

        labels = predict_labels(corpus, text)[0:20]

        ctx = {'type': 'extract', 'abstract': text, 'corpus': corpus}
        return render_template('magpie/results.html', results=labels, ctx=ctx)

    return render_template('magpie/extractor.html')


@blueprint.route('/extract-feedback', methods=['POST'])
def extract_feedback():
    return redirect('/thanks')


@blueprint.route('/word2vec', methods=['POST', 'GET'])
def word2vec():
    if request.method == 'POST':
        positive = request.form.get('positive', '')
        negative = request.form.get('negative', '')

        positive = [w.strip().lower() for w in positive.split(',') if w != '']
        negative = [w.strip().lower() for w in negative.split(',') if w != '']

        ctx = {'type': 'word2vec'}
        if positive:
            ctx['positive'] = ", ".join(positive)
        if negative:
            ctx['negative'] = ", ".join(negative)

        vector = get_word_vector('keywords', positive, negative)

        return render_template('magpie/results.html', results=vector, ctx=ctx)
    else:
        return render_template('magpie/word2vec.html')


@blueprint.route('/thanks', methods=['GET'])
def thanks():
    return render_template('magpie/thanks.html')
