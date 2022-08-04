from datetime import datetime, timedelta
from flask import Flask, request, redirect, render_template
import newrelic
import os
import jwt
import pymongo

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

app = Flask('ShortyLogin')



client = pymongo.MongoClient("mongodb+srv://tong:mongodb@cluster0.emupq.mongodb.net/?retryWrites=true&w=majority")
db = client.test
USERS = db['users']
SECRET = os.environ['JWT_SECRET']



@app.route('/users', methods=['POST'])
def create_one_user():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        if username is None or username == '':
            return 'Missing parameters', 400
        if password is None or password == '':
            return 'Missing parameters', 400
        result = USERS.find_one({"username": username, "password": password})
        if result is not None:
            return f'Username already exist', 409
        else:
            user = {"username": username, "password": password}
            USERS.insert_one(user)
            return f'Success', 200
    except Exception as e:
        print(e)
        return f'Unexpected error', 500


@app.route('/users/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    stamp = datetime.now() + timedelta(days=1)
    try:
        result = USERS.find_one({"username": username, "password": password})
        if result is not None:
            return "{encoded_jwt}".format(encoded_jwt=jwt.encode({"username": "{name}".format(name=username), "exp": stamp}, SECRET, algorithm="HS256")), 200
        else:
            return f"check the username and password", 403
    except Exception as e:
        print(e)
        return f'Unexpected error', 500

# Cross-origin resource sharing, Indicates which domains the requested resource can be shared to,
# either a specific domain name or * indicating all domains.
@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    from waitress import serve
    debug = True
    if debug:
        app.run(debug=True, host="0.0.0.0", port=8081)
    else:
        serve(app, host="0.0.0.0", port=8081)

# NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program python3 ShortyLogin.py