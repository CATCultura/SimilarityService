import json
import logging

import flask
from flask import request
from flask_restx import Api, Namespace, fields
from flasgger import swag_from, Swagger

from Service.ModelGenerator.ModelGenerator import ModelGenerator
from Service.SimilarityService import SimilarityService

logging.basicConfig(level=logging.INFO)

template = {
  "swagger": "2.0",
  "info": {
    "title": "Similarity service",
    "description": "This is the Open API documentation for the CatCultura's Similarity Service. Given a query q and a "
                   "parameter K to specify the number of results, the service returns the K most relevant events for "
                   "the given query q. The service uses a very basic Latent Semantic Analysis to perform the search.",
    "version": "1.0.0"
  },
  "host": "localhost:5500",  # overrides localhost:500
  "schemes": [
    "http"
  ]
}

app = flask.Flask(__name__)
swagger = Swagger(app, template=template)
# swagger.load_swagger_file('documentation/openAPIdoc.yml')

app.config['DEBUG'] = False


@app.route("/similarity", methods=['GET'])
@swag_from('documentation/similarity.yml')
def get_k_most_similar():
    logging.info("Request received.")
    args = request.args
    query = args.get('q', default="")
    logging.info(f'The query is {query}')
    k = args.get('k', default=10, type=int)
    logging.info(f'Number of requested results: {k}')
    if not query:
        logging.info(f'Query empty. Returning error code...')
        response_body = {
            "status": 400,
            "error": 'Bad request',
            "message": "You must provide a query parameter with the relevant query. The query cannot be blank"
        }
        return json.dumps(response_body, indent=4), 400
    else:
        sim_service = SimilarityService()
        logging.info(f'Initiating query matching...')
        result = sim_service.get_k_most_similar_events(query, k)
        logging.info(f'Returning answer...')
        return json.dumps(result, indent=4), 200


@app.route("/update_models", methods=['GET'])
def update_models():
    logging.info(f'Received request to update models with latest data.')
    model_generator = ModelGenerator()
    logging.info(f'Initiating model generation...')
    try:
        model_generator.generate_models()
    except Exception:
        logging.info(f'Unexpected error.')
        return 'Failure', 400
    logging.info(f'Generation successful.')
    return 'Success', 200


app.run(host='0.0.0.0', port=5500)
