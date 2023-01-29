import json

import numpy
from joblib import dump, load
from unidecode import unidecode
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from numpy import dot
from numpy.linalg import norm


def cosine_similarity(b):
    def _cosine_similarity(a):
        res = dot(a.reshape(b.shape), b.T) / (norm(a) * norm(b))
        return res

    return _cosine_similarity


def load_text_data(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


data = load_text_data('../data/current_data.json')
temp = []

with open('../configuration/stopwords.txt', 'r', encoding='utf-8') as file:
    temp = file.readlines()

stopwords = [unidecode(a.strip()) for a in temp]

text = []
for item in data:
    text.append(item['descripcio'])

vectorizer = TfidfVectorizer()
vectorizer.strip_accents='unicode'
vectorizer.stop_words = stopwords
print("Initiating tf-idf extraction...")
vectorizer.fit(text)
dump(vectorizer, '../data/tf-idf.joblib')
result = vectorizer.transform(text)
vocab = vectorizer.vocabulary
query = "recital de poesia"

query = vectorizer.transform([query])

svd = TruncatedSVD(n_components=1000, n_iter=10, random_state=52)
print("Initiating SVD computation...")
svd.fit(result)
dump(svd, '../data/svd.joblib')
print(svd.explained_variance_ratio_.sum())
print("Initiating SVD transform...")
truncated_matrix = svd.transform(result)

print(query.shape)


query = svd.transform(query)

sim = cosine_similarity(query)
sim_list = np.apply_along_axis(sim, 1, truncated_matrix)
sim_list = sim_list.reshape((sim_list.shape[0]))
top_5 = np.argpartition(sim_list, -5)[-5:]

print(sim_list[top_5])

mapper = {}
for k,v in zip(top_5, sim_list[top_5]):
    mapper[k] = v

for k,v in mapper.items():
    print(f'value = {v}')
    print(data[k]['denominacio'])
    print(data[k]['descripcio'])



