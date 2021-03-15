from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'views'
    FLASK_APP = 'app'

    MAIL_SERVER : 'smtp.ethereal.email'
    MAIL_PORT : 587
    MAIL_USE_TLS : True
    MAIL_DEBUG : True
    MAIL_USERNAME : 'madalyn.okuneva@ethereal.email'
    MAIL_PASSWORD : 'SrQxbcYkaNB8ZEarfV'
    MAIL_DEFAULT_SENDER : 'Teste <teste@teste.com.br>'


# Here, we set the inheritance of the ProdConfig with the Config
class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    DATABASE_URI = environ.get('DEV_DATABASE_URI')
