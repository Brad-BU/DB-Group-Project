import pymysql
import csi3335 as cfg
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User


class MainForm(FlaskForm):
    team_data = []
    con = pymysql.connect(host=cfg.mysql['location'], user=cfg.mysql['user'], password=cfg.mysql['password'],
                          db=cfg.mysql['database'])
    cur = con.cursor()
    sql = "select distinct team_name from teamsupd;"
    cur.execute(sql)
    temp = list(cur.fetchall())

    for td in temp:
        for t in td:
            t = str(t)
            team_data.append(t)

    team = SelectField('Team', choices=team_data)
    year = SelectField('Year', choices=[])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
