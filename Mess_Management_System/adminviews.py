"""
The Admin views
"""
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image

from flask import (Flask, flash, redirect, render_template, render_template,
                   request, url_for)
from Mess_Management_System import app, db, login_manager
from Mess_Management_System.models import Admin, Dishes, User
from Mess_Management_System.userviews import year


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == app.config['ADMIN_USERNAME'] and \
                password == app.config['ADMIN_PASSWORD']:
            Admin.admin = True
            return redirect(url_for('admin_dashboard'))
    return render_template(
        'admin.html',
        year=year
    )


@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    if Admin.admin == True:
        return render_template(
            'admin_dashboard.html',
            year=year
        )
    return unauthorized()


@app.route('/admin/logout', methods=['GET'])
def admin_logout():
    Admin.admin = False
    return redirect(url_for('index'))


@app.route('/add/dishes', methods=['GET', 'POST'])
def add_dishes():
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
        dish = Dishes(name=name, picture=buffer.getvalue(),
                      price=price, cook_time=cook_time, description=description)
        db.session.add(dish)
        db.session.commit()
        flash(f"{name} dish added successfully!", category='success')
        return redirect(url_for('admin_dashboard'))
    return render_template(
        'add_dish.html',
        year=year
    )


@login_manager.unauthorized_handler
def unauthorized():
    flash("You are unauthorized to access the page!",
          category='warning')
    return redirect(url_for('index'))
