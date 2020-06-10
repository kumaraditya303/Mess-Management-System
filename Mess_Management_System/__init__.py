"""
The flask application package
"""

from flask import Flask
from flask_dance.contrib.google import make_google_blueprint
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
# login_manager.session_protection = 'strong'
mail = Mail(app)
migrate = Migrate(app, db)
google_blueprint = make_google_blueprint(
    client_id=app.config['CLIENT_ID'],
    client_secret=app.config['CLIENT_SECRET'],
    scope=['profile', 'email'],
    reprompt_select_account=True,
    reprompt_consent=False, redirect_url='/login/oauth')
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
