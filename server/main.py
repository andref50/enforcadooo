from app import app, data
from app.updates import update_word, refresh_word, update_placar

from flask import jsonify, request, render_template
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()
scheduler.add_job(update_word, 'cron', hour=3)
scheduler.add_job(refresh_word, 'interval', minutes=1)
scheduler.start()


@app.route('/', methods = ['GET', 'POST'])
def index(): 
    if request.method == 'GET':
        response = data.to_dict()
        return render_template('index.html', data=response)
    
    if request.method == 'POST':
        req = request.json
        update_placar(req)
        return jsonify(req)

if __name__ == '__main__':
    app.run()