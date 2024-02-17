from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

books = [{'title': 'Software Engineering', 'id': '1'},
         {'title': 'Algorithm Design', 'id': '2'},
         {'title': 'Python', 'id': '3'}]


@app.route('/')
@app.route('/home/')
def index():
    return render_template('index.html')


@app.route('/cities/')
def cities():
    return render_template('cities.html')

@app.route('/activities/')
def activities():
    return render_template('activities.html')


@app.route('/flights/')
def flights():
    return render_template('flights.html')

@app.route('/hotels/')
def hotels():
    return render_template('hotels.html')

@app.route('/about/')
def about():
    repo_link = "https://gitlab.com/kkx2402GL/cs331e-idb"

    return render_template('about.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
