from flask import Flask
from flask_login import LoginManager
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Please log in as admin.'

from .models import AdminUser

@login_manager.user_loader
def load_user(user_id):
    return AdminUser() if user_id == 'admin' else None

from . import routes