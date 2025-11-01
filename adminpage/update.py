import os
import sqlite3

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_stats = basedir + '/server/database/wordlist_db__dev' 


def current_word():
    data = {}
    with sqlite3.connect(db_stats) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM WORDLIST WHERE ativa=True;")
        word_query = cursor.fetchone()
        data['id']      = word_query[0]
        data['palavra'] = word_query[1]
        data['dica']    = word_query[2]
        data['acertos'] = word_query[3]
        data['erros']   = word_query[4]

        return data
    
def list_words():
    with sqlite3.connect(db_stats) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM WORDLIST WHERE used=True;")
        word_query = cursor.fetchall()

        return word_query
    
def check_word_exist(palavra):
    with sqlite3.connect(db_stats) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM WORDLIST WHERE palavra='{palavra}';")
        word_query = cursor.fetchone()

        return word_query
    
def update_word(palavra):
    with sqlite3.connect(db_stats) as conn:
        cursor = conn.cursor()

        cursor.execute("UPDATE WORDLIST SET ativa=False WHERE ativa=True;")
        cursor.execute(f"UPDATE WORDLIST SET ativa=True WHERE palavra='{palavra}';")
        cursor.execute("UPDATE curDay SET curDay=curDay+1")

def create_new_word(palavra, dica):
    with sqlite3.connect(db_stats) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usedCount")
        contador = cursor.fetchone()

        cursor.execute("UPDATE WORDLIST SET ativa=False WHERE ativa=True;")
        cursor.execute(f"INSERT INTO WORDLIST (palavra, dica, acertos, erros, used, ativa) VALUES ('{palavra.lower()}', '{dica.capitalize()}', 0, 0, {contador[0]+1}, True);")
        cursor.execute("UPDATE curDay SET curDay=curDay+1")

