"""
The flask application package
"""
from flask import Flask
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.google import make_google_blueprint
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)
from Mess_Management_System.models import OAuth
login_manager = LoginManager(app)
mail = Mail(app)
migrate = Migrate(app, db)
google_blueprint = make_google_blueprint(
    client_id=app.config['CLIENT_ID'],
    client_secret=app.config['CLIENT_SECRET'],
    scope=['profile', 'email'],
    reprompt_select_account=True,
    reprompt_consent=False, redirect_url='/login/oauth')
app.register_blueprint(google_blueprint, url_prefix='/google_login')
google_blueprint.backend = SQLAlchemyStorage(OAuth, db.session, current_user)

import Mess_Management_System.adminviews
import Mess_Management_System.userviews