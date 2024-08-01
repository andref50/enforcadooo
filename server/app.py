from flask import Flask, jsonify, request
from flask_cors import CORS
import schedule


app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={r'/*': {'origins': '*'}})


data = {
        'palavra': 'JUDOCA',
        'dica': 'Esporte',
        '_day': 0
        }


@app.route('/', methods = ['GET'])
def index(): 
    if request.method == 'GET':
        return jsonify(data)


if __name__ == '__main__':
    app.run()