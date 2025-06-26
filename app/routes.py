from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash

from app import app, db
from app.forms import AdminLoginForm
from app.models import AdminUser, Recipe
from app.config import Config

from slugify import slugify 

@app.route('/admin/recipes')
@login_required
def admin_recipes():
    recipes = Recipe.query.order_by(Recipe.title).all()
    return render_template('admin_recipes.html', recipes=recipes)

@app.route('/admin/recipes/new', methods=['GET', 'POST'])
@login_required
def new_recipe():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        shortname = slugify(title)
        recipe = Recipe(title=title, shortname=shortname, description=description)
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe created.', 'success')
        return redirect(url_for('admin_recipes'))
    return render_template('recipe_form.html', action='New', recipe=None)

@app.route('/admin/recipes/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    if request.method == 'POST':
        recipe.title = request.form['title']
        recipe.description = request.form['description']
        recipe.shortname = slugify(recipe.title)
        db.session.commit()
        flash('Recipe updated.', 'success')
        return redirect(url_for('admin_recipes'))
    return render_template('recipe_form.html', action='Edit', recipe=recipe)

@app.route('/admin/recipes/<int:id>/delete', methods=['POST'])
@login_required
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted.', 'info')
    return redirect(url_for('admin_recipes'))
@app.before_request
def seed_data():
    if not Recipe.query.first():
        sample = [
            Recipe(title='Scrambled Eggs', shortname='scrambled-eggs', description='Tasty eggs made from eggs.'),
            Recipe(title='Pasta',          shortname='pasta',          description='A delicious pasta dish with a rich sauce.'),
            Recipe(title='Chocolate Cake',  shortname='chocolate-cake', description='A moist chocolate cake with creamy frosting.')
        ]
        db.session.bulk_save_objects(sample)
        db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    recipes = Recipe.query.all()
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

@app.route('/admin/logout')
def admin_logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('admin_login'))