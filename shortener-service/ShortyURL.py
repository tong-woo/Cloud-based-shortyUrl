from flask import Flask, request, redirect, render_template, g
from bson import ObjectId
import validators
import os
import jwt
import newrelic
import pymongo

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

SECRET = os.environ['JWT_SECRET']

app = Flask('ShortyURL')

client = pymongo.MongoClient("mongodb+srv://tong:mongodb@cluster0.emupq.mongodb.net/?retryWrites=true&w=majority")
db = client.test
USERS = db['urls']

IDS_COUNTER = 0

CLOSED_ENDPOINTS = ['update_one_url', 'delete_one_url', 'create_url', 'get_urls', 'delete_url']


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/<id>', methods=['GET'])
def get_one_url(id):
    try:
        found = URLs.find_one({"_id": ObjectId(id)})
        if found is None:
            return f'Not found', 404
        else:
            return redirect(found['url'], 302)

    except Exception as e:
        print(e)
        return f'Unexpected error', 500


@app.route('/<id>', methods=['PUT'])
def update_one_url(id):
    try:
        username = g.username
        url = request.form.get('url')
        document = {
            "username": username,
            "_id": ObjectId(id)
        }
        # check url if correct
        if validators.url(url):
            updated = URLs.update_one(document, {"$set": {"url": url}})
            if updated.matched_count == 0:
                return f'not found', 404
            else:
                return f'Success', 200
        else:
            return f'url error', 400
    except Exception as e:
        print(e)
        return f'error', 500


@app.route('/<id>', methods=['DELETE'])
def delete_one_url(id):
    try:
        username = g.username
        document = {
            "_id": ObjectId(id),
            "username": username
        }
        deleted = URLs.delete_one(document)
        if deleted.deleted_count == 0:
            return f'not found', 404
        else:
            return f'Success', 204
    except Exception as e:
        print(e)
        return f'Unexpected error', 500



@app.route('/', methods=['POST'])
def create_url():
    # check for URL correctness
    try:
        url = request.form.get('url')
        username = g.username
        if validators.url(url):
            # shorten the URL
            document = {
                "username": username,
                "url": url
            }
            return_id = URLs.insert_one(document)
            return "{id}".format(id=return_id.inserted_id), 201
        else:
            return f'Incorrect URL', 400
    except Exception as e:
        print(e)
        return f'A Error', 500


@app.route('/', methods=['GET'])
def get_urls():
    try:
        username = g.username
        print(username)
        urls_cursor = URLs.find({"username": username})
        urls_to_return = {}
        for urls in urls_cursor:
            urls_to_return[str(urls['_id'])] = urls['url']
        return urls_to_return, 200
    except Exception as e:
        print(e)
        return f'Unexpected Error', 500


@app.route('/', methods=['DELETE'])
def delete_url():
    # check for URL correctness
    try:
        username = g.username
        # Delete all key and url pairs in the dictionary
        # if it's not empty
        deleted = URLs.delete_many({"username": username})
        if deleted.deleted_count == 0:
            return f'Dict is already empty', 404
        else:
            return f'all user URLs has been removed', 200
    except Exception as e:
        print(e)
        return f'Unexpected Error', 500


@app.before_request
def authentication_middleware():
    if request.endpoint not in CLOSED_ENDPOINTS:  # Methods without AUTH
        return None
    tmp_jwt = request.headers.get('x-access-token')
    print(tmp_jwt)
    if tmp_jwt is None or tmp_jwt == '':
        return 'Forbidden', 403
    try:
        jwt_data = jwt.decode(tmp_jwt, SECRET, algorithms=["HS256"])
        username = jwt_data['username']
        g.username = username
    except Exception as e:
        print(e)
        return 'Forbidden', 403


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    from waitress import serve
    debug = True
    if debug:
        app.run(debug=True, host="0.0.0.0", port=8080)
    else:
        serve(app, host="0.0.0.0", port=8080)

#NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program python3 ShortyURL.py