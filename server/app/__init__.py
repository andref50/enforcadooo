from flask import Flask
from config import Config
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv

from app.models import Data


app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r'/*': {'origins': '*'}})

db = SQLAlchemy(app)

data = Data()

load_dotenv()

from app import models

