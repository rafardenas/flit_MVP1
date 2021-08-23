import os
from dotenv import load_dotenv
#sys.path.append(os.getcwd())
#sys.path.append('.')
#basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.abspath(".")
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://' + os.environ.get('DBUSER') + ':' + os.environ.get('DBPASS') + '@' + os.environ.get('DBSERVER') + '/' + os.environ.get('DBNAME') 
    SQLALCHEMY_DATABASE_URI= 'postgresql://yfbificbrvdrqc:11aa198971d2355884a02ee13cb9069ee840f2c9e79ed5439d1989e965db09f7@ec2-52-1-20-236.compute-1.amazonaws.com:5432/d4006onmci8j0o'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
    #    'postgres://', 'postgresql://') or \
    #    'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['rafardenas@gmail.com']
    POSTS_PER_PAGE = 25
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or "http://localhost:9200"
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    API_KEY_SENDGRID = os.environ.get('API_KEY_SENDGRID')


    




    