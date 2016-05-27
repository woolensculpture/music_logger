from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = '127.0.0.1/music_logger'
db = SQLAlchemy(app)


def connect():
    return 'Hello World!'


def add_track(json):
    return


def remove_track(json):
    return


def update_track(json):
    return


def search(json):
    return


if __name__ == '__main__':
    app.run()
