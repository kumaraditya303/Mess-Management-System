"""
The database model
"""
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import UserMixin
from libgravatar import Gravatar

from Mess_Management_System import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    avatar = db.Column(db.Text, nullable=False,
                       default=Gravatar(str(email)).get_image())
    balance = db.Column(db.Float, nullable=True, default=0.0)
    order_history = db.Column(db.JSON, nullable=True,default='')
    total_balance = db.Column(db.Float, nullable=True, default=0.0)
    password = db.Column(db.Text, nullable=True, unique=False, default=None)


class Dishes(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    picture = db.Column(db.LargeBinary, unique=False, nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    description = db.Column(db.Text, unique=False, nullable=False)
    cook_time = db.Column(db.Interval, unique=False, nullable=False)


class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


class Admin:
    admin = False
