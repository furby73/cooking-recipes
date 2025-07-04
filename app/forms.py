from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired

class AdminLoginForm(FlaskForm):
    password = PasswordField('Admin Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')