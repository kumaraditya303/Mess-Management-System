"""
The Admin views
"""
from datetime import timedelta

from io import BytesIO

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image
from werkzeug.security import check_password_hash

from Mess_Management_System import db, login_manager
from Mess_Management_System.model.models import Dishes, User
from Mess_Management_System.view.userviews import year

admin = Blueprint('admin', __name__,
                  static_folder='Mess_Management_System/static',
                  template_folder='Mess_Management_System/templates')


@admin.route('/', methods=['GET', 'POST'])
def admin_login():
    """Admin Login Route

    Returns:
        str: Admin Login template
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.admin and \
                check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin.admin_dashboard'))
        flash('Wrong Credentials!', category='warning')
        return redirect(request.url)
    return render_template(
        'admin.html',
        year=year
    )


@admin.route('/dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    """Admin Dashboard route

    Returns:
        str: Admin Dashboard template
    """

    if not current_user.admin:
        return unauthorized()
    return render_template(
        'admin_dashboard.html',
        year=year
    )


@admin.route('/logout', methods=['GET'])
@login_required
def admin_logout():
    """Admin logout route

    Returns:
        str: Redirect to homepage
    """
    if not current_user.admin:
        return unauthorized()
    logout_user()
    return redirect(url_for('user.index'))


@admin.route('/add/dishes', methods=['GET', 'POST'])
@login_required
def add_dishes():
    """Add dish to database

    Returns:
        str: Dish add template
    """
    if not current_user.admin:
        return unauthorized()
    if request.method == 'POST':
        name = request.form['name']
        picture = request.files['picture']
        description = request.form['description']
        image = Image.open(picture)
        image_resized = image.resize((256, 256))
        buffer = BytesIO()
        image_resized.save(buffer, format='JPEG')
        price = request.form['price']
        hours = int(request.form['cooktime'][:2])
        minutes = int(request.form['cooktime'][4:5])
        cook_time = timedelta(hours=hours, minutes=minutes)
        dish = Dishes(name=name,
                      picture=buffer.getvalue(),
                      price=price,
                      cook_time=cook_time,
                      description=description)
        db.session.add(dish)
        db.session.commit()
        flash(f"{name} dish added successfully!", category='success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template(
        'add_dish.html',
        year=year
    )


@login_manager.unauthorized_handler
def unauthorized():
    """Unauthorized warning route

    Returns:
        str: Redirect to homepage
    """
    flash("You are unauthorized to access the page!",
          category='warning')
    return redirect(url_for('user.index'))
