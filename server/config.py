import os
from dotenv import load_dotenv

parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

load_dotenv()

class Config:
    CORS_HEADERS = 'Content-Type'
    #SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(parentdir, os.getenv('DATABASE_URL'))
    KEY = os.getenv('CIPHER_KEY')  
    DEV_PROD = os.getenv('DEV_PROD')

# config = Config()
# print(config.SQLALCHEMY_DATABASE_URI)