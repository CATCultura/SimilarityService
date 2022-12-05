import json
import logging

from numpy import dot
from numpy.linalg import norm
import numpy as np

from Service.DataManager.ModelManager import ModelManager
from Service.ModelGenerator.ModelGenerator import ModelGenerator


def cosine_similarity(b):
    def _cosine_similarity(a):
        res = dot(a.reshape(b.shape), b.T) / (norm(a) * norm(b))
        return res

    return _cosine_similarity


def load_mapping(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


class SimilarityService:

    def __init__(self):
        # self.remote_url = 'http://10.4.41.41:8081/allevents'
        self._model_manager = ModelManager()
        self._model_generator = ModelGenerator()

    def get_k_most_similar_events(self, q, k):
        self._model_manager.load_models()
        svd_model = self._model_manager.svd
        vec_model = self._model_manager.vectorizer
        tfidf_matrix = np.load('data/svd_mat.npy')

        query_vector = svd_model.transform(vec_model.transform([q]))
        similarity_function = cosine_similarity(query_vector)
        similarity_score_list = np.apply_along_axis(similarity_function, 1, tfidf_matrix)
        similarity_score_list = similarity_score_list.reshape((similarity_score_list.shape[0]))

        assert k <= similarity_score_list.size

        top_k = np.argpartition(similarity_score_list, -k)[-k:]
        top_k = top_k[np.argsort(similarity_score_list[top_k])]

        logging.info(top_k)
        logging.info(similarity_score_list[top_k])

        mapping = load_mapping('data/map.json')

        top_k = top_k.tolist()
        top_k.reverse()

        logging.info('Reversed')
        logging.info(top_k)
        logging.info(similarity_score_list[top_k])
        self._model_manager.unload_models()
        # returning the ids of the relevant events
        result = []
        for k in top_k:
            result.append(mapping[str(k)])

        return result

    def update_models(self, data=None):
        self._model_generator.generate_models(data)