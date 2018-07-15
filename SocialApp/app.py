from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)

import forms
import models
import sqlite3

DEBUG = True

app = Flask(__name__)
app.secret_key = 'auoesh.bouoastuh.43,uoausoehuoshuosth3ououea.auoub!'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.user.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


def initialize():
    models.DATABASE.connect()
    models.DATABASE.create_tables([models.User], safe=True)
    models.DATABASE.closer()


@app.before_request
def before_request():
    """"Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    """""Close the database connection after request. """
    g.db.close()
    return response

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        flash("Yay, you registered", "sucess")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            confrimpassword=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


def check_password_hash(password, data):
    pass


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.emails == form.email.data)
        except models.DoesNOtExit:
            flash("Your email or password doesn't match !", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in:", "Sucess")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You.ve been logged out! Come back soon!", "sucess")
    return redirect(url_for('index'))

@app.route('/new_post', methods=('GET', 'POST'))
@login_required #makes sures the user is logged in before been able to post
def post():
    form = forms.PostForm()
    if form.validate_on_submit():
        models.Post.create(user=g.user._get_current_object(),
                           content=form.content.data.strip())
        flash("Message Posted! Thanks!", "sucess")
        return redirect(url_for('index'))
    return render_template('post.html', form=form)

@app.route('/')
def index():
    return 'Hey!'

"""
models.initialize()
try:
    models.User.create_user(
        username='Steve',
        email='stephenashom40@gmail.com',
        password='passsword',
        admin=True
        )
    except ValueError:
        pass
""" 
if __name__ == '__main__':
    app.run(debug=DEBUG)
