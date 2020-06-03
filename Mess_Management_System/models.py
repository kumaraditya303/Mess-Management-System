"""
The database model
"""
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import UserMixin
from Mess_Management_System import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=True)
    avatar = db.Column(db.Text, nullable=False)


class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
