from flask import Flask
from config import Config
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from app.models import Data


app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r'/*': {'origins': '*'}}, support_credentials=True)


db = SQLAlchemy(app)

data = Data()

from app import models

