"""
The user views
"""
from datetime import datetime
from io import BytesIO
import json
from flask import (Blueprint, flash, redirect, render_template, request,
                   send_file, url_for, jsonify)
from flask_dance.contrib.google import google
from flask_login import current_user, login_required, login_user, logout_user
from itsdangerous import BadSignature, BadTimeSignature, SignatureExpired
from werkzeug.security import check_password_hash, generate_password_hash

from Mess_Management_System import app, db, login_manager, serializer
from Mess_Management_System.model.models import Dishes, User, Order
from Mess_Management_System.notifiers.passwordreset import password_reset_email
from Mess_Management_System.notifiers.registration import registration_email
year = datetime.now().year

user = Blueprint('user', __name__,
                 static_folder='Mess_Management_System/static',
                 template_folder='Mess_Management_System/templates/')


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
        return redirect(url_for('user.dashboard'))
    return render_template(
        'balance.html',
        year=datetime.now().year
    )


@user.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """User Dashboard"""
    order_history = Order.query.filter_by(id=current_user.id).all()
    return render_template(
        'dashboard.html',
        year=year,
        orders=order_history
    )


@user.route('/login', methods=['GET', 'POST'])
def userlogin():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and password:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('user.dashboard'))
        flash('Wrong Credentials', category='warning')
        return redirect(url_for('user.userlogin'))
    return render_template(
        'login.html',
        year=year
    )


@user.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
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
            registration_email(app=app, email=email, url=url_for(
                'user.index', _external=True))
            flash('Registration success', category='success')
            return redirect(url_for('user.dashboard'))
        flash('User already exists!', category='warning')
        return redirect(url_for('user.register'))
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
    return redirect(url_for('user.dashboard'))


@user.route('/logout', methods=['GET'])
@login_required
def logout():
    """Logout User"""
    logout_user()
    flash("Logged out successfully",
          category='success')
    return redirect(url_for('user.index'))


@user.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        if User.query.filter_by(email=email).first():
            flash('Password reset link sent to your email!',
                  category='success')
            url = url_for('user.forgot_password', token=serializer.dumps(
                email, salt='reset-password'), _external=True)
            password_reset_email(app=app, email=[email], url=url)
            return redirect(url_for('user.index'))
        flash('Email is not registered!', category='warning')
        return redirect(url_for('user.forgot'))
    return render_template(
        'reset.html',
        year=year
    )


@user.route('/forgot/<token>', methods=['GET', 'POST'])
def forgot_password(token):
    if request.method == 'POST':
        try:
            email = serializer.loads(
                token, salt='reset-password', max_age=3600)
        except (SignatureExpired, BadSignature, BadTimeSignature):
            flash('Reset link is expired or invalid!', category='warning')
            return redirect(url_for('user.forgot'))
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if not check_password_hash(user.password, password):
            user.password = generate_password_hash(password, method='sha256')
            db.session.commit()
            flash('Password reset was success!', category='success')
            return redirect(url_for('user.userlogin'))
        flash("Same password cannot be changed", category='warning')
        return redirect(request.url)
    return render_template(
        'reset_password.html',
        year=year,
        token=token
    )


@user.route('/dishes/<string:name>', methods=['GET'])
def dishes_picture(name):
    """Send Dish picture"""
    picture = Dishes.query.filter_by(name=name).first_or_404()
    return send_file(BytesIO(picture.picture),
                     mimetype='image/jpg', as_attachment=False,
                     attachment_filename=f"{name}.jpg")


@user.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    price = 0
    if request.method == 'POST':
        form = dict(request.form)
        form = {k: v for (k, v) in form.items() if not v == '0'}
        for dish, quantity in form.items():
            dish_ordered = Dishes.query.filter_by(name=dish).first()
            price += dish_ordered.price*int(quantity)
        if current_user.balance > price:
            for dish, quantity in form.items():
                dish_ordered = Dishes.query.filter_by(name=dish).first()
                order = Order(user=current_user.id,
                              order=dish_ordered.id,
                              quantity=int(quantity),
                              price=int(quantity)*dish_ordered.price,
                              time=datetime.now())
                db.session.add(order)
            current_user.balance -= price
            db.session.commit()
            flash('Food ordered successfully!', category='success')
            return redirect(url_for('user.dashboard'))
        flash('You don\'t have enough balance!', category='warning')
        return redirect(url_for('user.order'))
    return render_template(
        'order.html',
        year=year,
        dishes=Dishes.query.all()
    )
