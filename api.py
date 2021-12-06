import json
import os
from flask import Flask, request, jsonify
from hashlib import sha256
from backend import *

# Creating the API for the DB so that the backend can communicate with the GUI that 
# Will be used by the End user as the UI to create their database

if not os.path.exists('./data'):
    os.makedirs('./data')

# Initializing the app
api = Flask(__name__)


# Creaing the main route page
@api.route('/api/v1/', methods=["GET", "POST", "PATCH", "DEL"])
def api_main_page():
    params = request.args
   
   # GET for only reading data
   # POST for writing the data
   # PATCH to update data
   # DEL to delete data 


    if request.method == "GET":

        query = params["query"]
        # Each user has to authenticate using a certain key
        auth = params["key"]

        my_hash = sha256(params['username'].encode()).hexdigest()

        if my_hash == auth:
           
            # cheking if the user wants something specefic
            if params["mode"] == "specific":
                
                user = params["username"]
                db_name = params["dbname"]
                table_name = params["tablename"]
                header = params["header"]
                value = params["value"]

                select_specific_data(user, db_name, table_name, header, value)
           
           # Checking if the wants all the data from the table
            elif params["mode"] == "all":

                user = params["username"]
                db_name = params["dbname"]
                table_name = params["tablename"]

                select_all_data_from_table(user, db_name, table_name)

        else:
            return "error"


    elif request.method == "POST":
        auth = params["key"]

        my_hash = sha256(params['username'].encode()).hexdigest()

        if my_hash == auth:

            if params["mode"] == "new_user":

                username = params["username"]

                try:
                    create_new_user(username)
                except:
                    return "error"

            elif params["mode"] == "new_database":

                username = params["username"]
                db_name = params["dbname"]

                try:
                    create_new_database(username, db_name)
                    return "Done"
                except:
                    return "error"


            elif params["mode"] == "new_table":

                username = params["username"]
                db_name = params["dbname"]
                table_name = params["tablename"]
                table_values = params["table_values"]

                values = []

                for i in table_values.split():
                    values.append(i)

                try:
                    create_new_table(username, db_name, values, table_name)
                    return 200

                except:
                    return "error"


            elif params["mode"] == "new_value":

                username = params["username"]
                db_name = params["dbname"]
                table_name = params["tablename"]
                
                # values = params["values"]
                actual_values = {}
                
                with open("./data/{}/{}/{}.json".format(username, db_name, table_name), "r") as file:

                    data = json.load(file)

                    for i in data.keys():
                        if i in params:
                            actual_values[i] = params[i]
                        else:
                            pass 

                    write_into_table(
                        values = actual_values,
                        db_name = db_name,
                        table_name = table_name,
                        user = username
                        )

                    with open("./data/{}/{}/{}.json".format(username, db_name, table_name), "r") as file:
                        data = json.load(file)

                        return data


    elif request.method == "PATCH":

        params = request.args()
        auth = params["key"]

        my_hash = sha256(params['username'].encode()).hexdigest()

        if my_hash == auth:

            if params['mode'] == 'update_table_value':

                username = params['username']
                db_name = params['db_name']
                table_name = params['table_name']
                table_header = params['table_header']
                table_values = params['table_values']

                try:
                    update_data(username, db_name, table_name, table_header, table_values)

                except:
                    return 404


if __name__ == "__main__":
    api.run(debug=True)
