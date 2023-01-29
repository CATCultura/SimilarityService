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
#
# for i, event in enumerate(dt):
#     event['id'] = i

# with open('data/current_data.json', 'w', encoding='utf-8') as f:
#      print(json.dumps(data, indent=4), file=f)

with open('../data/current_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# model_generator = ModelGenerator()
#
# model_generator.generate_models(data)

sim_service = SimilarityService()
query = "yungblud"
res = sim_service.get_k_most_similar_events(query, 5)


for i, s in res.items():
    for event in data:
        if event['id'] == i:
            if s >= 0.5:
                print(f'Good enough match {s}')
            else:
                print(f'Somewhat related match {s}')
            print(event['denominacio'])
            print(event['descripcio'])
            print("***********")





