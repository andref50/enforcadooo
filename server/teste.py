import os
import sqlite3
from flask import Flask, jsonify, request

# app = Flask(__name__)

# data = {
#         'palavra': 'PALÍNDROMO',
#         'dica': 'Gramática',
#         'curDay': 3
#         }

# @app.route('/', methods = ['GET'])
# def index(): 
#     if request.method == 'GET':
#         return jsonify(data)

path = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(path, 'database/wordlist_db')

conn = sqlite3.connect(db)
cursor = conn.cursor()
cursor.execute("SELECT * FROM WORDLIST WHERE used=False ORDER BY RANDOM() LIMIT 1;")
select = cursor.fetchall()

data = {
        'palavra': select[0][1],
        'dica': select[0][2],
        'curDay': 3
        }

print(select[0])
print(data)

cursor.execute(f"UPDATE WORDLIST SET used=True WHERE ID={select[0][0]}")
cursor.execute(f"UPDATE WORDLIST SET ativa=True WHERE ID={select[0][0]}")
conn.commit()

conn.close()

# if __name__ == '__main__':
    # app.run()