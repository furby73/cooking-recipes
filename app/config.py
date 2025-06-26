import os
from werkzeug.security import generate_password_hash

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')  # fix typo
    ADMIN_PASSWORD_HASH = os.environ.get(
        'ADMIN_PASSWORD_HASH',
        generate_password_hash('yourpassword')
    )