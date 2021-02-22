from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from wtforms import StringField, PasswordField

class UserForm(FlaskForm):
    username = StringField("username")
    password = PasswordField("password")
    img = StringField("user_img")

class LoginForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(), Length(min=1, max =20)],)

    password = PasswordField("password", validators=[InputRequired(), Length(min=6, max=20)],)