import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://miguel:JfSKUWcn15$@192.168.122.133/scott'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
