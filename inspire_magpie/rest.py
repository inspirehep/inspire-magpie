import os
import time

from flask import Flask, request, jsonify
from gensim.models import Word2Vec

from inspire_magpie.config import DATA_DIR
from inspire_magpie.labels import get_labels
from magpie import MagpieModel
from magpie.nn.models import berger_cnn
from magpie.utils import load_from_disk

app = Flask('magpie')

models = dict()

supported_corpora = ['keywords', 'categories']


def get_cached_model(corpus):
    """ Get the cached Keras NN model or rebuild it if missed. """
    global models

    if corpus not in models:
        models[corpus] = build_model_for_corpus(corpus)

    return models[corpus]


def build_model_for_corpus(corpus):
    """ Build an appropriate Keras NN model depending on the corpus """
    keras_model = None
    no_of_labels = -1

    if corpus == 'keywords':
        keras_model = berger_cnn(embedding_size=100, output_length=1000)
        no_of_labels = 1000
    elif corpus == 'categories':
        keras_model = berger_cnn(embedding_size=50, output_length=14)
        no_of_labels = 14

    model_path = os.path.join(DATA_DIR, corpus, 'model.pickle')
    keras_model.load_weights(model_path)

    w2v_path = os.path.join(DATA_DIR, corpus, 'word2vec.pickle')
    w2v_model = Word2Vec.load(w2v_path)

    scaler_path = os.path.join(DATA_DIR, corpus, 'scaler.pickle')
    scaler = load_from_disk(scaler_path)

    labels = get_labels(no_of_labels)

    model = MagpieModel(
        keras_model=keras_model,
        word2vec_model=w2v_model,
        scaler=scaler,
        labels=labels,
    )

    return model


@app.route('/')
@app.route('/hello')
def hello():
    """ Function for testing purposes """
    return 'Hello World!'


@app.route("/predict", methods=['POST'])
def predict():
    """
    Takes a following JSON as input:
    {
        'text': 'my abstract'       # the text to be fed to the model
        'corpus': 'keywords'        # corpus to work on. Currently supported are
                                    # in the supported_corpora variable
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

    corpus = json.get('corpus', supported_corpora[0])
    if corpus not in supported_corpora:
        return jsonify({'status_code': 404, 'keywords': [],
                        'info': 'Corpus ' + corpus + ' is not available'})

    model = get_cached_model(corpus)
    labels = model.predict_from_text(json['text'])

    return jsonify({
        'status_code': 200,
        'labels': labels,
    })


@app.route("/word2vec", methods=['POST'])
def word2vec():
    """
    Takes a following JSON as input:
    {
        'corpus': 'keywords'            # corpus to work on. Currently supported
                                        # are in the supported_corpora variable
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
    w2v_model = get_cached_model(corpus).word2vec_model

    for word in positive + negative:
        if word not in w2v_model[corpus]:
            return jsonify({'status_code': 404, 'similar_words': None,
                            'info': '{0} does not have a representation in the '
                                    '{1} corpus'.format(word, corpus)})

    return jsonify({
        'status_code': 200,
        'vector': w2v_model[corpus].most_similar(positive=positive,
                                                 negative=negative)
    })


@app.route("/feedback", methods=['POST'])
def feedback():
    """
    Takes a following JSON as input:
    {
        'corpus': 'keywords',       # corpus to work on. Currently supported
                                    # are in the supported_corpora variable
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

    corpus = json.get('corpus', supported_corpora[0])
    if corpus not in supported_corpora:
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


if __name__ == "__main__":
    app.run(port=5051, debug=True)
