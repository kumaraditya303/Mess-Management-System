"""
The user views
"""
from Mess_Management_System.models import Dishes, User
from Mess_Management_System import db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from flask_dance.contrib.google import google
from datetime import datetime
from io import BytesIO

from flask import (flash, redirect, render_template,
                   request, send_file, url_for, Blueprint)


year = datetime.now().year

user = Blueprint('user', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@user.route('/', methods=['GET'])
def index():
    """Homepage"""
    dishes = Dishes.query.all()
    if not dishes:
        flash("No dishes are available in Mess!",
              category='warning')
    return render_template(
        'index.html',
        year=year,
        dishes=dishes
    )


@user.route('/balance', methods=['GET', 'POST'])
@login_required
def balance():
    """Add balance to user account"""
    if request.method == 'POST':
        user_balance = request.form['balance']
        user = User.query.filter_by(id=current_user.id).first()
        user.balance += float(user_balance)
        user.total_balance += float(user_balance)
        db.session.commit()
        flash(f"₹ {user_balance} was added successfully to your Mess account!",
              category='success')
        return redirect(url_for('dashboard'))
    return render_template(
        'balance.html',
        year=datetime.now().year
    )


@user.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """User Dashboard"""
    return render_template(
        'dashboard.html',
        year=year
    )


@user.route('/login', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Wrong Credentials', category='warning')
        return redirect(url_for('userlogin'))
    return render_template(
        'login.html',
        year=year
    )


@user.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(
            request.form['password'], method='sha256')
        if not User.query.filter_by(email=email).first():
            user = User(name=name, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Registration success', category='success')
            return redirect(url_for('dashboard'))
        flash('User already exists!', category='warning')
        return redirect(url_for('register'))
    return render_template(
        'register.html',
        year=year
    )


@user.route('/login/oauth', methods=['GET'])
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


@user.route('/logout', methods=['GET'])
@login_required
def logout():
    """Logout User"""
    logout_user()
    flash("Logged out successfully",
          category='success')
    return redirect(url_for('index'))


@user.route('/dishes/<string:name>', methods=['GET'])
def dishes_picture(name):
    """Send Dish picture"""
    picture = Dishes.query.filter_by(name=name).first_or_404()
    return send_file(BytesIO(picture.picture),
                     mimetype='image/jpg', as_attachment=False,
                     attachment_filename=f"{name}.jpg")
