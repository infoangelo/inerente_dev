import os

SQLALCHEMY_DATABASE_URI = os.getenv('DB_CONN')
SECRET_KEY = os.getenv('SECRET_KEY')
