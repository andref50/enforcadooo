from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def stats():
    if request.method == 'GET':
        print('oi')
        return '<h1>Oiii</h1>'

if __name__ == '__main__':
    app.run()