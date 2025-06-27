from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash

from app import app, db
from app.forms import AdminLoginForm
from app.models import AdminUser, Recipe, RecipeStep
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
        
        step_counter = 1
        while f'step-{step_counter}' in request.form:
            instruction = request.form[f'step-{step_counter}'].strip()
            if instruction:
                step = RecipeStep(
                    step_number=step_counter,
                    instruction=instruction,
                    recipe_id=recipe.id
                )
                db.session.add(step)
            step_counter += 1
        
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
        
        for step in recipe.steps:
            db.session.delete(step)
        
        step_counter = 1
        while f'step-{step_counter}' in request.form:
            instruction = request.form[f'step-{step_counter}'].strip()
            if instruction:
                step = RecipeStep(
                    step_number=step_counter,
                    instruction=instruction,
                    recipe_id=recipe.id
                )
                db.session.add(step)
            step_counter += 1
        
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
        scrambled_eggs = Recipe(
            title='Scrambled Eggs',
            shortname='scrambled-eggs',
            description='Tasty eggs made from eggs.'
        )
        scrambled_eggs.steps = [
            RecipeStep(step_number=1, instruction='Crack eggs'),
            RecipeStep(step_number=2, instruction='Whisk eggs'),
            RecipeStep(step_number=3, instruction='Cook them')
        ]
        
        pasta = Recipe(
            title='Pasta',
            shortname='pasta',
            description='A delicious pasta dish with a rich sauce.'
        )
        pasta.steps = [
            RecipeStep(step_number=1, instruction='Boil water'),
            RecipeStep(step_number=2, instruction='Add pasta'),
            RecipeStep(step_number=3, instruction='Drain pasta')
        ]
        
        chocolate_cake = Recipe(
            title='Chocolate Cake',
            shortname='chocolate-cake',
            description='A moist chocolate cake with creamy frosting.'
        )
        chocolate_cake.steps = [
            RecipeStep(step_number=1, instruction='Preheat oven'),
            RecipeStep(step_number=2, instruction='Mix dry ingredients in a bowl'),
            RecipeStep(step_number=3, instruction='Add ingredients and mix'),
            RecipeStep(step_number=4, instruction='Bake for 30 minutes')
        ]
        
        db.session.add(scrambled_eggs)
        db.session.add(pasta)
        db.session.add(chocolate_cake)
        db.session.commit()
@app.route('/')
@app.route('/index')
def index():
    recipes = Recipe.query.all()
    return render_template( 'index.html', recipes=recipes)
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

@app.route('/recipe/<string:shortname>')
def recipe_detail(shortname):
    recipe = Recipe.query.filter_by(shortname=shortname).first_or_404()
    return render_template('recipe_detail.html', recipe=recipe)