import os

from flask import Flask, redirect, url_for
from flask.ext.rq import RQ
from flask.ext.heroku import Heroku

from iatilib import db, redis


def create_app(**config):
    app = Flask('iatilib.frontend', static_url_path='/docs')

    app.config.update(config)

    Heroku(app)

    if "REDISTOGO_URL" in os.environ:
        app.config.update({
            'RQ_DEFAULT_HOST': app.config["REDIS_HOST"],
            'RQ_DEFAULT_PORT': app.config["REDIS_PORT"],
            'RQ_DEFAULT_PASSWORD': app.config['REDIS_PASSWORD']
        })

    db.init_app(app)
    redis.init_app(app)

    RQ(app)

    @app.route('/')
    def homepage():
        return redirect(url_for('static', filename='api/index.html'))

    @app.route('/error')
    def error():
        return redirect(url_for('static', filename='api/error/index.html'))

    from .api1 import api

    app.register_blueprint(api, url_prefix="/api/1")
    return app
