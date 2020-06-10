#!/bin/python3
"""
This script runs the Mess Management System
application using a development server.
"""

from os import environ

from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_login import current_user

from Mess_Management_System import app, db, google_blueprint
from Mess_Management_System.model.models import OAuth
from Mess_Management_System.view.adminviews import admin
from Mess_Management_System.view.userviews import user

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
