from flask_login import UserMixin
from . import db

class AdminUser(UserMixin):
    def __init__(self, id='admin'):
        self.id = id

    @property
    def is_active(self):
        return True

    def get_id(self):
        return self.id

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    shortname = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    cover_image = db.Column(db.String(200))  # S3 URL
    steps = db.relationship('RecipeStep', backref='recipe',
                            cascade='all, delete-orphan',
                            lazy='dynamic',
                            order_by='RecipeStep.step_number')
    ingredients = db.relationship('RecipeIngredient', backref='recipe',
                                  cascade='all, delete-orphan',
                                  lazy='dynamic',
                                  order_by='RecipeIngredient.id')

class RecipeStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step_number = db.Column(db.Integer, nullable=False)
    instruction = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    weight = db.Column(db.String(50), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
