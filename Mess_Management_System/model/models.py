"""
The database model
"""
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import UserMixin
from libgravatar import Gravatar

from Mess_Management_System import db


class User(UserMixin, db.Model):
    """User database class

    Args:
        UserMixin : Flask-Login Mixin   
        db : Database Model Base Class
    """
    __tablename__ = 'messusers'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    avatar = db.Column(db.Text, nullable=False,
                       default=Gravatar(str(email)).get_image())
    balance = db.Column(db.Float, nullable=True, default=0.0)
    total_balance = db.Column(db.Float, nullable=True, default=0.0)
    password = db.Column(db.Text, nullable=True, unique=False)
    admin = db.Column(db.Boolean, nullable=False, unique=False, default=False)


class Dishes(db.Model):
    """Dish database class

    Args:
        db : Database Model Base Class
    """
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    picture = db.Column(db.LargeBinary, nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    orders = db.relationship('Order', backref='orders',
                             cascade='all,delete', lazy=True)
    description = db.Column(db.Text, unique=False, nullable=False)
    cook_time = db.Column(db.Interval, unique=False, nullable=False)


class OAuth(OAuthConsumerMixin, db.Model):
    """OAuth database class

    Args:
        OAuthConsumerMixin : Flask-Dance Mixin
        db : Database Model Base Class
    """
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


class Order(db.Model):
    """User Order database class

    Args:
        db : Database Model Base Class
    """
    id = db.Column(db.Integer, primary_key=True, nullable=True, unique=True)
    user = db.Column(db.Integer, db.ForeignKey(User.id),
                     default=None, unique=False, nullable=True)
    order = db.Column(db.Integer, db.ForeignKey(Dishes.id),
                      default=None, unique=False, nullable=True)
    quantity = db.Column(db.Integer, unique=False, nullable=False, default=0)
    time = db.Column(db.DateTime, default=None, unique=False, nullable=True)
    price = db.Column(db.Float, default=0.0, unique=False, nullable=True)
