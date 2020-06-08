"""
The Admin views
"""
from datetime import timedelta
from io import BytesIO

from flask import Blueprint, flash, redirect, render_template, request, url_for
from PIL import Image
from functools import wraps

from Mess_Management_System import app, db, login_manager

from Mess_Management_System.model.models import Admin, Dishes
from Mess_Management_System.view.userviews import year

admin = Blueprint('admin', __name__,
                  static_folder='Mess_Management_System/static',
                  template_folder='Mess_Management_System/templates')


def requires_admin():
    """Checks if user is admin"""
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not Admin:
                return unauthorized()
            return f(*args, **kwargs)
        return wrapped
    return wrapper


@admin.route('/', methods=['GET', 'POST'])
def admin_login():
    """Login admin"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == app.config['ADMIN_USERNAME'] and \
                password == app.config['ADMIN_PASSWORD']:
            Admin.admin = True
            return redirect(url_for('admin.admin_dashboard'))
    return render_template(
        'admin.html',
        year=year
    )


@admin.route('/dashboard', methods=['GET'])
@requires_admin()
def admin_dashboard():
    """Admin Dashboard"""
    if Admin.admin:
        return render_template(
            'admin_dashboard.html',
            year=year
        )
    return unauthorized()


@admin.route('/logout', methods=['GET'])
@requires_admin()
def admin_logout():
    """Admin Logout"""
    Admin.admin = False
    return redirect(url_for('user.index'))


@admin.route('/add/dishes', methods=['GET', 'POST'])
@requires_admin()
def add_dishes():
    """Add Dish"""
    if request.method == 'POST':
        name = request.form['name']
        picture = request.files['picture']
        description = request.form['description']
        image = Image.open(picture)
        image_resized = image.resize((256, 256))
        buffer = BytesIO()
        image_resized.save(buffer, format='JPEG')
        price = request.form['price']
        cook_time = timedelta(minutes=int(request.form['cooktime']))
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
    """Unauthorized User"""
    flash("You are unauthorized to access the page!",
          category='warning')
    return redirect(url_for('user.index'))
