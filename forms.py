from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from wtforms import StringField, PasswordField

class UserForm(FlaskForm):
    username = StringField("username")
    password = PasswordField("password")
    img = StringField("image")

class LoginForm(FlaskForm):
    username = StringField("username")

    password = PasswordField("password")

class EditUserForm(FlaskForm):
    """Edit user form"""

    username = StringField('username')
    img = StringField("image")

class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""
    