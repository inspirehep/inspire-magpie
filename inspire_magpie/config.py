import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
LOG_FOLDER = os.path.join(os.environ['HOME'], 'keras-results')

WORD2VEC_PATH = os.path.join(DATA_DIR, 'word2vec.gensim')
SCALER_PATH = os.path.join(DATA_DIR, 'scaler.pickle')

NO_OF_LABELS = 10000
