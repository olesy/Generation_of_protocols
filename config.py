import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "nhuJu3"
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT") or "nhuJu3r"
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                              'postgresql+psycopg2://postgres:nhuJu3@localhost:5432/' \
                              'doc_api?client_encoding = utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or False
    BABEL_DEFAULT_LOCALE = "ru"