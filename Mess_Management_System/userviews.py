from datetime import datetime

from flask import redirect, render_template, url_for
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import google
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message

from Mess_Management_System import app, db, google_blueprint, login_manager
from Mess_Management_System.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template(
        'index.html', year=datetime.now().year)


@app.route('/dashboard')
@login_required
def dashboard():
    return f"Welcomr {current_user.email }"


@app.route('/login')
def login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    account = google.get('oauth2/v1/userinfo')
    account = account.json()
    email = account['email']
    name = account['name']
    avatar = account['picture']
    if not (user:=User.query.filter_by(email=email).first()):
        user = User(email=email, name=name, avatar=avatar)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('dashboard'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
