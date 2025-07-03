from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from app import app, db
from app.forms import AdminLoginForm
from app.models import AdminUser, Recipe, RecipeStep
from app.config import Config
from app.s3_helpers import upload_file, delete_file, create_bucket_if_not_exists
from slugify import slugify

@app.before_request
def init_s3():
    create_bucket_if_not_exists()

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
        
        # Handle cover image
        cover_image_url = None
        cover_image_file = request.files.get('cover_image')
        if cover_image_file and cover_image_file.filename != '':
            cover_image_url = upload_file(
                cover_image_file.stream,
                cover_image_file.filename,
                'covers'
            )
        
        recipe = Recipe(
            title=title,
            shortname=shortname,
            description=description,
            cover_image=cover_image_url
        )
        db.session.add(recipe)
        db.session.commit()
        
        # Add steps
        step_counter = 1
        while f'step-{step_counter}' in request.form:
            instruction = request.form[f'step-{step_counter}'].strip()
            if instruction:
                # Handle step image
                step_image_url = None
                step_image_file = request.files.get(f'step-image-{step_counter}')
                if step_image_file and step_image_file.filename != '':
                    step_image_url = upload_file(
                        step_image_file.stream,
                        step_image_file.filename,
                        'steps'
                    )
                
                step = RecipeStep(
                    step_number=step_counter,
                    instruction=instruction,
                    image=step_image_url,
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
        
        # Handle cover image update
        if 'remove_cover_image' in request.form and recipe.cover_image:
            delete_file(recipe.cover_image)
            recipe.cover_image = None
        else:
            cover_image_file = request.files.get('cover_image')
            if cover_image_file and cover_image_file.filename != '':
                # Delete old image if exists
                if recipe.cover_image:
                    delete_file(recipe.cover_image)
                # Upload new image
                recipe.cover_image = upload_file(
                    cover_image_file.stream,
                    cover_image_file.filename,
                    'covers'
                )
        
        # Process steps
        existing_steps = {step.step_number: step for step in recipe.steps}
        new_step_numbers = []
        step_counter = 1
        
        while f'step-{step_counter}' in request.form:
            instruction = request.form[f'step-{step_counter}'].strip()
            if instruction:
                # Find existing step or create new
                step = existing_steps.get(step_counter)
                if not step:
                    step = RecipeStep(step_number=step_counter, recipe_id=recipe.id)
                
                step.instruction = instruction
                
                # Handle step image removal
                if f'remove_step_image-{step_counter}' in request.form and step.image:
                    delete_file(step.image)
                    step.image = None
                
                # Handle new step image upload
                step_image_file = request.files.get(f'step-image-{step_counter}')
                if step_image_file and step_image_file.filename != '':
                    # Delete old image if exists
                    if step.image:
                        delete_file(step.image)
                    # Upload new image
                    step.image = upload_file(
                        step_image_file.stream,
                        step_image_file.filename,
                        'steps'
                    )
                
                db.session.add(step)
                new_step_numbers.append(step_counter)
            step_counter += 1
        
        # Delete steps that were removed
        for step_num, step in existing_steps.items():
            if step_num not in new_step_numbers:
                if step.image:
                    delete_file(step.image)
                db.session.delete(step)
        
        db.session.commit()
        flash('Recipe updated.', 'success')
        return redirect(url_for('admin_recipes'))
    
    return render_template('recipe_form.html', action='Edit', recipe=recipe)

@app.route('/admin/recipes/<int:id>/delete', methods=['POST'])
@login_required
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    
    # Delete cover image
    if recipe.cover_image:
        delete_file(recipe.cover_image)
    
    # Delete step images
    for step in recipe.steps:
        if step.image:
            delete_file(step.image)
    
    # Delete recipe
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted.', 'info')
    return redirect(url_for('admin_recipes'))

@app.before_request
def seed_data():
    if not Recipe.query.first():
        # Create sample recipes with their steps
        scrambled_eggs = Recipe(
            title='Scrambled Eggs',
            shortname='scrambled-eggs',
            description='Tasty eggs made from eggs.'
        )
        scrambled_eggs.steps = [
            RecipeStep(step_number=1, instruction='Crack eggs into a bowl'),
            RecipeStep(step_number=2, instruction='Whisk eggs until smooth'),
            RecipeStep(step_number=3, instruction='Cook in buttered pan over medium heat')
        ]
        
        pasta = Recipe(
            title='Pasta',
            shortname='pasta',
            description='A delicious pasta dish with a rich sauce.'
        )
        pasta.steps = [
            RecipeStep(step_number=1, instruction='Boil water in a large pot'),
            RecipeStep(step_number=2, instruction='Add pasta and cook for 8-10 minutes'),
            RecipeStep(step_number=3, instruction='Drain pasta and mix with sauce')
        ]
        
        chocolate_cake = Recipe(
            title='Chocolate Cake',
            shortname='chocolate-cake',
            description='A moist chocolate cake with creamy frosting.'
        )
        chocolate_cake.steps = [
            RecipeStep(step_number=1, instruction='Preheat oven to 350°F (175°C)'),
            RecipeStep(step_number=2, instruction='Mix dry ingredients in a bowl'),
            RecipeStep(step_number=3, instruction='Add wet ingredients and mix'),
            RecipeStep(step_number=4, instruction='Pour into pan and bake for 30 minutes')
        ]
        
        # Add all objects to session
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