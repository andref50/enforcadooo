from flask import Flask, render_template, jsonify

app = Flask(__name__, static_folder="vuejs/dist/assets", template_folder="vuejs/dist")

@app.route('/', methods=['GET'])
def jinja():
   data_for_js = {
        'username': 'Alice',
        'user_id': 123,
        'settings': {'theme': 'dark', 'notifications': True}
    }
   return render_template('index.html', data=data_for_js)

if __name__ == "__main__":
   app.run()