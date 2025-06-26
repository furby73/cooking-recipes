from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash

from app import app
from app.forms import AdminLoginForm
from app.models import AdminUser
from app.config import Config


@app.route('/')
@app.route('/index')
def index():
    recipes = [
        {
            "title" : "scrambled eggs",
            "description" : "tasty eggs made from eggs"
        },
        {
            "title" : "pasta",
            "description" : "a delicious pasta dish with a rich sauce"
        },
        {
            "title" : "chocolate cake",
            "description" : "a moist chocolate cake with creamy frosting"
        }
    ]
    return render_template('index.html', recipes=recipes)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if check_password_hash(Config.ADMIN_PASSWORD_HASH, form.password.data):
            login_user(AdminUser())
            flash('Logged in successfully.', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid password.', 'danger')
    return render_template('admin_login.html', form=form)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

# Admin logout
@app.route('/admin/logout')
def admin_logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('admin_login'))