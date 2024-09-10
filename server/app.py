import os
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={r'/*': {'origins': '*'}})

# SQLITE3 DATABASE CONNECTION
path = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(path, 'database/wordlist_db')
conn = sqlite3.connect(db)
cursor = conn.cursor()

data = {}

# RETRIEVE DATA
cursor.execute("SELECT * FROM WORDLIST WHERE ativa=True;")
word_query = cursor.fetchone()

cursor.execute("SELECT * FROM curDay")
curDay_query = cursor.fetchone()

data['palavra'] = word_query[1]
data['dica']    = word_query[2]
data['curDay']  = curDay_query[0]

conn.close()

def update_word():
    conn = sqlite3.connect(db)
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
        word_query = cursor.fetchall()

    cursor.execute("SELECT * FROM curDay")
    curDay_query = cursor.fetchone()

    data['palavra'] = word_query[1]
    data['dica']    = word_query[2]
    data['curDay']  = curDay_query[0]

    cursor.execute(f"UPDATE WORDLIST SET used={usedCount_query[0]} + 1, ativa=True WHERE ID={word_query[0]}")

    conn.commit()
    conn.close()


scheduler = BackgroundScheduler()
scheduler.add_job(update_word, 'interval', hours=1)
scheduler.start()


@app.route('/', methods = ['GET'])
def index(): 
    if request.method == 'GET':
        return jsonify(data)


if __name__ == '__main__':
    app.run()
