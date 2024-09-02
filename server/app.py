import random
from flask import Flask, jsonify, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={r'/*': {'origins': '*'}})

data = {'curDay': 0}


def update_word():
    with open("WORDLIST", "r", encoding='utf-8') as f:
        lines = f.readlines()

    selection = random.randint(0, len(lines) - 1)

    palavra = lines[selection].split(',')[0].strip()
    dica = lines[selection].split(',')[1].split('\n')[0].strip()

    data['word'] = palavra
    data['tip'] = dica
    data['curDay'] += 1


scheduler = BackgroundScheduler()
scheduler.add_job(update_word, trigger='interval', seconds=60)
scheduler.start()


@app.route('/', methods = ['GET'])
def index(): 
    if request.method == 'GET':
        return jsonify(data)


if __name__ == '__main__':
    app.run()
