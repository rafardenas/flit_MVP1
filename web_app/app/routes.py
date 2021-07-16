"""import os 
import sys
#sys.path.append(os.getcwd())

from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_migrate import Config, current 
from web_app.app import app, db
from web_app.app.forms import *

from flask_login import current_user, login_user, logout_user, login_required
from web_app.app.models import User, Post
from datetime import datetime
from web_app.config2 import Config


# routes are defined with the following decorator
# in flask, the routes/links are defined with python functions
#we use the functions to send the information e.g. the inference
#then, we use the render_template function to decode it and present it with the filled placeholders



"""






        

