from flask import Flask, jsonify, request
from flask_cors import CORS
import schedule
import threading


app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={r'/*': {'origins': '*'}})


def update_days():
    data['curDay'] += 1
    print(data['curDay'])


data = {
        'palavra': 'JUDOCA',
        'dica': 'Esporte',
        'curDay': 0
        }

schedule.every(10).seconds.do(update_days)


@app.route('/', methods = ['GET'])
def index(): 
    if request.method == 'GET':
        return jsonify(data)


if __name__ == '__main__':
    app.run()
    while True:
        schedule.run_pending();
