import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request

app = Flask(__name__)

load_dotenv()
KEY = os.getenv('API_KEY')
DEV_PROD = os.getenv('DEV_PROD')

print(KEY)
print(DEV_PROD)

@app.route('/', methods=['GET'])
def stats():
    if request.method == 'GET':
        print('oi')
        return '<h1>Oiii</h1>'

if __name__ == '__main__':
    app.run()
