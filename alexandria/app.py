import os

from flask import Flask, render_template
from alexandria.extensions import db, migrate, bcrypt, login_manager

from alexandria.models import users, documentlinks

def create_app(config_setting='dev'):
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)

    if config_setting == 'prod': # only trigger SSLify if the app is running on Heroku
        #sslify = SSLify(app)
        from alexandria.settings import ProductionConfig
        #app.config.from_object('config.ProductionConfig')
        app.config.from_object(ProductionConfig)
    elif config_setting == 'test':
        from alexandria.settings import TestConfig
        #app.config.from_object('config.ProductionConfig')
        app.config.from_object(TestConfig)
    else:
        from alexandria.settings import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app

def register_extensions(app):
    #assets.init_app(app)
    bcrypt.init_app(app)
    #cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    #debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    #mail.init_app(app)
    return None


def register_blueprints(app):
    # Prevents circular imports
    #from linksApp.views import links
    from alexandria.views import users
    app.register_blueprint(users.blueprint)
    from alexandria.views import public
    app.register_blueprint(public.blueprint)
    from alexandria.views import documents
    app.register_blueprint(documents.blueprint)
    return None
    

def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


