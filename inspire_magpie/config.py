import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
LOG_FOLDER = os.path.join(os.environ['HOME'], 'keras-results')

KEYWORD_WORD2VEC = os.path.join(DATA_DIR, 'keywords', 'word2vec100.gensim')
KEYWORD_SCALER = os.path.join(DATA_DIR, 'keywords', 'scaler100.pickle')

CATEGORY_WORD2VEC = os.path.join(DATA_DIR, 'categories', 'word2vec100.gensim')
CATEGORY_SCALER = os.path.join(DATA_DIR, 'categories', 'scaler100.pickle')

NO_OF_LABELS = 10000
