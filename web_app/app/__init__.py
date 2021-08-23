import os 
from flask import Flask, current_app
from web_app.config2 import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from elasticsearch import Elasticsearch
import psycopg2




db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth_bp.login"
login.login_message = ('Por favor inicia sesion para ver los fletes disponibles')
mail = Mail()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)


    from web_app.app.auth.auth import auth_bp
    from web_app.app.errors.errors import errors_bp
    from web_app.app.main.main import main_bp
    from web_app.app.user.user import user_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(errors_bp, url_prefix="/error")
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix="/user")
    #app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None
    #DATABASE_URL = os.environ['DATABASE_URL']
    #psycopg2.connect(database='db', user='user', host='host', password='pwwd', port='port', sslmode='require')
    #psycopg2.connect(C, sslmode='require')

    
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            #===========SMTPHandler:

            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            # app.logger.addHandler(mail_handler) Uncoment to send log through email

            #==========RotatingFile Handler
            if app.config['LOG_TO_STDOUT']:
                stream_handler = logging.StreamHandler()
                stream_handler.setLevel(logging.INFO)
                app.logger.addHandler(stream_handler)

            else:
                if not os.path.exists('logs'):
                    os.mkdir('logs')
                file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
                file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
                file_handler.setLevel(logging.INFO)
                app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Flit_beta startup")
    
    return app

from web_app.app import routes, models

        











