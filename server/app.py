from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={r'/*': {'origins': '*'}})


data = {
        '_id': 0,
        'title': 'Mr.Bean'
        }

# data_json = data.json()

accepted = {
    'status': 'OK'
}


@app.route('/', methods = ['GET', 'POST'])
def index(): 
    if request.method == 'GET':
        return jsonify(data)
    if request.method == 'POST':
        return jsonify(accepted)


if __name__ == '__main__':
    app.run()