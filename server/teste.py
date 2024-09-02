from flask import Flask, jsonify, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={r'/*': {'origins': '*'}})


def update_days():
    print('oi')


scheduler = BackgroundScheduler()
scheduler.add_job(update_days, trigger='cron', hour=12, minute=6)
scheduler.start()


data = {
        'palavra': 'PALÍNDROMO',
        'dica': 'Gramática',
        'curDay': 3
        }

@app.route('/', methods = ['GET'])
def index(): 
    if request.method == 'GET':
        return jsonify(data)


if __name__ == '__main__':
    app.run()