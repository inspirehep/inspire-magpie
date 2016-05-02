import json

from flask import Flask, render_template, redirect, request
import requests

from config import EXTRACT_URL, WORD2VEC_URL

app = Flask(__name__)

headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}


@app.route('/', methods=['POST', 'GET'])
def extractor():
    if request.method == 'POST':
        text = request.form.get('text', '')
        corpus = request.form.get('corpus', 'keywords')
        extract_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

        response = requests.post(EXTRACT_URL, data=json.dumps({'corpus': corpus, 'text': text}), headers=extract_headers)

        contents = json.loads(response.text)

        contents['labels'] = contents['labels'][0:20]

        ctx = {'type': 'extract', 'abstract': text, 'corpus': corpus}
        return render_template('magpie/results.html', results=contents, ctx=ctx)

    return render_template('magpie/extractor.html')

@app.route('/extract-feedback', methods=['POST'])
def extract_feedback():
    print request.form
    text = request.form.get('text', '')

    return redirect('/thanks')


@app.route('/word2vec', methods=['POST', 'GET'])
def word2vec():
    if request.method == 'POST':
        positive = request.form.get('positive', None)
        negative = request.form.get('negative', None)

        data = {'corpus': 'keywords'}
        ctx = {'type': 'word2vec'}
        if positive:
            data['positive'] = [w.strip() for w in positive.split(',')]
            ctx['positive'] = ", ".join(data['positive'])
        if negative:
            data['negative'] = [w.strip() for w in negative.split(',')]
            ctx['negative'] = ", ".join(data['negative'])

        response = requests.post(WORD2VEC_URL,
                                 data=json.dumps(data),
                                 headers=headers)
        contents = json.loads(response.text)

        return render_template('magpie/results.html', results=contents, ctx=ctx)
    else:
        return render_template('magpie/word2vec.html')

@app.route('/thanks', methods=['GET'])
def thanks():
    return render_template('magpie/thanks.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
