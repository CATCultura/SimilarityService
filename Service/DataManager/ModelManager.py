import logging
import os

from joblib import load, dump


class ModelManager:

    def __init__(self):
        self._path = f'data{os.sep}'
        self.vectorizer = None
        self.svd = None

    def load_models(self):
        logging.info("Loading tf-idf model")
        self.vectorizer = load(self._path+'tf-idf.joblib')

        logging.info("Loading svd model")
        self.svd = load(self._path+'svd.joblib')

    def unload_models(self):
        logging.info("Unloading tf-idf model")
        self.vectorizer = None

        logging.info("Unloading svd model")
        self.svd = None

    def save_models(self, vec, svd):
        logging.info("Saving tf-idf model")
        dump(vec, self._path+'tf-idf.joblib')

        logging.info("Saving svd model")
        dump(svd, self._path+'svd.joblib')
