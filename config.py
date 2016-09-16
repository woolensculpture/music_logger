"""configs of the music logger, to change which config is loaded(Production, Staging, Development) go to music_logger.py
 and change the class in the app.config.from_object()"""


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "secret?"
    DB_USER = 'root'
    DB_PASSWORD = ''
    DB_HOST = ''
    DB_NAME = 'music_logger'
    SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_NAME


class Production(Config):
    DB_USER = ''
    DB_PASSWORD = ''
    DB_HOST = ''
    DB_NAME = ''


class Staging(Config):
    DB_USER = ''
    DB_PASSWORD = ''
    DB_HOST = ''
    DB_NAME = ''
    TESTING = True


class Development(Config):
    TESTING = True
    DEBUG = True
    DB_USER = 'music_logger'
    DB_HOST = 'localhost'
    DB_NAME = 'music_logger'
