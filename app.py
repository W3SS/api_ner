from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

from serve import get_model_api


# define the app
app = Flask(__name__)
CORS(app) # needed for cross-domain requests, allow everything by default


# logging
logHandler = logging.FileHandler('app.log')
logHandler.setLevel(logging.INFO)
app.logger.addHandler(logHandler)
app.logger.setLevel(logging.INFO)


# load the model
model_api = get_model_api()


# API route
@app.route('/api', methods=['POST'])
def api():
    """API function

    All model-specific logic to be defined in the get_model_api()
    function
    """
    input_data = request.json
    app.logger.info(input_data)
    output_data = model_api(input_data)
    app.logger.info(output_data)

    try:
        with open("app.log", "a") as f:
            f.write(str(output_data))
    except Exception:
        pass

    response = jsonify(output_data)
    return response


@app.route('/')
def index():
    return "Index API"

# HTTP Errors handlers
@app.errorhandler(404)
def url_error(e):
    return """
    Wrong URL!
    <pre>{}</pre>""".format(e), 404


@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally.
    app.run(host='0.0.0.0', debug=True)
