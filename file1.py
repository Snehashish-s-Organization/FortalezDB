# Author: Snehashish Laskar
# Date: 3-12-2021

# imports
import json
import os
from flask import Flask, request, jsonify
from hashlib import sha256



def create_new_user(name):
    if not os.path.exists("./data/{}".format(name)):
        os.makedirs("./data/{}".format(name))

    else:
        print("User already exists")


def create_new_database(user, dbname):
    """
    This function creates a new database by making a new directory in the
    folder of the user to whom the database belongs to.
    The parameters are:
    -> user: The username of the user to whom the database belongs to
    -> dbname: The name of the database you want to create
    """
    target_path = f"./data/{user}/"

    if not os.path.exists(target_path+dbname):
        os.makedirs(target_path+dbname)

    else:
        raise Exception("Database exists")


# Function to create a new table
def create_new_table(user, dbname, table_values, table_name):
    """
    This function creates a new table in an already existing database
    The parameters are:
    -> user : The username of the person to whom the database belongs to
    -> dbname : The name of the database
    -> table_values: The list of table headers ex: ["Name", "Age", "Gender"]
    -> table_name: The name of the table
    """
    target_path = f"./data/{user}/{dbname}/"

    if not os.path.exists(target_path+f"{table_name}.json"):
        with open(target_path+f"{table_name}.json", "w+") as file:
            table = {}

            for i in table_values:
                table[i] = []

            print(table)
            json.dump(table, file, indent=True)
    else:
        raise Exception("The table already exists in the database")


def write_into_table(values: dict, table_name, db_name, user):
    """
    This function writes data into the table of a given database
    The parameters are:
    -> values: The Values to be inserted into the database
    Structure of the parameter values:
    {
        "table_value_no_1": Value,
        "table_value_no_2: Value,
        "table_value_no_3: Value,
    }
    -> table_name: Name of the table into which the data needs to be inserted
    -> db_name: Name of the database that contains the table
    -> user: Name of the User to whom the database belongs to
    """
    if os.path.exists(f"./data/{user}/{db_name}/{table_name}.json"):
        with open(f"./data/{user}/{db_name}/{table_name}.json", "r") as file:
            table_data = json.load(file)

        # if len(values.keys()) == len(table_data.keys()):
        for i, j in values.items():
            lis = table_data[i]
            lis.append(j)
            table_data[i] = lis

        with open(f"./data/{user}/{db_name}/{table_name}.json", "w+") as file:
            json.dump(table_data, file, indent=True)

        # else:
        #     raise Exception("The Values do not match the Table's headers")

    else:
        raise Exception("The Table or the database don't exist")


def select_all_data_from_table(user, db_name, table_name):
    """
    This function resembles the SQL query "SELECT * FROM table"
    This returns all the data in the table
    The parameters are:
    -> user: Name of the user to whom the database belongs to
    -> db_name: Name of the database
    -> table_name: Name of the table
    """
    if os.path.exists(f"./data/{user}/{db_name}/{table_name}.json"):
        with open(f"./data/{user}/{db_name}/{table_name}.json", "r") as file:
            data = json.load(file)

        return data
    else:
        raise Exception("The table does not exist")


def select_specific_data(user, db_name, table_name, key, key_value):
    """
    This function resembles the SQL query "SELECT * FROM table WHERE something = something"
    The parameters are:
    -> user: Name of the user to whom the database belongs to
    -> db_name: Name of the database
    -> table_name: Name of the table
    -> key: The Header you are targeting
    -> key_value: The Value that you are looking for

    """
    if os.path.exists(f"./data/{user}/{db_name}/{table_name}.json"):
        with open(f"./data/{user}/{db_name}/{table_name}.json", "r") as file:
            data = json.load(file)
            index = None
            for i in data:
                if i == key:
                    list_of_values = data[i]
                    for j in list_of_values:
                        if j == key_value:
                            index = list_of_values.index(j)
            results = {}
            for i in data:
                item = data[i][index]
                results[i] = item

            return results


def update_data(user, db_name, table_name, key, key_value):

    if os.path.exists(f"./data/{user}/{db_name}/{table_name}.json"):
        with open(f"./data/{user}/{db_name}/{table_name}.json", "w+") as file:
            data = json.load(file)

            if key in data.keys():
                data[key] = key_value
                json.dump(data, file, indent=4)
                

# Creating the API for the DB so that the backend can communicate with the GUI that 
# Will be used by the End user as the UI to create their database


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

        my_hash = sha256("snehashish090".encode()).hexdigest()

        if my_hash == auth:
           
            # cheking if the user wants something specefic
            if params["mode"] == "specific":
                user = params["user"]
                db_name = params["dbname"]
                table_name = params["tablename"]
                header = params["header"]
                value = params["value"]

                select_specific_data(user, db_name, table_name, header, value)
           
           # Checking if the wants all the data from the table
            elif params["mode"] == "all":
                user = params["user"]
                db_name = params["dbname"]
                table_name = params["tablename"]

                select_all_data_from_table(user, db_name, table_name)

        else:
            return "error"

    elif request.method == "POST":
        auth = params["key"]

        my_hash = sha256("snehashish090".encode()).hexdigest()

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
