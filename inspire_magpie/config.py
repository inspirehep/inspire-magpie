import os
import sys

DATA_DIR = os.path.join(sys.prefix, 'inspire_magpie_data')
LOG_FOLDER = os.path.join(sys.prefix, 'var', 'log', 'keras-results')

WORD2VEC_PATH = os.path.join(DATA_DIR, 'word2vec.gensim')
SCALER_PATH = os.path.join(DATA_DIR, 'scaler.pickle')

NO_OF_LABELS = 10000
