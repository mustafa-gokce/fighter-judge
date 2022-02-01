import os

VALID_USERNAME = "estu"
VALID_PASSWORD = "1234"
FILE_PATH = os.getcwd() + "/database/login.db"
TESTING = False
DEBUG = True
ENV = 'production'  # production
SECRET_KEY = 'mysecretkey'
SQLALCHEMY_DATABASE_URI = "sqlite:///" + FILE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False
