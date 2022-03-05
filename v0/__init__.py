import os

from flask import Flask
from flask_cors import CORS

from . import auth
from . import db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # initiliaze database
    db.init_app(app)

    # enable CORS
    CORS(app, origins=["https://127.0.0.1:8080","http://127.0.0.1:8080"], supports_credentials=True)

    app.register_blueprint(auth.bp)

    return app
