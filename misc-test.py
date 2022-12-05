import json

from Service.DataManager.DataFetcher import DataFetcher
from Service.DataManager.ModelManager import ModelManager
from Service.ModelGenerator.ModelGenerator import ModelGenerator
from Service.SimilarityService import SimilarityService

import logging

logging.basicConfig(level=logging.INFO)
# logging.debug('This will get logged')


# data_fetcher = DataFetcher()
#
# dt = data_fetcher.get_data()
# with open('data/current_data.json', 'w', encoding='utf-8') as f:
#     print(json.dumps(dt, indent=4), file=f)

#
# for i, event in enumerate(data):
#     event['id'] = i
#
# with open('data/current_data.json', 'w', encoding='utf-8') as f:
#     print(json.dumps(data, indent=4), file=f)

with open('data/current_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

model_generator = ModelGenerator()

model_generator.generate_models()

sim_service = SimilarityService()
query = "taller de ioga"
res = sim_service.get_k_most_similar_events(query, 5)


for i in res:
    for event in data:
        if event['id'] == i:
            print(event['denominacio'])
            print(event['descripcio'])




