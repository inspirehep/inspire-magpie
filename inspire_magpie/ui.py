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
    print request.form
    text = request.form.get('text', '')

    return redirect('/thanks')


@blueprint.route('/word2vec', methods=['POST', 'GET'])
def word2vec():
    if request.method == 'POST':
        positive = request.form.get('positive', None)
        negative = request.form.get('negative', None)

        positive = [w.strip() for w in positive.split(',')]
        negative = [w.strip() for w in negative.split(',')]

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
