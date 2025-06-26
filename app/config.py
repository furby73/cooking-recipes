import os
from werkzeug.security import generate_password_hash

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    ADMIN_PASSWORD_HASH = os.environ.get(
        'ADMIN_PASSWORD_HASH',
        generate_password_hash('yourpassword')
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///recipes.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False