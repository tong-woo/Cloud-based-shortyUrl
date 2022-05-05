from flask import Flask, request, redirect, render_template, g
import validators
import os
import jwt
import newrelic

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

SECRET = os.environ['JWT_SECRET']

app = Flask('ShortyURL')

URLs = {

}
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
        all_urls = {}
        for username in URLs:
            all_urls.update(URLs[username])
        print(all_urls.items())
        if id in all_urls:
            return redirect(all_urls[id], 302)
        else:
            return f'Not found', 404
    except Exception as e:
        print(e)
        return f'Unexpected error', 500


@app.route('/<id>', methods=['PUT'])
def update_one_url(id):
    try:
        username = g.username
        if username not in URLs or id not in URLs[username]:
            return f'not found', 404
        else:
            # check url if correct
            if validators.url(request.form.get('url')):
                URLs[username][id] = request.form.get('url')
            else:
                return f'url error', 400
            return f'Success', 200
    except Exception as e:
        print(e)
        return f'error', 500


@app.route('/<id>', methods=['DELETE'])
def delete_one_url(id):
    try:
        username = g.username
        if username not in URLs or id not in URLs[username]:
            return f'not found', 404
        else:
            URLs[username].pop(id)
            return f'Success', 204
    except Exception as e:
        print(e)
        return f'Unexpected error', 500


@app.route('/', methods=['POST'])
def create_url():
    # check for URL correctness
    try:
        global IDS_COUNTER
        url = request.form.get('url')
        username = g.username
        if validators.url(url):
            # shorten the URL
            if username not in URLs:
                URLs[username] = {}
            URLs[username]["{}".format(IDS_COUNTER)] = url
            print(URLs)
            IDS_COUNTER += 1
            return "{id}".format(id=IDS_COUNTER - 1), 201
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
        if username not in URLs:
            return {}, 200
        return URLs[username], 200
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
        if username not in URLs:
            return f'Dict is already empty', 404
        if bool(URLs[username]):
            URLs[username].clear()
            return f'all items(key, url) in the dict has been removed', 200
        else:
            return f'Dict is already empty', 404
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