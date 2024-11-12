from app import login, db
from app.models import User

from flask import redirect, url_for

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

@login.unauthorized_handler
def unauthorized_user():
    return redirect(url_for('login'))