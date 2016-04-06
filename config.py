import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
LOG_FOLDER = os.path.join(os.environ['HOME'], 'keras-results')

NO_OF_LABELS = 1000
