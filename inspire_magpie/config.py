import os

from magpie.config import EMBEDDING_SIZE

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
LOG_FOLDER = os.path.join(os.environ['HOME'], 'keras-results')

_dim = str(EMBEDDING_SIZE)

KEYWORD_WORD2VEC = os.path.join(DATA_DIR, 'keywords', 'word2vec' + _dim + '.gensim')
KEYWORD_SCALER = os.path.join(DATA_DIR, 'keywords', 'scaler' + _dim + '.pickle')

CATEGORY_WORD2VEC = os.path.join(DATA_DIR, 'categories', 'word2vec' + _dim + '.gensim')
CATEGORY_SCALER = os.path.join(DATA_DIR, 'categories', 'scaler' + _dim + '.pickle')

EXPERIMENT_WORD2VEC = os.path.join(DATA_DIR, 'experiments', 'word2vec' + _dim + '.gensim')
EXPERIMENT_SCALER = os.path.join(DATA_DIR, 'experiments', 'scaler' + _dim + '.pickle')

NO_OF_LABELS = 1000
