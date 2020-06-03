#!/bin/python3
"""
This script runs the Library_Management_System application using a development server.
"""

from os import environ
from Mess_Management_System import app
from Mess_Management_System import db

if __name__ == '__main__':
    db.create_all()
    environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '8000'))
    except ValueError:
        PORT = 8000
    app.run(HOST, PORT, threaded=True)
