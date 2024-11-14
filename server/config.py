import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

class Config:
    CORS_HEADERS = 'Content-Type'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    KEY = os.getenv('API_KEY')
    DEV_PROD = os.getenv('DEV_PROD')