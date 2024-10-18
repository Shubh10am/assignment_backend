import os
import mongoengine
from flask import g
from flask import Flask

from flask_cors import CORS


class BaseConfig(object):
    DEBUG = True
    JWT_IDENTITY_CLAIM = 'identity'
    JWT_TOKEN_LOCATION = ('headers',)
    JWT_COOKIE_CSRF_PROTECT = False
    MONGODB_SETTINGS = {
        "db": "ottermap_db",
        "host": "localhost",
        "port": 27017,
        "connect": False
    }


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = 'development'
    SECRET_KEY = 'test'
    JWT_SECRET_KEY = 'test'


class ProductionConfig(BaseConfig):
    DEBUG = False
    ENV = 'production'
    SECRET_KEY = os.getenv('SECRET_KEY', 'test')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'test')
    MONGODB_SETTINGS = {
        "db": "ottermap_db",
        "host": os.getenv('MONGO_HOST', 'mongodb+srv://shubham12342019:shubh123@cluster0.oymgv.mongodb.net/'),
        "connect": False
    }


def init_app():
    config = DevelopmentConfig    # for development
    # config = DevelopmentConfig if os.getenv('FLASK_ENV') == 'production' else ProductionConfig

    app.config.from_object(config)
    mongoengine.connect(**app.config["MONGODB_SETTINGS"])

    return app


def after_function(flask_app):
    @flask_app.after_request
    def add_header(response):
        response.headers['X-Client-Email'] = getattr(g, 'client_email', "")
        return response


app = Flask(__name__)
init_app()
after_function(app)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173"]}},
            methods=["GET", "POST", "PUT", "DELETE"], supports_credentials=True)
