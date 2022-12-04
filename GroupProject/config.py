import os
import csi3335fa2022 as cfg


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # mysql+pymysql://web:mypass@localhost:3306/baseball
    enginestr = "mysql+pymysql://" + cfg.mysql['user'] + ":" + cfg.mysql['password'] + "@" + cfg.mysql['location'] + ":3306/" + cfg.mysql['database']
    SQLALCHEMY_DATABASE_URI = enginestr
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
