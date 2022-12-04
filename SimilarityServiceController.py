import json

import flask
from flask import request

from Service.SimilarityService import SimilarityService

import logging

logging.basicConfig(level=logging.INFO)
logging.debug('This will get logged')

app = flask.Flask(__name__)
app.config['DEBUG'] = True


@app.route("/similarity", methods=['GET'])
def get_k_most_similar():
    args = request.args
    query = args.get('q', default="")
    k = args.get('k', default=10, type=int)
    if not query:
        response_body = {
            "status": 400,
            "message": "You must provide a query parameter with the relevant query. The query cannot be blank"
        }
        return json.dumps(response_body, indent=4), 400
    else:
        sim_service = SimilarityService()
        result = sim_service.get_k_most_similar_events(query, k)
        return json.dumps(result, indent=4), 200


@app.route("/update_models", methods=['GET'])
def update_models():
    # TODO request all events and recompute and save models
    pass


app.run(host='0.0.0.0', port=5500)
