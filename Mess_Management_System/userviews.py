"""
The user views
"""
from datetime import datetime
from io import BytesIO
from flask import(render_template, redirect,
                  url_for, flash, send_file, request)
from flask_dance.contrib.google import google
from flask_login import current_user, login_required, login_user, logout_user

from Mess_Management_System import app, db, login_manager
from Mess_Management_System.models import Dishes, User

year = datetime.now().year


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET'])
def index():
    dishes = Dishes.query.all()
    if not dishes:
        flash("No dishes are available in Mess!",
              category='warning')
    return render_template(
        'index.html',
        year=year,
        dishes=dishes
    )


@app.route('/balance', methods=['GET', 'POST'])
@login_required
def balance():
    if request.method == 'POST':
        balance = request.form['balance']
        user = User.query.filter_by(id=current_user.id).first()
        user.balance += float(balance)
        user.total_balance += float(balance)
        db.session.commit()
        flash(f"₹ {balance} was added successfully to your Mess account!",
              category='success')
        return redirect(url_for('dashboard'))
    return render_template(
        'balance.html',
        year=datetime.now().year
    )


@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template(
        'dashboard.html',
        year=year
    )


@app.route('/login', methods=['GET'])
def login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    account = google.get('oauth2/v1/userinfo')
    account = account.json()
    email = account['email']
    name = account['name']
    avatar = account['picture']
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, name=name, avatar=avatar)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash("Logged in successfully!",
          category='success')
    return redirect(url_for('dashboard'))


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully",
          category='success')
    return redirect(url_for('index'))


@app.route('/dishes/<string:name>', methods=['GET'])
def dishes_picture(name):
    picture = Dishes.query.filter_by(name=name).first_or_404()
    return send_file(BytesIO(picture.picture),
                     mimetype='image/jpg', as_attachment=False,
                     attachment_filename=f"{name}.jpg")
