import os
from dotenv import load_dotenv, find_dotenv

load_dotenv()

class Config(object):
    DB_SERVER = os.environ.get('DB_SERVER')
    DB_PORT = 5432
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME= os.environ.get('DB_NAME')
    SECRET_KEY=os.environ.get('SECRET_KEY')