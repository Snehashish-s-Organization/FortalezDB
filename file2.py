from flask import Flask, request, jsonify
import json
from hashlib import sha256

api = Flask(__name__)


@api.route('/api/v1/', methods = ["GET", "POST", "PATCH", "DEL"])
def api_main_page():
    params = request.args

    if request.method == "GET":
        query = params["query"]
        auth = params["key"]

        my_hash = sha256("snehashish090".encode()).hexdigest()

        if my_hash == auth:
            return jsonify(query)
        else:
            return 404


if __name__ == "__main__":
    api.run(debug=True)