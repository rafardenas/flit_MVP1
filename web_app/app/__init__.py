import os 
import sys
from flask import Flask
from web_app.config2 import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_mail import Mail
from flask_bootstrap import Bootstrap





app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.init_app(app)
login.login_view = "auth_bp.login"
mail = Mail(app)
bootstrap = Bootstrap(app)


from web_app.app.auth.auth import auth_bp
from web_app.app.errors.errors import errors_bp
from web_app.app.main.main import main_bp
from web_app.app.user.user import user_bp
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(errors_bp, url_prefix="/error")
app.register_blueprint(main_bp)
app.register_blueprint(user_bp, url_prefix="/user")

#db.create_all()
#db.drop_all()

if not app.debug:
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

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Microblog startup")

from web_app.app import routes, models

        











