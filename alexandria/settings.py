import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'you-do-not-know-how-it-feels-to-be-me'
    POSTS_PER_PAGE = 20
    #if 'DYNO' in os.environ:
    #    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    #else:
    #    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost:5432/local_ese'

class DevelopmentConfig(Config):
    ENV = 'dev'
    DEVELOPMENT = True
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost:5432/local_dse'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #if 'DYNO' in os.environ:
    #    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    #else:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost:5432/local_alexandria'

class ProductionConfig(Config):
    ENV = 'prod'
    DEVELOPMENT = False
    DEBUG = False
    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost:5432/local_dse'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    if 'DYNO' in os.environ:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    else:
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost:5432/local_alexandria'

class TestConfig(Config):
    ENV = 'test'
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost:5432/test_alexandria'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False  # Allows form testing
    #if 'DYNO' in os.environ:
    #    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    #else:
    #    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost:5432/local_ese'