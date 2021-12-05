from flask import Flask, request, jsonify
from hashlib import sha256
from file1 import *


api = Flask(__name__)


@api.route('/api/v1/', methods=["GET", "POST", "PATCH", "DEL"])
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

                select_all_data_from_table(user, db_name, table_name)

        else:
            return 404

    elif request.method == "POST":
        auth = params["key"]

        my_hash = sha256("snehashish090".encode()).hexdigest()

        if my_hash == auth:

            if params["mode"] == "new_user":
                username = params["username"]

                try:
                    create_new_user(username)
                except:
                    return 404

            elif params["mode"] == "new_database":
                username = params["username"]
                db_name = params["dbname"]

                try:
                    create_new_database(username, db_name)
                    return "Done"
                except:
                    return 404

            elif params["mode"] == "new_table":
                username = params["username"]
                db_name = params["dbname"]
                table_name = params["tablename"]
                table_values = params["table_values"]

                # try:
                #     create_new_table(username, db_name, table_name, table_values)
                # except:
                #     return 404
                return table_values


if __name__ == "__main__":
    api.run(debug=True)
