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

    def __repr__(self):
        return f'<Recipe {self.shortname}>'