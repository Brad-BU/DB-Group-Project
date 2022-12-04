from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(UserMixin, db.Model, Base):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '{}'.format(self.id) + ' {}'.format(self.username)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserActions(db.Model, Base):
    __tablename__ = "UserActions"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, index=True)
    username = db.Column(db.String(64), index=True)
    search_filter0 = db.Column(db.String(64), index=True)
    search_filter1 = db.Column(db.String(64), index=True)
    result = db.Column(db.String(256), index=True)
    datetime = db.Column(db.String(64), index=True)

    def __repr__(self):
        return f"User ID: {self.userId} || Username: {self.username} || Filter1: {self.search_filter0} || Filter2: {self.search_filter1} || Result - {self.result} || Date-time: {self.datetime}"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
