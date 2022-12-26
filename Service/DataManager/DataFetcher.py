import json
from base64 import b64encode

import logging

import requests as requests

from Service.DataManager.RequestFailure import RequestFailure


def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


class DataFetcher:

    def __init__(self):
        self._url = 'http://10.4.41.41:8081/allevents'

    def get_data(self):
        headers = {
            'Authorization': basic_auth('admin', 'admin')
        }
        logging.info('Sending the request...')
        req = requests.get(self._url, headers=headers)
        if req.status_code == 200:
            logging.info('Data successfully received.')
            return json.loads(req.text)
        else:
            logging.warning('Error fetching the data.')
            raise RequestFailure("Request unsuccessful")


