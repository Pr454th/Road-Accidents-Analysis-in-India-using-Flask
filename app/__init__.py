from flask import Flask


def create_app(test_config=None):
    fapp = Flask(__name__)
    fapp.secret_key = 'super secret key'
    from . import app
    fapp.register_blueprint(app.bp)
    return fapp
