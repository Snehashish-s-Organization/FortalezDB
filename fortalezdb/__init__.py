import json
import os
import requests

class init:

    def __init__(self, username, url, database, auth_key):

        self.username = username
        self.url = url
        self.database = database
        self.auth_key = auth_key

    

def create_new_table(db,table_name,table_values):
    username = db.username
    db_name = db.database
    auth_key = db.auth_key
    url = db.url

    values = ' '.join(table_values)

    request  = '{}/?key={}&dbname={}&tablename={}&username={}&table_values={}'.format(url, auth_key, db_name, table_name, username, values)
    
    try:
        requests.post(request)  

    except Exception as ex:
        return ex
    









