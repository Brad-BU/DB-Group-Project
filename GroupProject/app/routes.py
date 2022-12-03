import pymysql
import string
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
            user_action = UserActions()
            user_action.userId = temp[0]
            user_action.username = temp[1]
            user_action.search_filter0 = request.form.get('select1')
            user_action.search_filter1 = request.form.get('select2')
            user_action.result = str(generate_result())
            user_action.datetime = str(datetime.now())
            # uncomment to submit to the database
            db.session.add(user_action)
            db.session.commit()
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
    con = pymysql.connect(host=cfg.mysql['location'], user=cfg.mysql['user'], password=cfg.mysql['password'],
                          db=cfg.mysql['database'])
    cur = con.cursor()
    sql = "select * from useractions;"
    cur.execute(sql)
    temp = list(cur.fetchall())
    user_data = []
    for td in temp:
        s = ""
        for t in td:
            t = str(t)
            s = s + " " + t
        user_data.append(s)

    return render_template('adminView.html', user_data=user_data)


def generate_result():
    if request.method == 'POST':
        if request.form['button1'] == 'Submit1':
            try:
                # Connect to database
                con = pymysql.connect(host=cfg.mysql['location'], user=cfg.mysql['user'],
                                      password=cfg.mysql['password'],
                                      db=cfg.mysql['database'])
                cur = con.cursor()
                # Generate first portion of data for division standings
                team = request.form.get('select1')
                year = request.form.get('select2')
                sql = '''
                SELECT DISTINCT team_name, team_w, team_l, lgid
                FROM teamsupd 
                WHERE yearid = %s AND team_name = %s;
                '''
                cur.execute(sql, [year, team])
                table = list(cur.fetchall())
                table = list(table[0])
                # , (team_w / (team_w + team_l) )
                w1 = int(table[1])
                l1 = int(table[2])
                percent = w1 / (w1 + l1)
                # Get lg id from team to calculate games behind
                lgid = table[3]
                # Get the rest of the needed data for division standings
                sql = '''
                SELECT team_name, team_w, team_l
                FROM teamsupd
                WHERE yearid = %s AND lgid = %s
                ORDER BY team_w DESC
                LIMIT 1;
                '''
                # get the games behind the average of the differences between the leading team wins and the trailing team wins,
                # and the leading teams losses and the trailing team losses
                cur.execute(sql, [year, lgid])
                table.append(percent)
                other = list(cur.fetchall())
                other = list(other[0])
                w2 = int(other[1])
                l2 = int(other[2])
                # (w2 - w1) + (l2 - l1) / 2
                games_behind = (abs(w2 - w1) + abs(l2 - l1)) / 2.0
                table.append(str(games_behind))
                print(table)
                print(other)
                return table
            except Exception:
                con.rollback()
                print("Database exception.")
                raise

        elif request.form['button2'] == 'Submit2':
            return 'button2'

