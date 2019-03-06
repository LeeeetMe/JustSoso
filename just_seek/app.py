from flask import Flask
from flask_redis import FlaskRedis

redis_store = FlaskRedis()


def create_app(config_object='just_seek.settings'):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    redis_store.init_app(app)
    return app
