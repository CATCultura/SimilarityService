import json
import logging

from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from unidecode import unidecode
import numpy as np

from Service.DataManager.DataFetcher import DataFetcher
from Service.DataManager.ModelManager import ModelManager

relevant_fields = ['descripcio', 'denominacio', 'subtitol']


def load_stopwords():
    temp = []
    with open('configuration/stopwords.txt', 'r', encoding='utf-8') as file:
        temp = file.readlines()
    stopwords = [unidecode(a.strip()) for a in temp]
    return stopwords


def sanitize_text(text):
    res = text.split("NOTA DE L'AGENDA")
    return res[0]


def extract_relevant_info(events: dict):
    mapper = {}
    text = []
    for i, event in enumerate(events):
        event_text = ""
        mapper[i] = event['id']
        for field in relevant_fields:
            if event[field]:
                event_text = f'{event_text} \n\n {sanitize_text(event[field])}'
        if event_text:
            text.append(event_text)
        else:
            logging.info(f'Event with id {event["id"]} has no useful textual data. Skipping it...')
    return text, mapper


def persist(mapping, path):
    with open(path, 'w', encoding='utf-8') as file:
        print(json.dumps(mapping, indent=4), file=file)


class ModelGenerator:

    def __init__(self):
        self._data_fetcher = DataFetcher()
        self._model_manager = ModelManager()

    def generate_models(self, direct_data=None):
        data = {}
        if direct_data:
            data = direct_data
        else:
            data = self._data_fetcher.get_data()

        txt, mapping = extract_relevant_info(data)
        persist(mapping, 'data/map.json')
        vec_model = self._generate_tfidfvec(txt)
        tfidf_matrix = vec_model.transform(txt)
        svd = self._generate_svd(tfidf_matrix)

        computed_mat = svd.transform(tfidf_matrix)
        np.save('data/svd_mat', computed_mat)

        self._model_manager.save_models(vec_model, svd)

    @staticmethod
    def _generate_tfidfvec(textual_data):
        stopwords = load_stopwords()
        vectorizer = TfidfVectorizer()
        vectorizer.strip_accents = 'unicode'
        vectorizer.stop_words = stopwords
        logging.info("Initiating tf-idf extraction...")
        vectorizer.fit(textual_data)
        return vectorizer

    @staticmethod
    def _generate_svd(original_matrix):
        svd = TruncatedSVD(n_components=300, n_iter=15, random_state=98)
        logging.info("Initiating SVD computation...")
        svd.fit(original_matrix)
        logging.info(f'Explained variance: {svd.explained_variance_ratio_.sum()}')
        return svd
