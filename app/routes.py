from flask import render_template
from app import app

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
