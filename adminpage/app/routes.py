from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user
from app.forms import LoginForm, UpdateWordForm

import sqlalchemy as sa
from app import db
from app.models import User

from update import current_word, list_words, check_word_exist, update_word, create_new_word


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html', current_user=current_user, current_word=current_word(), list_words=list_words())

@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    form = UpdateWordForm()
    if form.validate_on_submit():
        palavra = check_word_exist(form.palavra.data)
        if palavra is not None:
            update_word(form.palavra.data)
            return redirect(url_for('index'))
        else:
            create_new_word(form.palavra.data, form.dica.data)
            return redirect(url_for('index'))
    return render_template('update.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or passsword')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))