import pymysql
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, UserActions
from datetime import datetime
import csi3335 as cfg



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    con = pymysql.connect(host=cfg.mysql['location'], user=cfg.mysql['user'], password=cfg.mysql['password'],
                          db=cfg.mysql['database'])
    cur = con.cursor()
    sql = "select distinct team_name from teamsupd;"
    cur.execute(sql)
    temp = list(cur.fetchall())
    team_data = []
    for td in temp:
        for t in td:
            t = str(t)
            team_data.append(t)

    sql = "select distinct yearid from teamsupd order by yearid desc;"
    cur.execute(sql)
    temp = list(cur.fetchall())
    year_data = []
    for yd in temp:
        for y in yd:
            y = str(y)
            year_data.append(y)

    sql = "select distinct playerid from people order by playerid asc;"
    cur.execute(sql)
    temp = list(cur.fetchall())
    player_data = []
    for pd in temp:
        for p in pd:
            p = str(p)
            player_data.append(p)
    title = "Home"
    # this is where you would add the user-action class and
    # create the data to add to the schema
    if request.method == "POST":
        if request.form['select1'] == 'None' or request.form['select2'] == 'None':
            flash('Must select category for each')  # why doesn't this work
        else:
            temp = str(current_user)
            temp = temp.split(' ')
            u = UserActions()
            u.userId = temp[0]
            u.username = temp[1]
		# may need to add players
            u.search_filter0 = request.form.get('select1')
            u.search_filter1 = request.form.get('select2')
            print(request.form.get('select1'))
            u.result = 'result'
            u.datetime = str(datetime.now())
            return render_template('searchResults.html', team_data=team_data)
    return render_template('index.html', title=title, team_data=team_data, year_data=year_data, player_data=player_data)


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


@app.route('/results', methods=['POST', 'GET'])
def submit():
    return render_template('searchResults.html')
