from flask import render_template
from app import app
from app.forms import AdminLogin
from flask import render_template, redirect, url_for

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
    form = AdminLogin()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('admin_login.html', form=form)
