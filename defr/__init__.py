import os

from flask import Flask
from defr.filp import settings

from flask_sqlalchemy import SQLAlchemy


def create_app(test_config=None):
    app=Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = f"postgresql://{settings['pguser']}:{settings['pgpass']}@{settings['pghost']}:{settings['pgport']}/{settings['pgdb']}",
        SQALCHEMY_TRACK_MODIFICATIONS = False
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

        
    @app.route('/hello')
    def hello():
        return "Hello, World"
    
    from .tables import db
    db.init_app(app)

    from . import route
    app.register_blueprint(route.bp)
    
    

    return app
