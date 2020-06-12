#!/bin/python3
"""
This script runs the Mess Management System
application using a development server.
"""

from os import environ

from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_login import current_user

from Mess_Management_System import app, db, google_blueprint
from Mess_Management_System.model.models import OAuth, User
from Mess_Management_System.view.adminviews import admin
from Mess_Management_System.view.userviews import user
from getpass import getpass
import re
from werkzeug.security import generate_password_hash


@app.cli.command("createsuperuser")
def createsuperuser():
    name = input('Name: ')
    email = input('Email: ')
    while not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        print('Invalid email address, enter again!')
        email = input('Email: ')
    password = getpass()
    while len(password) < 8:
        print('Password is too short!')
        password = getpass()
    password = generate_password_hash(password, method='sha256')
    if not User.query.filter_by(email=email).first():
        admin = User(name=name, email=email,
                     password=password, admin=True)
        db.session.add(admin)
        db.session.commit()
        print('Admin User created successfullt!')
    else:
        print('Admin User already exists!')


if __name__ == '__main__':
    db.create_all()
    app.register_blueprint(google_blueprint, url_prefix='/google_login')
    google_blueprint.backend = SQLAlchemyStorage(
        OAuth, db.session, current_user)
    app.register_blueprint(user)
    app.register_blueprint(admin, url_prefix='/admin')
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '8000'))
    except ValueError:
        PORT = 8000
    app.run(HOST, PORT, threaded=True)
