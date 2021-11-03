from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from application.config import Config
from elasticsearch import Elasticsearch


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

def aed(value):
    return "AED {:,.2f}".format(value)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    from application.users.routes import users
    from application.listings.routes import listings
    from application.main.routes import main
    from application.errors.handlers import errors

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    app.jinja_env.globals.update(aed=aed)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    app.register_blueprint(users)
    app.register_blueprint(listings)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
