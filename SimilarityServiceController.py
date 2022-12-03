import flask

app = flask.Flask(__name__)
app.config['DEBUG'] = True


@app.route("/similarity", methods=['GET'])
def get_k_most_similar():
    pass


@app.route("/update_models", methods=['GET'])
def update_models():
    pass
