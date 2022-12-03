import json

from joblib import load
from numpy import dot
from numpy.linalg import norm
import numpy as np

import logging


def cosine_similarity(b):
    def _cosine_similarity(a):
        res = dot(a.reshape(b.shape), b.T) / (norm(a) * norm(b))
        return res

    return _cosine_similarity


def load_text_data(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


def get_k_most_similar(q, k, matrix):
    temporal_result = svd.transform(vectorizer.transform([q]))
    sim = cosine_similarity(temporal_result)
    sim_list = np.apply_along_axis(sim, 1, matrix)
    sim_list = sim_list.reshape((sim_list.shape[0]))
    assert k <= sim_list.size
    top_k = np.argpartition(sim_list, -k)[-k:]
    top_k = top_k[np.argsort(sim_list[top_k])]
    print(top_k)
    print(str(sim_list[5]))
    print(sim_list[top_k])
    return top_k


def extract_text(events):
    text = []
    for event in events:
        text.append(event['descripcio'])
    return text


full_data = load_text_data('../data/current_data.json')

descriptions = extract_text(full_data)

logging.info("Loading tf-idf model")
vectorizer = load('../models/tf-idf.joblib')

logging.info("Loading svd model")
svd = load('../models/svd.joblib')

truncated_matrix = svd.transform(vectorizer.transform(descriptions))

query = input("Enter your query: ")

most_similar = get_k_most_similar(query, 5, truncated_matrix)

ordered = most_similar.tolist().reverse()

for i, number in enumerate(most_similar):
    print(f'Position {i + 1}')
    print(full_data[number]['denominacio'])
    print(full_data[number]['descripcio'])
