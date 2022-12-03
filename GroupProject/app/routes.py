import pymysql
from flask import render_template, flash, redirect, url_for, request, jsonify
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, MainForm
from app.models import User, UserActions
from datetime import datetime
import csi3335 as cfg



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = MainForm()
    temp = list(get_years("Altoona Mountain City"))
    form.year.choices = temp
    title = "Home"
    # this is where you would add the user-action class and
    # create the data to add to the schema
    if request.method == "POST":
        temp = str(current_user)
        temp = temp.split(' ')
        user_action = UserActions()
        user_action.userId = temp[0]
        user_action.username = temp[1]
        user_action.search_filter0 = form.team.data
        user_action.search_filter1 = form.year.data
        results = str(generate_result(form))
        user_action.result = results
        user_action.datetime = str(datetime.now())
        db.session.add(user_action)
        db.session.commit()
        return render_template('searchResults.html', results=results)
    return render_template('index.html', title=title, form=form)

@app.route('/year/<team>')
def year(team):
    year_data = get_years(team=team)
    return jsonify({'years':year_data})

def get_years(team):
    year_data = []
    con = pymysql.connect(host=cfg.mysql['location'], user=cfg.mysql['user'], password=cfg.mysql['password'],
                          db=cfg.mysql['database'])
    cur = con.cursor()
    sql = "select distinct yearid from teamsupd where team_name = %s order by yearid desc;"
    cur.execute(sql, [team])
    temp = list(cur.fetchall())
    for yd in temp:
        for y in yd:
            y = str(y)
            year_data.append(y)
    return year_data

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


def generate_result(form):
    if request.method == 'POST':
        if request.form['button1'] == 'Submit1':
            try:
                # Connect to database
                con = pymysql.connect(host=cfg.mysql['location'], user=cfg.mysql['user'],
                                      password=cfg.mysql['password'],
                                      db=cfg.mysql['database'])
                cur = con.cursor()
                # Generate first portion of data for division standings
                team = form.team.data
                year = form.year.data
                print(team)
                print(year)
                sql = '''
                SELECT DISTINCT team_name, team_w, team_l, lgid, divid
                FROM teamsupd 
                WHERE yearid = %s AND team_name = %s;
                '''
                cur.execute(sql, [year, team])
                table = list(cur.fetchall())
                print(table)
                table = list(table[0])
                # , (team_w / (team_w + team_l) )
                w1 = int(table[1])
                l1 = int(table[2])
                percent = w1 / (w1 + l1)
                table.append(percent)
                # Get lg id from team to calculate games behind
                lgid = table[3]
                divid = table[4]
                if divid is not None:
                    # Get the rest of the needed data for division standings
                    sql = '''
                            SELECT team_name, team_w, team_l
                            FROM teamsupd
                            WHERE yearid = %s AND lgid = %s AND divid = %s
                            ORDER BY team_w DESC
                            LIMIT 1;
                          '''
                    # get the games behind the average of the differences between the leading team wins and the trailing team wins,
                    # and the leading teams losses and the trailing team losses
                    cur.execute(sql, [year, lgid, divid])
                    other = list(cur.fetchall())
                    other = list(other[0])
                    w2 = int(other[1])
                    l2 = int(other[2])
                    # (w2 - w1) + (l2 - l1) / 2
                    games_behind = (abs(w2 - w1) + abs(l2 - l1)) / 2.0
                    table.append(str(games_behind))
                    return table
                ######################
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

