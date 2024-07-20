from flask import Flask, jsonify, request
from flask_cors import CORS
import requests


app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={r'/*': {'origins': '*'}})


data = {
        '_id': 0,
        'title': 'Mr.Bean'
        }


@app.route('/', methods = ['GET', 'POST'])
def index(): 
    return jsonify(data)

if __name__ == '__main__':
    app.run()