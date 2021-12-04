from flask import Flask, request, jsonify
from hashlib import sha256
from file1 import *


api = Flask(__name__)


@api.route('/api/v1/', methods = ["GET", "POST", "PATCH", "DEL"])
def api_main_page():
    params = request.args

    if request.method == "GET":
        query = params["query"]
        auth = params["key"]

        my_hash = sha256("snehashish090".encode()).hexdigest()

        if my_hash == auth:
            if params["mode"] == "specific":
                user = params["user"]
                db_name = params["dbname"]
                table_name = params["tablename"]
                header = params["header"]
                value = params["value"]

                select_specific_data(user, db_name, table_name, header, value)

            elif params["mode"] == "all":
                user = params["user"]
                db_name = params["dbname"]
                table_name = params["tablename"]




        else:
            return 404


if __name__ == "__main__":
    api.run(debug=True)
