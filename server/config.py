import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    CORS_HEADERS = 'Content-Type'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, '/database/wordlist_db')