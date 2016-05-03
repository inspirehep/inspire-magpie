import os
import time

from flask import Blueprint, request, jsonify

from .api import get_word_vector, predict_labels
from .errors import WordDoesNotExist
from .config import SUPPORTED_CORPORA

blueprint = Blueprint('rest', __name__, url_prefix="/api")


@blueprint.route("/predict", methods=['POST'])
def predict():
    """
    Takes a following JSON as input:
    {
        'text': 'my abstract'       # the text to be fed to the model
        'corpus': 'keywords'        # corpus to work on. Currently supported are
                                    # in the SUPPORTED_CORPORA variable
    }

    :return:
    {
        'status_code': 200      # 200, 400, 403 etc
        'labels': []            # list of two-element tuples each with a label
                                # and its confidence value e.g. [('jan', 0.95)]
    }
    """

    json = request.json
    if not json or 'text' not in json:
        return jsonify({'status_code': 400, 'keywords': []})

    corpus = json.get('corpus', SUPPORTED_CORPORA[0])
    if corpus not in SUPPORTED_CORPORA:
        return jsonify({'status_code': 404, 'keywords': [],
                        'info': 'Corpus ' + corpus + ' is not available'})

    labels = predict_labels(corpus, json['text'])

    return jsonify({
        'status_code': 200,
        'labels': labels,
    })


@blueprint.route("/word2vec", methods=['POST'])
def word2vec():
    """
    Takes a following JSON as input:
    {
        'corpus': 'keywords'            # corpus to work on. Currently supported
                                        # are in the SUPPORTED_CORPORA variable
        'positive': ['cern', 'geneva']  # words to add
        'negative': ['heidelberg']      # words to subtract
    }

    :return:
    {
        'status_code': 200      # 200, 400, 403 etc
        'similar_words': []     # list of the form [('w1', 0.99), ('w2', 0.67)]
    }
    """

    json = request.json
    if not json or not ('positive' in json or 'negative' in json) or 'corpus' not in json:
        return jsonify({'status_code': 400, 'similar_words': []})

    positive, negative = json.get('positive', []), json.get('negative', [])
    corpus = json['corpus']
    try:
        vector = get_word_vector(corpus, positive, negative)
    except WordDoesNotExist as err:
        return jsonify({'status_code': 404, 'similar_words': None,
                        'info': err})
    return jsonify({
        'status_code': 200,
        'vector': vector
    })


@blueprint.route("/feedback", methods=['POST'])
def feedback():
    """
    Takes a following JSON as input:
    {
        'corpus': 'keywords',       # corpus to work on. Currently supported
                                    # are in the SUPPORTED_CORPORA variable
        'text': 'my abstract',      # the text that the labels describe
        'labels': []                # list of two-element tuples each with a label
                                    # and a binary value e.g. [('jan', 1)]
    }

    :return:
    {
        'status_code': 200      # 200, 400, 403 etc
    }
    """
    json = request.json
    if not json or \
       'text' not in json or \
       'labels' not in json or \
       type(json['labels']) != list:
        return jsonify({'status_code': 400, 'info': 'Field error'})

    for elem in json['labels']:
        if type(json['labels']) != list or len(elem) != 2:
            return jsonify({'status_code': 400, 'info': 'Error in labels field'})

    corpus = json.get('corpus', SUPPORTED_CORPORA[0])
    if corpus not in SUPPORTED_CORPORA:
        return jsonify({'status_code': 404,
                        'info': 'Corpus ' + corpus + ' is not available'})

    filepath = os.path.join(DATA_DIR, corpus, 'feedback')
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    filename = os.path.join(filepath, 'magpie' + time.strftime('%d%m%H%M%S'))

    # For the name conflicts
    tail = 0
    while os.path.exists(filename):
        potential_name = filename + str(tail)
        if not os.path.exists(potential_name):
            filename = potential_name
            break
        else:
            tail += 1

    def format_line(s): return (s + '\n').encode('utf-8')

    with open(filename + '.txt', 'wb+') as f:
        f.write(format_line(json['text']))

    labels = [lab for (lab, is_lab) in json['labels'] if is_lab == 1]

    with open(filename + '.lab', 'wb+') as f:
        for lab in labels:
            f.write(format_line(lab))

    return jsonify({'status_code': 200})
