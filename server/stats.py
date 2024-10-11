from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r'/*': {'origins': '*'}})

app.route('/', methods=['GET'])
def stats():
    return '<h1>Oiii</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)