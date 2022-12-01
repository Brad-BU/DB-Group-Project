from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, UserActions
import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    title = "Home"
    # this is where you would add the user-action class and
    # create the data to add to the schema
    select = request.form.get('val')
    print(select)
    return render_template('index.html', title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # prevents an already logged-in user from going to login page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Checks the username and password exist
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
            return redirect(next_page)

        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # prevents an already logged-in user from going to login page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations! You are now a registered user!")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/admin')
@login_required
def admin():
    headings = ("ID", "Username", "Search: Team Name",
                "Search: Year", "Result", "Time", "Date")
    data = ()
    return render_template('adminView.html', headings=headings, data=data)
