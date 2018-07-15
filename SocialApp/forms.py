from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)

from models import User

def name_exists(forms, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that same name already exist')

def email_exists(forms, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that same email already exist')


class RegistrationForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-z0-9]*$',
                message=("Username should be one word, letters, "
                         "numbers and underscores only.")
            ),
            name_exists
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )

    password = PasswordField(
        'password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Password must match')
        ]
    )

    Confirmpassword = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )

class LoginForm(Form):
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email()
                             ])
    password = PasswordField(
        'password',
        validators = [
            DataRequired()
        ]
    )

class PostForm(Form):
    content = TextAreaField("what's up?",
                            validators={DataRequired()})
