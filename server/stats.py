from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r'/*': {'origins': '*'}})

app.route('/', methods=['GET'])
def stats():
    return jsonify({'data': 'oiiii'})

if __name__ == '__main__':
    app.run()