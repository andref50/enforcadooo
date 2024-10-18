import os
from sys import platform

if platform == 'win32':
    from dotenv import load_dotenv

import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

if platform == 'win32':
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(BASEDIR, '.env'))
key = os.getenv('API_KEY')

def encrypt (raw):
    raw = pad(raw.encode(), 16)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(raw))

app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={r'/*': {'origins': '*'}})

data = {}

# SQLITE3 DATABASE CONNECTION
path = os.path.dirname(os.path.abspath(__file__))
if platform == 'win32':
    db = os.path.join(path, 'database/wordlist_db__dev')
    print(f'┌───────────────────────────────────┐')
    print(f'│   UTILIZANDO BANCO DE DADOS DEV   │')
    print(f'│               {platform}               │')
    print(f'└───────────────────────────────────┘')
else:
    db = os.path.join(path, 'database/wordlist_db')
    print(f'┌───────────────────────────────────┐')
    print(f'│  UTILIZANDO BANCO DE DADOS PROD   │')
    print(f'│               {platform}               │')
    print(f'└───────────────────────────────────┘')

    
# RETRIEVE DATA
with sqlite3.connect(db) as conn:
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM WORDLIST WHERE ativa=True;")
    word_query = cursor.fetchone()

    cursor.execute("SELECT * FROM curDay")
    curDay_query = cursor.fetchone()

    # data['palavra'] = word_query[1]
    data['palavra'] = encrypt(word_query[1]).decode('utf-8', 'ignore')
    data['dica']    = word_query[2]
    data['curDay']  = curDay_query[0]

def update_word():
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        # UPDATE curDay AT BEGINNING    
        cursor.execute("UPDATE curDay SET curDay=curDay + 1")
        cursor.execute("UPDATE WORDLIST SET ativa=False WHERE ativa=True;")

        cursor.execute("SELECT * FROM usedCount")
        usedCount_query = cursor.fetchone()

        cursor.execute(f"SELECT * FROM WORDLIST WHERE used={usedCount_query[0]} ORDER BY RANDOM() LIMIT 1")
        word_query = cursor.fetchone()

        if not word_query:
            cursor.execute("UPDATE usedCount SET usedCount=usedCount + 1")
            cursor.execute("SELECT * FROM usedCount")
            usedCount_query = cursor.fetchone()
            cursor.execute(f"SELECT * FROM WORDLIST WHERE used={usedCount_query[0]} ORDER BY RANDOM() LIMIT 1")
            word_query = cursor.fetchone()

        cursor.execute("SELECT * FROM curDay")
        curDay_query = cursor.fetchone()

        # data['palavra'] = word_query[1]
        data['palavra'] = encrypt(word_query[1]).decode('utf-8', 'ignore')
        data['dica']    = word_query[2]
        data['curDay']  = curDay_query[0]

        cursor.execute(f"UPDATE WORDLIST SET used={usedCount_query[0]} + 1, ativa=True WHERE ID={word_query[0]}")

        conn.commit()


scheduler = BackgroundScheduler()
scheduler.add_job(update_word, 'cron', hour=3)
# scheduler.add_job(update_word, 'interval', minutes=1)
scheduler.start()


@app.route('/', methods = ['GET', 'POST'])
def index(): 
    if request.method == 'GET':
        return jsonify(data)
    
    if request.method == 'POST':
        path = os.path.dirname(os.path.abspath(__file__))
        if platform == 'win32':
            db = os.path.join(path, 'database/wordlist_db__dev')
        else:
            db = os.path.join(path, 'database/wordlist_db')
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()

            asd = request.json

            if(asd['status'] == 'winner'):
                cursor.execute(f"UPDATE WORDLIST SET acertos=acertos+1 WHERE ativa=True;")

            elif(asd['status'] == 'lost'):
                cursor.execute(f"UPDATE WORDLIST SET erros=erros+1 WHERE ativa=True;")

            conn.commit()

        return jsonify(asd)


if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0')
