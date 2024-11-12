from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar')
    submit = SubmitField('Login')

class UpdateWordForm(FlaskForm):
    palavra = StringField('Palavra', validators=[DataRequired()])
    dica = StringField('Dica', validators=[DataRequired()])
    